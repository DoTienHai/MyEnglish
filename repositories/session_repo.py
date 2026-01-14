
from repositories.repo_base import BaseRepository
from model.session import Session
from repositories.db_connect import DBConnect

class SessionRepository(BaseRepository):
    table_name = "sessions"
    columns = [
        "id",
        "title",
        "source_text",
        "source_reference",
        "translated_text",
        "completed",
        "score",
        "created_at"
    ]
    model_class = Session

    def __init__(self, db: DBConnect):
        super().__init__(db)
        
    def get(self, id: int) -> Session:
        return super().get(id)
    
    def get_session_progress_summary(self):
        query = f"SELECT \
                    SUM(CASE WHEN completed = 100 THEN 1 ELSE 0 END), \
                    SUM(CASE WHEN completed != 100 AND completed != 0 THEN 1 ELSE 0 END), \
                    SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) \
                FROM {self.table_name}"
        completed, in_progress, open = self.db.fetch_one(query)
        return completed, in_progress, open

    def get_not_done_sessions(self):
        query = f"SELECT * FROM {self.table_name} WHERE completed != 100"
        rows = self.db.fetch_all(query)
        return [self.to_entity(row) for row in rows]
    
        
if __name__ == "__main__":
    db = DBConnect("test.db")
    session_repo = SessionRepository(db)
    new_sesion = Session(
        id=None,
        title="Test Session",
        source_text="This is a test.",
        source_reference="N/A",
        translated_text="",
        completed=0.0,
        score=0.0,
        created_at="2024-01-01 00:00:00"
    )
    last_session_id = session_repo.create(new_sesion)
    print(last_session_id)
    read_session = session_repo.get(last_session_id)
    print(read_session.to_dict())
    read_session.title = "Updated Test Session"
    session_repo.update(read_session)
    updated_session = session_repo.get(last_session_id)
    print(updated_session.to_dict())
