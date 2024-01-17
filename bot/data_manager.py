import os
from dotenv.main import load_dotenv
import sqlite3

load_dotenv()
TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
class UserDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_users_table()

    def _create_users_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    balance INTEGER
                )
            """)
            conn.commit()

    def is_user_exists(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
            result = cursor.fetchone()
        return result is not None

    def add_new_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 0))
            conn.commit()

    def get_user_balance(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            result = cursor.fetchone()
        return result[0] if result else 0

    def update_user_balance(self, user_id, new_balance):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
            conn.commit()