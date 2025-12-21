from src.db.connect import get_connection
from src.db.schema import init_schema
from src.db.repository import insert_game_log

from src.crawlers.npb_fetcher import fetch_playbyplay_contents, extract_log_elements
from src.crawlers.npb_parse import parse_log_element

from src.processors.npb_state import GameState


def main():
    conn = get_connection()
    init_schema(conn)
    cur = conn.cursor()

    URL = "https://npb.jp/scores/2025/0328/g-s-01/playbyplay.html"
    contents = fetch_playbyplay_contents(URL)

    state = GameState(game_id=1)

    log_count = 0
    for log in extract_log_elements(contents):
        log_count += 1
        if log_count < 5:
            continue  # 처음 4개 로그는 건너뜀
        else:
            event = parse_log_element(log)
            if event["type"] == "pinch_hitter":
                row = state.apply(event)
                insert_game_log(cur, row, event["type"])
                event["type"] = "play"
            row = state.apply(event)
            insert_game_log(cur, row, event["type"])

    conn.commit()
    conn.close()


main()
