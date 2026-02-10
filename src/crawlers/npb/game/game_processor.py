from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.game.game_parser import NPBGameParser
from src.repositories.game_repositories import GameRepositories
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_game(game_url):
    try:    
        html = fetch_html(game_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        game_data = NPBGameParser.parse_game(html)
        if not game_data:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        game_data["season_id"] = GameRepositories.get_season_id(game_data["season_id"], "NPB")
        game_data["away_team_id"] = GameRepositories.get_team_id(game_data["away_team_id"])
        game_data["home_team_id"] = GameRepositories.get_team_id(game_data["home_team_id"])
        game_data["sta_id"] = GameRepositories.get_stadium_id(game_data["sta_id"])

        game_id = GameRepositories.select_game(game_data)
        if game_id:
            return GameProcessResult(ProcessResult.SKIPPED, game_id)

        game_id = GameRepositories.insert_game(game_data)
        return GameProcessResult(ProcessResult.CREATED, game_id)

    except Exception as e:
        raise