import sqlite3
from datetime import datetime
from pathlib import Path


class LogContext:
    # Universal path til database
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / 'Database' / 'drinks.db'
    def get_connection(self):
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def get_all_logs(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LogTable")
        logs = cursor.fetchall()  # Hent alle logs
        conn.close()
        return logs

    def get_logs_by_type(self, log_type):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM LogTable
            WHERE Type = ?
        """, (log_type,))
        logs = cursor.fetchall()
        conn.close()
        return logs

    def create_log(self, log_msg, log_type):
        conn = self.get_connection()
        cursor = conn.cursor()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO LogTable (Time, LogMsg, Type)
            VALUES (?, ?, ?)
        """, (time_now, log_msg, log_type))
        conn.commit()
        conn.close()
        print("Log oprettet.")

