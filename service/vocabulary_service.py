import random
from datetime import datetime
from repositories.db_connect import DBConnect
from repositories.vocabulary_repo import VocabularyRepository
from model.vocabulary import Vocabulary


class VocabularyService:
    """
    Service layer for Vocabulary entity.
    Handles business logic related to vocabulary operations.
    """

    def __init__(self):
        self.vocab_repo = VocabularyRepository(DBConnect())

    def create_vocabulary(self, word: str, part_of_speech: str,
                          vi_meaning: str, eng_description: str,
                          example: str, note: str = "") -> int:
        now = datetime.now().isoformat()
        new_vocab = Vocabulary(
            id=None,
            word=word,
            part_of_speech=part_of_speech,
            vi_meaning=vi_meaning,
            eng_description=eng_description,
            example=example,
            note=note,
            correct_count=0,
            wrong_count=0,
            created_at=now
        )
        vocab_id = self.vocab_repo.create(new_vocab)
        return vocab_id

    def update_vocabulary(self, vocab_id: int,
                          word: str = None,
                          part_of_speech: str = None,
                          vi_meaning: str = None,
                          eng_description: str = None,
                          example: str = None,
                          note: str = None,
                          correct_count: int = None,
                          wrong_count: int = None):
        """Update an existing vocabulary entry."""
        vocabulary = self.vocab_repo.get(vocab_id)
        if not vocabulary:
            msg = f"Vocabulary with id {vocab_id} does not exist."
            raise ValueError(msg)
        if word:
            vocabulary.word = word
        if part_of_speech:
            vocabulary.part_of_speech = part_of_speech
        if vi_meaning:
            vocabulary.vi_meaning = vi_meaning
        if eng_description:
            vocabulary.eng_description = eng_description
        if example:
            vocabulary.example = example
        if note:
            vocabulary.note = note
        if correct_count is not None:
            if correct_count < 0:
                raise ValueError("correct_count must be non-negative")
            vocabulary.correct_count = correct_count
        if wrong_count is not None:
            if wrong_count < 0:
                raise ValueError("wrong_count must be non-negative")
            vocabulary.wrong_count = wrong_count
        self.vocab_repo.update(vocabulary)

    def get_random_vocabulary(self) -> Vocabulary | None:
        """Get a random vocabulary entry."""
        all_vocabularies = self.vocab_repo.get_all_vocabulary_complete()
        if not all_vocabularies:
            return None
        return Vocabulary(*random.choice(all_vocabularies))

    def count_vocabulary_by_date(self, from_date: str) -> list[tuple]:
        """Get vocabulary count grouped by creation date."""
        return self.vocab_repo.count_vocabulary_grouped_by_date(from_date)

    def get_all_vocabulary(self) -> list[Vocabulary]:
        """Get all vocabulary entries."""
        return self.vocab_repo.all()

    def total_vocabulary(self) -> int:
        """Get total number of vocabulary entries."""
        return self.vocab_repo.count_all()

    def get_vocabulary_by_id(self, vocab_id: int) -> Vocabulary:
        """Get vocabulary entry by ID."""
        return self.vocab_repo.get(vocab_id)

    def delete_vocabulary(self, vocab_id: int):
        """Delete a vocabulary entry by ID."""
        self.vocab_repo.delete(vocab_id)


if __name__ == "__main__":
    vocab_service = VocabularyService()
    all_vocabs = vocab_service.get_all_vocabulary()
    print(all_vocabs)
