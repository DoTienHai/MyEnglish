from datetime import datetime
from repositories.db_connect import DBConnect
from repositories.vocabulary_repo import VocabularyRepository
from model.vocabulary import Vocabulary
import random

class VocabularyService:
    def __init__(self):
        self.vocab_repo = VocabularyRepository(DBConnect())

    
    def create_vocabulary(self, word: str, part_of_speech: str, meaning: str, description: str, example: str) -> int:
        now = datetime.now().isoformat()
        new_vocab = Vocabulary(
            id=None,
            word=word,
            part_of_speech=part_of_speech,
            meaning=meaning,
            description=description,
            example=example,
            correct_count=0,
            wrong_count=0,
            created_at=now
        )
        vocab_id = self.vocab_repo.create(new_vocab)
        return vocab_id
    
    def update_vocabulary(self, vocab_id: int, correct_count: int = None, wrong_count: int = None):
        vocabulary = (Vocabulary)(self.vocab_repo.get(vocab_id))
        if not vocabulary:
            raise ValueError(f"Vocabulary with id {vocab_id} does not exist.")
        
        if correct_count is not None:
            vocabulary.correct_count = correct_count
        if wrong_count is not None:
            vocabulary.wrong_count = wrong_count
        
        self.vocab_repo.update(vocabulary)
        
    def random_vocabulary(self) -> list[Vocabulary]:
        all_vocabularies = self.vocab_repo.all()
        if len(all_vocabularies) == 0:
            return None
        return random.choice(all_vocabularies)