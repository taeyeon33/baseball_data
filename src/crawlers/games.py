import argparse

from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.processors.game_processor import process_game
from src.crawlers.processors.schedule_processor import get_game_urls

def crawl_games(league: str, start_date, end_date):
    if not league:
        raise ValueError("리그가 선택되지 않았습니다.")
    
    if league == "NPB":
        resolver = NPBResolver()
    else:
        raise ValueError(f"{league}는 존재하지 않습니다.")

    schedule_urls  = resolver.get_schedule_urls(start_date, end_date)
    game_urls = get_game_urls(schedule_urls,  start_date, end_date)

    # if game_urls.count() < 1:
    #     raise ValueError("해당 날짜에 진행된 게임이 없습니다.")
    
    # for game_url in game_urls:
    #     process_game(game_url, resolver)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)

    args = parser.parse_args()

    crawl_games(
        league=args.league,
        start_date=args.start_date,
        end_date=args.end_date
    )

if __name__ == "__main__":
    main()