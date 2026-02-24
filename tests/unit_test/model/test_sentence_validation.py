"""Unit tests for Sentence model validation"""
import pytest
from model.sentence import Sentence


def build_sentence(sentence_factory, **overrides) -> Sentence:
    """Helper to build Sentence from fixture dict with overrides"""
    return Sentence(**sentence_factory(**overrides))


class TestSentenceScoreValidation:
    """Test score field validation"""
    
    def test_score_negative_raises_error(self, sentence_factory):
        """Score < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            build_sentence(sentence_factory, score=-5.0)
    
    def test_score_over_10_raises_error(self, sentence_factory):
        """Score > 10 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot exceed 10"):
            build_sentence(sentence_factory, score=15.0)
    
    def test_score_exactly_zero_is_valid(self, sentence_factory):
        """Score = 0 is a valid boundary value"""
        sentence = build_sentence(sentence_factory, score=0.0)
        assert sentence.score == 0.0
    
    def test_score_exactly_10_is_valid(self, sentence_factory):
        """Score = 10 is a valid boundary value"""
        sentence = build_sentence(sentence_factory, score=10.0)
        assert sentence.score == 10.0
    
    def test_score_decimal_is_valid(self, sentence_factory):
        """Score can be a decimal value"""
        sentence = build_sentence(sentence_factory, score=8.5)
        assert sentence.score == 8.5
    
    def test_score_type_validation(self, sentence_factory):
        """Score must be numeric"""
        with pytest.raises(TypeError, match="must be numeric"):
            build_sentence(sentence_factory, score="8.5")
    
    def test_score_setter_validates_update(self, sentence_factory):
        """Update score after creation must also validate"""
        sentence = build_sentence(sentence_factory, score=5.0)
        
        # Valid update
        sentence.score = 8.0
        assert sentence.score == 8.0
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot exceed 10"):
            sentence.score = 20.0
    
    def test_score_accepts_integer(self, sentence_factory):
        """Score can be an integer (converted to float)"""
        sentence = build_sentence(sentence_factory, score=5)
        assert sentence.score == 5.0
        assert isinstance(sentence.score, float)


class TestSentenceCriticalFieldsValidation:
    """Test validation for critical fields (paragraph_id, sentence_index, input_sentence)"""
    
    def test_paragraph_id_zero_raises_error(self, sentence_factory):
        """Paragraph ID = 0 must raise ValueError"""
        with pytest.raises(ValueError, match="must be positive"):
            build_sentence(sentence_factory, paragraph_id=0)
    
    def test_paragraph_id_negative_raises_error(self, sentence_factory):
        """Negative paragraph ID must raise ValueError"""
        with pytest.raises(ValueError, match="must be positive"):
            build_sentence(sentence_factory, paragraph_id=-5)
    
    def test_paragraph_id_not_integer_raises_error(self, sentence_factory):
        """Non-integer paragraph ID must raise TypeError"""
        with pytest.raises(TypeError, match="must be an integer"):
            build_sentence(sentence_factory, paragraph_id="1")
    
    def test_sentence_index_negative_raises_error(self, sentence_factory):
        """Negative sentence index must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            build_sentence(sentence_factory, sentence_index=-1)
    
    def test_sentence_index_not_integer_raises_error(self, sentence_factory):
        """Non-integer sentence index must raise TypeError"""
        with pytest.raises(TypeError, match="must be an integer"):
            build_sentence(sentence_factory, sentence_index=1.5)
    
    def test_sentence_index_zero_is_valid(self, sentence_factory):
        """Sentence index = 0 is valid (first sentence)"""
        sentence = build_sentence(sentence_factory, sentence_index=0)
        assert sentence.sentence_index == 0
    
    def test_input_sentence_empty_string_raises_error(self, sentence_factory):
        """Empty input_sentence must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_sentence(sentence_factory, input_sentence="")
    
    def test_input_sentence_whitespace_only_raises_error(self, sentence_factory):
        """Whitespace-only input_sentence must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_sentence(sentence_factory, input_sentence="   ")
    
    def test_input_sentence_not_string_raises_error(self, sentence_factory):
        """Non-string input_sentence must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            build_sentence(sentence_factory, input_sentence=123)
    
    def test_input_sentence_trimmed(self, sentence_factory):
        """Input sentence should be trimmed"""
        sentence = build_sentence(sentence_factory, input_sentence="  Test sentence  ")
        assert sentence.input_sentence == "Test sentence"


class TestSentenceFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_score_raises_error(self, sentence_factory):
        """from_dict() must also validate score"""
        invalid_data = sentence_factory(score=15.0)
        
        with pytest.raises(ValueError, match="cannot exceed 10"):
            Sentence.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_paragraph_id_raises_error(self, sentence_factory):
        """from_dict() must validate paragraph_id"""
        invalid_data = sentence_factory(paragraph_id=0)
        
        with pytest.raises(ValueError, match="must be positive"):
            Sentence.from_dict(invalid_data)
    
    def test_from_dict_with_empty_input_sentence_raises_error(self, sentence_factory):
        """from_dict() must validate empty input_sentence"""
        invalid_data = sentence_factory(input_sentence="")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Sentence.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self, sentence_factory):
        """from_dict() with valid data must succeed"""
        valid_data = sentence_factory(score=8.5)
        
        sentence = Sentence.from_dict(valid_data)
        assert sentence.score == 8.5
