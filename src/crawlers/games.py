import argparse

from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.npb.game.game_processor import process_game
from src.crawlers.npb.schedule.schedule_processor import get_game_urls
from src.crawlers.npb.playbyplay.playbyplay_processor import process_pbplog
from src.domain.enums import ProcessResult

def crawl_games(league: str, start_date, end_date):
    if not league:
        raise ValueError("리그가 선택되지 않았습니다.")
    
    if league == "NPB":
        resolver = NPBResolver()
    else:
        raise ValueError(f"{league}는 존재하지 않습니다.")

    schedule_urls  = resolver.get_schedule_urls(start_date, end_date)
    if len(schedule_urls) < 1:
        raise ValueError(f"일정 URL을 가져오는 도중 오류가 발생했습니다.")
    
    game_urls = get_game_urls(schedule_urls,  start_date, end_date)
    if len(game_urls) < 1:
        raise ValueError("해당 날짜에 진행된 게임이 없습니다.")
    
    for game_url in game_urls:
        pbp_url = resolver.playbyplay_url(game_url)
        result = process_game(pbp_url)

        if result.status == ProcessResult.SKIPPED:
            # job skipped 카운트 증가
            continue

        if result.status == ProcessResult.FAILED:
            # job failed 카운트 증가 + 로그 남기기
            continue

        if result.status == ProcessResult.CREATED:
            game_data = result.game_data
            game_id = game_data["game_id"]
            print(f"Game ID: {game_id} - {game_data['away_team_id']} vs {game_data['home_team_id']} on {game_data['game_date']}")
            process_pbplog(pbp_url, game_id, game_data["season_id"], game_data["away_team_id"], game_data["home_team_id"])

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