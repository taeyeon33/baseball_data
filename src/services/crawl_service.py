import subprocess
import sys

from datetime import datetime
from src.repositories.crawl_repositories import create_job, mark_job_running
from src.config import PROJECT_ROOT

def start_games_crawl(league, start_date, end_date):
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
    
    now = datetime.utcnow().isoformat()

    # job_id = create_job(
    #     job_type="games",
    #     start_date=start_date,
    #     end_date=end_date,
    #     created_at=now
    # )

    subprocess.Popen(
        [
            sys.executable,
            "-m", "src.crawlers.games",
            "--league", league,
            # "--job-id", str(job_id),
            "--job-id", str(1),
            "--start-date", start_date,
            "--end-date", end_date,
        ],
        cwd=PROJECT_ROOT
    )

    # mark_job_running(1, started_at=now, check=True)

    return 1

