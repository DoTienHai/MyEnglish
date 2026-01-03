import os
import sqlite3
import threading

class DBConnect:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DBConnect, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_path="app_data.db"):
        if self._initialized:
            return
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.db_path = db_path
        self.conn = None
        self.connect()
        self._initialized = True
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def execute(self, query, params=(), commit=False):
        with DBConnect._lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                if commit:
                    self.conn.commit()
                lastrowid = cursor.lastrowid
                return lastrowid  # trả về ID trực tiếp
            finally:
                cursor.close()
    
    def fetch_all(self, query, params=()):
        with DBConnect._lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            finally:
                cursor.close()

    def fetch_one(self, query, params=()):
        with DBConnect._lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchone()
            finally:
                cursor.close()

                
if __name__ == "__main__":
    db = DBConnect(r"test.db")
