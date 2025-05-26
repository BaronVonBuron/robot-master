import sqlite3
from collections import namedtuple
Bottle = namedtuple('Bottle',
                        ['position', 'urscript_get', 'urscript_pour', 'urscript_back', 'img', 'title', 'bottle_type'])
class BottleContext:

    # anders path til database (dette skal laves om senere)
    # DB_PATH = r"C:\Users\ko2an\PycharmProjects\robotProgram_protoype-master\DrinksRobot\API\DAL\Database\drinks.db"
    # jacob path til database
    DB_PATH = r"C:\Users\ko2an\PycharmProjects\robotProgram_protoype-master\DrinksRobot\API\DAL\Database\drinks.db"

    def get_connection(self):
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def update_bottle_use_count(self, bottle_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                UPDATE BottleTable
                SET UseCount = UseCount + 1
                WHERE BottleId = ?
            """, (bottle_id,))
        conn.commit()
        conn.close()
        print(f"UseCount for flaske {bottle_id} er nu opdateret.")

    def get_all_bottles(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BottleTable")
        bottles = cursor.fetchall()  # Hent alle rækker
        print("Bottles fetched:", bottles)  # Debugging line
        conn.close()
        return bottles

    def create_bottle(self, position, urscript_get, urscript_pour, urscript_back, img, title, bottle_type, use_count=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO BottleTable (BottlePosition, URScriptGet, URScriptPour, URScriptBack, Img, Title, BottleType, UseCount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (position, urscript_get, urscript_pour, urscript_back, img, title, bottle_type, use_count))
        conn.commit()
        conn.close()
        print("Flaske oprettet.")

    def delete_bottle(self, bottle_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                DELETE FROM BottleTable
                WHERE BottleId = ?
            """, (bottle_id,))
        conn.commit()
        conn.close()
        print(f"Flaske med ID '{bottle_id}' blev slettet.")

    def get_Bottles_with_id(self, bottle_ids):
        conn = self.get_connection()
        cursor = conn.cursor()
        bottle_list = []

        for bottle_id in bottle_ids:
            cursor.execute("""
                    SELECT BottleId, Title, URScriptGet, URScriptPour, URScriptBack
                    FROM BottleTable
                    WHERE BottleId = ?
                """, (bottle_id,))
            row = cursor.fetchone()
            if row:
                bottle_list.append(MinimalBottle(*row))  # Use your minimal class

        conn.close()
        return bottle_list

    class MinimalBottle:
        def __init__(self, bottle_id, title, urscript_get, urscript_pour, urscript_back):
            self.bottle_id = bottle_id
            self.title = title
            self.urscript_get = urscript_get
            self.urscript_pour = urscript_pour
            self.urscript_back = urscript_back
