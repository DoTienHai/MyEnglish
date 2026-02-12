"""Unit tests for SentenceRepository"""
from typing import List
import pytest
from repositories.sentence_repo import SentenceRepository
from repositories.paragraph_repo import ParagraphRepository
from model.sentence import Sentence
from model.paragraph import Paragraph


class TestSentenceRepositoryCreate:
    """Tests for create operation"""

    def test_create_sentence_success(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test creating a sentence successfully"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        
        assert sentence_id is not None
        assert isinstance(sentence_id, int)
        assert sentence_id > 0

    def test_created_sentence_can_be_retrieved(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test that created sentence can be retrieved"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        retrieved = sentence_repo.get(sentence_id)
        
        assert retrieved is not None
        assert retrieved.input_sentence == sample_sentence.input_sentence
        assert retrieved.user_translation == sample_sentence.user_translation
        assert retrieved.machine_translation == sample_sentence.machine_translation
        assert retrieved.score == sample_sentence.score

    def test_create_multiple_sentences(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test creating multiple sentences"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_id_1 = sentence_repo.create(sample_sentence)
        sentence_id_2 = sentence_repo.create(sample_sentence_2)
        
        assert sentence_id_1 is not None
        assert sentence_id_2 is not None
        assert sentence_id_1 != sentence_id_2

    def test_created_sentence_has_correct_fields(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test that created sentence has all correct fields"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        retrieved = sentence_repo.get(sentence_id)
        
        assert retrieved.paragraph_id == sample_sentence.paragraph_id
        assert retrieved.sentence_index == sample_sentence.sentence_index
        assert retrieved.input_sentence == sample_sentence.input_sentence
        assert retrieved.user_translation == sample_sentence.user_translation
        assert retrieved.machine_translation == sample_sentence.machine_translation
        assert retrieved.score == sample_sentence.score
        assert retrieved.note == sample_sentence.note


class TestSentenceRepositoryRead:
    """Tests for read operations"""

    def test_get_existing_sentence(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test getting an existing sentence"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        retrieved = sentence_repo.get(sentence_id)
        
        assert retrieved is not None
        assert isinstance(retrieved, Sentence)
        assert retrieved.id == sentence_id

    def test_get_nonexistent_sentence_returns_none(
        self,
        sentence_repo: SentenceRepository
    ) -> None:
        """Test getting a non-existent sentence returns None"""
        result = sentence_repo.get(9999)
        
        assert result is None

    def test_get_all_sentences_empty_database(
        self,
        sentence_repo: SentenceRepository
    ) -> None:
        """Test getting all sentences from empty database"""
        all_sentences = sentence_repo.all()
        
        assert isinstance(all_sentences, list)
        assert len(all_sentences) == 0

    def test_get_all_sentences_with_data(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test getting all sentences"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        all_sentences = sentence_repo.all()
        
        assert len(all_sentences) == 2
        assert all(isinstance(s, Sentence) for s in all_sentences)

    def test_get_by_paragraph_id_and_sentence_index(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test getting sentence by paragraph_id and sentence_index"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        
        retrieved = sentence_repo.get_by_paragraph_id_and_sentence_index(
            paragraph_id=1,
            sentence_index=1
        )
        
        assert retrieved is not None
        assert retrieved.paragraph_id == 1
        assert retrieved.sentence_index == 1

    def test_get_by_paragraph_id_and_sentence_index_not_found(
        self,
        sentence_repo: SentenceRepository
    ) -> None:
        """Test getting non-existent sentence by paragraph_id and sentence_index"""
        retrieved = sentence_repo.get_by_paragraph_id_and_sentence_index(
            paragraph_id=999,
            sentence_index=999
        )
        
        assert retrieved is None


class TestSentenceRepositoryUpdate:
    """Tests for update operations"""

    def test_update_sentence_translation(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test updating sentence translation"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        sentence = sentence_repo.get(sentence_id)
        
        sentence.user_translation = "Dịch mới của câu"
        sentence_repo.update(sentence)
        
        updated = sentence_repo.get(sentence_id)
        assert updated.user_translation == "Dịch mới của câu"

    def test_update_sentence_score(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test updating sentence score"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        sentence = sentence_repo.get(sentence_id)
        
        sentence.score = 0.75
        sentence_repo.update(sentence)
        
        updated = sentence_repo.get(sentence_id)
        assert updated.score == 0.75

    def test_update_sentence_note(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test updating sentence note"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        sentence = sentence_repo.get(sentence_id)
        
        sentence.note = "Updated note"
        sentence_repo.update(sentence)
        
        updated = sentence_repo.get(sentence_id)
        assert updated.note == "Updated note"

    def test_update_preserves_other_fields(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test that updating one field preserves other fields"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        sentence = sentence_repo.get(sentence_id)
        original_input = sentence.input_sentence
        
        sentence.score = 0.50
        sentence_repo.update(sentence)
        
        updated = sentence_repo.get(sentence_id)
        assert updated.input_sentence == original_input
        assert updated.score == 0.50


class TestSentenceRepositoryDelete:
    """Tests for delete operations"""

    def test_delete_existing_sentence(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test deleting an existing sentence"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_id = sentence_repo.create(sample_sentence)
        assert sentence_repo.get(sentence_id) is not None
        
        sentence_repo.delete(sentence_id)
        
        assert sentence_repo.get(sentence_id) is None

    def test_delete_nonexistent_sentence_does_not_raise(
        self,
        sentence_repo: SentenceRepository
    ) -> None:
        """Test that deleting non-existent sentence doesn't raise error"""
        # Should not raise exception
        sentence_repo.delete(9999)

    def test_delete_reduces_count(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test that deleting sentence reduces count"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        initial_count = sentence_repo.count_all()
        assert initial_count == 2
        
        all_sentences = sentence_repo.all()
        sentence_repo.delete(all_sentences[0].id)
        
        new_count = sentence_repo.count_all()
        assert new_count == 1


class TestSentenceRepositoryFilter:
    """Tests for filter operations"""

    def test_filter_by_paragraph_id(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test filtering sentences by paragraph_id"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        filtered = sentence_repo.filter(paragraph_id=1)
        
        assert len(filtered) == 2
        assert all(s.paragraph_id == 1 for s in filtered)

    def test_filter_by_sentence_index(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test filtering sentences by sentence_index"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        filtered = sentence_repo.filter(sentence_index=1)
        
        assert len(filtered) == 1
        assert filtered[0].sentence_index == 1

    def test_filter_returns_empty_list_when_no_match(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test that filter returns empty list when no match"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        
        filtered = sentence_repo.filter(paragraph_id=999)
        
        assert isinstance(filtered, list)
        assert len(filtered) == 0


class TestSentenceRepositoryCount:
    """Tests for count operations"""

    def test_count_all_empty_database(
        self,
        sentence_repo: SentenceRepository
    ) -> None:
        """Test count all on empty database"""
        count = sentence_repo.count_all()
        
        assert count == 0

    def test_count_all_with_data(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test count all with data"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        count = sentence_repo.count_all()
        
        assert count == 2

    def test_count_by_paragraph_id(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test count by paragraph_id"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        count = sentence_repo.count_by(paragraph_id=1)
        
        assert count == 2


class TestSentenceRepositoryAvgScore:
    """Tests for average score calculation"""

    def test_get_avg_score_empty_database(
        self,
        sentence_repo: SentenceRepository
    ) -> None:
        """Test getting average score from empty database"""
        avg_score = sentence_repo.get_avg_score()
        
        assert avg_score is None

    def test_get_avg_score_single_sentence(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence
    ) -> None:
        """Test getting average score with single sentence"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        
        avg_score = sentence_repo.get_avg_score()
        
        assert avg_score == 0.95

    def test_get_avg_score_multiple_sentences(
        self,
        paragraph_repo: ParagraphRepository,
        sentence_repo: SentenceRepository,
        sample_paragraph: Paragraph,
        sample_sentence: Sentence,
        sample_sentence_2: Sentence
    ) -> None:
        """Test getting average score with multiple sentences"""
        # Create paragraph first (foreign key requirement)
        paragraph_id = paragraph_repo.create(sample_paragraph)
        sample_sentence.paragraph_id = paragraph_id
        sample_sentence_2.paragraph_id = paragraph_id
        
        sentence_repo.create(sample_sentence)
        sentence_repo.create(sample_sentence_2)
        
        avg_score = sentence_repo.get_avg_score()
        
        # (0.95 + 0.88) / 2 = 0.915
        assert abs(avg_score - 0.915) < 0.001
