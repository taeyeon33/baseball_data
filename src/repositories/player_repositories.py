import sqlite3
from src.db.connect import get_connection

class PlayerRepositories:
    def select_season_player(p_name: str, season_id: int, team_id: int) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = """
                SELECT p.player_id
                FROM player_team_history AS pth
                JOIN players AS p
                ON pth.player_id = p.player_id
                WHERE pth.team_id = ? 
                AND pth.season_id = ? 
                AND (
                        p.last_name = ?
                        OR
                        (p.last_name || SUBSTR(p.first_name, 1, 1)) = ?
                    )
            """
            row = cur.execute(sql, (team_id, season_id, p_name, p_name)).fetchone()
            return row["player_id"] if row else None

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def insert_player(rows: dict, table: str) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()

            columns = ", ".join(rows.keys())
            placeholders = ", ".join(["?"] * len(rows))
            values = list(rows.values())

            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
            cur.execute(sql, values)
            conn.commit()

            idx = cur.lastrowid

            return idx
        
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()