"""Unit tests for Sentence model validation"""
import pytest
from model.sentence import Sentence


class TestSentenceScoreValidation:
    """Test score field validation"""
    
    def test_score_negative_raises_error(self):
        """Score < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=0,
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=-5.0,  # Invalid
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_score_over_10_raises_error(self):
        """Score > 10 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot exceed 10"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=0,
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=15.0,  # Invalid
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_score_exactly_zero_is_valid(self):
        """Score = 0 is a valid boundary value"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,
            input_sentence="Test sentence",
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=0.0,  # Valid boundary
            note="",
            created_at="2026-01-26 12:00:00"
        )
        assert sentence.score == 0.0
    
    def test_score_exactly_10_is_valid(self):
        """Score = 10 is a valid boundary value"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,
            input_sentence="Test sentence",
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=10.0,  # Valid boundary
            note="",
            created_at="2026-01-26 12:00:00"
        )
        assert sentence.score == 10.0
    
    def test_score_decimal_is_valid(self):
        """Score can be a decimal value"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,
            input_sentence="Test sentence",
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=8.5,  # Valid decimal
            note="",
            created_at="2026-01-26 12:00:00"
        )
        assert sentence.score == 8.5
    
    def test_score_type_validation(self):
        """Score must be numeric"""
        with pytest.raises(TypeError, match="must be numeric"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=0,
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score="8.5",  # String instead of float
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_score_setter_validates_update(self):
        """Update score after creation must also validate"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,
            input_sentence="Test sentence",
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=5.0,
            note="",
            created_at="2026-01-26 12:00:00"
        )
        
        # Valid update
        sentence.score = 8.0
        assert sentence.score == 8.0
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot exceed 10"):
            sentence.score = 20.0
    
    def test_score_accepts_integer(self):
        """Score can be an integer (converted to float)"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,
            input_sentence="Test sentence",
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=5,  # Integer instead of float
            note="",
            created_at="2026-01-26 12:00:00"
        )
        assert sentence.score == 5.0
        assert isinstance(sentence.score, float)


class TestSentenceCriticalFieldsValidation:
    """Test validation for critical fields (paragraph_id, sentence_index, input_sentence)"""
    
    def test_paragraph_id_zero_raises_error(self):
        """Paragraph ID = 0 must raise ValueError"""
        with pytest.raises(ValueError, match="must be positive"):
            Sentence(
                id=1,
                paragraph_id=0,  # Invalid: must be > 0
                sentence_index=0,
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_paragraph_id_negative_raises_error(self):
        """Negative paragraph ID must raise ValueError"""
        with pytest.raises(ValueError, match="must be positive"):
            Sentence(
                id=1,
                paragraph_id=-5,  # Invalid
                sentence_index=0,
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_paragraph_id_not_integer_raises_error(self):
        """Non-integer paragraph ID must raise TypeError"""
        with pytest.raises(TypeError, match="must be an integer"):
            Sentence(
                id=1,
                paragraph_id="1",  # String instead of int
                sentence_index=0,
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_sentence_index_negative_raises_error(self):
        """Negative sentence index must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=-1,  # Invalid: must be >= 0
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_sentence_index_not_integer_raises_error(self):
        """Non-integer sentence index must raise TypeError"""
        with pytest.raises(TypeError, match="must be an integer"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=1.5,  # Float instead of int
                input_sentence="Test sentence",
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_sentence_index_zero_is_valid(self):
        """Sentence index = 0 is valid (first sentence)"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,  # Valid: first sentence
            input_sentence="Test sentence",
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=5.0,
            note="",
            created_at="2026-01-26 12:00:00"
        )
        assert sentence.sentence_index == 0
    
    def test_input_sentence_empty_string_raises_error(self):
        """Empty input_sentence must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=0,
                input_sentence="",  # Empty string
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_input_sentence_whitespace_only_raises_error(self):
        """Whitespace-only input_sentence must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=0,
                input_sentence="   ",  # Whitespace only
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_input_sentence_not_string_raises_error(self):
        """Non-string input_sentence must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            Sentence(
                id=1,
                paragraph_id=1,
                sentence_index=0,
                input_sentence=123,  # Integer instead of string
                user_translation="Câu test",
                machine_translation="Câu kiểm tra",
                score=5.0,
                note="",
                created_at="2026-01-26 12:00:00"
            )
    
    def test_input_sentence_trimmed(self):
        """Input sentence should be trimmed"""
        sentence = Sentence(
            id=1,
            paragraph_id=1,
            sentence_index=0,
            input_sentence="  Test sentence  ",  # Has leading/trailing spaces
            user_translation="Câu test",
            machine_translation="Câu kiểm tra",
            score=5.0,
            note="",
            created_at="2026-01-26 12:00:00"
        )
        assert sentence.input_sentence == "Test sentence"


class TestSentenceFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_score_raises_error(self):
        """from_dict() must also validate score"""
        invalid_data = {
            "id": 1,
            "paragraph_id": 1,
            "sentence_index": 0,
            "input_sentence": "Test sentence",
            "user_translation": "Câu test",
            "machine_translation": "Câu kiểm tra",
            "score": 15.0,  # Invalid
            "note": "",
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot exceed 10"):
            Sentence.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_paragraph_id_raises_error(self):
        """from_dict() must validate paragraph_id"""
        invalid_data = {
            "id": 1,
            "paragraph_id": 0,  # Invalid
            "sentence_index": 0,
            "input_sentence": "Test sentence",
            "user_translation": "Câu test",
            "machine_translation": "Câu kiểm tra",
            "score": 5.0,
            "note": "",
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="must be positive"):
            Sentence.from_dict(invalid_data)
    
    def test_from_dict_with_empty_input_sentence_raises_error(self):
        """from_dict() must validate empty input_sentence"""
        invalid_data = {
            "id": 1,
            "paragraph_id": 1,
            "sentence_index": 0,
            "input_sentence": "",  # Invalid
            "user_translation": "Câu test",
            "machine_translation": "Câu kiểm tra",
            "score": 5.0,
            "note": "",
            "created_at": "2026-01-26 12:00:00"
        }
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Sentence.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self):
        """from_dict() with valid data must succeed"""
        valid_data = {
            "id": 1,
            "paragraph_id": 1,
            "sentence_index": 0,
            "input_sentence": "Test sentence",
            "user_translation": "Câu test",
            "machine_translation": "Câu kiểm tra",
            "score": 8.5,  # Valid
            "note": "",
            "created_at": "2026-01-26 12:00:00"
        }
        
        sentence = Sentence.from_dict(valid_data)
        assert sentence.score == 8.5
