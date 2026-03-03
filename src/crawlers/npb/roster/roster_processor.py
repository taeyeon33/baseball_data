import sqlite3
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.roster.roster_parser import NPBRosterParser
from src.crawlers.npb.player.player_processor import process_player
from src.repositories.player_repositories import PlayerRepositories
from src.repositories.base_repository import BaseRepository
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_roster(conn: sqlite3.Connection, roster_url: str, game_data: dict):
    try:
        html = fetch_html(roster_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지가 존재하지 않습니다.")

        season_id = game_data["season_id"]
        away_team_id = game_data["away_team_id"]
        home_team_id = game_data["home_team_id"]
        roster = NPBRosterParser.parse_roster(html, away_team_id, home_team_id)
        if not roster:
            return GameProcessResult(ProcessResult.FAILED, None, "로스터가 존재하지 않습니다.")
        
        for player in roster:
            team_id = player["team_id"]
            player_id = PlayerRepositories.select_season_player(conn, player["name"], season_id, team_id)
            if not player_id:
                player_id = process_player(conn, player["number"], player["link"], season_id, team_id)
            else:
                if player["number"]:
                    PlayerRepositories.update_uniform_number(conn, player_id, season_id, team_id, player["number"])

            player["player_id"] = player_id
            insert_data = {
                "game_id": game_data["game_id"],
                "team_id": team_id,
                "player_id": player["player_id"]
            }
            BaseRepository.insert(conn, "game_rosters", insert_data, False, True)

        return GameProcessResult(ProcessResult.CREATED, roster, "성공")

    except Exception as e:
        return GameProcessResult(ProcessResult.FAILED, None, str(e))