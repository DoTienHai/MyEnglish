import datetime
from datetime import datetime, timedelta
from service.session_service import SessionService
from service.sentence_service import SentenceService
from service.vocabulary_service import VocabularyService

class HomeViewModel:
    def __init__(self, session_service: SessionService, sentence_service: SentenceService, vocabulary_service: VocabularyService):
        self.session_service = session_service
        self.sentence_service = sentence_service
        self.vocabulary_service = vocabulary_service

    def get_session_progress_summary(self):
        return self.session_service.get_session_progress_summary()
    
    def count_vocabulary_by_date(self, number_of_days: int):
        date = (datetime.now() - timedelta(days=number_of_days)).date().isoformat()
        data_raw = self.vocabulary_service.count_vocabulary_grouped_by_date(date)
        data = {}
        for number in range(number_of_days):
            date = (datetime.now() - timedelta(days=number_of_days-number)).date().isoformat()
            data[date] = 0
        for item in data_raw:
            data[item[0]] = item[1]
        return data
    
    def get_avg_score(self):
        return round(self.sentence_service.get_avg_score(), 2)
    
    def get_not_done_sessions(self):
        data = []
        for session in self.session_service.get_not_done_sessions():
            data.append({
                "id": session.id,
                "title": session.title,
                "completed": session.completed,
                "score": session.score,
                "created_at": session.created_at
            })
        return data