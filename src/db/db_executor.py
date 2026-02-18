from src.db.connect import get_connection
from src.repositories.base_repository import BaseRepository

def insert_and_commit(table: str, rows: dict, return_id: bool = False, ignore: bool = False):
    conn = get_connection()
    try:
        result = BaseRepository.insert(conn, table, rows, return_id, ignore)
        conn.commit()
        return result
    
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Database error: {e}")

    finally:
        conn.close()