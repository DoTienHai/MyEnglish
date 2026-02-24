"""Unit tests for Vocabulary model validation"""
import pytest
from model.vocabulary import Vocabulary


def build_vocabulary(vocabulary_factory, **overrides) -> Vocabulary:
    """Helper to build Vocabulary from fixture dict with overrides"""
    return Vocabulary(**vocabulary_factory(**overrides))

class TestVocabularyCriticalFieldsValidation:
    """Test validation for critical fields (word)"""
    
    def test_word_empty_string_raises_error(self, vocabulary_factory):
        """Empty word must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_vocabulary(vocabulary_factory, word="")
    
    def test_word_whitespace_only_raises_error(self, vocabulary_factory):
        """Whitespace-only word must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            build_vocabulary(vocabulary_factory, word="   ")
    
    def test_word_not_string_raises_error(self, vocabulary_factory):
        """Non-string word must raise TypeError"""
        with pytest.raises(TypeError, match="must be a string"):
            build_vocabulary(vocabulary_factory, word=123)
    
    def test_word_trimmed(self, vocabulary_factory):
        """Word should be trimmed"""
        vocab = build_vocabulary(vocabulary_factory, word="  test  ")
        assert vocab.word == "test"


class TestVocabularyCorrectCountValidation:
    """Test correct_count field validation"""
    
    def test_correct_count_negative_raises_error(self, vocabulary_factory):
        """Correct count < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            build_vocabulary(vocabulary_factory, correct_count=-5)
    
    def test_correct_count_zero_is_valid(self, vocabulary_factory):
        """Correct count = 0 is a valid boundary value"""
        vocab = build_vocabulary(vocabulary_factory, correct_count=0, wrong_count=0)
        assert vocab.correct_count == 0
    
    def test_correct_count_positive_is_valid(self, vocabulary_factory):
        """Positive correct count is valid"""
        vocab = build_vocabulary(vocabulary_factory, correct_count=10, wrong_count=5)
        assert vocab.correct_count == 10
    
    def test_correct_count_type_validation(self, vocabulary_factory):
        """Correct count must be an integer"""
        with pytest.raises(TypeError, match="must be an integer"):
            build_vocabulary(vocabulary_factory, correct_count=5.5)
    
    def test_correct_count_setter_validates_update(self, vocabulary_factory):
        """Update correct_count after creation must also validate"""
        vocab = build_vocabulary(vocabulary_factory, correct_count=5, wrong_count=2)
        
        # Valid update
        vocab.correct_count = 10
        assert vocab.correct_count == 10
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            vocab.correct_count = -1


class TestVocabularyWrongCountValidation:
    """Test wrong_count field validation"""
    
    def test_wrong_count_negative_raises_error(self, vocabulary_factory):
        """Wrong count < 0 must raise ValueError"""
        with pytest.raises(ValueError, match="cannot be negative"):
            build_vocabulary(vocabulary_factory, correct_count=5, wrong_count=-3)
    
    def test_wrong_count_zero_is_valid(self, vocabulary_factory):
        """Wrong count = 0 is a valid boundary value"""
        vocab = build_vocabulary(vocabulary_factory, correct_count=10, wrong_count=0)
        assert vocab.wrong_count == 0
    
    def test_wrong_count_positive_is_valid(self, vocabulary_factory):
        """Positive wrong count is valid"""
        vocab = build_vocabulary(vocabulary_factory, correct_count=5, wrong_count=8)
        assert vocab.wrong_count == 8
    
    def test_wrong_count_type_validation(self, vocabulary_factory):
        """Wrong count must be an integer"""
        with pytest.raises(TypeError, match="must be an integer"):
            build_vocabulary(vocabulary_factory, correct_count=5, wrong_count="3")
    
    def test_wrong_count_setter_validates_update(self, vocabulary_factory):
        """Update wrong_count after creation must also validate"""
        vocab = build_vocabulary(vocabulary_factory, correct_count=5, wrong_count=2)
        
        # Valid update
        vocab.wrong_count = 5
        assert vocab.wrong_count == 5
        
        # Invalid update
        with pytest.raises(ValueError, match="cannot be negative"):
            vocab.wrong_count = -1


class TestVocabularyFromDictValidation:
    """Test validation when creating from dict (DB retrieval)"""
    
    def test_from_dict_with_invalid_correct_count_raises_error(self, vocabulary_factory):
        """from_dict() must also validate correct_count"""
        invalid_data = vocabulary_factory(correct_count=-5)
        
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_invalid_wrong_count_raises_error(self, vocabulary_factory):
        """from_dict() must also validate wrong_count"""
        invalid_data = vocabulary_factory(correct_count=5, wrong_count=-3)
        
        with pytest.raises(ValueError, match="cannot be negative"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_empty_word_raises_error(self, vocabulary_factory):
        """from_dict() must validate empty word"""
        invalid_data = vocabulary_factory(word="")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            Vocabulary.from_dict(invalid_data)
    
    def test_from_dict_with_valid_data_succeeds(self, vocabulary_factory):
        """from_dict() with valid data must succeed"""
        valid_data = vocabulary_factory(correct_count=10, wrong_count=5)
        
        vocab = Vocabulary.from_dict(valid_data)
        assert vocab.correct_count == 10
        assert vocab.wrong_count == 5
