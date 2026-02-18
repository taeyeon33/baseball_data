import sqlite3

class DetailRepositories:
    def select_detail(conn: sqlite3.Connection, detail: str, lang: str):
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