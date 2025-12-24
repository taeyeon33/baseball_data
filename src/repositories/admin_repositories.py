import sqlite3
from src.db.connect import get_connection

def fetch_all_tables():
    tables = table_exists("all", "sqlite_%")

    schema = {}

    for table in tables:
        if any(c in table for c in ("batter", "pitcher_game_stats", "pitcher_season_stats", "game_logs")):
            continue
        
        schema[table] = get_columns(table)

    return schema

def fetch_all_players():
    conn = get_connection()
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT * FROM players ORDER BY last_name
        """
    ).fetchall()
    
    conn.close()
    return rows

def table_exists(type, params):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    condition = "name NOT LIKE ?" if type == "all" else "name = ?"
    sql = f"""
        SELECT name FROM sqlite_master WHERE type = 'table' AND {condition}
    """
    cur.execute(sql, (params,))

    returnData = []
    if (type == "all"):
        returnData = [row["name"] for row in cur.fetchall()]
    else:
        returnData = cur.fetchone() is not None

    conn.close()
    return returnData

def get_columns(table):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    columns = []

    cur.execute(f"PRAGMA table_info({table})")
    for col in cur.fetchall():
        columns.append({
            "name": col["name"],
            "type": col["type"],
            "notnull": bool(col["notnull"]),
            "primary_key": bool(col["pk"]),
            "default": col["dflt_value"]
        })
    
    conn.close()
    return columns

def insert_row(table, rows):
    conn = get_connection()
    cur = conn.cursor()

    columns = ", ".join(rows.keys())
    placeholders = ", ".join(["?"] * len(rows))
    values = list(rows.values())

    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    cur.execute(sql, values)
    conn.commit()

    idx = cur.lastrowid

    conn.close()
    return idx