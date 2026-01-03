from repositories.db_connect import DBConnect


class DBInit:
    def __init__(self, db:DBConnect):
        self.db = db
        
    def create_tables(self):
        session_table = """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            source_text TEXT NOT NULL,
            source_reference TEXT DEFAULT "",
            translated_text TEXT DEFAULT "",
            completed REAL DEFAULT 0.0 CHECK(completed >= 0 AND completed <= 100),
            score REAL DEFAULT 0.0 CHECK(score >= 0 AND score <= 10),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """

        sentence_table = """
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY,
            session_id INTEGER NOT NULL,
            sentence_index INTEGER NOT NULL,
            source_sentence TEXT NOT NULL,
            translated_sentence TEXT,
            cloud_translated_sentence TEXT,
            score REAL DEFAULT 0.0 CHECK(score >= 0 AND score <= 10),
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );
        """
        
        vocab_table = """
        CREATE TABLE IF NOT EXISTS vocabularies (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            part_of_speech TEXT,
            meaning TEXT,
            description TEXT,
            example TEXT,
            correct_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(word)
        );
        """
        
        self.db.execute(session_table, commit=True)
        self.db.execute(sentence_table, commit=True)
        self.db.execute(vocab_table, commit=True)
        
        
if __name__ == "__main__":
    db = DBConnect("test.db")
    db_init = DBInit(db)
    db_init.create_tables()