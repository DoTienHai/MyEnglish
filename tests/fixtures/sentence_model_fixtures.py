"""Sentence fixtures - Sample data for testing"""
import pytest


@pytest.fixture
def sample_sentence_base() -> dict:
    """Base sentence data - High quality translation (0.95 score)"""
    return {
        "id": None,
        "paragraph_id": 1,
        "sentence_index": 1,
        "input_sentence": "The quick brown fox jumps over the lazy dog.",
        "user_translation": "Con cáo nâu nhanh nhảy qua con chó lười biếng.",
        "machine_translation": "Con cáo nâu nhanh nhảy qua con chó lười biếng.",
        "score": 0.95,
        "note": "Good translation",
        "created_at": "2026-01-26 12:00:00"
    }


@pytest.fixture
def sentence_factory(sample_sentence_base: dict):
    """Factory for creating sentence dicts with overrides"""
    def _factory(**overrides):
        data = dict(sample_sentence_base)
        data.update(overrides)
        return data

    return _factory


@pytest.fixture
def sample_sentence_2() -> dict:
    """Sample sentence 2 data - Medium quality translation (0.88 score)"""
    return {
        "id": None,
        "paragraph_id": 1,
        "sentence_index": 2,
        "input_sentence": "This is a common English sentence used for testing.",
        "user_translation": "Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra.",
        "machine_translation": "Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra.",
        "score": 0.88,
        "note": "Acceptable translation",
        "created_at": "2026-01-26 12:05:00"
    }


# ============ Builder Fixtures (tạo model objects từ dicts) ============

@pytest.fixture
def sample_sentence_base_model(sample_sentence_base: dict):
    """Sentence model - High quality translation (0.95 score)"""
    from model.sentence import Sentence
    return Sentence(**sample_sentence_base)


@pytest.fixture
def sample_sentence_2_model(sample_sentence_2: dict):
    """Sentence model 2 - Medium quality translation (0.88 score)"""
    from model.sentence import Sentence
    return Sentence(**sample_sentence_2)
