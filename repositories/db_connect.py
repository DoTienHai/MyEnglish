import os
import sqlite3
import threading

# DBConnect class to manage SQLite database connections
class DBConnect:
    # Singleton instance
    # to ensure only one connection per application
    _instance = None
    # Thread lock for thread-safe singleton
    # especially important for multi-threaded applications
    _lock = threading.Lock()

    # Singleton implementation
    # __new__ is responsible for creating a new instance of the class.
    # It checks if an instance already exists; if not, it creates one.
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DBConnect, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance
    
    # Initializer
    # __init__ is responsible for initializing the instance.
    def __init__(self, db_path="data.db"):
        if self._initialized:
            return
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.db_path = db_path
        self.conn = None
        self.connect()
        self._initialized = True
        
    # Connect to the SQLite database
    # If the database file does not exist, it will be created.
    # The check_same_thread=False parameter allows the connection to be used across multiple threads.
    # Enabling foreign key constraints with PRAGMA foreign_keys = ON; --> ensures that foreign key constraints are enforced.
    # explained: PRAGMA foreign_keys = ON; is necessary because, by default, SQLite does not enforce foreign key constraints.
    # what is foreign key constraints: Foreign key constraints ensure referential integrity between tables, meaning that relationships between tables are maintained correctly.
    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def commit(self):
        if self.conn:
            self.conn.commit()
    
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
