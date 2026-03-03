import sqlite3

class BaseRepository:
    @staticmethod
    def insert(conn: sqlite3.Connection, table: str, rows: dict, return_id: bool = False, ignore: bool = False):
        try:
            cur = conn.cursor()

            columns = ", ".join(rows.keys())
            placeholders = ", ".join(["?"] * len(rows))
            values = list(rows.values())

            insert_clause = "INSERT OR IGNORE" if ignore else "INSERT"

            sql = f"{insert_clause} INTO {table} ({columns}) VALUES ({placeholders})"
            cur.execute(sql, values)

            if return_id:
                return cur.lastrowid

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")