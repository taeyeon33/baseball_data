import sqlite3
from datetime import datetime
from src.db.connect import get_connection

class CrawlJobRepositories:
    def mark_job_running(job_id: int, started_at: datetime):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = f"UPDATE crawl_jobs SET status = 'running', started_at = ? WHERE job_id = ?"

            cur.execute(sql, (started_at, job_id))
            conn.commit()

            cnt = cur.rowcount

            return cnt

        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def mark_job_completed(job_id: int, finished_at: datetime):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = f"UPDATE crawl_jobs SET status = 'completed', finished_at = ? WHERE job_id = ?"

            cur.execute(sql, (finished_at, job_id))
            conn.commit()

            return cur.rowcount
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def mark_job_failed(job_id: int, finished_at: datetime):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = f"UPDATE crawl_jobs SET status = 'failed', finished_at = ? WHERE job_id = ?"
            
            cur.execute(sql, (finished_at, job_id))
            conn.commit()

            return cur.rowcount
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def get_job(job_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM crawl_jobs WHERE job_id = ?", (job_id,))

            return cur.fetchone()
        
        finally:
            conn.close()

    def mark_item_running(item_id: int, started_at: datetime):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = "UPDATE crawl_job_items SET status = 'running', started_at = ? WHERE item_id = ?"

            cur.execute(sql, (started_at, item_id))
            conn.commit()

            return cur.rowcount
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def mark_item_completed(item_id: int, finished_at: datetime):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = "UPDATE crawl_job_items SET status = 'completed', finished_at = ? WHERE item_id = ?"

            cur.execute(sql, (finished_at, item_id))
            conn.commit()

            return cur.rowcount
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def mark_item_failed(item_id: int, finished_at: datetime, error_msg: str):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = "UPDATE crawl_job_items SET status = 'failed', finished_at = ?, error_msg = ? WHERE item_id = ?"

            cur.execute(sql, (finished_at, error_msg, item_id))
            conn.commit()

            return cur.rowcount
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def mark_item_skipped(item_id: int, error_msg: str = None):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = "UPDATE crawl_job_items SET status = 'skipped', error_msg = ? WHERE item_id = ?"

            cur.execute(sql, (error_msg, item_id))
            conn.commit()

            return cur.rowcount
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def get_items_by_job(job_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM crawl_job_items WHERE job_id = ?", (job_id,))

            return cur.fetchall()
        
        finally:
            conn.close()

    def count_total_items(job_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM crawl_job_items WHERE job_id = ?", (job_id,))
            return cur.fetchone()[0]
        
        finally:
            conn.close()

    def get_failed_items(job_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM crawl_job_items WHERE job_id = ? AND status = 'failed'", (job_id,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        
        finally:
            conn.close()

    def count_success_items(job_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM crawl_job_items WHERE job_id = ? AND status = 'completed'", (job_id,))
            return cur.fetchone()[0]
        
        finally:
            conn.close()