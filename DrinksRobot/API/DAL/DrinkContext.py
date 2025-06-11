import sqlite3
from datetime import datetime
from pathlib import Path


class DrinkContext:
    # Universal path til database
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / 'Database' / 'drinks.db'

    def get_connection(self):
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def create_drink_with_content(self, drink_name, img, bottles, use_count):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO DrinkTable (DrinkName, Img, UseCount)
                VALUES (?, ?, ?)
            """, (drink_name, img, use_count))
            drink_id = cursor.lastrowid

            for bottle_id in bottles:
                bottle_id = int(bottle_id)
                cursor.execute("""
                    SELECT Title FROM BottleTable WHERE bottleId = ?
                """, (bottle_id,))
                result = cursor.fetchone()

                if result:
                    bottle_name = result[0]
                    cursor.execute("""
                        INSERT INTO ContentTable (BottleName, BottleId, DrinkId)
                        VALUES (?, ?, ?)
                    """, (bottle_name, bottle_id, drink_id))
                else:
                    print(f"Warning: Bottle with id {bottle_id} not found.")

            conn.commit()
            print(f"Drink '{drink_name}' created with ID {drink_id}")
            return drink_id

        except Exception as e:
            conn.rollback()
            print("Error creating drink:", e)
            return None

        finally:
            conn.close()

    def update_drink_use_count(self, drink_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE DrinkTable
            SET UseCount = UseCount + 1
            WHERE DrinkId = ?
        """, (drink_id,))
        conn.commit()
        conn.close()
        print(f"UseCount for drink {drink_id} er nu opdateret.")

    def get_all_drinks(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DrinkTable")
        drinks = cursor.fetchall()
        conn.close()
        return drinks

    def get_drink_by_id(self, drink_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM DrinkTable WHERE DrinkId = ?
        """, (drink_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def get_bottle_ids_by_drink_id(self, drink_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT BottleId
            FROM ContentTable
            WHERE DrinkId = ?
        """, (drink_id,))
        bottle_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return bottle_ids

    def get_urscripts_by_bottle_id(self, bottle_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT URScriptGet, URScriptPour, URScriptBack
            FROM BottleTable
            WHERE BottleId = ?
        """, (bottle_id,))
        urscripts = cursor.fetchone()
        conn.close()
        return urscripts if urscripts else []

    def get_all_drinks_with_bottles(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                d.DrinkId,
                d.DrinkName,
                d.Img,
                d.UseCount,
                b.BottleId,
                b.Title
            FROM DrinkTable d
            LEFT JOIN ContentTable c ON d.DrinkId = c.DrinkId
            LEFT JOIN BottleTable b ON c.BottleId = b.BottleId
            ORDER BY d.DrinkId
        """)
        rows = cursor.fetchall()
        conn.close()
        drinks = {}
        for row in rows:
            drink_id = row[0]
            if drink_id not in drinks:
                drinks[drink_id] = {
                    "DrinkId": row[0],
                    "DrinkName": row[1],
                    "Img": row[2],
                    "UseCount": row[3],
                    "Bottles": []
                }
            if row[3] is not None:
                drinks[drink_id]["Bottles"].append({
                    "BottleId": row[4],
                    "Title": row[5]
                })
        return list(drinks.values())







