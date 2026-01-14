from datetime import datetime
from model.session import Session
from repositories.db_connect import DBConnect
from repositories.session_repo import SessionRepository

class SessionService:
    def __init__(self):
        self.session_repo = SessionRepository(DBConnect())
        self.session = None
    def create_session(self, title: str, source_text: str, source_reference: str) -> dict:
        now = datetime.now().isoformat()
        new_session = Session(
            id=None,
            title=title,
            source_text=source_text,
            source_reference=source_reference,
            translated_text="",
            completed=0.0,
            score=0.0,
            created_at=now
        )
        session_id = self.session_repo.create(new_session)
        return session_id
    
    def update_session(self, session_id: int, translated_text: str = None, completed: float = None, score: float = None):
        session = self.session_repo.get(session_id)
        if not session:
            raise ValueError(f"Session with id {session_id} does not exist.")
        
        if translated_text is not None:
            session.translated_text = translated_text
        if completed is not None:
            session.completed = completed
        if score is not None:
            session.score = score
        
        self.session_repo.update(session)
    
    def get_session_progress_summary(self):
        return self.session_repo.get_session_progress_summary()
    
    def get_not_done_sessions(self):
        return self.session_repo.get_not_done_sessions()
    
    def get_session_by_id(self, session_id: int) -> Session:
        return self.session_repo.get(session_id)