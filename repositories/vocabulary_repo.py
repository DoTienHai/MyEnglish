from repositories.repo_base import BaseRepository
from model.vocabulary import Vocabulary
from repositories.db_connect import DBConnect

class VocabularyRepository(BaseRepository):
    table_name = "vocabularies"
    columns = [
        "id",
        "word",
        "part_of_speech",
        "meaning",
        "description",
        "example",
        "correct_count",
        "wrong_count",
        "created_at"
    ]
    model_class = Vocabulary

    def __init__(self, db: DBConnect):
        super().__init__(db)
        
    def get(self, id: int) -> Vocabulary:
        return super().get(id)
    
    def count_vocabulary_grouped_by_date(self, from_date: str):
        query = f"""
            SELECT
                date(created_at) AS day,
                COUNT(*) AS total
            FROM {self.table_name}
            WHERE date(created_at) >= date(?)
            GROUP BY date(created_at)
            ORDER BY day
        """
        return self.db.fetch_all(query, (from_date,))


    
    