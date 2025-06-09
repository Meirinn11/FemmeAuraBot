import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                last_period_date TEXT,
                cycle_length INTEGER DEFAULT 28,
                mood TEXT
            )
        ''')
        self.conn.commit()

    def save_period(self, user_id, last_period):
        self.cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, last_period_date)
            VALUES (?, ?)
        ''', (user_id, last_period))
        self.conn.commit()

    def save_mood(self, user_id, mood):
        self.cursor.execute('''
            UPDATE users SET mood = ? WHERE user_id = ?
        ''', (mood, user_id))
        self.conn.commit()