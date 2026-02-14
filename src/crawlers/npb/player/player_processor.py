from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.player.player_parser import PlayerParser
from src.repositories.player_repositories import PlayerRepositories
from src.repositories.game_repositories import GameRepositories
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult
import traceback
def process_player(link: str) -> int:
    try:
        resolver = NPBResolver()

        url = resolver.player_url(link)
        html = fetch_html(url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        player = PlayerParser.get_player(html)

        eng_url = resolver.player_eng_url(link)
        eng_html = fetch_html(eng_url)

        player_id = PlayerRepositories.insert_player(player, "players")
        
        player_history = dict()
        player_seasons = PlayerParser.get_player_history(html)
        year_list = player_seasons.keys()
        for year in year_list:
            if int(year) < 2016:
                continue
            player_history = {
                "player_id": player_id,
                "team_id": GameRepositories.get_team_id(player_seasons[year]),
                "uniform_number": None,
                "season_id": GameRepositories.get_season_id(year, "NPB"),
                "start_date": None,
                "end_date": None,
            }
            PlayerRepositories.insert_player(player_history, "player_team_history")
            
        player_names = PlayerParser.get_player_name(html, eng_html, player_id)
        PlayerRepositories.insert_player(player_names, "player_names")

        return player_id

    except Exception as e:
        print("Error 발생:")
        traceback.print_exc()
        return e