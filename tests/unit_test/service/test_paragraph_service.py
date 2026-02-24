"""Unit tests for ParagraphService"""
import pytest
from datetime import datetime
from service.paragraph_service import ParagraphService
from model.paragraph import Paragraph
from repositories.paragraph_repo import ParagraphRepository


class TestParagraphServiceCreate:
    """Tests for create_paragraph operation"""

    def test_create_paragraph_success(
        self,
        paragraph_repo: ParagraphRepository
    ) -> None:
        """Test creating a paragraph successfully"""
        service = ParagraphService()
        
        paragraph_id = service.create_paragraph(
            title="Test Paragraph",
            input_paragraph="This is a test paragraph.",
            reference="Test Source"
        )
        
        assert paragraph_id is not None
        assert isinstance(paragraph_id, int)
        assert paragraph_id > 0

    def test_create_paragraph_with_minimum_fields(
        self
    ) -> None:
        """Test creating a paragraph with only required fields"""
        service = ParagraphService()
        
        paragraph_id = service.create_paragraph(
            title="Minimal Paragraph",
            input_paragraph="Some content"
        )
        
        assert paragraph_id is not None
        assert paragraph_id > 0

    def test_created_paragraph_has_default_values(
        self
    ) -> None:
        """Test that created paragraph has correct default values"""
        service = ParagraphService()
        
        paragraph_id = service.create_paragraph(
            title="Test",
            input_paragraph="Content"
        )
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        
        assert paragraph.machine_translation == ""
        assert paragraph.completed == 0.0
        assert paragraph.score == 0.0

    def test_created_paragraph_has_created_at_timestamp(
        self
    ) -> None:
        """Test that created paragraph has timestamp"""
        service = ParagraphService()
        before = datetime.now()
        
        paragraph_id = service.create_paragraph(
            title="Test",
            input_paragraph="Content"
        )
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        
        assert paragraph.created_at is not None


class TestParagraphServiceUpdate:
    """Tests for update_paragraph operation"""

    def test_update_paragraph_title(
        self
    ) -> None:
        """Test updating paragraph title"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Original",
            input_paragraph="Content"
        )
        
        service.update_paragraph(
            paragraph_id,
            title="Updated Title"
        )
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        assert paragraph.title == "Updated Title"

    def test_update_paragraph_multiple_fields(
        self
    ) -> None:
        """Test updating multiple fields"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Original",
            input_paragraph="Original content"
        )
        
        service.update_paragraph(
            paragraph_id,
            title="New Title",
            reference="New Reference",
            machine_translation="Translation"
        )
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        assert paragraph.title == "New Title"
        assert paragraph.reference == "New Reference"
        assert paragraph.machine_translation == "Translation"

    def test_update_paragraph_completion_percentage(
        self
    ) -> None:
        """Test updating completion percentage"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Test",
            input_paragraph="Content"
        )
        
        service.update_paragraph(paragraph_id, completed=50.5)
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        assert paragraph.completed == 50.5

    def test_update_paragraph_completion_invalid_range(
        self
    ) -> None:
        """Test that completion must be between 0-100"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Test",
            input_paragraph="Content"
        )
        
        with pytest.raises(ValueError, match="completed must be between 0-100"):
            service.update_paragraph(paragraph_id, completed=150.0)

    def test_update_paragraph_score(
        self
    ) -> None:
        """Test updating score"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Test",
            input_paragraph="Content"
        )
        
        service.update_paragraph(paragraph_id, score=8.5)
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        assert paragraph.score == 8.5

    def test_update_paragraph_score_invalid_range(
        self
    ) -> None:
        """Test that score must be between 0-10"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Test",
            input_paragraph="Content"
        )
        
        with pytest.raises(ValueError, match="score must be between 0-10"):
            service.update_paragraph(paragraph_id, score=15.0)

    def test_update_nonexistent_paragraph_raises_error(
        self
    ) -> None:
        """Test that updating nonexistent paragraph raises error"""
        service = ParagraphService()
        
        with pytest.raises(ValueError, match="does not exist"):
            service.update_paragraph(9999, title="New Title")


class TestParagraphServiceRead:
    """Tests for read operations"""

    def test_get_paragraph_by_id(
        self
    ) -> None:
        """Test retrieving paragraph by ID"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="Test Paragraph",
            input_paragraph="Test content"
        )
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        
        assert paragraph is not None
        assert paragraph.id == paragraph_id
        assert paragraph.title == "Test Paragraph"

    def test_get_paragraph_returns_none_for_nonexistent(
        self
    ) -> None:
        """Test that nonexistent paragraph returns None"""
        service = ParagraphService()
        
        paragraph = service.get_paragraph_by_id(9999)
        
        assert paragraph is None

    def test_get_all_paragraphs(
        self
    ) -> None:
        """Test retrieving all paragraphs"""
        service = ParagraphService()
        
        # Create multiple paragraphs
        service.create_paragraph(title="Para1", input_paragraph="Content1")
        service.create_paragraph(title="Para2", input_paragraph="Content2")
        service.create_paragraph(title="Para3", input_paragraph="Content3")
        
        all_paragraphs = service.get_all_paragraphs()
        
        assert len(all_paragraphs) >= 3
        assert all(isinstance(p, Paragraph) for p in all_paragraphs)

    def test_get_incomplete_paragraphs(
        self
    ) -> None:
        """Test retrieving only incomplete paragraphs"""
        service = ParagraphService()
        
        # Create incomplete paragraph
        para1_id = service.create_paragraph(
            title="Incomplete",
            input_paragraph="Content"
        )
        
        # Create completed paragraph
        para2_id = service.create_paragraph(
            title="Complete",
            input_paragraph="Content"
        )
        service.update_paragraph(para2_id, completed=100.0)
        
        incomplete = service.get_incomplete_paragraphs()
        
        assert all(p.completed < 100 for p in incomplete)


class TestParagraphServiceDelete:
    """Tests for delete operation"""

    def test_delete_paragraph(
        self
    ) -> None:
        """Test deleting a paragraph"""
        service = ParagraphService()
        paragraph_id = service.create_paragraph(
            title="To Delete",
            input_paragraph="Content"
        )
        
        service.delete_paragraph(paragraph_id)
        
        paragraph = service.get_paragraph_by_id(paragraph_id)
        assert paragraph is None

    def test_delete_nonexistent_paragraph_does_not_raise_error(
        self
    ) -> None:
        """Test that deleting nonexistent paragraph doesn't raise error"""
        service = ParagraphService()
        
        # Should not raise exception
        service.delete_paragraph(9999)


class TestParagraphServiceProgress:
    """Tests for progress summary"""

    def test_get_paragraph_progress_summary(
        self
    ) -> None:
        """Test getting progress summary"""
        service = ParagraphService()
        
        # Create paragraphs with different states
        para1_id = service.create_paragraph(title="P1", input_paragraph="C1")
        para2_id = service.create_paragraph(title="P2", input_paragraph="C2")
        service.update_paragraph(para2_id, completed=50.0)
        para3_id = service.create_paragraph(title="P3", input_paragraph="C3")
        service.update_paragraph(para3_id, completed=100.0)
        
        summary = service.get_paragraph_progress_summary()
        
        assert summary is not None
        assert isinstance(summary, dict)
