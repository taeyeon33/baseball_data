import subprocess
import sys

from datetime import datetime, timezone
from src.repositories.crawl_job_repositories import CrawlJobRepositories
from src.db.db_executor import insert_and_commit
from src.config import PROJECT_ROOT

def start_game_crawler(league: str, start_date: str, end_date: str):
    if not start_date or not end_date:
        raise ValueError("날짜가 입력되지 않았습니다.")
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("날짜 형식이 올바르지 않습니다.")
    
    if start_dt > end_dt:
        raise ValueError("시작 날짜는 마지막 날짜보다 이전 날짜여야 합니다.")
    
    if start_dt.year != end_dt.year:
        raise ValueError("같은 연도의 기간만 가능합니다.")
    
    now = datetime.now(timezone.utc)

    try:
        job_data = {"job_type": "games", "start_date": start_date, "end_date": end_date, "created_at": now}
        job_id = insert_and_commit("crawl_jobs", job_data, True)

        if not job_id:
            return None

        subprocess.Popen(
            [
                sys.executable,
                "-m", "src.crawlers.games",
                "--league", league,
                "--job-id", str(job_id),
                "--start-date", start_date,
                "--end-date", end_date,
            ],
            cwd=PROJECT_ROOT
        )

        CrawlJobRepositories.mark_job_running(job_id, started_at=now)

        return job_id

    except Exception as e:
        raise RuntimeError(e)