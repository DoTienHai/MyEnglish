import re
from datetime import datetime
from repositories.db_connect import DBConnect
from repositories.sentence_repo import SentenceRepository
from model.sentence import Sentence

class SentenceService:
    def __init__(self):
        self.sentence_repo = SentenceRepository(DBConnect())
    
    def split_into_sentences(self, text: str) -> list:
        split_input = re.split(r'(?<=[.!?])[\s\n]+', text.strip())
        sentences = []
        for sentence in split_input:
            sentence = sentence.strip()
            if not sentence:
                continue
            sentences.append(sentence)
        return sentences
    
    def create_sentence(self, session_id:int, sentence_index:int, source_sentence:str, cloud_translation:str) -> int:
        now = datetime.now().isoformat()
        new_sentence = Sentence(
            id=None,
            session_id=session_id,
            sentence_index=sentence_index,
            source_sentence=source_sentence,
            translated_sentence="",
            cloud_translated_sentence=cloud_translation,
            score=0.0,
            note="",
            created_at=now
        )
        sentence_id = self.sentence_repo.create(new_sentence)
        return sentence_id
    
    def update_sentence(self, sentence_id:int, translated_sentence:str = None, cloud_translated_sentence:str = None, score:float = None, note:str = None):
        sentence = self.sentence_repo.get(sentence_id)
        if not sentence:
            raise ValueError(f"Sentence with id {sentence_id} does not exist.")
        
        if translated_sentence is not None:
            sentence.translated_sentence = translated_sentence
        if cloud_translated_sentence is not None:
            sentence.cloud_translated_sentence = cloud_translated_sentence
        if score is not None:
            sentence.score = score
        if note is not None:
            sentence.note = note

        self.sentence_repo.update(sentence)
        
    def get_sentence_by_session_id(self, session_id:int) -> list[Sentence]:
        sentences = self.sentence_repo.filter(session_id=session_id)
        return sentences
    
    def count_sentences_by_session_id(self, session_id:int) -> int:
        count = self.sentence_repo.count_by(session_id=session_id)
        return count

    def get_sentence_by_session_id_and_sentence_index(self, session_id:int, sentence_index:int) -> Sentence:
        return self.sentence_repo.get_by_session_id_and_sentence_index(session_id, sentence_index)
    
if __name__ == "__main__":
    sentence_service = SentenceService()
    sentences = sentence_service.count_sentences_by_session_id(1)
    print(sentences)

