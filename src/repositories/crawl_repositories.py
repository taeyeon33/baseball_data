import sqlite3
from src.db.connect import get_connection

def create_job(job_type, start_date, end_date, created_at):
    conn = get_connection()
    try:
        cur = conn.cursor()

        values = list(job_type, start_date, end_date, created_at)

        sql = f"INSERT INTO crawl_jobs(job_type, start_date, end_date, status, created_at) VALUES (?, ?, ?, 'pending', ?)"

        cur.execute(sql, values)
        conn.commit()

        job_id = cur.lastrowid

        return job_id
    
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()

def mark_job_running(job_id, started_at):
    conn = get_connection()
    try:
        cur = conn.cursor()

        values = list(started_at, job_id)

        sql = f"UPDATE crawl_jobs SET status = 'running', started_at = ? WHERE job_id = ?"

        cur.execute(sql, values)
        conn.commit()

        cnt = cur.rowcount

        return cnt

    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()