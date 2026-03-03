import sqlite3
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.box.box_parser import NPBBoxParser
from src.crawlers.npb.box.box_game_state import GameBoxState
from src.crawlers.npb.box.box_player_state import PlayerBoxState
from src.repositories.base_repository import BaseRepository
from src.repositories.player_repositories import PlayerRepositories
from src.repositories.game_repositories import GameRepositories
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult
import traceback

def process_box(conn: sqlite3.Connection, box_url: str, game_id: str, away_team_id: int, home_team_id: int, player_list: list):
    try:
        html = fetch_html(box_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지가 존재하지 않습니다.")

        player_map = {
            (p["name"].strip(), p["team_id"]): p["player_id"]
            for p in player_list
        }

        participation_data = NPBBoxParser.parse_participation_data(html, away_team_id, home_team_id)
        if not participation_data:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지 파싱 중 오류가 발생하였습니다.")
        print(participation_data)
        for part in participation_data:
            player_id = player_map.get((part["player_name"], part["team_id"]))
            if not player_id:
                return GameProcessResult(ProcessResult.FAILED, None, f"Roster에 존재하지 않는 선수: name: {part['player_name']}, team: {part['team_id']}")
            
            positions = part["positions"]
            for position in positions:
                part_data = {
                    "game_id": game_id,
                    "team_id": part["team_id"],
                    "player_id": player_id,
                    "position_code": position,
                    "batting_order": part["batting_order"],
                    "is_starting": part["is_starting"],
                }
                BaseRepository.insert(conn, "game_participations", part_data)

                player_position_data = PlayerRepositories.select_player_position(conn, player_id, position)
                if not player_position_data:
                    position_data = {
                        "player_id": player_id,
                        "position_code": position,
                    }
                    BaseRepository.insert(conn, "player_positions", position_data)

            if part["decisions"]:
                decision_data = {
                    "game_id": game_id,
                    "player_id": player_id,
                    "decision_type": part["decisions"]
                }
                BaseRepository.insert(conn, "game_pitcher_decisions", decision_data)
        

        return GameProcessResult(ProcessResult.CREATED, None, "성공")
        away_batter_data = NPBBoxParser.parse_away_batter_data(html)
        home_batter_data = NPBBoxParser.parse_home_batter_data(html)

        away_pitcher_data = NPBBoxParser.parse_away_pitcher_data(html)
        home_pitcher_data = NPBBoxParser.parse_home_pitcher_data(html)

        all_batter_data = PlayerBoxState.build_all_batter_data(game_id, away_batter_data, home_batter_data, player_map, away_team_id, home_team_id)
        all_pitcher_data = PlayerBoxState.build_all_pitcher_data(game_id, away_pitcher_data, home_pitcher_data, player_map, away_team_id, home_team_id)

        log_data = GameRepositories.get_game_logs(conn, game_id)

        game_state = GameBoxState(game_id)
        game_state.set_team_setting("away", away_batter_data, away_pitcher_data)
        game_state.set_team_setting("home", home_batter_data, home_pitcher_data)
        
        for log in log_data:
            print(log)

    except Exception as e:
        print("Error 발생:")
        traceback.print_exc()
        return GameProcessResult(ProcessResult.FAILED, None, str(e))