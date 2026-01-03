from repositories.repo_base import BaseRepository
from model.sentence import Sentence
from repositories.db_connect import DBConnect

class SentenceRepository(BaseRepository):
    table_name = "sentences"
    columns = [
        "id",
        "session_id",
        "sentence_index",
        "source_sentence",
        "translated_sentence",
        "cloud_translated_sentence",
        "score",
        "note",
        "created_at"
    ]
    model_class = Sentence

    def __init__(self, db: DBConnect):
        super().__init__(db)
        
    def get(self, id: int) -> Sentence:
        return super().get(id)
    
    