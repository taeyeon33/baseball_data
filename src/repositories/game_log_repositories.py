import sqlite3
from src.db.connect import get_connection

class GameLogRepositories:
    def insert_game_log(rows: dict) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()

            columns = ", ".join(rows.keys())
            placeholders = ", ".join(["?"] * len(rows))
            values = list(rows.values())

            sql = f"INSERT INTO game_logs ({columns}) VALUES ({placeholders})"

            cur.execute(sql, values)
            conn.commit()

            idx = cur.lastrowid

            return idx

        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()