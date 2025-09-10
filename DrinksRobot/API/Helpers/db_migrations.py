import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'DAL' / 'Database' / 'drinks.db'


def _column_exists(conn, table: str, column: str) -> bool:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cur.fetchall()]
    return column in cols


def ensure_db_schema():
    conn = sqlite3.connect(DB_PATH)
    try:
        # Add ScriptName column to DrinkTable if missing
        if not _column_exists(conn, 'DrinkTable', 'ScriptName'):
            conn.execute("ALTER TABLE DrinkTable ADD COLUMN ScriptName TEXT")
            conn.commit()
    finally:
        conn.close()
