import traceback
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.playbyplay.playbyplay_parser import NPBPlaybyplayParser
from src.crawlers.npb.playbyplay.playbyplay_state import GameLogState
from src.crawlers.npb.player.player_processor import process_player
from src.repositories.player_repositories import PlayerRepositories
from src.repositories.detail_repositories import DetailRepositories
from src.repositories.game_log_repositories import GameLogRepositories
from src.crawlers.npb.playbyplay.detail_mapper import DetailMapper
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_pbplog(game_url, game_id, season_id, away_team_id, home_team_id):
    try:
        html = fetch_html(game_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        log_data = NPBPlaybyplayParser.parse_pbp(html)
        if not log_data:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        state = GameLogState(game_id=game_id)

        log_count = 0
        for log in log_data:
            log_count += 1
            
            event = NPBPlaybyplayParser._get_log_type(log)
            event["season_id"] = season_id
            print(f"Event: {event}")
            if event["type"] == "inning_change":
                row = state.apply(event)
                log_idx = GameLogRepositories.insert_game_log(row)
                if not log_idx:
                    return GameProcessResult(ProcessResult.FAILED, None)

            else:
                player = NPBPlaybyplayParser._get_player(log)
                team_id = away_team_id if state.half else home_team_id
                player_id = PlayerRepositories.select_season_player(player["name"], season_id, team_id)
                print(f"Player name: {player['name']}, Team ID: {team_id}, Season ID: {season_id}, Player ID from DB: {player_id}")
                if not player_id:
                    player_id = process_player(player["link"])

                event["player_id"] = player_id
                print(f"Player: {player}, Player ID: {player_id}")

                if event["type"] == "pinch_hitter":
                    row = state.apply(event)
                    log_idx = GameLogRepositories.insert_game_log(row)
                    if not log_idx:
                        return GameProcessResult(ProcessResult.FAILED, None)
                    event["type"] = "play"

                if event["type"] == "play" or event["type"] == "steal_base":
                    detail = NPBPlaybyplayParser._get_detail(log)
                    detail_code = DetailRepositories.select_detail(detail, "jp")
                    if not detail_code:
                        detail_data = DetailMapper.parse(detail)
                        detail_code = DetailRepositories.insert_detail(detail_data)
                        dt_check = DetailRepositories.insert_detail_translation(detail_code, "jp", detail)
                        if not detail_code or not dt_check:
                            return GameProcessResult(ProcessResult.FAILED, None)
                    event["detail_code"] = detail_code

                row = state.apply(event)
                print(f"Play event row: {row}")
                log_idx = GameLogRepositories.insert_game_log(row)
                if not log_idx:
                    return GameProcessResult(ProcessResult.FAILED, None)
        
    except Exception as e:
        print("Error 발생:")
        traceback.print_exc()
        return e