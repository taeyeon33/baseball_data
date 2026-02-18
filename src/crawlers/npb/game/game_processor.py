import sqlite3
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.game.game_parser import NPBGameParser
from src.repositories.game_repositories import GameRepositories
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_game(conn: sqlite3.Connection, game_url: str, game_id: str):
    try:
        GameRepositories.insert_game(conn, game_id, "scheduled")

        html = fetch_html(game_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지가 존재하지 않습니다.")

        game_data = NPBGameParser.parse_game(html)
        if not game_data:
            return GameProcessResult(ProcessResult.FAILED, None, "페이지에 데이터가 존재하지 않습니다.")

        game_data["game_id"] = game_id
        year = game_data["season_id"]
        game_data["season_id"] = GameRepositories.get_season_id(conn, year, "NPB")
        game_data["away_team_id"] = GameRepositories.get_team_id(conn, game_data["away_team_id"])
        game_data["home_team_id"] = GameRepositories.get_team_id(conn, game_data["home_team_id"])
        game_data["sta_id"] = GameRepositories.get_stadium_id(conn, game_data["sta_id"], year)

        if not game_data["season_id"]:
            return GameProcessResult(ProcessResult.FAILED, game_data, "시즌 데이터가 존재하지 않습니다.")

        game_row = GameRepositories.select_game(conn, game_id)
        if game_row and game_row["status"] != "scheduled":
            return GameProcessResult(ProcessResult.SKIPPED, game_row, "이미 크롤링 완료된 게임입니다.")

        GameRepositories.update_game(conn, game_data)

        score_data = NPBGameParser._parse_score_by_inning(html)
        if score_data:
            GameRepositories.insert_score(conn, game_id, score_data)

        return GameProcessResult(ProcessResult.CREATED, game_data, "성공")

    except Exception as e:
        return GameProcessResult(ProcessResult.FAILED, None, str(e))
