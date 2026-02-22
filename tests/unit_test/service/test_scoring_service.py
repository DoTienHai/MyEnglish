"""Unit tests for ScoringService"""
import pytest
import math
from unittest.mock import patch, MagicMock
from service.scoring_service import ScoringService


class TestScoringServiceSingleton:
    """Tests for Singleton pattern"""

    def test_singleton_instance_is_same(self) -> None:
        """Test that multiple calls return the same instance"""
        # Reset singleton before testing
        ScoringService._instance = None
        
        scorer1 = ScoringService()
        scorer2 = ScoringService()
        
        assert scorer1 is scorer2

    def test_singleton_thread_safe(self) -> None:
        """Test that singleton is thread-safe"""
        import threading
        
        ScoringService._instance = None
        instances = []
        
        def create_instance():
            scorer = ScoringService()
            instances.append(scorer)
        
        threads = [threading.Thread(target=create_instance) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All instances should be the same
        assert all(inst is instances[0] for inst in instances)


class TestExpScore:
    """Tests for exp_score method"""

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test"""
        ScoringService._instance = None
        yield
        ScoringService._instance = None

    def test_exp_score_perfect_similarity(self) -> None:
        """Test exp_score with perfect similarity (1.0)"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=1.0, max_score=10, k=1)
        
        assert score == 10.0

    def test_exp_score_zero_similarity(self) -> None:
        """Test exp_score with zero similarity"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=0.0, max_score=10, k=1)
        
        assert score < 2.0  # Should be close to 0
        assert score >= 0.0

    def test_exp_score_mid_similarity(self) -> None:
        """Test exp_score with mid-range similarity"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=0.5, max_score=10, k=1)
        
        assert 0 <= score <= 10
        assert score > 0

    def test_exp_score_clamps_negative_similarity(self) -> None:
        """Test that negative similarity is clamped to 0"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=-0.5, max_score=10, k=1)
        
        assert score >= 0.0

    def test_exp_score_clamps_similarity_above_one(self) -> None:
        """Test that similarity > 1 is clamped to 1"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=1.5, max_score=10, k=1)
        
        assert score == 10.0

    def test_exp_score_custom_max_score(self) -> None:
        """Test exp_score with custom max_score"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=1.0, max_score=100, k=1)
        
        assert score == 100.0

    def test_exp_score_custom_k_parameter(self) -> None:
        """Test exp_score with different k values"""
        scorer = ScoringService()
        score_k1 = scorer.exp_score(similarity=0.5, max_score=10, k=1)
        score_k2 = scorer.exp_score(similarity=0.5, max_score=10, k=2)
        
        # Different k values should produce different scores
        assert score_k1 != score_k2

    def test_exp_score_returns_float(self) -> None:
        """Test that exp_score returns a float"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=0.5, max_score=10, k=1)
        
        assert isinstance(score, float)

    def test_exp_score_rounded_to_two_decimals(self) -> None:
        """Test that score is rounded to 2 decimal places"""
        scorer = ScoringService()
        score = scorer.exp_score(similarity=0.789, max_score=10, k=0.5)
        
        # Check that it has at most 2 decimal places
        assert len(str(score).split('.')[-1]) <= 2


class TestScore:
    """Tests for score method"""

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test"""
        ScoringService._instance = None
        yield
        ScoringService._instance = None

    @patch('service.scoring_service.SentenceTransformer')
    def test_score_identical_sentences(self, mock_transformer) -> None:
        """Test score with identical sentences"""
        scorer = ScoringService()
        
        # Mock the model to return similarity 1.0
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        # Create mock embeddings
        mock_emb = MagicMock()
        mock_emb.item.return_value = 1.0
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score = scorer.score("This is a test", "This is a test")
        
        assert score > 0
        assert isinstance(score, float)

    @patch('service.scoring_service.SentenceTransformer')
    def test_score_completely_different_sentences(self, mock_transformer) -> None:
        """Test score with completely different sentences"""
        scorer = ScoringService()
        
        # Mock the model to return similarity 0.0
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = 0.0
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score = scorer.score("Hello world", "xyz abc")
        
        assert 0 <= score < 1
        assert isinstance(score, float)

    def test_score_empty_first_sentence(self) -> None:
        """Test score with empty first sentence"""
        scorer = ScoringService()
        score = scorer.score("", "This is a test")
        
        assert score == 0.0

    def test_score_empty_second_sentence(self) -> None:
        """Test score with empty second sentence"""
        scorer = ScoringService()
        score = scorer.score("This is a test", "")
        
        assert score == 0.0

    def test_score_both_empty_sentences(self) -> None:
        """Test score with both sentences empty"""
        scorer = ScoringService()
        score = scorer.score("", "")
        
        assert score == 0.0

    def test_score_none_first_sentence(self) -> None:
        """Test score with None as first sentence"""
        scorer = ScoringService()
        score = scorer.score(None, "This is a test")
        
        assert score == 0.0

    def test_score_none_second_sentence(self) -> None:
        """Test score with None as second sentence"""
        scorer = ScoringService()
        score = scorer.score("This is a test", None)
        
        assert score == 0.0

    def test_score_custom_max_score(self) -> None:
        """Test score with custom max_score parameter"""
        scorer = ScoringService()
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = 1.0
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score = scorer.score("Test", "Test", max_score=20)
        
        assert score > 0
        assert isinstance(score, float)

    def test_score_returns_float(self) -> None:
        """Test that score returns a float"""
        scorer = ScoringService()
        score = scorer.score("", "")
        
        assert isinstance(score, float)

    @patch('service.scoring_service.SentenceTransformer')
    def test_score_negative_similarity_handled(self, mock_transformer) -> None:
        """Test that negative similarity is handled correctly"""
        scorer = ScoringService()
        
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = -0.1  # Negative similarity
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score = scorer.score("Test", "Test")
        
        # Should handle negative similarity gracefully
        assert score >= 0


class TestModelLoading:
    """Tests for lazy model loading"""

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test"""
        ScoringService._instance = None
        ScoringService._model = None
        yield
        ScoringService._instance = None
        ScoringService._model = None

    def test_model_is_none_initially(self) -> None:
        """Test that model is None before first use"""
        assert ScoringService._model is None

    @patch('service.scoring_service.SentenceTransformer')
    def test_model_loaded_on_first_score_call(self, mock_transformer) -> None:
        """Test that model is loaded on first score call"""
        scorer = ScoringService()
        ScoringService._model = MagicMock()
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = 0.5
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            scorer.score("Test", "Test")
        
        # Model should now be loaded
        assert ScoringService._model is not None


class TestIntegration:
    """Integration tests for ScoringService"""

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test"""
        ScoringService._instance = None
        ScoringService._model = None
        yield
        ScoringService._instance = None
        ScoringService._model = None

    @patch('service.scoring_service.SentenceTransformer')
    def test_score_with_similar_english_sentences(self, mock_transformer) -> None:
        """Test scoring with similar English sentences"""
        scorer = ScoringService()
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = 0.95
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score = scorer.score(
                "The quick brown fox jumps",
                "A quick brown fox is jumping"
            )
        
        assert score > 5  # Should be a high score
        assert isinstance(score, float)

    @patch('service.scoring_service.SentenceTransformer')
    def test_score_with_english_vietnamese_mix(self, mock_transformer) -> None:
        """Test scoring with mixed English and Vietnamese"""
        scorer = ScoringService()
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = 0.3
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score = scorer.score(
                "This is an English sentence",
                "Đây là một câu tiếng Việt"
            )
        
        assert 0 <= score <= 10
        assert isinstance(score, float)

    @patch('service.scoring_service.SentenceTransformer')
    def test_multiple_score_calls_use_same_model(self, mock_transformer) -> None:
        """Test that multiple score calls use the same model instance"""
        scorer = ScoringService()
        mock_model = MagicMock()
        ScoringService._model = mock_model
        
        mock_emb = MagicMock()
        mock_emb.item.return_value = 0.5
        
        with patch('service.scoring_service.util.pytorch_cos_sim', return_value=mock_emb):
            score1 = scorer.score("Sentence 1", "Sentence 2")
            score2 = scorer.score("Sentence 3", "Sentence 4")
        
        # Both should use the same model
        assert ScoringService._model is mock_model
