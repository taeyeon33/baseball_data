from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.player.player_parser import PlayerParser
from src.repositories.player_repositories import PlayerRepositories
from src.repositories.game_repositories import GameRepositories
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult
import traceback
def process_player(link: str, season_id: int = None, team_id: int = None) -> int:
    try:
        resolver = NPBResolver()

        url = resolver.player_url(link)
        html = fetch_html(url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        player = PlayerParser.get_player(html)

        eng_url = resolver.player_eng_url(link)
        eng_html = fetch_html(eng_url)

        # 나중에 team_type 컬럼 추가해서 ALLSTARS_TEAM_IDS 제거하기
        ALLSTARS_TEAM_IDS = {13, 14}
        player_id = PlayerRepositories.select_player(player["last_name"] + player["first_name"], player["birthday"])
        if player_id:
            if team_id and team_id in ALLSTARS_TEAM_IDS:
                PlayerRepositories.insert_player({"player_id": player_id, "team_id": team_id, "season_id": season_id}, "player_team_history")
            return player_id
        
        player_id = PlayerRepositories.insert_player(player, "players")

        if team_id and team_id in ALLSTARS_TEAM_IDS:
            PlayerRepositories.insert_player({"player_id": player_id, "team_id": team_id, "season_id": season_id}, "player_team_history")
        
        player_names = PlayerParser.get_player_name(html, eng_html, player_id)
        PlayerRepositories.insert_player(player_names, "player_names")

        player_history = dict()
        player_seasons = PlayerParser.get_player_history(html)
        for year, teams in player_seasons.items():
            if int(year) < 2016:
                continue
            
            season_id = GameRepositories.get_season_id(year, "NPB")

            for team in teams:
                team_id = GameRepositories.get_team_id(team)

                player_history = {
                    "player_id": player_id,
                    "team_id": team_id,
                    "uniform_number": None,
                    "season_id": season_id,
                    "start_date": None,
                    "end_date": None,
                }
            
                PlayerRepositories.insert_player(player_history, "player_team_history")

        return player_id

    except Exception as e:
        print("Error 발생:")
        traceback.print_exc()
        return e