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
