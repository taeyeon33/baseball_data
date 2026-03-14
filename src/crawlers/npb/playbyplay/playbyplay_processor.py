import re
import sqlite3
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.playbyplay.playbyplay_parser import NPBPlaybyplayParser
from src.crawlers.npb.playbyplay.playbyplay_state import GameLogState
from src.repositories.detail_repositories import DetailRepositories
from src.repositories.base_repository import BaseRepository
from src.crawlers.npb.playbyplay.detail_mapper import DetailMapper
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_pbplog(conn: sqlite3.Connection, game_url: str, game_id: str, season_id: int, away_team_id: int, home_team_id: int, player_list: list):
    try:
        html = fetch_html(game_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지가 존재하지 않습니다.")
        
        log_data = NPBPlaybyplayParser.parse_pbp(html)
        if not log_data:
            return GameProcessResult(ProcessResult.FAILED, None, "GameLog가 존재하지 않습니다.")
        
        state = GameLogState(game_id)

        player_map = {
            p["link"]: p["player_id"]
            for p in player_list
        }

        log_count = 0
        for log in log_data:
            log_count += 1
            
            event = NPBPlaybyplayParser.get_log_type(log)
            event["season_id"] = season_id
            if event["type"] == "inning_change":
                row = state.apply(event)
                print(f"Event row: {row}")
                log_idx = BaseRepository.insert(conn, "game_logs", row, True)
                if not log_idx:
                    return GameProcessResult(ProcessResult.FAILED, None, f"DB 오류: game_logs / type: {event['type']}")

            else:
                player = NPBPlaybyplayParser.get_player(log)
                team_id = away_team_id if state.half else home_team_id
                player_id = player_map.get(player["link"])
                if not player_id:
                    return GameProcessResult(ProcessResult.FAILED, None, f"Roster에 존재하지 않는 선수: name: {player['name']}, team: {team_id}")

                event["player_id"] = player_id

                if event["type"] == "pinch_hitter":
                    row = state.apply(event)
                    print(f"Event row: {row}")
                    log_idx = BaseRepository.insert(conn, "game_logs", row, True)
                    if not log_idx:
                        return GameProcessResult(ProcessResult.FAILED, None, f"DB 오류: game_logs / type: {event['type']}")
                    event["type"] = "play"

                if event["type"] == "play" or event["type"] == "steal_base":
                    detail = NPBPlaybyplayParser.get_detail(log)
                    if event["type"] == "steal_base":
                        detail = re.sub(r"^（.*?）", "", detail)
                    detail_code = DetailRepositories.select_detail(conn, detail, "jp")
                    if not detail_code:
                        detail_data = DetailMapper.parse(detail)
                        detail_code = BaseRepository.insert(conn, "details", detail_data, True, True)
                        dt_data = {"detail_code": detail_code, "language": "jp", "detail_text": detail}
                        dt_check = BaseRepository.insert(conn, "detail_translations", dt_data, True, True)
                        if not detail_code or not dt_check:
                            return GameProcessResult(ProcessResult.FAILED, None, "Detail Check Error")
                    event["detail_code"] = detail_code

                row = state.apply(event)
                print(f"Event row: {row}")
                log_idx = BaseRepository.insert(conn, "game_logs", row, True)
                if not log_idx:
                    return GameProcessResult(ProcessResult.FAILED, None, f"DB 오류: game_logs / type: {event['type']}")
                
        percent = (log_count / len(log_data)) * 100
        if percent < 100:
            return GameProcessResult(ProcessResult.FAILED, None, "GameLog 일부만 클로링 되었습니다.")
        
        return GameProcessResult(ProcessResult.CREATED, None, "성공")

    except Exception as e:
        return GameProcessResult(ProcessResult.FAILED, None, str(e))