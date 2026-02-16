import sqlite3
from src.db.connect import get_connection

class GameRepositories:
    def get_season_id(year: str, league: str) -> str:
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = """
                SELECT s.season_id 
                FROM seasons AS s 
                JOIN leagues AS l 
                ON s.league_id = l.league_id 
                WHERE s.season = ? 
                AND l.league = ?
            """
            row = cur.execute(sql, (year, league)).fetchone()
            return row["season_id"] if row else None

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def get_team_id(team_name: str) -> str:
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = """
                SELECT team_id
                FROM teams
                WHERE full_name = ? 
                OR team_name = ?
                OR full_name LIKE '%' || ? || '%'
            """
            row = cur.execute(sql, (team_name, team_name, team_name)).fetchone()
            return row["team_id"] if row else None
        
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def get_stadium_id(sta_name: str, year: str) -> str:
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = """
                SELECT st.sta_id
                FROM stadiums AS st 
                JOIN stadium_names AS sn 
                ON st.sta_id = sn.sta_id
                WHERE sn.name_jp_short = ?
                AND sn.start_year <= ?
                AND (sn.end_year IS NULL OR sn.end_year >= ?)
            """
            row = cur.execute(sql, (sta_name, int(year), int(year))).fetchone()
            return row["sta_id"] if row else None

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def select_game(rows):
        conn = get_connection()
        try:
            cur = conn.cursor()

            sql = """
                SELECT game_id
                FROM games
                WHERE season_id = ? AND game_date = ? AND away_team_id = ? AND home_team_id = ? AND sta_id = ?
            """

            row = cur.execute(sql, (rows["season_id"], rows["game_date"], rows["away_team_id"], rows["home_team_id"], rows["sta_id"])).fetchone()
            return row["game_id"] if row else None

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def insert_game(rows):
        conn = get_connection()
        try:
            cur = conn.cursor()

            columns = ", ".join(rows.keys())
            placeholders = ", ".join(["?"] * len(rows))
            values = list(rows.values())

            sql = f"INSERT INTO games ({columns}) VALUES ({placeholders})"
        
            cur.execute(sql, values)
            conn.commit()

            idx = cur.lastrowid

            return idx

        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()

    def insert_score(game_id: int, score_data: dict) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()

            for i, data in score_data.items():
                sql = """
                    INSERT INTO scores (game_id, inning, half, runs)
                    VALUES (?, ?, ?, ?)
                """
                cur.execute(sql, (game_id, i, "top", data["top"]))

                if data["bottom_raw"].lower() == "x":
                    continue
            
                cur.execute(sql, (game_id, i, "bottom", data["bottom"]))
            
            conn.commit()

        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}")
        
        finally:
            conn.close()