import sqlite3
from datetime import datetime
from pathlib import Path


class DrinkContext:
   # DB_PATH = r"C:\Users\ko2an\PycharmProjects\robotProgram_protoype-master\DrinksRobot\API\DAL\Database\drinks.db"
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
                       """, (bottle_name, bottle_id, drink_id ))
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








