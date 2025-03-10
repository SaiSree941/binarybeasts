import sqlite3

def create_user_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            difficulty_level TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, difficulty_level):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, difficulty_level)
        VALUES (?, ?, ?)
    """, (user_id, username, difficulty_level))
    conn.commit()
    conn.close()