def init_schema(conn):
    cur = conn.cursor()

    create_game_logs_table(cur)

    conn.commit()

def create_game_logs_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS game_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            inning INTEGER NOT NULL,
            half BOOLEAN NOT NULL,
            seq INTEGER DEFAULT 0,
            log_type TEXT NOT NULL,
            out INTEGER DEFAULT NULL,
            on_1b BOOLEAN DEFAULT FALSE,
            on_2b BOOLEAN DEFAULT FALSE,  
            on_3b BOOLEAN DEFAULT FALSE,
            ball INTEGER DEFAULT 0,
            strike INTEGER DEFAULT 0,
            batter_id INTEGER DEFAULT NULL,
            pitcher_id INTEGER DEFAULT NULL,
            detail_code TEXT DEFAULT NULL,
            raw_text TEXT
        )
        """
    )