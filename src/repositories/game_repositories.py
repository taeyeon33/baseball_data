import sqlite3
from src.db.connect import get_connection

def insert_game(game_data):
    conn = get_connection()
    try:
        cur = conn.cursor()

        game_data

    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        conn.close()