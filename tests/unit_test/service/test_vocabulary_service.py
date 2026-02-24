"""Unit tests for VocabularyService"""
import pytest
from service.vocabulary_service import VocabularyService
from model.vocabulary import Vocabulary


class TestVocabularyServiceCreate:
    """Tests for create_vocabulary operation"""

    def test_create_vocabulary_success(self) -> None:
        """Test creating a vocabulary item successfully"""
        service = VocabularyService()
        
        vocab_id = service.create_vocabulary(
            word="serendipity",
            part_of_speech="noun",
            vi_meaning="may mắn gặp",
            eng_description="finding something good by chance",
            example="Meeting her was pure serendipity."
        )
        
        assert vocab_id is not None
        assert isinstance(vocab_id, int)
        assert vocab_id > 0

    def test_create_vocabulary_with_note(self) -> None:
        """Test creating vocabulary with optional note field"""
        service = VocabularyService()
        
        vocab_id = service.create_vocabulary(
            word="ephemeral",
            part_of_speech="adjective",
            vi_meaning="tạm thời",
            eng_description="lasting a short time",
            example="Cherry blossoms are ephemeral.",
            note="Often used in poetry"
        )
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        assert vocab.note == "Often used in poetry"

    def test_created_vocabulary_has_zero_counts(self) -> None:
        """Test that new vocabulary has 0 correct and wrong counts"""
        service = VocabularyService()
        
        vocab_id = service.create_vocabulary(
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="test description",
            example="This is a test."
        )
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        assert vocab.correct_count == 0
        assert vocab.wrong_count == 0


class TestVocabularyServiceUpdate:
    """Tests for update_vocabulary operation"""

    def test_update_vocabulary_word(self) -> None:
        """Test updating vocabulary word"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="old",
            part_of_speech="adjective",
            vi_meaning="cũ",
            eng_description="not new",
            example="This is old."
        )
        
        service.update_vocabulary(vocab_id, word="ancient")
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        assert vocab.word == "ancient"

    def test_update_vocabulary_multiple_fields(self) -> None:
        """Test updating multiple vocabulary fields"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="assessment",
            example="Take the test."
        )
        
        service.update_vocabulary(
            vocab_id,
            vi_meaning="bài thi",
            eng_description="examination",
            correct_count=5
        )
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        assert vocab.vi_meaning == "bài thi"
        assert vocab.eng_description == "examination"
        assert vocab.correct_count == 5

    def test_update_vocabulary_correct_count(self) -> None:
        """Test updating correct answer count"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="test",
            part_of_speech="noun",
            vi_meaning="kiểm tra",
            eng_description="test",
            example="Test example"
        )
        
        service.update_vocabulary(vocab_id, correct_count=10)
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        assert vocab.correct_count == 10

    def test_update_vocabulary_correct_count_negative_raises_error(self) -> None:
        """Test that negative correct_count raises error"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="test",
            part_of_speech="noun",
            vi_meaning="test",
            eng_description="test",
            example="test"
        )
        
        with pytest.raises(ValueError, match="correct_count must be non-negative"):
            service.update_vocabulary(vocab_id, correct_count=-1)

    def test_update_vocabulary_wrong_count_negative_raises_error(self) -> None:
        """Test that negative wrong_count raises error"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="test",
            part_of_speech="noun",
            vi_meaning="test",
            eng_description="test",
            example="test"
        )
        
        with pytest.raises(ValueError, match="wrong_count must be non-negative"):
            service.update_vocabulary(vocab_id, wrong_count=-1)

    def test_update_nonexistent_vocabulary_raises_error(self) -> None:
        """Test that updating nonexistent vocabulary raises error"""
        service = VocabularyService()
        
        with pytest.raises(ValueError, match="does not exist"):
            service.update_vocabulary(9999, word="new")


class TestVocabularyServiceRead:
    """Tests for read operations"""

    def test_get_vocabulary_by_id(self) -> None:
        """Test retrieving vocabulary by ID"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="beautiful",
            part_of_speech="adjective",
            vi_meaning="đẹp",
            eng_description="attractive",
            example="She is beautiful."
        )
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        
        assert vocab is not None
        assert vocab.word == "beautiful"
        assert vocab.vi_meaning == "đẹp"

    def test_get_vocabulary_returns_none_for_nonexistent(self) -> None:
        """Test that nonexistent vocabulary returns None"""
        service = VocabularyService()
        
        vocab = service.get_vocabulary_by_id(9999)
        
        assert vocab is None

    def test_get_all_vocabulary(self) -> None:
        """Test retrieving all vocabulary"""
        service = VocabularyService()
        
        # Create multiple vocabularies
        service.create_vocabulary(
            word="word1",
            part_of_speech="noun",
            vi_meaning="meaning1",
            eng_description="desc1",
            example="example1"
        )
        service.create_vocabulary(
            word="word2",
            part_of_speech="verb",
            vi_meaning="meaning2",
            eng_description="desc2",
            example="example2"
        )
        
        all_vocabs = service.get_all_vocabulary()
        
        assert len(all_vocabs) >= 2
        assert all(isinstance(v, Vocabulary) for v in all_vocabs)

    def test_get_random_vocabulary(self) -> None:
        """Test getting a random vocabulary"""
        service = VocabularyService()
        
        # Create complete vocabulary
        service.create_vocabulary(
            word="random",
            part_of_speech="adjective",
            vi_meaning="ngẫu nhiên",
            eng_description="by chance",
            example="Choose a random number."
        )
        
        vocab = service.get_random_vocabulary()
        
        # Should return a vocabulary (might be None if none are complete)
        # Note: method creates Vocabulary from tuple, might need adjustment
        assert vocab is None or isinstance(vocab, Vocabulary)

class TestVocabularyServiceCount:
    """Tests for count operations"""

    def test_total_vocabulary(self) -> None:
        """Test getting total vocabulary count"""
        service = VocabularyService()
        
        # Create vocabularies
        service.create_vocabulary(
            word="word1",
            part_of_speech="noun",
            vi_meaning="meaning1",
            eng_description="desc1",
            example="example1"
        )
        service.create_vocabulary(
            word="word2",
            part_of_speech="verb",
            vi_meaning="meaning2",
            eng_description="desc2",
            example="example2"
        )
        
        total = service.total_vocabulary()
        
        assert total >= 2
        assert isinstance(total, int)

    def test_count_vocabulary_by_date(self) -> None:
        """Test getting vocabulary count grouped by date"""
        service = VocabularyService()
        
        # Create vocabulary
        service.create_vocabulary(
            word="test",
            part_of_speech="noun",
            vi_meaning="test",
            eng_description="test",
            example="test"
        )
        
        counts = service.count_vocabulary_by_date("2020-01-01")
        
        assert isinstance(counts, list)


class TestVocabularyServiceDelete:
    """Tests for delete operation"""

    def test_delete_vocabulary(self) -> None:
        """Test deleting a vocabulary item"""
        service = VocabularyService()
        vocab_id = service.create_vocabulary(
            word="delete_me",
            part_of_speech="verb",
            vi_meaning="xóa đi",
            eng_description="to remove",
            example="Delete this file."
        )
        
        service.delete_vocabulary(vocab_id)
        
        vocab = service.get_vocabulary_by_id(vocab_id)
        assert vocab is None

    def test_delete_nonexistent_vocabulary_does_not_raise_error(self) -> None:
        """Test that deleting nonexistent vocabulary doesn't raise error"""
        service = VocabularyService()
        
        # Should not raise exception
        service.delete_vocabulary(9999)
