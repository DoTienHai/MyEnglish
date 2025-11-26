import os
import re
import sqlite3
import threading


class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path="app_data.db"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path="app_data.db"):
        if self._initialized:
            return
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self._initialized = True

    # -----------------------------
    # Core methods
    # -----------------------------
    def connect(self):
        """Kết nối SQLite database và bật foreign key."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def execute(self, query, params=(), commit=False):
        with DatabaseManager._lock:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                if commit:
                    self.conn.commit()
                lastrowid = cursor.lastrowid
                return lastrowid  # trả về ID trực tiếp
            finally:
                cursor.close()


    # -----------------------------
    # Tạo bảng
    # -----------------------------
    def create_tables(self):
        
        schema = """
        PRAGMA foreign_keys = ON;

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

        CREATE TABLE IF NOT EXISTS vocabulary (
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
        self.conn.executescript(schema)
        self.conn.commit()

    # -----------------------------
    # Sessions (bài đọc input)
    # -----------------------------
    def create_session(self, title, source_text, source_reference=""):
        if not title.strip():
            title = ""
        
        if not source_text.strip():
            raise ValueError("source_text không được để trống")
        
        if source_reference.strip():
            source_reference = source_reference.strip()

        session_id = self.execute(
            """
            INSERT INTO sessions (title, source_text, source_reference)
            VALUES (?, ?, ?)
            """,
            (title, source_text, source_reference),
            commit=True
        )
        return session_id

    def update_session(self, session_id, title=None, source_text=None, source_reference=None,
                    translated_text=None, completed=None, score=None):
        fields = []
        params = []

        if title is not None:
            fields.append("title = ?")
            params.append(title)
        if source_text is not None:
            fields.append("source_text = ?")
            params.append(source_text)
        if source_reference is not None:
            fields.append("source_reference = ?")
            params.append(source_reference)
        if translated_text is not None:
            fields.append("translated_text = ?")
            params.append(translated_text)
        if completed is not None:
            fields.append("completed = ?")
            params.append(completed)
        if score is not None:
            fields.append("score = ?")
            params.append(score)

        if not fields:
            return 0

        query = f"UPDATE sessions SET {', '.join(fields)} WHERE id = ?"
        params.append(session_id)

        self.execute(query, params, commit=True)
        return self.cursor.rowcount

    def delete_session(self, session_id):
        self.execute(
            "DELETE FROM sessions WHERE id = ?",
            (session_id,),
            commit=True
        )

    def get_sessions(self):
        cur = self.execute(
            """
            SELECT id, title, source_text, source_reference, created_at
            FROM sessions
            ORDER BY datetime(created_at) ASC
            """
        )
        return cur.fetchall()

    # -----------------------------
    # Sentences
    # -----------------------------
    def create_sentence(self, session_id, sentence_index, source_sentence):
        sentence_id=self.execute(
            """
            INSERT INTO sentences 
            (session_id, sentence_index, source_sentence)
            VALUES (?, ?, ?)
            """,
            (session_id, sentence_index, source_sentence),
            commit=True
        )
        return sentence_id



    def update_sentence(self, sentence_id, session_id=None, sentence_index=None, source_sentence=None,
                        translation_sentence=None, cloud_translation=None, score=None, note=None):
        fields = []
        values = []
        
        if session_id is not None:
            fields.append("session_id = ?")
            values.append(session_id)
        if sentence_index is not None:
            fields.append("sentence_index = ?")
            values.append(sentence_index)
        if source_sentence is not None:
            fields.append("source_sentence = ?")
            values.append(source_sentence)
        if translation_sentence is not None:
            fields.append("translated_sentence = ?")
            values.append(translation_sentence)
        if cloud_translation is not None:
            fields.append("cloud_translated_sentence = ?")
            values.append(cloud_translation)
        if score is not None:
            fields.append("score = ?")
            values.append(score)
        if note is not None:
            fields.append("note = ?")
            values.append(note)
        
        if not fields:
            return 0

        query = f"""
            UPDATE sentences
            SET {', '.join(fields)}
            WHERE id = ?
        """

        values.append(sentence_id)
        self.execute(query, values, commit=True)
        return sentence_id


    def delete_sentence(self, sentence_id):
        self.execute(
            "DELETE FROM sentences WHERE id = ?",
            (sentence_id,),
            commit=True
        )

    def get_sentences_by_session(self, session_id):
        cur = self.execute(
            """
            SELECT id, sentence_index, source_sentence, translated_sentence, cloud_translated_sentence, score, note
            FROM sentences
            WHERE session_id = ?
            ORDER BY sentence_index
            """,
            (session_id,)
        )
        return cur.fetchall()

    # -----------------------------
    # Vocabulary
    # -----------------------------
    def create_vocabulary(self, word):
        vocab_id = self.execute(
            """
            INSERT OR IGNORE INTO vocabulary (word)
            VALUES (?)
            """,
            (word,),
            commit=True
        )
        return vocab_id

    def update_vocabulary(self, vocab_id, word=None, part_of_speech=None, meaning=None, 
                          description=None, example=None, correct=None, wrong=None):
        fields = []
        params = []

        if word is not None:
            fields.append("word = ?")
            params.append(word)
        if part_of_speech is not None:
            fields.append("part_of_speech = ?")
            params.append(part_of_speech)
        if meaning is not None:
            fields.append("meaning = ?")
            params.append(meaning)
        if description is not None:
            fields.append("description = ?")
            params.append(description)
        if example is not None:
            fields.append("example = ?")
            params.append(example)
        if correct is not None:
            fields.append("correct = ?")
            params.append(correct)
        if wrong is not None:
            fields.append("wrong = ?")
            params.append(wrong)

        if not fields:
            return 0

        query = f"UPDATE vocabulary SET {', '.join(fields)} WHERE id = ?"
        params.append(vocab_id)
        self.execute(query, params, commit=True)
        return self.cursor.rowcount


    def delete_vocabulary(self, vocab_id):
        self.execute(
            "DELETE FROM vocabulary WHERE id = ?",
            (vocab_id,),
            commit=True
        )

    def get_vocabulary(self):
        cur = self.execute(
            """
            SELECT id, word, part_of_speech, meaning, description, example, correct, wrong
            FROM vocabulary
            """
        )
        return cur.fetchall()

    # -----------------------------
    # Utility
    # -----------------------------
    def __del__(self):
        self.close()


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    db = DatabaseManager(db_path="data\\app_data.db")

    # Tạo 1 bài đọc input
    session_id = db.create_session("Bài đọc 1", "Hello world. This is a test.")

    # Thêm câu
    s1 = db.create_sentence(session_id, 1, "Hello world.", translation="Xin chào thế giới.", cloud_translation="Hello world.")
    s2 = db.create_sentence(session_id, 2, "This is a test.", translation="Đây là một bài kiểm tra.", cloud_translation="This is a test.")

    # Thêm từ vựng
    vocab_id = db.create_vocabulary("world", meaning="thế giới")
    db.link_vocab_to_sentence(vocab_id, s1)
    db.link_vocab_to_sentence(vocab_id, s2)

    # Xem dữ liệu
    print("Bài đọc input:")
    print(db.get_sessions())

    print("\nCác câu trong session:")
    print(db.get_sentences_by_session(session_id))

    print("\nNgữ cảnh từ 'world':")
    print(db.get_vocab_contexts(vocab_id))

    # Xóa bài đọc input (cascade sẽ xóa câu + liên kết từ vựng)
    db.delete_session(session_id)

    print("\nSau khi xóa bài đọc input:")
    print("Bài đọc input:", db.get_sessions())
    print("Ngữ cảnh từ 'world':", db.get_vocab_contexts(vocab_id))  # nếu còn câu khác liên kết, sẽ hiển thị; ở ví dụ này tất cả bị xóa

