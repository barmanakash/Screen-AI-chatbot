import sqlite3
import os
from cryptography.fernet import Fernet

# Simple Key Management (Stored locally in the directory)
KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_FILE, "rb") as f:
    SECRET_KEY = f.read()

cipher = Fernet(SECRET_KEY)

class SecureMemory:
    def __init__(self, db_path="local_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS secure_store (
                    key TEXT PRIMARY KEY,
                    encrypted_value BLOB
                )
            """)

    def save(self, key: str, value: str):
        encrypted_data = cipher.encrypt(value.encode())
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO secure_store (key, encrypted_value) VALUES (?, ?)",
                (key, encrypted_data)
            )

    def get(self, key: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT encrypted_value FROM secure_store WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            return cipher.decrypt(row[0]).decode()
        return None