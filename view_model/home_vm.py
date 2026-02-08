from datetime import datetime, timedelta
from service.paragraph_service import ParagraphService
from service.sentence_service import SentenceService
from service.vocabulary_service import VocabularyService


class HomeViewModel:
    def __init__(self, paragraph_service: ParagraphService, sentence_service: SentenceService, vocabulary_service: VocabularyService):
        self.paragraph_service = paragraph_service
        self.sentence_service = sentence_service
        self.vocabulary_service = vocabulary_service

    def get_paragraph_progress_summary(self) -> dict:
        data = self.paragraph_service.get_paragraph_progress_summary()
        return data

    def count_vocabulary_by_date(self, number_of_days: int):
        date = (datetime.now() - timedelta(days=number_of_days)
                ).date().isoformat()
        data_raw = self.vocabulary_service.count_vocabulary_by_date(date)
        data = {}
        for number in range(number_of_days):
            date = (datetime.now() -
                    timedelta(days=number_of_days-number)).date().isoformat()
            data[date] = 0
        for item in data_raw:
            data[item[0]] = item[1]
        return data

    def get_avg_score(self):
        if self.sentence_service.get_avg_score() is None:
            return 0.0
        return round(self.sentence_service.get_avg_score(), 2)

    def get_incomplete_paragraphs(self):
        data = []
        for paragraph in self.paragraph_service.get_incomplete_paragraphs():
            data.append({
                "id": paragraph.id,
                "title": paragraph.title,
                "completed": paragraph.completed,
                "score": paragraph.score,
                "created_at": paragraph.created_at
            })
        return data

    def get_all_paragraphs(self) -> list[dict]:
        """Get all paragraphs (Open, In-Progress, Completed)"""
        data = []
        for paragraph in self.paragraph_service.get_all_paragraphs():
            data.append({
                "id": paragraph.id,
                "title": paragraph.title,
                "completed": paragraph.completed,
                "score": paragraph.score,
                "created_at": paragraph.created_at
            })
        return data

    def get_all_vocabulary(self) -> list[dict]:
        all_vocabulary = self.vocabulary_service.get_all_vocabulary()
        data = []
        for vocab in all_vocabulary:
            data.append({
                "id": vocab.id,
                "word": vocab.word,
                "part_of_speech": vocab.part_of_speech,
                "vi_meaning": vocab.vi_meaning,
                "eng_description": vocab.eng_description,
                "example": vocab.example,
                "correct_count": vocab.correct_count,
                "wrong_count": vocab.wrong_count,
            })
        return data

    def create_vocabulary(self, payload: dict):
        print("Creating vocabulary with payload:", payload)
        word = payload.get("word", "")
        part_of_speech = payload.get("part_of_speech", "")
        vi_meaning = payload.get("vi_meaning", "")
        eng_description = payload.get("eng_description", "")
        example = payload.get("example", "")
        self.vocabulary_service.create_vocabulary(
            word, part_of_speech, vi_meaning, eng_description, example)

    def delete_vocabulary(self, payload: dict):
        print("Deleting vocabulary with payload:", payload)
        vocab_id = payload.get("id")
        self.vocabulary_service.delete_vocabulary(vocab_id)

    def update_vocabulary(self, payload: dict):
        print("Updating vocabulary with payload:", payload)
        vocab_id = payload.get("id")
        word = payload.get("word")
        part_of_speech = payload.get("part_of_speech")
        vi_meaning = payload.get("vi_meaning")
        eng_description = payload.get("eng_description")
        example = payload.get("example")
        note = payload.get("note")
        correct_count = payload.get("correct_count")
        wrong_count = payload.get("wrong_count")
        self.vocabulary_service.update_vocabulary(
            vocab_id, word, part_of_speech, vi_meaning, eng_description, example, note, correct_count, wrong_count)

    def delete_paragraph(self, payload: dict):
        print("Deleting paragraph with payload:", payload)
        paragraph_id = payload.get("id")
        self.paragraph_service.delete_paragraph(paragraph_id)

    def update_paragraph(self, payload: dict):
        """Update paragraph """
        print("Updating paragraph with payload:", payload)
        paragraph_id = payload.get("id")
        new_title = payload.get("title", "")
        self.paragraph_service.update_paragraph(paragraph_id=paragraph_id, title=new_title)