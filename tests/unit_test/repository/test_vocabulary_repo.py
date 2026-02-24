"""Unit tests for VocabularyRepository"""
import pytest
from repositories.vocabulary_repo import VocabularyRepository
from model.vocabulary import Vocabulary


class TestVocabularyRepositoryCreate:
    """Tests for create operation"""

    def test_create_vocabulary_success(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test creating a vocabulary item successfully"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        
        assert vocab_id is not None
        assert isinstance(vocab_id, int)
        assert vocab_id > 0

    def test_created_vocabulary_can_be_retrieved(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test that created vocabulary can be retrieved"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        retrieved = vocabulary_repo.get(vocab_id)
        
        assert retrieved is not None
        assert retrieved.word == sample_vocabulary_base_model.word
        assert retrieved.vi_meaning == sample_vocabulary_base_model.vi_meaning
        assert retrieved.example == sample_vocabulary_base_model.example

    def test_create_multiple_vocabulary_items(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary,
        sample_vocabulary_2_model: Vocabulary
    ) -> None:
        """Test creating multiple vocabulary items"""
        vocab_id_1 = vocabulary_repo.create(sample_vocabulary_base_model)
        vocab_id_2 = vocabulary_repo.create(sample_vocabulary_2_model)
        
        assert vocab_id_1 is not None
        assert vocab_id_2 is not None
        assert vocab_id_1 != vocab_id_2

    def test_created_vocabulary_has_correct_fields(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test that created vocabulary has all correct fields"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        retrieved = vocabulary_repo.get(vocab_id)
        
        assert retrieved.word == sample_vocabulary_base_model.word
        assert retrieved.part_of_speech == sample_vocabulary_base_model.part_of_speech
        assert retrieved.vi_meaning == sample_vocabulary_base_model.vi_meaning
        assert retrieved.eng_description == sample_vocabulary_base_model.eng_description
        assert retrieved.example == sample_vocabulary_base_model.example
        assert retrieved.note == sample_vocabulary_base_model.note
        assert retrieved.correct_count == sample_vocabulary_base_model.correct_count
        assert retrieved.wrong_count == sample_vocabulary_base_model.wrong_count


class TestVocabularyRepositoryRead:
    """Tests for read operations"""

    def test_get_existing_vocabulary(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test getting an existing vocabulary item"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        retrieved = vocabulary_repo.get(vocab_id)
        
        assert retrieved is not None
        assert isinstance(retrieved, Vocabulary)
        assert retrieved.id == vocab_id

    def test_get_nonexistent_vocabulary_returns_none(
        self,
        vocabulary_repo: VocabularyRepository
    ) -> None:
        """Test getting a non-existent vocabulary returns None"""
        result = vocabulary_repo.get(9999)
        
        assert result is None

    def test_get_all_vocabulary_empty_database(
        self,
        vocabulary_repo: VocabularyRepository
    ) -> None:
        """Test getting all vocabulary from empty database"""
        all_vocabulary = vocabulary_repo.all()
        
        assert isinstance(all_vocabulary, list)
        assert len(all_vocabulary) == 0

    def test_get_all_vocabulary_with_data(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary,
        sample_vocabulary_2_model: Vocabulary
    ) -> None:
        """Test getting all vocabulary items"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        vocabulary_repo.create(sample_vocabulary_2_model)
        
        all_vocabulary = vocabulary_repo.all()
        
        assert len(all_vocabulary) == 2
        assert all(isinstance(v, Vocabulary) for v in all_vocabulary)

    def test_get_all_vocabulary_method(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test get_all_vocabulary method"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        all_vocabulary = vocabulary_repo.get_all_vocabulary()
        
        assert isinstance(all_vocabulary, list)
        assert len(all_vocabulary) >= 1


class TestVocabularyRepositoryUpdate:
    """Tests for update operations"""

    def test_update_vocabulary_meaning(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test updating vocabulary meaning"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        vocab = vocabulary_repo.get(vocab_id)
        
        vocab.vi_meaning = "Định nghĩa mới"
        vocabulary_repo.update(vocab)
        
        updated = vocabulary_repo.get(vocab_id)
        assert updated.vi_meaning == "Định nghĩa mới"

    def test_update_vocabulary_example(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test updating vocabulary example"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        vocab = vocabulary_repo.get(vocab_id)
        
        vocab.example = "New example sentence"
        vocabulary_repo.update(vocab)
        
        updated = vocabulary_repo.get(vocab_id)
        assert updated.example == "New example sentence"

    def test_update_correct_count(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test updating correct count"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        vocab = vocabulary_repo.get(vocab_id)
        
        vocab.correct_count = 10
        vocabulary_repo.update(vocab)
        
        updated = vocabulary_repo.get(vocab_id)
        assert updated.correct_count == 10

    def test_update_wrong_count(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test updating wrong count"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        vocab = vocabulary_repo.get(vocab_id)
        
        vocab.wrong_count = 5
        vocabulary_repo.update(vocab)
        
        updated = vocabulary_repo.get(vocab_id)
        assert updated.wrong_count == 5

    def test_update_preserves_other_fields(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test that updating one field preserves other fields"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        vocab = vocabulary_repo.get(vocab_id)
        original_word = vocab.word
        
        vocab.correct_count = 7
        vocabulary_repo.update(vocab)
        
        updated = vocabulary_repo.get(vocab_id)
        assert updated.word == original_word
        assert updated.correct_count == 7


class TestVocabularyRepositoryDelete:
    """Tests for delete operations"""

    def test_delete_existing_vocabulary(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test deleting an existing vocabulary item"""
        vocab_id = vocabulary_repo.create(sample_vocabulary_base_model)
        assert vocabulary_repo.get(vocab_id) is not None
        
        vocabulary_repo.delete(vocab_id)
        
        assert vocabulary_repo.get(vocab_id) is None

    def test_delete_nonexistent_vocabulary_does_not_raise(
        self,
        vocabulary_repo: VocabularyRepository
    ) -> None:
        """Test that deleting non-existent vocabulary doesn't raise error"""
        # Should not raise exception
        vocabulary_repo.delete(9999)

    def test_delete_reduces_count(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary,
        sample_vocabulary_2_model: Vocabulary
    ) -> None:
        """Test that deleting vocabulary reduces count"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        vocabulary_repo.create(sample_vocabulary_2_model)
        
        initial_count = vocabulary_repo.count_all()
        assert initial_count == 2
        
        all_vocabulary = vocabulary_repo.all()
        vocabulary_repo.delete(all_vocabulary[0].id)
        
        new_count = vocabulary_repo.count_all()
        assert new_count == 1


class TestVocabularyRepositoryFilter:
    """Tests for filter operations"""

    def test_filter_by_word(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test filtering vocabulary by word"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        filtered = vocabulary_repo.filter(word="serendipity")
        
        assert len(filtered) == 1
        assert filtered[0].word == "serendipity"

    def test_filter_by_part_of_speech(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary,
        sample_vocabulary_2_model: Vocabulary
    ) -> None:
        """Test filtering vocabulary by part of speech"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        vocabulary_repo.create(sample_vocabulary_2_model)
        
        filtered = vocabulary_repo.filter(part_of_speech="noun")
        
        assert len(filtered) == 1
        assert filtered[0].part_of_speech == "noun"

    def test_filter_returns_empty_list_when_no_match(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test that filter returns empty list when no match"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        filtered = vocabulary_repo.filter(word="nonexistent")
        
        assert isinstance(filtered, list)
        assert len(filtered) == 0


class TestVocabularyRepositoryCount:
    """Tests for count operations"""

    def test_count_all_empty_database(
        self,
        vocabulary_repo: VocabularyRepository
    ) -> None:
        """Test count all on empty database"""
        count = vocabulary_repo.count_all()
        
        assert count == 0

    def test_count_all_with_data(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary,
        sample_vocabulary_2_model: Vocabulary
    ) -> None:
        """Test count all with data"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        vocabulary_repo.create(sample_vocabulary_2_model)
        
        count = vocabulary_repo.count_all()
        
        assert count == 2

    def test_count_by_part_of_speech(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test count by part of speech"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        count = vocabulary_repo.count_by(part_of_speech="noun")
        
        assert count == 1

    def test_count_vocabulary_method(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test count_vocabulary (via get_all_vocabulary)"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        all_vocabulary = vocabulary_repo.get_all_vocabulary()
        
        assert len(all_vocabulary) >= 1


class TestVocabularyRepositoryGroupedByDate:
    """Tests for count grouped by date"""

    def test_count_vocabulary_grouped_by_date_empty(
        self,
        vocabulary_repo: VocabularyRepository
    ) -> None:
        """Test count grouped by date on empty database"""
        result = vocabulary_repo.count_vocabulary_grouped_by_date("2026-01-01")
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_count_vocabulary_grouped_by_date_with_data(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test count grouped by date with data"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        result = vocabulary_repo.count_vocabulary_grouped_by_date("2026-01-01")
        
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0][1] >= 1  # total count


class TestVocabularyRepositoryExists:
    """Tests for exists operation"""

    def test_exists_returns_true_for_existing_vocabulary(
        self,
        vocabulary_repo: VocabularyRepository,
        sample_vocabulary_base_model: Vocabulary
    ) -> None:
        """Test that exists returns True for existing vocabulary"""
        vocabulary_repo.create(sample_vocabulary_base_model)
        
        exists = vocabulary_repo.exists(word="serendipity")
        
        assert exists is True

    def test_exists_returns_false_for_nonexistent_vocabulary(
        self,
        vocabulary_repo: VocabularyRepository
    ) -> None:
        """Test that exists returns False for non-existent vocabulary"""
        exists = vocabulary_repo.exists(word="nonexistent")
        
        assert exists is False
