import re
import argparse
import traceback
from datetime import datetime, timezone

from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.npb.schedule.schedule_processor import get_game_urls
from src.crawlers.npb.game.game_processor import process_game
from src.crawlers.npb.roster.roster_processor import process_roster
from src.crawlers.npb.playbyplay.playbyplay_processor import process_pbplog
from src.crawlers.npb.box.box_processor import process_box
from src.repositories.crawl_job_repositories import CrawlJobRepositories
from src.domain.enums import ProcessResult
from src.db.connect import get_connection
from src.db.db_executor import insert_and_commit
from src.db.unit_of_work import UnitOfWork

def crawl_games(league: str, job_id: int, start_date, end_date):
    item_id = None
    
    try:
        if not league:
            print("리그가 선택되지 않았습니다.")
            CrawlJobRepositories.mark_job_failed(job_id, datetime.now(timezone.utc))
            return
        
        if league == "NPB":
            resolver = NPBResolver()
        else:
            print(f"{league}는 존재하지 않습니다.")
            CrawlJobRepositories.mark_job_failed(job_id, datetime.now(timezone.utc))
            return

        schedule_urls  = resolver.get_schedule_urls(start_date, end_date)
        if len(schedule_urls) < 1:
            print(f"일정 URL을 가져오는 도중 오류가 발생했습니다.")
            CrawlJobRepositories.mark_job_failed(job_id, datetime.now(timezone.utc))
            return
        
        game_urls = get_game_urls(schedule_urls,  start_date, end_date)
        if len(game_urls) < 1:
            print("해당 날짜에 진행된 게임이 없습니다.")
            CrawlJobRepositories.mark_job_completed(job_id, datetime.now(timezone.utc))
            return
        
        for game_url in game_urls:
            item_id = None
            match = re.search(r"(\d{4})/(\d{4})/([a-z0-9\-]+)/", game_url)
            if not match:
                continue
            game_id = "".join(match.groups())

            item_id = int(insert_and_commit("crawl_job_items", {"job_id": job_id, "game_id": game_id}, True))
            CrawlJobRepositories.mark_item_running(item_id, datetime.now(timezone.utc))

            with UnitOfWork(get_connection) as uow:
                conn = uow.conn

                result = process_game(conn, game_url, game_id)
                print(f"game_url: {game_url}, result: {result}")
                if result.status == ProcessResult.SKIPPED:
                    CrawlJobRepositories.mark_item_skipped(item_id, "이미 완료된 게임")
                    continue

                if result.status != ProcessResult.CREATED:
                    raise Exception(result.msg)

                game_data = result.data

                result = process_roster(
                    conn,
                    resolver.roster_url(game_url),
                    game_data
                )
                if result.status != ProcessResult.CREATED:
                    raise Exception(result.msg)

                roster_data = result.data
                result = process_pbplog(
                    conn,
                    resolver.playbyplay_url(game_url),
                    game_data["game_id"],
                    game_data["season_id"],
                    game_data["away_team_id"],
                    game_data["home_team_id"],
                    roster_data
                )
                if result.status != ProcessResult.CREATED:
                    raise Exception(result.msg)

                result = process_box(
                    conn,
                    resolver.box_url(game_url),
                    game_data["game_id"],
                    game_data["away_team_id"],
                    game_data["home_team_id"],
                    roster_data
                )
                if result.status != ProcessResult.CREATED:
                    raise Exception(result.msg)

            CrawlJobRepositories.mark_item_completed(item_id, datetime.now(timezone.utc))

        total_items = len(game_urls)
        completed_items = CrawlJobRepositories.count_success_items(job_id)
        failed_items = len(CrawlJobRepositories.get_failed_items(job_id))
        skipped_items = len([i for i in CrawlJobRepositories.get_items_by_job(job_id) if i['status'] == 'skipped'])

        if failed_items > 0 or completed_items + skipped_items != total_items:
            CrawlJobRepositories.mark_job_failed(job_id, datetime.now(timezone.utc))
        else:
            CrawlJobRepositories.mark_job_completed(job_id, datetime.now(timezone.utc))

    except Exception as e:
        print("Error 발생:")
        traceback.print_exc()

        if item_id:
            CrawlJobRepositories.mark_item_failed(item_id, datetime.now(timezone.utc), str(e))
        
        CrawlJobRepositories.mark_job_failed(job_id, datetime.now(timezone.utc))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--league", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)

    args = parser.parse_args()

    crawl_games(
        job_id=args.job_id,
        league=args.league,
        start_date=args.start_date,
        end_date=args.end_date
    )

if __name__ == "__main__":
    main()