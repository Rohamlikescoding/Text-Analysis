from  datetime import datetime, timezone
import sqlite3


DB_PATH = "text-history.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_database():
    connection = get_connection()
    try:
        connection.execute("""CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENt,
        created_at TEXT,
        raw_text TEXT,
        word_count INTEGER,
        character_count INTEGER
        )
        """)
        connection.commit()
    finally:
        connection.close()


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
