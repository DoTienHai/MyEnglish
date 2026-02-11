
from repositories.repo_base import BaseRepository
from model.paragraph import Paragraph
from repositories.db_connect import DBConnect

class ParagraphRepository(BaseRepository):
    table_name = "paragraphs"
    columns = [
        "id",
        "title",
        "input_paragraph",
        "reference",
        "machine_translation",
        "completed",
        "score",
        "created_at"
    ]
    model_class = Paragraph

    def __init__(self, db: DBConnect):
        super().__init__(db)
        
    def get_paragraph_progress_summary(self):
        query = f"SELECT \
                    SUM(CASE WHEN completed = 100 THEN 1 ELSE 0 END), \
                    SUM(CASE WHEN completed != 100 AND completed != 0 THEN 1 ELSE 0 END), \
                    SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) \
                FROM {self.table_name}"
        completed, in_progress, open = self.db.fetch_one(query)
        return {
            "completed": completed,
            "in_progress": in_progress,
            "open": open
        }

    def get_incomplete_paragraphs(self):
        query = f"SELECT * FROM {self.table_name} WHERE completed < 100"
        rows = self.db.fetch_all(query)
        return [self.to_entity(row) for row in rows]
    
if __name__ == "__main__":  # pragma: no cover
    db = DBConnect("test.db")
    paragraph_repo = ParagraphRepository(db)
    new_paragraph = Paragraph(
        id=None,
        title="Test Paragraph",
        input_paragraph="This is a test paragraph.",
        reference="N/A",
        machine_translation="",
        completed=0.0,
        score=0.0,
        created_at="2024-01-01 00:00:00"
    )
    last_paragraph_id = paragraph_repo.create(new_paragraph)
    print(last_paragraph_id)
    read_paragraph = paragraph_repo.get(last_paragraph_id)
    print(read_paragraph.to_dict())
    read_paragraph.title = "Updated Test Paragraph"
    paragraph_repo.update(read_paragraph)
    updated_paragraph = paragraph_repo.get(last_paragraph_id)
    print(updated_paragraph.to_dict())
