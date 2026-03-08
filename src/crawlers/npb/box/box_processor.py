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

        player_id_map = {
            (p["link"]): p["player_id"]
            for p in player_list
        }

        player_link_map = {
            (p["player_id"]): p["link"]
            for p in player_list
        }

        participation_data = NPBBoxParser.parse_participation_data(html, away_team_id, home_team_id)
        if not participation_data:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지 파싱 중 오류가 발생하였습니다.")
        
        for part in participation_data:
            player_id = player_id_map.get(part["link"])
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
        
        away_batter_data = NPBBoxParser.parse_away_batter_data(html)
        home_batter_data = NPBBoxParser.parse_home_batter_data(html)

        away_pitcher_data = NPBBoxParser.parse_away_pitcher_data(html)
        home_pitcher_data = NPBBoxParser.parse_home_pitcher_data(html)

        box_state = PlayerBoxState(game_id, away_team_id, home_team_id, player_id_map)
        box_state.build_all_batter_data(away_batter_data, home_batter_data)
        box_state.build_all_pitcher_data(away_pitcher_data, home_pitcher_data)

        log_data = GameRepositories.get_game_logs(conn, game_id)
        
        game_state = GameBoxState(game_id, player_list, player_id_map)
        game_state.set_team_setting("away", away_batter_data, away_pitcher_data)
        game_state.set_team_setting("home", home_batter_data, home_pitcher_data)
        
        for idx, log in enumerate(log_data):
            log_type = log["log_type"]

            if log_type == "inning_change":
                game_state.inning_change()
                half = "top" if game_state.half else "bottom"
                runs = GameRepositories.get_game_score_inning(game_id, game_state.inning, half)
                if runs > 0:
                    game_state.update_score(runs)
                continue

            if log_type == "pitching_change":
                pitcher_id = log["pitcher_id"]

                next_log = log_data[idx + 1]
                if next_log["log_type"] == "pinch_hitter":
                    next_log = log_data[idx + 2]
                on_1b = next_log["on_1b"]
                on_2b = next_log["on_2b"]
                on_3b = next_log["on_3b"]

                runner = 0
                if on_1b:
                    runner += 1
                if on_2b:
                    runner += 1
                if on_3b:
                    runner += 1

                team = "home" if game_state.half else "away"
                svo = game_state.check_svo(team, runner)
                game_state.set_svo(team, svo)

                batter_list = home_batter_data if game_state.half else away_batter_data
                link = player_link_map.get(pitcher_id)
                batting_order_map = {
                    (b["link"]): b["batting_order"]
                    for b in batter_list
                }
                batting_order = batting_order_map.get(link)
                    
                game_state.change_pitcher(pitcher_id, batting_order)
                continue
        
            if log_type == "pinch_hitter":
                continue

            if log_type == "steal_base":
                continue

            if log_type == "play":
                continue

            print(log)

        return GameProcessResult(ProcessResult.CREATED, None, "성공")

    except Exception as e:
        print("Error 발생:")
        traceback.print_exc()
        return GameProcessResult(ProcessResult.FAILED, None, str(e))