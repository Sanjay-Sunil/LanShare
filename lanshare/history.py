import sqlite3
from datetime import datetime

import config


class HistoryManager:
    def __init__(self, db_file=config.DATABASE_FILE):
        self.db_file = db_file
        self.initialize_database()

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def initialize_database(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                peer_name TEXT,
                peer_ip TEXT,
                filename TEXT,
                file_size INTEGER,
                direction TEXT,
                status TEXT,
                timestamp TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def add_transfer(self, peer_name, peer_ip, filename, file_size, direction, status):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transfers
                (peer_name, peer_ip, filename, file_size, direction, status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                peer_name,
                peer_ip,
                filename,
                file_size,
                direction,
                status,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()

    def get_all(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transfers ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def clear_history(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transfers")
        conn.commit()
        conn.close()

    def show_history(self):
        rows = self.get_all()

        if not rows:
            print("No transfer history yet.")
            return

        header = "{:<4}{:<16}{:<16}{:<22}{:<10}{:<10}{:<10}{}".format(
            "ID", "Peer Name", "Peer IP", "Filename", "Size", "Direction", "Status", "Timestamp"
        )
        print(header)
        print("-" * len(header))

        for row in rows:
            tid, peer_name, peer_ip, filename, file_size, direction, status, timestamp = row
            print(
                "{:<4}{:<16}{:<16}{:<22}{:<10}{:<10}{:<10}{}".format(
                    tid, peer_name, peer_ip, filename, file_size, direction, status, timestamp
                )
            )
