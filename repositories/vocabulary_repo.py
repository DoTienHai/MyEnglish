from repositories.repo_base import BaseRepository
from model.vocabulary import Vocabulary
from repositories.db_connect import DBConnect

class VocabularyRepository(BaseRepository[Vocabulary]):
    table_name = "vocabulary_items"
    columns = [
        "id",
        "word",
        "part_of_speech",
        "vi_meaning",
        "eng_description",
        "example",
        "note",
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
    
    def get_all_vocabulary(self):
        return self.all()
    
    def count_all(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        row = self.db.fetch_one(query)
        return row[0] if row else 0
    
    def get_all_vocabulary_complete(self) -> list[Vocabulary] | None:
        # TO DO: get all vocabulary entries with complete examples and vi_meaning (non-empty example field)
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE example IS NOT NULL AND example != '' AND vi_meaning IS NOT NULL AND vi_meaning != ''
        """
        rows = self.db.fetch_all(query)
        return [self.to_entity(row) for row in rows] if rows else None
        
        
        


    
    