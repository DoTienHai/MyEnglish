from repositories.db_connect import DBConnect


# DB initialization: create tables if they do not exist
class DBInit:
    def __init__(self, db:DBConnect):
        self.db = db

    def create_tables(self):
        # Table: paragraphs
        # Description:
        #   Stores information about each working/learning paragraph.
        #
        # Columns:
        #   id                   : Primary key, unique identifier for each paragraph
        #   title                : Short title or description of the paragraph
        #   input_paragraph      : Original input paragraph provided by the user
        #   reference            : Reference: link or source for the paragraph
        #   machine_translation  : Machine-generated result (e.g. AI translation)
        #   completed            : Completion progress in percentage (0–100)
        #   score                : Evaluation score (0–10)
        #   created_at           : Timestamp when the paragraph was created
        paragraph_table = """
        CREATE TABLE IF NOT EXISTS paragraphs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            input_paragraph TEXT NOT NULL,
            reference TEXT DEFAULT "",
            machine_translation TEXT DEFAULT "",
            completed REAL DEFAULT 0.0 CHECK(completed >= 0 AND completed <= 100),
            score REAL DEFAULT 0.0 CHECK(score >= 0 AND score <= 10),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # Table: sentences
        # Description:
        #   Stores individual sentences associated with paragraphs.
        #
        # Columns:
        #   id                        : Primary key, unique identifier for each sentence
        #   paragraph_id              : Foreign key referencing the associated paragraph
        #   sentence_index            : Index of the sentence within the paragraph
        #   input_sentence            : Original sentence text
        #   user_translation          : User-provided translation of the sentence
        #   machine_translation       : Machine-generated translation of the sentence
        #   score                     : Evaluation score for the sentence (0–10)
        #   note                      : Additional notes or comments about the sentence
        #   created_at                : Timestamp when the sentence was created
        #
        #  Explanation of Foreign Key:
        #     The paragraph_id column is a foreign key that references the id column in the paragraphs table.
        #     This establishes a relationship between sentences and their corresponding paragraphs,
        #     ensuring that each sentence is associated with a valid paragraph.
        #  Explanation of ON DELETE CASCADE:
        #     The ON DELETE CASCADE clause ensures that when a paragraph is deleted from the paragraphs table,
        #     all associated sentences in the sentences table are automatically deleted as well.
        sentence_table = """
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY,
            paragraph_id INTEGER NOT NULL,
            sentence_index INTEGER NOT NULL,
            input_sentence TEXT NOT NULL,
            user_translation TEXT,
            machine_translation TEXT,
            score REAL DEFAULT 0.0 CHECK(score >= 0 AND score <= 10),
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (paragraph_id) REFERENCES paragraphs(id) ON DELETE CASCADE
        );
        """
        
        # Table: vocabulary_items
        # Description:
        #   Stores vocabulary words along with their details and frequency statistics.
        #
        # Columns:
        #   id                : Primary key, unique identifier for each vocabulary entry
        #   word              : The vocabulary word
        #   part_of_speech    : Part of speech (e.g., noun, verb, adjective)
        #   vi_meaning        : Meaning of the word in Vietnamese
        #   eng_description   : English description or definition of the word
        #   example           : Example sentence using the word
        #   note              : Additional notes or comments about the word
        #   correct_count     : Number of times the word was answered correctly
        #   wrong_count       : Number of times the word was answered incorrectly
        #   created_at        : Timestamp when the vocabulary entry was created
        vocab_table = """
        CREATE TABLE IF NOT EXISTS vocabulary_items (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            part_of_speech TEXT,
            vi_meaning TEXT,
            eng_description TEXT,
            example TEXT,
            note TEXT,
            correct_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        self.db.execute(paragraph_table, commit=True)
        self.db.execute(sentence_table, commit=True)
        self.db.execute(vocab_table, commit=True)
        
        
if __name__ == "__main__":
    db = DBConnect("test.db")
    db_init = DBInit(db)
    db_init.create_tables()
    
    
