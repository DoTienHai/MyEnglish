"""Vocabulary fixtures - Sample data for testing"""
import pytest


@pytest.fixture
def sample_vocabulary_base() -> dict:
    """Base vocabulary data - Common word with correct/wrong counts"""
    return {
        "id": None,
        "word": "serendipity",
        "part_of_speech": "noun",
        "vi_meaning": "Tình cờ may mắn, sự gặp gỡ vui vẻ khó lường",
        "eng_description": "The occurrence of events by chance in a happy or beneficial way",
        "example": "Meeting her was pure serendipity.",
        "note": "Common word in English literature",
        "correct_count": 3,
        "wrong_count": 1,
        "created_at": "2026-01-26 12:00:00"
    }


@pytest.fixture
def vocabulary_factory(sample_vocabulary_base: dict):
    """Factory for creating vocabulary dicts with overrides"""
    def _factory(**overrides):
        data = dict(sample_vocabulary_base)
        data.update(overrides)
        return data

    return _factory


@pytest.fixture
def sample_vocabulary_2() -> dict:
    """Sample vocabulary 2 data - Adjective with high accuracy"""
    return {
        "id": None,
        "word": "ephemeral",
        "part_of_speech": "adjective",
        "vi_meaning": "Tạm thời, chỉ tồn tại trong thời gian ngắn",
        "eng_description": "Lasting for a very short time; transitory",
        "example": "The beauty of cherry blossoms is ephemeral.",
        "note": "Often used in poetry and literature",
        "correct_count": 2,
        "wrong_count": 0,
        "created_at": "2026-01-26 13:00:00"
    }


# ============ Builder Fixtures (tạo model objects từ dicts) ============

@pytest.fixture
def sample_vocabulary_base_model(sample_vocabulary_base: dict):
    """Vocabulary model - Common word with correct/wrong counts"""
    from model.vocabulary import Vocabulary
    return Vocabulary(**sample_vocabulary_base)


@pytest.fixture
def sample_vocabulary_2_model(sample_vocabulary_2: dict):
    """Vocabulary model 2 - Adjective with high accuracy"""
    from model.vocabulary import Vocabulary
    return Vocabulary(**sample_vocabulary_2)

# ============ Factory Fixtures for get_all_vocabulary_complete() tests ============

@pytest.fixture
def vocabulary_complete_factory(vocabulary_factory):
    """Factory for creating complete vocabulary with all required fields"""
    def _factory(**overrides):
        defaults = {
            "word": "serendipity",
            "part_of_speech": "noun",
            "vi_meaning": "may mắn gặp",
            "eng_description": "finding something good by chance",
            "example": "She found a serendipity gift in the store",
            "note": "positive feeling",
            "correct_count": 0,
            "wrong_count": 0,
            "created_at": "2024-01-01 10:00:00"
        }
        defaults.update(overrides)
        return vocabulary_factory(**defaults)
    
    return _factory


@pytest.fixture
def vocabulary_no_example_factory(vocabulary_factory):
    """Factory for creating vocabulary without example (empty string)"""
    def _factory(**overrides):
        defaults = {
            "word": "abcdef",
            "part_of_speech": "verb",
            "vi_meaning": "định nghĩa",
            "eng_description": "description here",
            "example": "",  # Empty example
            "note": "note",
            "correct_count": 0,
            "wrong_count": 0,
            "created_at": "2024-01-01 10:00:00"
        }
        defaults.update(overrides)
        return vocabulary_factory(**defaults)
    
    return _factory


@pytest.fixture
def vocabulary_no_vi_meaning_factory(vocabulary_factory):
    """Factory for creating vocabulary without vi_meaning (empty string)"""
    def _factory(**overrides):
        defaults = {
            "word": "testword",
            "part_of_speech": "adjective",
            "vi_meaning": "",  # Empty vi_meaning
            "eng_description": "test description",
            "example": "This is a test example",
            "note": "test note",
            "correct_count": 0,
            "wrong_count": 0,
            "created_at": "2024-01-02 10:00:00"
        }
        defaults.update(overrides)
        return vocabulary_factory(**defaults)
    
    return _factory


# ============ Model Builder Factories ============

@pytest.fixture
def vocabulary_complete_model(vocabulary_complete_factory):
    """Complete vocabulary model - Has all required fields"""
    from model.vocabulary import Vocabulary
    data = vocabulary_complete_factory()
    return Vocabulary(**data)


@pytest.fixture
def vocabulary_no_example_model(vocabulary_no_example_factory):
    """Vocabulary model without example"""
    from model.vocabulary import Vocabulary
    data = vocabulary_no_example_factory()
    return Vocabulary(**data)


@pytest.fixture
def vocabulary_no_vi_meaning_model(vocabulary_no_vi_meaning_factory):
    """Vocabulary model without vi_meaning"""
    from model.vocabulary import Vocabulary
    data = vocabulary_no_vi_meaning_factory()
    return Vocabulary(**data)