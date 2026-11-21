from  datetime import datetime, timezone
import sqlite3
from typing import Optional

from fastapi import HTTPException

 

DB_PATH = "text-history.db"
USER_DB_PATH = "user.db"

def get_user_connection():
    connection = sqlite3.connect(USER_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_databases():
    connection = get_connection()
    try:
        connection.execute("""CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENt,
        created_at TEXT,
        raw_text TEXT,
        word_count INTEGER,
        character_count INTEGER)""")
        connection.commit()
    finally:
        connection.close()

    # users table in user.db
    user_connection = get_user_connection()
    try:
        user_connection.execute("""CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            full_name TEXT
        )""")
        user_connection.commit()
    finally:
        user_connection.close()

def add_history(raw_text: str, word_count: int, character_count: int):
    created_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    try:
        connection.execute("""INSERT INTO history(created_at, raw_text, word_count, character_count) VALUES (?, ?, ?, ? )""", (created_at, raw_text,word_count, character_count))
        connection.commit()
    finally:
        connection.close()

def get_history():
    connection = get_connection()
    try:
        return [dict(r) for r in connection.execute("SELECT * FROM history ORDER BY id DESC LIMIT 50")]
    finally:
        connection.close()

def get_user(username: str) -> Optional[dict]:
    connection = get_user_connection()
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
    connection = sqlite3.connect(USER_DB_PATH)
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