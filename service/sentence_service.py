from datetime import datetime
from repositories.db_connect import DBConnect
from repositories.sentence_repo import SentenceRepository
from model.sentence import Sentence
from shared.text_utils import split_into_sentences


class SentenceService:
    """
    Service layer for Sentence entity.
    Handles business logic related to sentence operations.
    """

    def __init__(self):
        self.sentence_repo = SentenceRepository(DBConnect())

    def create_sentence(self, paragraph_id: int, sentence_index: int,
                        input_sentence: str,
                        machine_translation: str) -> int:
        now = datetime.now().isoformat()
        new_sentence = Sentence(
            id=None,
            paragraph_id=paragraph_id,
            sentence_index=sentence_index,
            input_sentence=input_sentence,
            user_translation="",
            machine_translation=machine_translation,
            score=0.0,
            note="",
            created_at=now
        )
        sentence_id = self.sentence_repo.create(new_sentence)
        return sentence_id

    def update_sentence(self, sentence_id: int,
                        user_translation: str = None,
                        machine_translation: str = None,
                        score: float = None,
                        note: str = None):
        sentence = self.sentence_repo.get(sentence_id)
        if not sentence:
            msg = f"Sentence with id {sentence_id} does not exist."
            raise ValueError(msg)

        if user_translation is not None:
            sentence.user_translation = user_translation
        if machine_translation is not None:
            sentence.machine_translation = machine_translation
        if score is not None:
            if not (0 <= score <= 10):
                raise ValueError("score must be between 0-10")
            sentence.score = score
        if note is not None:
            sentence.note = note

        self.sentence_repo.update(sentence)

    def get_sentences_by_paragraph_id(
            self, paragraph_id: int) -> list[Sentence]:
        """Get all sentences in a paragraph."""
        return self.sentence_repo.filter(paragraph_id=paragraph_id)

    def count_sentences_by_paragraph_id(self, paragraph_id: int) -> int:
        """Count sentences in a paragraph."""
        return self.sentence_repo.count_by(paragraph_id=paragraph_id)

    def get_sentence_by_paragraph_and_index(
            self, paragraph_id: int,
            sentence_index: int) -> Sentence | None:
        """Get a specific sentence by paragraph ID and index."""
        return self.sentence_repo.get_by_paragraph_id_and_sentence_index(
            paragraph_id, sentence_index)

    def get_avg_score(self) -> float:
        """Get average score of all sentences."""
        return self.sentence_repo.get_avg_score()


if __name__ == "__main__":  # pragma: no cover
    sentence_service = SentenceService()
    count = sentence_service.count_sentences_by_paragraph_id(1)
    print(count)

