import sqlite3
from contants.app_const import DB


def init_db():
    with sqlite3.connect(DB) as db:
        cursor = db.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rank INTEGER DEFAULT 0
        )
        """
        )
        db.commit()


def register_user(username, password):
    with sqlite3.connect(DB) as db:
        cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users(username, password) VALUES (?, ?)", (username, password)
    )
    db.commit()


def login_user(username, password):
    with sqlite3.connect(DB) as db:
        cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password)
    )
    return cursor.fetchone()


def get_user_rank(username):
    with sqlite3.connect(DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT rank FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None


def get_users_by_rank():
    with sqlite3.connect(DB) as db:
        cursor = db.cursor()
        cursor.execute("SELECT username, rank FROM users ORDER BY rank DESC")
        return cursor.fetchall()


def update_user_rank(username, rank_increment):
    with sqlite3.connect(DB) as db:
        cursor = db.cursor()
        # Update the rank by incrementing it with the given rank_increment value
        cursor.execute(
            "UPDATE users SET rank = rank + ? WHERE username = ?",
            (rank_increment, username),
        )
        db.commit()

init_db()