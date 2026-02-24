"""Unit tests for SentenceService"""
import pytest
from service.sentence_service import SentenceService
from service.paragraph_service import ParagraphService
from model.sentence import Sentence


class TestSentenceServiceCreate:
    """Tests for create_sentence operation"""

    def test_create_sentence_success(self) -> None:
        """Test creating a sentence successfully"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="This is a test."
        )
        
        sentence_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="This is a test.",
            machine_translation="Đây là một bài kiểm tra."
        )
        
        assert sentence_id is not None
        assert isinstance(sentence_id, int)
        assert sentence_id > 0

    def test_create_sentence_multiple_in_paragraph(self) -> None:
        """Test creating multiple sentences in same paragraph"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="First. Second. Third."
        )
        
        sent1_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="First.",
            machine_translation="Đầu tiên."
        )
        
        sent2_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=2,
            input_sentence="Second.",
            machine_translation="Thứ hai."
        )
        
        assert sent1_id != sent2_id
        assert sent1_id > 0
        assert sent2_id > 0

    def test_created_sentence_has_default_values(self) -> None:
        """Test that created sentence has correct default values"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="Test sentence."
        )
        
        sentence_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="Test sentence.",
            machine_translation="Câu test."
        )
        
        sentence = sentence_service.get_sentences_by_paragraph_id(paragraph_id)[0]
        
        assert sentence.user_translation == ""
        assert sentence.score == 0.0
        assert sentence.note == ""


class TestSentenceServiceUpdate:
    """Tests for update_sentence operation"""

    def setUp(self):
        """Set up test fixtures"""
        self.para_service = ParagraphService()
        self.sentence_service = SentenceService()

    def test_update_sentence_user_translation(self) -> None:
        """Test updating user translation"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="Test."
        )
        
        sentence_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="Test.",
            machine_translation="Kiểm tra."
        )
        
        sentence_service.update_sentence(
            sentence_id,
            user_translation="Bài kiểm tra."
        )
        
        sentences = sentence_service.get_sentences_by_paragraph_id(paragraph_id)
        assert sentences[0].user_translation == "Bài kiểm tra."

    def test_update_sentence_score(self) -> None:
        """Test updating sentence score"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="Test."
        )
        
        sentence_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="Test.",
            machine_translation="Kiểm tra."
        )
        
        sentence_service.update_sentence(sentence_id, score=8.5)
        
        sentences = sentence_service.get_sentences_by_paragraph_id(paragraph_id)
        assert sentences[0].score == 8.5

    def test_update_sentence_score_invalid_range(self) -> None:
        """Test that score must be between 0-10"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="Test."
        )
        
        sentence_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="Test.",
            machine_translation="Kiểm tra."
        )
        
        with pytest.raises(ValueError, match="score must be between 0-10"):
            sentence_service.update_sentence(sentence_id, score=15.0)

    def test_update_sentence_multiple_fields(self) -> None:
        """Test updating multiple sentence fields"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="Test."
        )
        
        sentence_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="Test.",
            machine_translation="Kiểm tra."
        )
        
        sentence_service.update_sentence(
            sentence_id,
            user_translation="Bài thi.",
            score=9.0,
            note="Good translation"
        )
        
        sentences = sentence_service.get_sentences_by_paragraph_id(paragraph_id)
        sentence = sentences[0]
        assert sentence.user_translation == "Bài thi."
        assert sentence.score == 9.0
        assert sentence.note == "Good translation"

    def test_update_nonexistent_sentence_raises_error(self) -> None:
        """Test that updating nonexistent sentence raises error"""
        sentence_service = SentenceService()
        
        with pytest.raises(ValueError, match="does not exist"):
            sentence_service.update_sentence(9999, user_translation="new")


class TestSentenceServiceRead:
    """Tests for read operations"""

    def test_get_sentences_by_paragraph_id(self) -> None:
        """Test retrieving sentences by paragraph ID"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="First. Second."
        )
        
        sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="First.",
            machine_translation="Thứ nhất."
        )
        
        sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=2,
            input_sentence="Second.",
            machine_translation="Thứ hai."
        )
        
        sentences = sentence_service.get_sentences_by_paragraph_id(paragraph_id)
        
        assert len(sentences) == 2
        assert all(isinstance(s, Sentence) for s in sentences)
        assert all(s.paragraph_id == paragraph_id for s in sentences)

    def test_get_sentence_by_paragraph_and_index(self) -> None:
        """Test retrieving sentence by paragraph ID and index"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="First. Second."
        )
        
        sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="First.",
            machine_translation="Thứ nhất."
        )
        
        sentence = sentence_service.get_sentence_by_paragraph_and_index(
            paragraph_id, 1
        )
        
        assert sentence is not None
        assert sentence.input_sentence == "First."

    def test_get_avg_score(self) -> None:
        """Test getting average sentence score"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="First. Second."
        )
        
        sent1_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=1,
            input_sentence="First.",
            machine_translation="Thứ nhất."
        )
        
        sent2_id = sentence_service.create_sentence(
            paragraph_id=paragraph_id,
            sentence_index=2,
            input_sentence="Second.",
            machine_translation="Thứ hai."
        )
        
        # Update scores
        sentence_service.update_sentence(sent1_id, score=8.0)
        sentence_service.update_sentence(sent2_id, score=6.0)
        
        avg_score = sentence_service.get_avg_score()
        
        assert avg_score is not None
        assert isinstance(avg_score, float)


class TestSentenceServiceCount:
    """Tests for count operations"""

    def test_count_sentences_by_paragraph_id(self) -> None:
        """Test counting sentences in a paragraph"""
        para_service = ParagraphService()
        sentence_service = SentenceService()
        
        paragraph_id = para_service.create_paragraph(
            title="Test",
            input_paragraph="First. Second. Third."
        )
        
        for i in range(1, 4):
            sentence_service.create_sentence(
                paragraph_id=paragraph_id,
                sentence_index=i,
                input_sentence=f"Sentence {i}",
                machine_translation=f"Câu {i}"
            )
        
        count = sentence_service.count_sentences_by_paragraph_id(paragraph_id)
        
        assert count == 3
        assert isinstance(count, int)

    def test_create_paragraph_empty_input_raises_error(self) -> None:
        """Test that creating paragraph with empty input_paragraph raises error"""
        para_service = ParagraphService()
        
        with pytest.raises(ValueError, match="Input paragraph cannot be empty"):
            para_service.create_paragraph(
                title="Empty",
                input_paragraph=""
            )
