"""Unit tests for shared text utilities"""
import pytest
from shared.text_utils import split_into_sentences


class TestSplitIntoSentences:
    """Tests for split_into_sentences function"""

    def test_split_single_sentence_with_period(self) -> None:
        """Test splitting a single sentence ending with period"""
        text = "This is a sentence."
        result = split_into_sentences(text)
        expected = ["This is a sentence."]
        
        assert result == expected

    def test_split_single_sentence_with_question_mark(self) -> None:
        """Test splitting a single sentence ending with question mark"""
        text = "Is this a question?"
        result = split_into_sentences(text)
        expected = ["Is this a question?"]
        
        assert result == expected

    def test_split_single_sentence_with_exclamation(self) -> None:
        """Test splitting a single sentence ending with exclamation mark"""
        text = "This is amazing!"
        result = split_into_sentences(text)
        expected = ["This is amazing!"]
        
        assert result == expected

    def test_split_multiple_sentences_with_period(self) -> None:
        """Test splitting multiple sentences separated by periods"""
        text = "First sentence. Second sentence. Third sentence."
        result = split_into_sentences(text)
        expected = ["First sentence.", "Second sentence.", "Third sentence."]
        
        assert result == expected

    def test_split_mixed_punctuation(self) -> None:
        """Test splitting sentences with mixed punctuation marks"""
        text = "Is this a question? Yes, it is! Absolutely."
        result = split_into_sentences(text)
        expected = ["Is this a question?", "Yes, it is!", "Absolutely."]
        
        assert result == expected

    def test_split_with_multiple_spaces(self) -> None:
        """Test splitting sentences separated by multiple spaces"""
        text = "First sentence.   Second sentence.    Third sentence."
        result = split_into_sentences(text)
        expected = ["First sentence.", "Second sentence.", "Third sentence."]
        
        assert result == expected

    def test_split_with_newlines(self) -> None:
        """Test splitting sentences separated by newlines"""
        text = "First sentence.\nSecond sentence.\nThird sentence."
        result = split_into_sentences(text)
        expected = ["First sentence.", "Second sentence.", "Third sentence."]
        
        assert result == expected

    def test_split_with_mixed_whitespace(self) -> None:
        """Test splitting sentences with mixed spaces and newlines"""
        text = "First sentence. \n Second sentence.  \n Third sentence."
        result = split_into_sentences(text)
        expected = ["First sentence.", "Second sentence.", "Third sentence."]
        
        assert result == expected

    def test_split_with_leading_whitespace(self) -> None:
        """Test that leading whitespace is stripped"""
        text = "  \n  First sentence. Second sentence."
        result = split_into_sentences(text)
        expected = ["First sentence.", "Second sentence."]
        
        assert result == expected

    def test_split_with_trailing_whitespace(self) -> None:
        """Test that trailing whitespace is stripped"""
        text = "First sentence. Second sentence.  \n  "
        result = split_into_sentences(text)
        expected = ["First sentence.", "Second sentence."]
        
        assert result == expected

    def test_split_empty_string(self) -> None:
        """Test splitting an empty string"""
        text = ""
        result = split_into_sentences(text)
        expected = []
        
        assert result == expected

    def test_split_whitespace_only_string(self) -> None:
        """Test splitting a string with only whitespace"""
        text = "   \n\n   \t  "
        result = split_into_sentences(text)
        expected = []
        
        assert result == expected

    def test_split_single_word(self) -> None:
        """Test splitting a single word without punctuation"""
        text = "Hello"
        result = split_into_sentences(text)
        expected = ["Hello"]
        
        assert result == expected

    def test_split_removes_empty_sentences(self) -> None:
        """Test that empty sentences are filtered out"""
        text = "First.   .   Second."
        result = split_into_sentences(text)
        
        # All results should be non-empty strings
        assert all(sentence.strip() for sentence in result)
        assert len(result) >= 1

    def test_split_sentence_with_numbers_and_decimals(self) -> None:
        """Test sentences with numbers and decimals"""
        text = "The price is $49.99. Items cost $10.50."
        result = split_into_sentences(text)
        expected = ["The price is $49.99.", "Items cost $10.50."]
        
        assert result == expected

    def test_split_long_text(self) -> None:
        """Test splitting a longer text with multiple sentences"""
        text = (
            "Learning English is important. It opens many doors. "
            "Many people speak English around the world! "
            "Are you ready to start? Yes, let's begin!"
        )
        result = split_into_sentences(text)
        expected = [
            "Learning English is important.",
            "It opens many doors.",
            "Many people speak English around the world!",
            "Are you ready to start?",
            "Yes, let's begin!"
        ]
        
        assert result == expected

    def test_split_returns_list_of_strings(self) -> None:
        """Test that function returns list of strings"""
        text = "First. Second. Third."
        result = split_into_sentences(text)
        
        # Verify type
        assert isinstance(result, list)
        assert all(isinstance(s, str) for s in result)

    def test_split_preserves_sentence_content(self) -> None:
        """Test that sentence content is preserved correctly"""
        original = "The quick brown fox jumps. Over the lazy dog!"
        result = split_into_sentences(original)
        expected = ["The quick brown fox jumps.", "Over the lazy dog!"]
        
        assert result == expected

    def test_split_handles_unicode_characters(self) -> None:
        """Test splitting sentences with unicode characters"""
        text = "Xin chào. Bạn khỏe không? Tôi rất vui!"
        result = split_into_sentences(text)
        expected = ["Xin chào.", "Bạn khỏe không?", "Tôi rất vui!"]
        
        assert result == expected

    def test_split_sentence_with_hyphenated_words(self) -> None:
        """Test sentences containing hyphenated words"""
        text = "This is a self-contained sentence. Another one-word example."
        result = split_into_sentences(text)
        expected = ["This is a self-contained sentence.", "Another one-word example."]
        
        assert result == expected

    def test_split_paragraph_format(self) -> None:
        """Test splitting paragraph-style text"""
        paragraph = (
            "This is the first sentence. This is the second.\n"
            "This starts a new line. And this continues it!"
        )
        result = split_into_sentences(paragraph)
        expected = [
            "This is the first sentence.",
            "This is the second.",
            "This starts a new line.",
            "And this continues it!"
        ]
        
        assert result == expected
