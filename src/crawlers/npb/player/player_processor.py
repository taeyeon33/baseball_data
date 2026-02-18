import sqlite3
from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.player.player_parser import PlayerParser
from src.repositories.base_repository import BaseRepository
from src.repositories.player_repositories import PlayerRepositories
from src.repositories.game_repositories import GameRepositories
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_player(conn: sqlite3.Connection, back_number: int, link: str, season_id: int = None, team_id: int = None):
    try:
        resolver = NPBResolver()

        url = resolver.player_url(link)
        html = fetch_html(url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        player = PlayerParser.get_player(html)

        eng_url = resolver.player_eng_url(link)
        eng_html = fetch_html(eng_url)

        ALLSTARS_TEAM_IDS = {13, 14}
        player_id = PlayerRepositories.select_player(conn, player["last_name"] + player["first_name"], player["birthday"])
        if player_id:
            if team_id and team_id in ALLSTARS_TEAM_IDS:
                insert_data = {"player_id": player_id, "uniform_number": back_number, "team_id": team_id, "season_id": season_id}
                BaseRepository.insert(conn, "player_team_history", insert_data, False, True)
            return player_id
        
        player_id = BaseRepository.insert(conn, "players", player, True, True)

        if team_id and team_id in ALLSTARS_TEAM_IDS:
            insert_data = {"player_id": player_id, "uniform_number": back_number,  "team_id": team_id, "season_id": season_id}
            BaseRepository.insert(conn, "player_team_history", insert_data, False, True)
        
        player_names = PlayerParser.get_player_name(html, eng_html, player_id)
        BaseRepository.insert(conn, "player_names", player_names, False, True)

        player_history = dict()
        player_seasons = PlayerParser.get_player_history(html)
        for year, teams in player_seasons.items():
            if int(year) < 2016:
                continue
            
            season_id = GameRepositories.get_season_id(conn, year, "NPB")

            for team in teams:
                team_id = GameRepositories.get_team_id(conn, team)

                player_history = {
                    "player_id": player_id,
                    "team_id": team_id,
                    "uniform_number": None,
                    "season_id": season_id,
                    "start_date": None,
                    "end_date": None,
                }
            
                BaseRepository.insert(conn, "player_team_history", player_history, False, True)

        return player_id

    except Exception as e:
        raise RuntimeError(e)