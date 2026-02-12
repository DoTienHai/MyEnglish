"""Sentence fixtures - Sample data for testing"""
import pytest
from model.sentence import Sentence


@pytest.fixture
def sample_sentence() -> Sentence:
    """Sample sentence fixture - High quality translation (0.95 score)"""
    return Sentence(
        id=None,
        paragraph_id=1,
        sentence_index=1,
        input_sentence="The quick brown fox jumps over the lazy dog.",
        user_translation="Con cáo nâu nhanh nhảy qua con chó lười biếng.",
        machine_translation="Con cáo nâu nhanh nhảy qua con chó lười biếng.",
        score=0.95,
        note="Good translation",
        created_at="2026-01-26 12:00:00"
    )


@pytest.fixture
def sample_sentence_2() -> Sentence:
    """Sample sentence 2 fixture - Medium quality translation (0.88 score)"""
    return Sentence(
        id=None,
        paragraph_id=1,
        sentence_index=2,
        input_sentence="This is a common English sentence used for testing.",
        user_translation="Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra.",
        machine_translation="Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra.",
        score=0.88,
        note="Acceptable translation",
        created_at="2026-01-26 12:05:00"
    )
