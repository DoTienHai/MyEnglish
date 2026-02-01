from repositories.repo_base import BaseRepository
from model.sentence import Sentence
from repositories.db_connect import DBConnect


class SentenceRepository(BaseRepository):
    table_name = "sentences"
    columns = [
        "id",
        "paragraph_id",
        "sentence_index",
        "input_sentence",
        "user_translation",
        "machine_translation",
        "score",
        "note",
        "created_at"
    ]
    model_class = Sentence

    def __init__(self, db: DBConnect):
        super().__init__(db)
    
    def get_by_paragraph_id_and_sentence_index(
        self, paragraph_id: int, sentence_index: int
    ) -> Sentence | None:
        sql = """
        SELECT *
        FROM sentences
        WHERE paragraph_id = ? AND sentence_index = ?
        """
        row = self.db.fetch_one(sql, (paragraph_id, sentence_index))
        return self.to_entity(row) if row else None
    
    def get_avg_score(self):
        sql = """
        SELECT AVG(score) FROM sentences
        """
        row = self.db.fetch_one(sql)
        return row[0]
    