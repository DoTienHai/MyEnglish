"""Unit tests for Vocabulary model validation"""
import pytest
from model.vocabulary import Vocabulary


class TestVocabularyCriticalFieldsValidation:
    """Test validation for critical fields (word)"""
    
    def test_word_empty_string_raises_error(self):
        """Empty word must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Vocabulary(
                id=1,
                word="",  # Empty string
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=0,
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_word_whitespace_only_raises_error(self):
        """Whitespace-only word must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Vocabulary(
                id=1,
                word="   ",  # Whitespace only
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=0,
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_word_not_string_raises_error(self):
        """Non-string word must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            Vocabulary(
                id=1,
                word=123,  # Integer instead of string
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=0,
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_word_trimmed(self):
        """Word should be trimmed"""
        vocab = Vocabulary(
            id=1,
            word="  test  ",  # Has leading/trailing spaces
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=0,
            wrong_count=0,
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.word == "test"


class TestVocabularyCorrectCountValidation:
    """Test correct_count field validation"""
    
    def test_correct_count_negative_raises_error(self):
        """Correct count < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=-5,  # Invalid
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_correct_count_zero_is_valid(self):
        """Correct count = 0 is a valid boundary value"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=0,  # Valid boundary
            wrong_count=0,
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.correct_count == 0
    
    def test_correct_count_positive_is_valid(self):
        """Positive correct count is valid"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=10,  # Valid
            wrong_count=5,
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.correct_count == 10
    
    def test_correct_count_type_validation(self):
        """Correct count must be an integer"""
        with pytest.raises(TypeError, match="must be an integer"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=5.5,  # Float instead of int
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_correct_count_setter_validates_update(self):
        """Update correct_count after creation must also validate"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=5,
            wrong_count=2,
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        vocab.correct_count = 10
        assert vocab.correct_count == 10
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            vocab.correct_count = -1


class TestVocabularyWrongCountValidation:
    """Test wrong_count field validation"""
    
    def test_wrong_count_negative_raises_error(self):
        """Wrong count < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=5,
                wrong_count=-3,  # Invalid
                created_at="2026-01-26 12:00:00"
            )
    
    def test_wrong_count_zero_is_valid(self):
        """Wrong count = 0 is a valid boundary value"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=10,
            wrong_count=0,  # Valid boundary
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.wrong_count == 0
    
    def test_wrong_count_positive_is_valid(self):
        """Positive wrong count is valid"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=5,
            wrong_count=8,  # Valid
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.wrong_count == 8
    
    def test_wrong_count_type_validation(self):
        """Wrong count must be an integer"""
        with pytest.raises(TypeError, match="must be an integer"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=5,
                wrong_count="3",  # String instead of int
                created_at="2026-01-26 12:00:00"
            )
    
    def test_wrong_count_setter_validates_update(self):
        """Update wrong_count after creation must also validate"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=5,
            wrong_count=2,
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        vocab.wrong_count = 5
        assert vocab.wrong_count == 5
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            vocab.wrong_count = -1


class TestVocabularyFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_correct_count_raises_error(self):
        """from_dict() must also validate correct_count"""
        invalid_data = {
            "id": 1,
            "word": "test",
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": -5,  # Invalid
            "wrong_count": 0,
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_wrong_count_raises_error(self):
        """from_dict() must also validate wrong_count"""
        invalid_data = {
            "id": 1,
            "word": "test",
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": 5,
            "wrong_count": -3,  # Invalid
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_empty_word_raises_error(self):
        """from_dict() must validate empty word"""
        invalid_data = {
            "id": 1,
            "word": "",  # Invalid
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": 5,
            "wrong_count": 0,
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self):
        """from_dict() with valid data must succeed"""
        valid_data = {
            "id": 1,
            "word": "test",
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": 10,  # Valid
            "wrong_count": 5,     # Valid
            "created_at": "2026-01-26 12:00:00"
        }
        
        vocab = Vocabulary.from_dict(valid_data)
        assert vocab.correct_count == 10
        assert vocab.wrong_count == 5
    """Test correct_count field validation"""
    
    def test_correct_count_negative_raises_error(self):
        """Correct count < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=-5,  # Invalid
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_correct_count_zero_is_valid(self):
        """Correct count = 0 is a valid boundary value"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=0,  # Valid boundary
            wrong_count=0,
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.correct_count == 0
    
    def test_correct_count_positive_is_valid(self):
        """Positive correct count is valid"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=10,  # Valid
            wrong_count=5,
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.correct_count == 10
    
    def test_correct_count_type_validation(self):
        """Correct count must be an integer"""
        with pytest.raises(TypeError, match="must be an integer"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=5.5,  # Float instead of int
                wrong_count=0,
                created_at="2026-01-26 12:00:00"
            )
    
    def test_correct_count_setter_validates_update(self):
        """Update correct_count after creation must also validate"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=5,
            wrong_count=2,
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        vocab.correct_count = 10
        assert vocab.correct_count == 10
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            vocab.correct_count = -1


class TestVocabularyWrongCountValidation:
    """Test wrong_count field validation"""
    
    def test_wrong_count_negative_raises_error(self):
        """Wrong count < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=5,
                wrong_count=-3,  # Invalid
                created_at="2026-01-26 12:00:00"
            )
    
    def test_wrong_count_zero_is_valid(self):
        """Wrong count = 0 is a valid boundary value"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=10,
            wrong_count=0,  # Valid boundary
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.wrong_count == 0
    
    def test_wrong_count_positive_is_valid(self):
        """Positive wrong count is valid"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=5,
            wrong_count=8,  # Valid
            created_at="2026-01-26 12:00:00"
        )
        assert vocab.wrong_count == 8
    
    def test_wrong_count_type_validation(self):
        """Wrong count must be an integer"""
        with pytest.raises(TypeError, match="must be an integer"):
            Vocabulary(
                id=1,
                word="test",
                part_of_speech="noun",
                vi_meaning="kiểm tra",
                eng_description="a procedure to check quality",
                example="This is a test.",
                note="",
                correct_count=5,
                wrong_count="3",  # String instead of int
                created_at="2026-01-26 12:00:00"
            )
    
    def test_wrong_count_setter_validates_update(self):
        """Update wrong_count after creation must also validate"""
        vocab = Vocabulary(
            id=1,
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="a procedure to check quality",
            example="This is a test.",
            note="",
            correct_count=5,
            wrong_count=2,
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        vocab.wrong_count = 5
        assert vocab.wrong_count == 5
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            vocab.wrong_count = -1


class TestVocabularyFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_correct_count_raises_error(self):
        """from_dict() must also validate correct_count"""
        invalid_data = {
            "id": 1,
            "word": "test",
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": -5,  # Invalid
            "wrong_count": 0,
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_wrong_count_raises_error(self):
        """from_dict() must also validate wrong_count"""
        invalid_data = {
            "id": 1,
            "word": "test",
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": 5,
            "wrong_count": -3,  # Invalid
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self):
        """from_dict() with valid data must succeed"""
        valid_data = {
            "id": 1,
            "word": "test",
            "part_of_speech": "noun",
            "vi_meaning": "kiểm tra",
            "eng_description": "a procedure to check quality",
            "example": "This is a test.",
            "note": "",
            "correct_count": 10,  # Valid
            "wrong_count": 5,     # Valid
            "created_at": "2026-01-26 12:00:00"
        }
        
        vocab = Vocabulary.from_dict(valid_data)
        assert vocab.correct_count == 10
        assert vocab.wrong_count == 5
