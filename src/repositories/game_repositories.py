import sqlite3

class GameRepositories:
    def get_season_id(conn: sqlite3.Connection, year: str, league: str):
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

    def get_team_id(conn: sqlite3.Connection, team_name: str):
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

    def get_stadium_id(conn: sqlite3.Connection, sta_name: str, year: str):
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

    def select_game(conn: sqlite3.Connection, game_id: str):
        cur = conn.cursor()

        sql = "SELECT * FROM games WHERE game_id = ?"

        row = cur.execute(sql, (game_id,)).fetchone()
        return dict(row) if row else None

    def insert_game(conn: sqlite3.Connection, game_id: str, status: str):
        try:
            cur = conn.cursor()

            sql = f"INSERT OR IGNORE INTO games(game_id, status) VALUES (?, ?)"
        
            cur.execute(sql, (game_id, status))

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")

    def update_game(conn: sqlite3.Connection, game_data: dict):
        try:
            cur = conn.cursor()

            data = game_data.copy()
            game_id = data.pop("game_id")

            columns = ", ".join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())

            sql = f"UPDATE games SET {columns} WHERE game_id = ?"
        
            cur.execute(sql, values + [game_id])

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")

    def insert_score(conn: sqlite3.Connection, game_id: str, score_data: dict):
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

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
    def get_game_logs(conn: sqlite3.Connection, game_id: str):
        try:
            cur = conn.cursor()

            sql = """
                SELECT l.*, d.*
                FROM game_logs AS l
                LEFT OUTER JOIN details AS d
                ON l.detail_code = d.detail_code
                WHERE l.game_id = ?
                ORDER BY log_id ASC
            """
            
            rows = cur.execute(sql, (game_id,)).fetchall()
            return rows
        
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
    def get_game_score_inning(conn: sqlite3.Connection, game_id: str, inning: int, half: str):
        try:
            cur = conn.cursor()
            
            sql = "SELECT runs FROM scores WHERE game_id = ? AND inning = ? AND half = ?"

            row = cur.execute(sql, (game_id, inning, half)).fetchone()
            return row["runs"] if row else None

        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")