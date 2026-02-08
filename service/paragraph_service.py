from datetime import datetime
from model.paragraph import Paragraph
from repositories.db_connect import DBConnect
from repositories.paragraph_repo import ParagraphRepository


class ParagraphService:
    """
    Service layer for Paragraph entity.
    Handles business logic related to paragraph operations.
    """

    def __init__(self):
        self.paragraph_repo = ParagraphRepository(DBConnect())
        self.current_paragraph = None

    def create_paragraph(self, title: str, input_paragraph: str,
                         reference: str = "") -> int:
        now = datetime.now().isoformat()
        new_paragraph = Paragraph(
            id=None,
            title=title,
            input_paragraph=input_paragraph,
            reference=reference,
            machine_translation="",
            completed=0.0,
            score=0.0,
            created_at=now
        )
        paragraph_id = self.paragraph_repo.create(new_paragraph)
        return paragraph_id

    def update_paragraph(self, paragraph_id: int,
                         title: str = None,
                         input_paragraph: str = None,
                         reference: str = None,
                         machine_translation: str = None,
                         completed: float = None,
                         score: float = None):
        paragraph = self.paragraph_repo.get(paragraph_id)
        if not paragraph:
            raise ValueError(f"Paragraph with id {paragraph_id} does not exist.")

        if title is not None:
            paragraph.title = title
        if input_paragraph is not None:
            paragraph.input_paragraph = input_paragraph
        if reference is not None:
            paragraph.reference = reference
        if machine_translation is not None:
            paragraph.machine_translation = machine_translation
        if completed is not None:
            if not (0 <= completed <= 100):
                raise ValueError("completed must be between 0-100")
            paragraph.completed = completed
        if score is not None:
            if not (0 <= score <= 10):
                raise ValueError("score must be between 0-10")
            paragraph.score = score

        self.paragraph_repo.update(paragraph)

    def get_paragraph_progress_summary(self):
        """Get progress statistics for all paragraphs."""
        return self.paragraph_repo.get_paragraph_progress_summary()

    def get_incomplete_paragraphs(self) -> list[Paragraph]:
        """Get list of incomplete paragraphs."""
        return self.paragraph_repo.get_incomplete_paragraphs()

    def get_paragraph_by_id(self, paragraph_id: int) -> Paragraph:
        """Get paragraph information by ID."""
        return self.paragraph_repo.get(paragraph_id)

    def get_all_paragraphs(self) -> list[Paragraph]:
        """Get list of all paragraphs."""
        return self.paragraph_repo.all()

    def delete_paragraph(self, paragraph_id: int):
        """Delete a paragraph by ID."""
        self.paragraph_repo.delete(paragraph_id)


if __name__ == "__main__":
    paragraph_service = ParagraphService()
    summary = paragraph_service.get_paragraph_progress_summary()
    print(summary)
