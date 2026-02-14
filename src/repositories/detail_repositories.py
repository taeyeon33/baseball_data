import sqlite3
from src.db.connect import get_connection

class DetailRepositories:
    def select_detail(detail: str, lang: str) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = """
                SELECT d.detail_code 
                FROM details AS d
                JOIN detail_translations AS dt
                ON d.detail_code = dt.detail_code
                WHERE dt.detail_text = ? AND dt.language = ?
            """
            row = cur.execute(sql, (detail, lang)).fetchone()
            return row["detail_code"] if row else None

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def insert_detail(detail_data: dict) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()

            columns = ", ".join(detail_data.keys())
            placeholders = ", ".join(["?"] * len(detail_data))
            values = list(detail_data.values())

            sql = f"INSERT INTO details ({columns}) VALUES ({placeholders})"
        
            cur.execute(sql, values)
            conn.commit()

            idx = cur.lastrowid

            return idx
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def insert_detail_translation(detail_code: int, lang: str, detail_text: str) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = "INSERT INTO detail_translations (detail_code, language, detail_text) VALUES (?, ?, ?)"
            cur.execute(sql, (detail_code, lang, detail_text))
            conn.commit()

            idx = cur.lastrowid

            return idx
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()
    