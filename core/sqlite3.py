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
            source_reference TEXT, 
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY,
            session_id INTEGER NOT NULL,
            sentence_index INTEGER NOT NULL,
            source_sentence TEXT NOT NULL,
            translated_sentence TEXT,
            cloud_translated_sentence TEXT,
            score REAL,
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
            correct_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(word)
        );

        CREATE TABLE IF NOT EXISTS vocabulary_sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vocab_id INTEGER NOT NULL,
            sentence_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vocab_id) REFERENCES vocabulary(id) ON DELETE CASCADE,
            FOREIGN KEY (sentence_id) REFERENCES sentences(id) ON DELETE CASCADE
        );
        """
        self.conn.executescript(schema)
        self.conn.commit()

    # -----------------------------
    # Sessions (bài đọc input)
    # -----------------------------
    def add_session(self, title, source_text, source_reference=""):
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

        if not title:
            auto_title = f"bài viết số {session_id}"
            self.execute(
                "UPDATE sessions SET title = ? WHERE id = ?",
                (auto_title, session_id),
                commit=True
            )  
        return session_id

    def get_sessions(self):
        cur = self.execute(
            """
            SELECT id, title, source_text, source_reference, created_at
            FROM sessions
            ORDER BY datetime(created_at) ASC
            """
        )
        return cur.fetchall()

    def delete_session(self, session_id):
        self.execute(
            "DELETE FROM sessions WHERE id = ?",
            (session_id,),
            commit=True
        )


    # -----------------------------
    # Sentences
    # -----------------------------
    def add_sentence(self, session_id, sentence_index, source, translation=None, cloud_translation="", score=None, note=None):
        sentence_id=self.execute(
            """
            INSERT INTO sentences 
            (session_id, sentence_index, source_sentence, translated_sentence, cloud_translated_sentence, score, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, sentence_index, source, translation, cloud_translation, score, note),
            commit=True
        )
        return sentence_id


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

    def update_sentence(self, session_id, sentence_id, translation=None, cloud_translation=None, score=None, note=None):
        """
        Cập nhật một hoặc nhiều trường trong bảng sentences cho 1 record cụ thể.
        Chỉ những trường được truyền khác None mới được cập nhật.
        """
        # Gom các cặp field = value cần cập nhật
        fields = []
        values = []

        if translation is not None:
            fields.append("translated_sentence = ?")
            values.append(translation)
        if cloud_translation is not None:
            fields.append("cloud_translated_sentence = ?")
            values.append(cloud_translation)
        if score is not None:
            fields.append("score = ?")
            values.append(score)
        if note is not None:
            fields.append("note = ?")
            values.append(note)

        # Nếu không có gì để update thì bỏ qua
        if not fields:
            return 0

        # Tạo câu query động
        query = f"""
            UPDATE sentences
            SET {', '.join(fields)}
            WHERE sentence_index = ? AND session_id = ?
        """

        values.extend([sentence_id, session_id])
        self.execute(query, values, commit=True)
        return sentence_id


    def delete_sentence(self, sentence_id):
        self.execute(
            "DELETE FROM sentences WHERE id = ?",
            (sentence_id,),
            commit=True
        )


    # -----------------------------
    # Vocabulary
    # -----------------------------
    def add_vocabulary(self, word, part_of_speech=None, meaning=None, description=None):
        self.execute(
            """
            INSERT OR IGNORE INTO vocabulary (word, part_of_speech, meaning, description)
            VALUES (?, ?, ?, ?)
            """,
            (word, part_of_speech, meaning, description),
            commit=True
        )
        cur = self.execute("SELECT id FROM vocabulary WHERE word = ?", (word,))
        return cur.fetchone()[0]


    def delete_vocabulary(self, vocab_id):
        self.execute(
            "DELETE FROM vocabulary WHERE id = ?",
            (vocab_id,),
            commit=True
        )


    # -----------------------------
    # Vocabulary sentences
    # -----------------------------
    def link_vocab_to_sentence(self, vocab_id, sentence_id):
        self.execute(
            """
            INSERT INTO vocabulary_sentences (vocab_id, sentence_id)
            VALUES (?, ?)
            """,
            (vocab_id, sentence_id),
            commit=True
        )


    def get_vocab_contexts(self, vocab_id):
        cur = self.execute(
            """
            SELECT s.source_sentence, s.translated_sentence, s.cloud_translated_sentence
            FROM vocabulary_sentences vs
            JOIN sentences s ON vs.sentence_id = s.id
            WHERE vs.vocab_id = ?
            ORDER BY s.sentence_index
            """,
            (vocab_id,)
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
    session_id = db.add_session("Bài đọc 1", "Hello world. This is a test.")

    # Thêm câu
    s1 = db.add_sentence(session_id, 1, "Hello world.", translation="Xin chào thế giới.", cloud_translation="Hello world.")
    s2 = db.add_sentence(session_id, 2, "This is a test.", translation="Đây là một bài kiểm tra.", cloud_translation="This is a test.")

    # Thêm từ vựng
    vocab_id = db.add_vocabulary("world", meaning="thế giới")
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

