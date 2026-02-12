"""Vocabulary fixtures - Sample data for testing"""
import pytest
from model.vocabulary import Vocabulary


@pytest.fixture
def sample_vocabulary() -> Vocabulary:
    """Sample vocabulary fixture - Common word with correct/wrong counts"""
    return Vocabulary(
        id=None,
        word="serendipity",
        part_of_speech="noun",
        vi_meaning="Tình cờ may mắn, sự gặp gỡ vui vẻ khó lường",
        eng_description="The occurrence of events by chance in a happy or beneficial way",
        example="Meeting her was pure serendipity.",
        note="Common word in English literature",
        correct_count=3,
        wrong_count=1,
        created_at="2026-01-26 12:00:00"
    )


@pytest.fixture
def sample_vocabulary_2() -> Vocabulary:
    """Sample vocabulary 2 fixture - Adjective with high accuracy"""
    return Vocabulary(
        id=None,
        word="ephemeral",
        part_of_speech="adjective",
        vi_meaning="Tạm thời, chỉ tồn tại trong thời gian ngắn",
        eng_description="Lasting for a very short time; transitory",
        example="The beauty of cherry blossoms is ephemeral.",
        note="Often used in poetry and literature",
        correct_count=2,
        wrong_count=0,
        created_at="2026-01-26 13:00:00"
    )
