import subprocess
import sys

from datetime import datetime
from src.repositories.crawl_repositories import create_job, mark_job_running

def start_games_crawl(start_date, end_date):
    if not start_date or not end_date:
        raise ValueError("날짜가 입력되지 않았습니다.")
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("날짜 형식이 올바르지 않습니다.")
    
    if start_dt > end_dt:
        raise ValueError("시작 날짜는 마지막 날짜보다 이전 날짜여야 합니다.")
    
    now = datetime.utcnow().isoformat()

    job_id = create_job(
        job_type="games",
        start_date=start_date,
        end_date=end_date,
        created_at=now
    )

    subprocess.Popen(
        [
            sys.executable,
            "-m", "crawlers.games",
            "--job-id", str(job_id),
            "--start-date", start_date,
            "--end-date", end_date
        ]
    )

    """
    src/
    ├─ crawlers/
    │   ├─ games.py              # job entry point
    │   ├─ fetchers/
    │   │   └─ npb_playbyplay.py
    │   ├─ parsers/
    │   │   ├─ npb_playbyplay_parser.py
    │   │   └─ npb_event_parser.py
    │   ├─ processors/
    │   │   ├─ game_processor.py
    │   │   └─ entity_resolver.py
    │   └─ state/
    │       └─ game_state.py
    │
    ├─ repositories/
    │   ├─ game_repo.py
    │   ├─ player_repo.py
    │   ├─ detail_repo.py
    │   └─ game_log_repo.py

    """

    """
    src/
    ├─ crawlers/
    │   ├─ games.py                     # job entry (공통)
    │
    │   ├─ common/                      # 🔴 [NEW] 리그 공통 인터페이스
    │   │   ├─ base_fetcher.py
    │   │   ├─ base_parser.py
    │   │   ├─ base_box_parser.py
    │   │   └─ base_roster_parser.py
    │
    │   ├─ npb/                         # 🔴 [NEW] NPB 전용
    │   │   ├─ fetchers/
    │   │   │   ├─ playbyplay.py
    │   │   │   ├─ box.py
    │   │   │   └─ roster.py
    │   │   │
    │   │   ├─ parsers/
    │   │   │   ├─ playbyplay_parser.py
    │   │   │   ├─ event_parser.py
    │   │   │   ├─ box_parser.py
    │   │   │   └─ roster_parser.py
    │   │   │
    │   │   └─ resolver.py              # 🔴 [NEW] NPB URL / 페이지 해석
    │
    │   ├─ kbo/                         # 🔴 [NEW] KBO 전용
    │   │   ├─ fetchers/
    │   │   │   ├─ playbyplay.py
    │   │   │   ├─ box.py
    │   │   │   └─ roster.py
    │   │   │
    │   │   ├─ parsers/
    │   │   │   ├─ playbyplay_parser.py
    │   │   │   ├─ event_parser.py
    │   │   │   ├─ box_parser.py
    │   │   │   └─ roster_parser.py
    │   │   │
    │   │   └─ resolver.py              # 🔴 [NEW] KBO URL / 페이지 해석
    │
    │   ├─ processors/
    │   │   ├─ game_processor.py
    │   │   ├─ playbyplay_processor.py
    │   │   ├─ box_processor.py
    │   │   └─ entity_resolver.py
    │
    │   ├─ state/
    │   │   └─ game_state.py
    """

    mark_job_running(job_id, started_at=now)

    return job_id

