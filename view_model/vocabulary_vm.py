from service.vocabulary_service import VocabularyService
from model.vocabulary import Vocabulary

class VocabularyViewModel:
    def __init__(self, vocabulary_service:VocabularyService):
        self.vocabulary_service = vocabulary_service

    def random_vocabulary(self) -> list[Vocabulary]:
        return self.vocabulary_service.random_vocabulary()