import sqlite3

class PlayerRepositories:
    def select_season_player(conn: sqlite3.Connection, p_name: str, season_id: int, team_id: int):
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

    def select_player(conn: sqlite3.Connection, p_name: str, birthday: str):
        cur = conn.cursor()

        sql = """
            SELECT player_id, last_name, first_name
            FROM players
            WHERE birthday = ?
            AND (last_name || first_name) = ?
        """
        row = cur.execute(sql, (birthday, p_name)).fetchone()
        return row["player_id"] if row else None
        
    def update_uniform_number(conn: sqlite3.Connection, player_id: int, season_id: int, team_id: int, number: int):
        try:
            cur = conn.cursor()

            sql = f"UPDATE player_team_history SET uniform_number = ? WHERE player_id = ? AND season_id = ? AND team_id = ?"
            cur.execute(sql, (number, player_id, season_id, team_id))

            return cur.rowcount
        
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
    def select_player_position(conn: sqlite3.Connection, player_id: int, position_code: str):
        cur = conn.cursor()

        sql = "SELECT * FROM player_positions WHERE player_id = ? AND position_code = ?"

        cur.execute(sql, (player_id, position_code))
        return cur.fetchone()