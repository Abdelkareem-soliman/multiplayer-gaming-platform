import sqlite3

def init_postgres(app):
    conn = sqlite3.connect("gaming.db", check_same_thread=False)
    app.pg_conn = conn

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            player_id TEXT PRIMARY KEY,  -- ← changed from INTEGER to TEXT
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id TEXT PRIMARY KEY,  -- ← changed to TEXT (e.g., UUID)
            player_1_id TEXT,
            player_2_id TEXT,
            winner_id TEXT
        )
    ''')

    conn.commit()

