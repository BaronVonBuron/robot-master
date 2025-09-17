import sqlite3
from pathlib import Path


class MenuContext:
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / 'Database' / 'drinks.db'

    def get_connection(self):
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    # Catalog
    def list_catalog(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT CatalogBottleId, Title, BottleType, Img, URScriptGet, URScriptPour, URScriptBack
                FROM BottleCatalog ORDER BY Title
            """)
            rows = cur.fetchall()
            return [
                {
                    "catalog_bottle_id": r[0],
                    "title": r[1],
                    "bottle_type": r[2],
                    "img": r[3],
                    "urscript_get": r[4],
                    "urscript_pour": r[5],
                    "urscript_back": r[6],
                }
                for r in rows
            ]

    # Menus
    def create_menu(self, name: str) -> int:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO MenuTable (MenuName) VALUES (?)", (name,))
            conn.commit()
            return cur.lastrowid

    def list_menus(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT MenuId, MenuName, CreatedAt, IsActive FROM MenuTable ORDER BY MenuId DESC")
            return [
                {"menu_id": r[0], "menu_name": r[1], "created_at": r[2], "is_active": r[3] == 1}
                for r in cur.fetchall()
            ]

    def set_active_menu(self, menu_id: int) -> bool:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE MenuTable SET IsActive = 0")
            cur.execute("UPDATE MenuTable SET IsActive = 1 WHERE MenuId = ?", (menu_id,))
            conn.commit()
            return cur.rowcount > 0

    # Menu bottles
    def add_bottle_to_menu(self, menu_id: int, catalog_bottle_id: int, position: int | None = None) -> bool:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO MenuBottle (MenuId, CatalogBottleId, Position) VALUES (?,?,?)",
                (menu_id, catalog_bottle_id, position),
            )
            conn.commit()
            return True

    def remove_bottle_from_menu(self, menu_id: int, catalog_bottle_id: int) -> bool:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM MenuBottle WHERE MenuId = ? AND CatalogBottleId = ?",
                (menu_id, catalog_bottle_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def get_menu_bottles(self, menu_id: int):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT mb.CatalogBottleId, mb.Position,
                       bc.Title, bc.BottleType, bc.Img, bc.URScriptGet, bc.URScriptPour, bc.URScriptBack
                FROM MenuBottle mb
                JOIN BottleCatalog bc ON bc.CatalogBottleId = mb.CatalogBottleId
                WHERE mb.MenuId = ?
                ORDER BY COALESCE(mb.Position, 9999), bc.Title
                """,
                (menu_id,),
            )
            return [
                {
                    "catalog_bottle_id": r[0],
                    "position": r[1],
                    "title": r[2],
                    "bottle_type": r[3],
                    "img": r[4],
                    "urscript_get": r[5],
                    "urscript_pour": r[6],
                    "urscript_back": r[7],
                }
                for r in cur.fetchall()
            ]
