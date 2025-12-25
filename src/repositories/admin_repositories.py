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

def fetch_data_list(table):
    conn = get_connection()
    cur = conn.cursor()

    sql = f"SELECT * FROM {table} ORDER BY 1 DESC"
    rows = cur.execute(sql).fetchall()
    
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

def get_data(table, rows):
    conn = get_connection()
    cur = conn.cursor()

    where_clause = " AND ".join([f"{k} = ?" for k, v in rows.items()])
    values = list(rows.values())

    sql = f"SELECT * FROM {table} WHERE {where_clause}"

    data = cur.execute(sql, values).fetchone()
    conn.commit()

    conn.close()
    return data

def update_row(table, set_rows, where_rows):
    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{k} = ?" for k, v in set_rows.items()])
    where_clause = " AND ".join([f"{k} = ?" for k, v in where_rows.items()])

    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    params = tuple(set_rows.values()) + tuple(where_rows.values())

    cur.execute(sql, params)
    conn.commit()

    cnt = cur.rowcount

    conn.close()
    return cnt

def delete_row(table, rows):
    conn = get_connection()
    cur = conn.cursor()

    where_clause = " AND ".join([f"{k} = ?" for k, v in rows.items()])
    values = list(rows.values())

    sql = f"DELETE FROM {table} WHERE {where_clause}"

    cur.execute(sql, values)
    conn.commit()

    cnt = cur.rowcount

    conn.close()
    return cnt    