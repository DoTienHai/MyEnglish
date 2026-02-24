"""Unit tests for Paragraph model validation"""
import pytest
from model.paragraph import Paragraph


def build_paragraph(paragraph_factory, **overrides) -> Paragraph:
    """Helper to build Paragraph from fixture dict with overrides"""
    return Paragraph(**paragraph_factory(**overrides))


class TestParagraphCompletedValidation:
    """Test completed field validation"""
    
    def test_completed_negative_raises_error(self, paragraph_factory):
        """Completed < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            build_paragraph(paragraph_factory, completed=-10.0)
    
    def test_completed_over_100_raises_error(self, paragraph_factory):
        """Completed > 100 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot exceed 100"):
            build_paragraph(paragraph_factory, completed=150.0)
    
    def test_completed_exactly_zero_is_valid(self, paragraph_factory):
        """Completed = 0 is a valid boundary value"""
        para = build_paragraph(paragraph_factory, completed=0.0, score=0.0)
        assert para.completed == 0.0
    
    def test_completed_exactly_100_is_valid(self, paragraph_factory):
        """Completed = 100 is a valid boundary value"""
        para = build_paragraph(paragraph_factory, completed=100.0, score=10.0)
        assert para.completed == 100.0
    
    def test_completed_setter_validates_update(self, paragraph_factory):
        """Update completed after creation must also validate"""
        para = build_paragraph(paragraph_factory, completed=50.0, score=5.0)
        
        # Valid update
        para.completed = 75.0
        assert para.completed == 75.0
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot exceed 100"):
            para.completed = 200.0
    
    def test_completed_type_validation(self, paragraph_factory):
        """Completed must be numeric"""
        with pytest.raises(TypeError, match="must be numeric"):
            build_paragraph(paragraph_factory, completed="50%")
    
    def test_completed_accepts_integer(self, paragraph_factory):
        """Completed can be an integer (converted to float)"""
        para = build_paragraph(paragraph_factory, completed=50)
        assert para.completed == 50.0
        assert isinstance(para.completed, float)


class TestParagraphScoreValidation:
    """Test score field validation"""
    
    def test_score_negative_raises_error(self, paragraph_factory):
        """Score < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            build_paragraph(paragraph_factory, score=-5.0)
    
    def test_score_over_10_raises_error(self, paragraph_factory):
        """Score > 10 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot exceed 10"):
            build_paragraph(paragraph_factory, score=15.0)
    
    def test_score_exactly_zero_is_valid(self, paragraph_factory):
        """Score = 0 is a valid boundary value"""
        para = build_paragraph(paragraph_factory, completed=0.0, score=0.0)
        assert para.score == 0.0
    
    def test_score_exactly_10_is_valid(self, paragraph_factory):
        """Score = 10 is a valid boundary value"""
        para = build_paragraph(paragraph_factory, completed=100.0, score=10.0)
        assert para.score == 10.0
    
    def test_score_decimal_is_valid(self, paragraph_factory):
        """Score can be a decimal value"""
        para = build_paragraph(paragraph_factory, completed=75.5, score=8.5)
        assert para.score == 8.5
    
    def test_score_type_validation(self, paragraph_factory):
        """Score must be numeric"""
        with pytest.raises(TypeError, match="must be numeric"):
            build_paragraph(paragraph_factory, score="8.5")
    
    def test_score_setter_validates_update(self, paragraph_factory):
        """Update score after creation must also validate"""
        para = build_paragraph(paragraph_factory, completed=50.0, score=5.0)
        
        # Valid update
        para.score = 8.0
        assert para.score == 8.0
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            para.score = -1.0


class TestParagraphCriticalFieldsValidation:
    """Test validation for critical fields (title, input_paragraph)"""
    
    def test_title_empty_string_raises_error(self, paragraph_factory):
        """Empty title must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_paragraph(paragraph_factory, title="")
    
    def test_title_whitespace_only_raises_error(self, paragraph_factory):
        """Whitespace-only title must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_paragraph(paragraph_factory, title="   ")
    
    def test_title_not_string_raises_error(self, paragraph_factory):
        """Non-string title must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            build_paragraph(paragraph_factory, title=123)
    
    def test_input_paragraph_empty_string_raises_error(self, paragraph_factory):
        """Empty input_paragraph must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_paragraph(paragraph_factory, input_paragraph="")
    
    def test_input_paragraph_whitespace_only_raises_error(self, paragraph_factory):
        """Whitespace-only input_paragraph must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_paragraph(paragraph_factory, input_paragraph="   ")
    
    def test_input_paragraph_not_string_raises_error(self, paragraph_factory):
        """Non-string input_paragraph must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            build_paragraph(paragraph_factory, input_paragraph=None)
    
    def test_title_and_input_paragraph_trimmed(self, paragraph_factory):
        """Title and input_paragraph should be trimmed"""
        para = build_paragraph(
            paragraph_factory,
            title="  Test Title  ",
            input_paragraph="  Test Paragraph  "
        )
        assert para.title == "Test Title"
        assert para.input_paragraph == "Test Paragraph"


class TestParagraphFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_completed_raises_error(self, paragraph_factory):
        """from_dict() must also validate completed"""
        invalid_data = paragraph_factory(completed=200.0)
        
        with pytest.raises(ValueError, match="cannot exceed 100"):
            Paragraph.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_score_raises_error(self, paragraph_factory):
        """from_dict() must also validate score"""
        invalid_data = paragraph_factory(score=15.0)
        
        with pytest.raises(ValueError, match="cannot exceed 10"):
            Paragraph.from_dict(invalid_data)
    
    def test_from_dict_with_empty_title_raises_error(self, paragraph_factory):
        """from_dict() must validate empty title"""
        invalid_data = paragraph_factory(title="")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Paragraph.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self, paragraph_factory):
        """from_dict() with valid data must succeed"""
        valid_data = paragraph_factory(completed=75.0, score=8.5)
        
        para = Paragraph.from_dict(valid_data)
        assert para.completed == 75.0
        assert para.score == 8.5
