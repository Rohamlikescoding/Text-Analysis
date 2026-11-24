from  datetime import datetime, timezone
import sqlite3
from typing import Optional

from fastapi import HTTPException

 

DB_PATH = "text-history.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")  
    return connection

def create_database():
    connection = get_connection()
    try:
            connection.execute("""CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                hashed_password TEXT NOT NULL,
                full_name TEXT
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT,
                    raw_text TEXT,
                    word_count INTEGER,
                    character_count INTEGER,
                    username TEXT NOT NULL,
                    FOREIGN KEY (username) REFERENCES users(username)
                    )
                    """)
            connection.commit()
    finally:
            connection.close()


def add_history(raw_text: str, word_count: int, character_count: int, user):
    created_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    try:
        connection.execute("""INSERT INTO history(created_at, raw_text, word_count, character_count, username) VALUES (?, ?, ?, ? ,?)""", (created_at, raw_text,word_count, character_count, user))
        connection.commit()
    finally:
        connection.close()

def get_history(user):
    connection = get_connection()
    try:
        return [dict(r) for r in connection.execute("SELECT * FROM history WHERE username =? ORDER BY id DESC LIMIT 50 ",(user,))]
    finally:
        connection.close()

def get_user(username: str) -> Optional[dict]:
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT username, hashed_password, full_name FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    finally:
        connection.close()
    if row:
        return {
            "username": row["username"],
            "hashed_password": row["hashed_password"],
            "full_name": row["full_name"],
        }
    return None

def create_user(username: str, hashed_password: str, full_name: str = ""):
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO users (username, hashed_password, full_name) VALUES (?, ?, ?)",
            (username, hashed_password, full_name),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()