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

def fetch_data_list(table, options=None):
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = f"SELECT * FROM {table} ORDER BY 1 DESC"
        if options and options.get("player_name"):
            sql = f"SELECT p.last_name, p.first_name, t.* FROM players AS p JOIN {table} AS t ON p.player_id = t.player_id ORDER BY t.player_id DESC"
        if options and options.get("positions"):
            sql = f"SELECT * FROM {table} ORDER BY position_number ASC"
        rows = cur.execute(sql).fetchall()
        print(sql)
        return rows
    
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()

def table_exists(type, params):
    conn = get_connection()
    try:
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
        
        return returnData
    
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()

def get_columns(table):
    conn = get_connection()
    try:
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
        
        return columns
    
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()

def insert_row(table, rows):
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

def get_data(table, rows):
    conn = get_connection()
    try:
        cur = conn.cursor()

        where_clause = " AND ".join([f"{k} = ?" for k, v in rows.items()])
        values = list(rows.values())

        sql = f"SELECT * FROM {table} WHERE {where_clause}"

        data = cur.execute(sql, values).fetchone()
        conn.commit()

        return data
    
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()

def update_row(table, set_rows, where_rows):
    conn = get_connection()
    try:
        cur = conn.cursor()

        set_clause = ", ".join([f"{k} = ?" for k, v in set_rows.items()])
        where_clause = " AND ".join([f"{k} = ?" for k, v in where_rows.items()])

        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(set_rows.values()) + tuple(where_rows.values())

        cur.execute(sql, params)
        conn.commit()

        cnt = cur.rowcount

        return cnt
    
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()

def delete_row(table, rows):
    conn = get_connection()
    try:
        cur = conn.cursor()

        where_clause = " AND ".join([f"{k} = ?" for k, v in rows.items()])
        values = list(rows.values())

        sql = f"DELETE FROM {table} WHERE {where_clause}"

        cur.execute(sql, values)
        conn.commit()

        cnt = cur.rowcount

        return cnt
    
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()