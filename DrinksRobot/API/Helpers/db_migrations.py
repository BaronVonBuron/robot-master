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

        # Create BottleCatalog table (stores all bottles ever used)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS BottleCatalog (
                CatalogBottleId INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                BottleType TEXT,
                Img TEXT,
                URScriptGet TEXT,
                URScriptPour TEXT,
                URScriptBack TEXT,
                CreatedAt TEXT DEFAULT (datetime('now'))
            )
            """
        )

        # Create Menu tables
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS MenuTable (
                MenuId INTEGER PRIMARY KEY AUTOINCREMENT,
                MenuName TEXT NOT NULL,
                CreatedAt TEXT DEFAULT (datetime('now')),
                IsActive INTEGER DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS MenuBottle (
                MenuId INTEGER NOT NULL,
                CatalogBottleId INTEGER NOT NULL,
                Position INTEGER,
                PRIMARY KEY (MenuId, CatalogBottleId),
                FOREIGN KEY (MenuId) REFERENCES MenuTable(MenuId) ON DELETE CASCADE,
                FOREIGN KEY (CatalogBottleId) REFERENCES BottleCatalog(CatalogBottleId) ON DELETE CASCADE
            )
            """
        )

        # Backfill BottleCatalog from current BottleTable if catalog is empty
        cur = conn.cursor()
        cur.execute("SELECT COUNT(1) FROM BottleCatalog")
        count = cur.fetchone()[0]
        if count == 0:
            # Insert distinct bottles from BottleTable
            cur.execute(
                """
                INSERT INTO BottleCatalog (Title, BottleType, Img, URScriptGet, URScriptPour, URScriptBack)
                SELECT DISTINCT Title, BottleType, Img, URScriptGet, URScriptPour, COALESCE(URScriptBack,'')
                FROM BottleTable
                """
            )
            conn.commit()
    finally:
        conn.close()
