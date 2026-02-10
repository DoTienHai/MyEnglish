"""Unit tests for ParagraphRepository"""
from typing import Dict, List, Optional
import pytest
from repositories.paragraph_repo import ParagraphRepository
from model.paragraph import Paragraph


class TestParagraphRepositoryCreate:
    """Tests for create operation"""

    def test_create_paragraph_success(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test creating a paragraph successfully"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        
        assert paragraph_id is not None
        assert isinstance(paragraph_id, int)
        assert paragraph_id > 0

    def test_created_paragraph_can_be_retrieved(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test that created paragraph can be retrieved"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        retrieved = paragraph_repo.get(paragraph_id)
        
        assert retrieved is not None
        assert retrieved.title == sample_paragraph.title
        assert retrieved.input_paragraph == sample_paragraph.input_paragraph
        assert retrieved.reference == sample_paragraph.reference
        assert retrieved.machine_translation == sample_paragraph.machine_translation

    def test_create_multiple_paragraphs(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph,
        sample_paragraph_completed: Paragraph
    ) -> None:
        """Test creating multiple paragraphs"""
        paragraph_id_1 = paragraph_repo.create(sample_paragraph)
        paragraph_id_2 = paragraph_repo.create(sample_paragraph_completed)
        
        assert paragraph_id_1 is not None
        assert paragraph_id_2 is not None
        assert paragraph_id_1 != paragraph_id_2

    def test_created_paragraph_has_correct_fields(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test that created paragraph has all correct fields"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        retrieved = paragraph_repo.get(paragraph_id)
        
        assert retrieved.title == sample_paragraph.title
        assert retrieved.completed == sample_paragraph.completed
        assert retrieved.score == sample_paragraph.score
        assert retrieved.reference == sample_paragraph.reference
        assert retrieved.machine_translation == sample_paragraph.machine_translation


class TestParagraphRepositoryRead:
    """Tests for read operations"""

    def test_get_existing_paragraph(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test getting an existing paragraph"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        retrieved = paragraph_repo.get(paragraph_id)
        
        assert retrieved is not None
        assert isinstance(retrieved, Paragraph)
        assert retrieved.id == paragraph_id

    def test_get_nonexistent_paragraph_returns_none(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test getting a non-existent paragraph returns None"""
        result = paragraph_repo.get(9999)
        
        assert result is None

    def test_get_paragraph_preserves_data(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test that getting paragraph preserves all data accurately"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        retrieved = paragraph_repo.get(paragraph_id)
        
        assert retrieved.to_dict()["title"] == sample_paragraph.to_dict()["title"]
        assert retrieved.to_dict()["completed"] == sample_paragraph.to_dict()["completed"]
        assert retrieved.to_dict()["score"] == sample_paragraph.to_dict()["score"]

    def test_get_all_paragraphs_empty_database(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test getting all paragraphs from empty database"""
        all_paragraphs = paragraph_repo.all()
        
        assert isinstance(all_paragraphs, list)
        assert len(all_paragraphs) == 0

    def test_get_all_paragraphs_with_data(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph,
        sample_paragraph_completed: Paragraph,
        sample_paragraph_incomplete: Paragraph
    ) -> None:
        """Test getting all paragraphs"""
        paragraph_repo.create(sample_paragraph)
        paragraph_repo.create(sample_paragraph_completed)
        paragraph_repo.create(sample_paragraph_incomplete)
        
        all_paragraphs = paragraph_repo.all()
        
        assert len(all_paragraphs) == 3
        assert all(isinstance(p, Paragraph) for p in all_paragraphs)


class TestParagraphRepositoryUpdate:
    """Tests for update operations"""

    def test_update_paragraph_title(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test updating paragraph title"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        para = paragraph_repo.get(paragraph_id)
        
        para.title = "Updated Title"
        paragraph_repo.update(para)
        
        updated = paragraph_repo.get(paragraph_id)
        assert updated.title == "Updated Title"

    def test_update_paragraph_completed_progress(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test updating paragraph completion progress"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        para = paragraph_repo.get(paragraph_id)
        
        para.completed = 75.0
        para.score = 9.0
        paragraph_repo.update(para)
        
        updated = paragraph_repo.get(paragraph_id)
        assert updated.completed == 75.0
        assert updated.score == 9.0

    def test_update_complete_paragraph(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test updating paragraph to complete"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        para = paragraph_repo.get(paragraph_id)
        
        para.completed = 100.0
        para.score = 10.0
        paragraph_repo.update(para)
        
        updated = paragraph_repo.get(paragraph_id)
        assert updated.completed == 100.0

    def test_update_maintains_id(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test that update maintains the paragraph ID"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        para = paragraph_repo.get(paragraph_id)
        original_id = para.id
        
        para.title = "New Title"
        paragraph_repo.update(para)
        
        updated = paragraph_repo.get(paragraph_id)
        assert updated.id == original_id

    def test_update_nonexistent_paragraph_does_not_raise(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test updating a non-existent paragraph"""
        para = Paragraph(
            id=9999,
            title="Non-existent",
            input_paragraph="Test",
            reference="Ref",
            machine_translation="",
            completed=0.0,
            score=0.0,
            created_at="2026-01-26 12:00:00"
        )
        
        # Should not raise exception
        paragraph_repo.update(para)
        
        # Verify it wasn't actually updated
        assert paragraph_repo.get(9999) is None


class TestParagraphRepositoryDelete:
    """Tests for delete operations"""

    def test_delete_paragraph_success(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test deleting a paragraph"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        assert paragraph_repo.get(paragraph_id) is not None
        
        paragraph_repo.delete(paragraph_id)
        
        assert paragraph_repo.get(paragraph_id) is None

    def test_delete_nonexistent_paragraph_does_not_raise(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test deleting non-existent paragraph doesn't raise"""
        # Should not raise exception
        paragraph_repo.delete(9999)

    def test_delete_removes_from_all(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph,
        sample_paragraph_completed: Paragraph
    ) -> None:
        """Test that deleted paragraph is removed from all()"""
        paragraph_id_1 = paragraph_repo.create(sample_paragraph)
        paragraph_id_2 = paragraph_repo.create(sample_paragraph_completed)
        
        assert len(paragraph_repo.all()) == 2
        
        paragraph_repo.delete(paragraph_id_1)
        
        assert len(paragraph_repo.all()) == 1
        assert paragraph_repo.get(paragraph_id_2) is not None


class TestParagraphRepositoryCustomQueries:
    """Tests for custom query methods"""

    def test_get_incomplete_paragraphs_empty(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test get_incomplete_paragraphs with no data"""
        incomplete = paragraph_repo.get_incomplete_paragraphs()
        
        assert isinstance(incomplete, list)
        assert len(incomplete) == 0

    def test_get_incomplete_paragraphs_with_completed(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph_completed: Paragraph
    ) -> None:
        """Test that completed paragraphs are not in incomplete list"""
        paragraph_repo.create(sample_paragraph_completed)
        
        incomplete = paragraph_repo.get_incomplete_paragraphs()
        
        assert len(incomplete) == 0

    def test_get_incomplete_paragraphs_with_various_progress(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph,
        sample_paragraph_completed: Paragraph,
        sample_paragraph_incomplete: Paragraph,
        sample_paragraph_open: Paragraph
    ) -> None:
        """Test get_incomplete_paragraphs returns all non-complete"""
        paragraph_id_1 = paragraph_repo.create(sample_paragraph)          # 50%
        paragraph_id_2 = paragraph_repo.create(sample_paragraph_completed)  # 100% (should not be in list)
        paragraph_id_3 = paragraph_repo.create(sample_paragraph_incomplete) # 75%
        paragraph_id_4 = paragraph_repo.create(sample_paragraph_open)       # 0%
        
        incomplete = paragraph_repo.get_incomplete_paragraphs()
        
        assert len(incomplete) == 3
        assert all(p.completed < 100 for p in incomplete)

    def test_get_paragraph_progress_summary_empty_db(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test progress summary with empty database"""
        summary = paragraph_repo.get_paragraph_progress_summary()
        
        assert summary["completed"] == 0 or summary["completed"] is None
        assert summary["in_progress"] == 0 or summary["in_progress"] is None
        assert summary["open"] == 0 or summary["open"] is None

    def test_get_paragraph_progress_summary_with_data(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph,
        sample_paragraph_completed: Paragraph,
        sample_paragraph_incomplete: Paragraph,
        sample_paragraph_open: Paragraph
    ) -> None:
        """Test progress summary with various paragraphs"""
        paragraph_repo.create(sample_paragraph)               # 50% → in_progress
        paragraph_repo.create(sample_paragraph_completed)    # 100% → completed
        paragraph_repo.create(sample_paragraph_incomplete)   # 75% → in_progress
        paragraph_repo.create(sample_paragraph_open)         # 0% → open
        
        summary = paragraph_repo.get_paragraph_progress_summary()
        
        assert summary["completed"] == 1
        assert summary["in_progress"] == 2
        assert summary["open"] == 1

    def test_get_paragraph_progress_summary_all_completed(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph_completed: Paragraph
    ) -> None:
        """Test progress summary when all are completed"""
        for i in range(3):
            para = Paragraph(
                id=None,
                title=f"Completed {i}",
                input_paragraph="Test",
                reference="Ref",
                machine_translation="",
                completed=100.0,
                score=10.0,
                created_at="2026-01-26 12:00:00"
            )
            paragraph_repo.create(para)
        
        summary = paragraph_repo.get_paragraph_progress_summary()
        
        assert summary["completed"] == 3
        assert summary["in_progress"] == 0 or summary["in_progress"] is None
        assert summary["open"] == 0 or summary["open"] is None


class TestParagraphRepositoryDataIntegrity:
    """Tests for data integrity and edge cases"""

    def test_paragraph_to_entity_conversion(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test that paragraph is correctly converted to/from database"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        retrieved = paragraph_repo.get(paragraph_id)
        
        # Verify all fields match (except id which is assigned by DB)
        assert retrieved.title == sample_paragraph.title
        assert retrieved.completed == sample_paragraph.completed
        assert retrieved.score == sample_paragraph.score

    def test_multiple_updates_to_same_paragraph(
        self,
        paragraph_repo: ParagraphRepository,
        sample_paragraph: Paragraph
    ) -> None:
        """Test multiple sequential updates to same paragraph"""
        paragraph_id = paragraph_repo.create(sample_paragraph)
        
        for i in range(5):
            para = paragraph_repo.get(paragraph_id)
            para.completed = i * 20
            para.score = i
            paragraph_repo.update(para)
        
        final = paragraph_repo.get(paragraph_id)
        assert final.completed == 80
        assert final.score == 4

    def test_zero_completed_is_valid(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test that 0% completion is valid"""
        para = Paragraph(
            id=None,
            title="New Session",
            input_paragraph="Test",
            reference="Ref",
            machine_translation="",
            completed=0.0,
            score=0.0,
            created_at="2026-01-26 12:00:00"
        )
        
        paragraph_id = paragraph_repo.create(para)
        retrieved = paragraph_repo.get(paragraph_id)
        
        assert retrieved.completed == 0.0

    def test_one_hundred_completed_is_complete(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test that 100% completion marks paragraph as complete"""
        para = Paragraph(
            id=None,
            title="Finished Session",
            input_paragraph="Test",
            reference="Ref",
            machine_translation="",
            completed=100.0,
            score=10.0,
            created_at="2026-01-26 12:00:00"
        )
        
        paragraph_id = paragraph_repo.create(para)
        
        incomplete = paragraph_repo.get_incomplete_paragraphs()
        assert paragraph_id not in [p.id for p in incomplete]
