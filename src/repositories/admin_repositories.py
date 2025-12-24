import sqlite3
from src.db.connect import get_connection

def fetch_all_tables():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        """
    )

    tables = [row["name"] for row in cur.fetchall()]

    schema = {}

    for table in tables:
        if any(c in table for c in ("batter", "pitcher_game_stats", "pitcher_season_stats", "game_logs")):
            continue
        cur.execute(f"PRAGMA table_info({table})")
        columns = []

        for col in cur.fetchall():
            columns.append({
                "name": col["name"],
                "type": col["type"],
                "notnull": bool(col["notnull"]),
                "primary_key": bool(col["pk"]),
                "default": col["dflt_value"]
            })
        
        schema[table] = columns
    
    conn.close()

    return schema

def fetch_all_players():
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM players ORDER BY last_name
        """
    ).fetchall()
    conn.close()
    return rows