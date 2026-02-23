"""Unit tests for Paragraph model validation"""
import pytest
from model.paragraph import Paragraph


class TestParagraphCompletedValidation:
    """Test completed field validation"""
    
    def test_completed_negative_raises_error(self):
        """Completed < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=-10.0,  # Invalid
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_completed_over_100_raises_error(self):
        """Completed > 100 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot exceed 100"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=150.0,  # Invalid
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_completed_exactly_zero_is_valid(self):
        """Completed = 0 is a valid boundary value"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=0.0,  # Valid boundary
            score=0.0,
            created_at="2026-01-26 12:00:00"
        )
        assert para.completed == 0.0
    
    def test_completed_exactly_100_is_valid(self):
        """Completed = 100 is a valid boundary value"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=100.0,  # Valid boundary
            score=10.0,
            created_at="2026-01-26 12:00:00"
        )
        assert para.completed == 100.0
    
    def test_completed_setter_validates_update(self):
        """Update completed after creation must also validate"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=50.0,
            score=5.0,
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        para.completed = 75.0
        assert para.completed == 75.0
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot exceed 100"):
            para.completed = 200.0
    
    def test_completed_type_validation(self):
        """Completed must be numeric"""
        with pytest.raises(TypeError, match="must be numeric"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed="50%",  # String instead of float
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_completed_accepts_integer(self):
        """Completed can be an integer (converted to float)"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=50,  # Integer instead of float
            score=5.0,
            created_at="2026-01-26 12:00:00"
        )
        assert para.completed == 50.0
        assert isinstance(para.completed, float)


class TestParagraphScoreValidation:
    """Test score field validation"""
    
    def test_score_negative_raises_error(self):
        """Score < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=-5.0,  # Invalid
                created_at="2026-01-26 12:00:00"
            )
    
    def test_score_over_10_raises_error(self):
        """Score > 10 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot exceed 10"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=15.0,  # Invalid
                created_at="2026-01-26 12:00:00"
            )
    
    def test_score_exactly_zero_is_valid(self):
        """Score = 0 is a valid boundary value"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=0.0,
            score=0.0,  # Valid boundary
            created_at="2026-01-26 12:00:00"
        )
        assert para.score == 0.0
    
    def test_score_exactly_10_is_valid(self):
        """Score = 10 is a valid boundary value"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=100.0,
            score=10.0,  # Valid boundary
            created_at="2026-01-26 12:00:00"
        )
        assert para.score == 10.0
    
    def test_score_decimal_is_valid(self):
        """Score can be a decimal value"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=75.5,
            score=8.5,  # Valid decimal
            created_at="2026-01-26 12:00:00"
        )
        assert para.score == 8.5
    
    def test_score_type_validation(self):
        """Score must be numeric"""
        with pytest.raises(TypeError, match="must be numeric"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score="8.5",  # String instead of float
                created_at="2026-01-26 12:00:00"
            )
    
    def test_score_setter_validates_update(self):
        """Update score after creation must also validate"""
        para = Paragraph(
            id=1,
            title="Test",
            input_paragraph="Test paragraph",
            reference="Ref",
            machine_translation="MT",
            completed=50.0,
            score=5.0,
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        para.score = 8.0
        assert para.score == 8.0
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            para.score = -1.0


class TestParagraphCriticalFieldsValidation:
    """Test validation for critical fields (title, input_paragraph)"""
    
    def test_title_empty_string_raises_error(self):
        """Empty title must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Paragraph(
                id=1,
                title="",  # Empty string
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_title_whitespace_only_raises_error(self):
        """Whitespace-only title must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Paragraph(
                id=1,
                title="   ",  # Whitespace only
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_title_not_string_raises_error(self):
        """Non-string title must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            Paragraph(
                id=1,
                title=123,  # Integer instead of string
                input_paragraph="Test paragraph",
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_input_paragraph_empty_string_raises_error(self):
        """Empty input_paragraph must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="",  # Empty string
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_input_paragraph_whitespace_only_raises_error(self):
        """Whitespace-only input_paragraph must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph="   ",  # Whitespace only
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_input_paragraph_not_string_raises_error(self):
        """Non-string input_paragraph must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            Paragraph(
                id=1,
                title="Test",
                input_paragraph=None,  # None instead of string
                reference="Ref",
                machine_translation="MT",
                completed=50.0,
                score=5.0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_title_and_input_paragraph_trimmed(self):
        """Title and input_paragraph should be trimmed"""
        para = Paragraph(
            id=1,
            title="  Test Title  ",  # Has leading/trailing spaces
            input_paragraph="  Test Paragraph  ",
            reference="Ref",
            machine_translation="MT",
            completed=50.0,
            score=5.0,
            created_at="2026-01-26 12:00:00"
        )
        assert para.title == "Test Title"
        assert para.input_paragraph == "Test Paragraph"


class TestParagraphFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_completed_raises_error(self):
        """from_dict() must also validate completed"""
        invalid_data = {
            "id": 1,
            "title": "Test",
            "input_paragraph": "Test paragraph",
            "reference": "Ref",
            "machine_translation": "MT",
            "completed": 200.0,  # Invalid
            "score": 5.0,
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot exceed 100"):
            Paragraph.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_score_raises_error(self):
        """from_dict() must also validate score"""
        invalid_data = {
            "id": 1,
            "title": "Test",
            "input_paragraph": "Test paragraph",
            "reference": "Ref",
            "machine_translation": "MT",
            "completed": 50.0,
            "score": 15.0,  # Invalid
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot exceed 10"):
            Paragraph.from_dict(invalid_data)
    
    def test_from_dict_with_empty_title_raises_error(self):
        """from_dict() must validate empty title"""
        invalid_data = {
            "id": 1,
            "title": "",  # Invalid
            "input_paragraph": "Test paragraph",
            "reference": "Ref",
            "machine_translation": "MT",
            "completed": 50.0,
            "score": 5.0,
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Paragraph.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self):
        """from_dict() with valid data must succeed"""
        valid_data = {
            "id": 1,
            "title": "Test",
            "input_paragraph": "Test paragraph",
            "reference": "Ref",
            "machine_translation": "MT",
            "completed": 75.0,  # Valid
            "score": 8.5,       # Valid
            "created_at": "2026-01-26 12:00:00"
        }
        
        para = Paragraph.from_dict(valid_data)
        assert para.completed == 75.0
        assert para.score == 8.5
