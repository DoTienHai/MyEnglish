"""Unit tests for TranslationService"""
import pytest
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from service.translation_service import TranslationService, TranslationErrorMessage


class TestTranslationServiceSingleton:
    """Tests for Singleton pattern"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_singleton_instance_is_same(self) -> None:
        """Test that multiple calls return the same instance"""
        translator1 = TranslationService()
        translator2 = TranslationService()
        
        assert translator1 is translator2

    def test_singleton_with_key_path(self) -> None:
        """Test singleton with key path"""
        with patch('service.translation_service.os.path.exists', return_value=False):
            translator1 = TranslationService("fake_key.json")
            translator2 = TranslationService("different_key.json")
            
            # Should return same instance
            assert translator1 is translator2

    def test_singleton_thread_safe(self) -> None:
        """Test that singleton is thread-safe"""
        import threading
        
        instances = []
        
        def create_instance():
            translator = TranslationService()
            instances.append(translator)
        
        threads = [threading.Thread(target=create_instance) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All instances should be the same
        assert all(inst is instances[0] for inst in instances)


class TestTranslationServiceInitialization:
    """Tests for TranslationService initialization"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_init_without_key_uses_googletrans(self) -> None:
        """Test initialization without key uses googletrans"""
        translator = TranslationService()
        
        assert TranslationService._use_google_cloud is False
        assert TranslationService._googletrans is not None

    @patch('service.translation_service.os.path.exists', return_value=False)
    def test_init_with_nonexistent_key_uses_googletrans(self, mock_exists) -> None:
        """Test initialization with non-existent key falls back to googletrans"""
        translator = TranslationService("fake_key.json")
        
        assert TranslationService._use_google_cloud is False
        assert TranslationService._googletrans is not None

    @patch('service.translation_service.service_account.Credentials.from_service_account_file')
    @patch('service.translation_service.os.path.exists', return_value=True)
    def test_init_with_valid_key_uses_google_cloud(self, mock_exists, mock_creds) -> None:
        """Test initialization with valid key uses Google Cloud"""
        mock_credentials = MagicMock()
        mock_creds.return_value = mock_credentials
        
        key_content = {"project_id": "test-project"}
        m = mock_open(read_data=json.dumps(key_content))
        
        with patch('builtins.open', m):
            with patch('service.translation_service.translate.TranslationServiceClient'):
                TranslationService._instance = None
                TranslationService._lock = None
                TranslationService._key_path = None
                
                translator = TranslationService("valid_key.json")
        
        assert TranslationService._use_google_cloud is True

    @patch('service.translation_service.os.path.exists', return_value=True)
    def test_init_with_invalid_key_falls_back_to_googletrans(self, mock_exists) -> None:
        """Test initialization with invalid key falls back to googletrans"""
        m = mock_open(read_data="invalid json{")
        
        with patch('builtins.open', m):
            TranslationService._instance = None
            TranslationService._lock = None
            TranslationService._key_path = None
            
            translator = TranslationService("invalid_key.json")
        
        assert TranslationService._use_google_cloud is False
        assert TranslationService._googletrans is not None


class TestGetProjectId:
    """Tests for get_project_id classmethod"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_get_project_id_without_key(self) -> None:
        """Test get_project_id returns None when no key is set"""
        translator = TranslationService()
        project_id = TranslationService.get_project_id()
        
        assert project_id is None

    @patch('service.translation_service.service_account.Credentials.from_service_account_file')
    @patch('service.translation_service.os.path.exists', return_value=True)
    def test_get_project_id_with_key(self, mock_exists, mock_creds) -> None:
        """Test get_project_id returns correct project_id"""
        mock_credentials = MagicMock()
        mock_creds.return_value = mock_credentials
        
        key_content = {"project_id": "my-test-project"}
        m = mock_open(read_data=json.dumps(key_content))
        
        with patch('builtins.open', m):
            with patch('service.translation_service.translate.TranslationServiceClient'):
                TranslationService._instance = None
                TranslationService._lock = None
                TranslationService._key_path = None
                
                translator = TranslationService("valid_key.json")
        
        project_id = TranslationService.get_project_id()
        assert project_id == "my-test-project"


class TestGetProjectIdFromJson:
    """Tests for _get_project_id_from_json method"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_get_project_id_from_json_valid(self) -> None:
        """Test extracting project_id from valid JSON"""
        translator = TranslationService()
        
        key_content = {"project_id": "my-project", "other": "value"}
        m = mock_open(read_data=json.dumps(key_content))
        
        with patch('builtins.open', m):
            project_id = translator._get_project_id_from_json("test.json")
        
        assert project_id == "my-project"

    def test_get_project_id_from_json_missing_project_id(self) -> None:
        """Test extracting project_id when key is missing"""
        translator = TranslationService()
        
        key_content = {"other": "value"}
        m = mock_open(read_data=json.dumps(key_content))
        
        with patch('builtins.open', m):
            project_id = translator._get_project_id_from_json("test.json")
        
        assert project_id is None


class TestTranslateEnglishToVietnamese:
    """Tests for translate_eng_to_vn method"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_translate_with_googletrans_backend(self) -> None:
        """Test translation using googletrans backend"""
        translator = TranslationService()
        
        # Mock googletrans
        mock_result = MagicMock()
        mock_result.text = "Xin chào thế giới"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Hello world")
        
        assert result == "Xin chào thế giới"

    def test_translate_with_googletrans_success(self) -> None:
        """Test successful translation with googletrans"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Cảm ơn bạn"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Thank you")
        
        assert isinstance(result, str)
        assert len(result) > 0

    @patch('service.translation_service.service_account.Credentials.from_service_account_file')
    @patch('service.translation_service.os.path.exists', return_value=True)
    def test_translate_with_google_cloud_backend(self, mock_exists, mock_creds) -> None:
        """Test translation using Google Cloud backend"""
        mock_credentials = MagicMock()
        mock_creds.return_value = mock_credentials
        
        key_content = {"project_id": "test-project"}
        m = mock_open(read_data=json.dumps(key_content))
        
        # Mock Google Cloud response
        mock_response = MagicMock()
        mock_response.translations = [MagicMock(translated_text="Xin chào")]
        
        with patch('builtins.open', m):
            with patch('service.translation_service.translate.TranslationServiceClient') as mock_client:
                mock_instance = MagicMock()
                mock_instance.translate_text = MagicMock(return_value=mock_response)
                mock_client.return_value = mock_instance
                
                TranslationService._instance = None
                TranslationService._lock = None
                TranslationService._key_path = None
                
                translator = TranslationService("valid_key.json")
                
                # Override to use mocked client
                TranslationService._translate_cloud = mock_instance
                TranslationService._use_google_cloud = True
                
                result = translator.translate_eng_to_vn("Hello")
        
        assert isinstance(result, str)

    def test_translate_googletrans_retry_on_failure(self) -> None:
        """Test that googletrans retries on failure"""
        translator = TranslationService()
        
        # First call fails, second succeeds
        mock_result = MagicMock()
        mock_result.text = "Thành công"
        TranslationService._googletrans.translate = MagicMock(
            side_effect=[Exception("Error"), mock_result]
        )
        
        with patch('time.sleep'):
            result = translator.translate_eng_to_vn("Success")
        
        # Should still return the result from retry
        assert result == "Thành công"

    def test_translate_googletrans_max_retries_exceeded(self) -> None:
        """Test handling when all retries are exhausted"""
        translator = TranslationService()
        
        TranslationService._googletrans.translate = MagicMock(
            side_effect=Exception("Persistent error")
        )
        
        with patch('time.sleep'):
            result = translator.translate_eng_to_vn("Test")
        
        assert result == TranslationErrorMessage.GOOGLETRANS_FAILED.value

    def test_translate_returns_string(self) -> None:
        """Test that translate always returns a string"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Kết quả"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Result")
        
        assert isinstance(result, str)

    def test_translate_with_custom_retries(self) -> None:
        """Test translate with custom retry count"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Kết quả"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Test", retries=5)
        
        assert isinstance(result, str)

    @patch('service.translation_service.service_account.Credentials.from_service_account_file')
    @patch('service.translation_service.os.path.exists', return_value=True)
    def test_translate_google_cloud_max_retries_exceeded(self, mock_exists, mock_creds) -> None:
        """Test Google Cloud translation when all retries are exhausted"""
        mock_credentials = MagicMock()
        mock_creds.return_value = mock_credentials
        
        key_content = {"project_id": "test-project"}
        m = mock_open(read_data=json.dumps(key_content))
        
        with patch('builtins.open', m):
            with patch('service.translation_service.translate.TranslationServiceClient') as mock_client:
                mock_instance = MagicMock()
                mock_instance.translate_text = MagicMock(side_effect=Exception("API Error"))
                mock_client.return_value = mock_instance
                
                TranslationService._instance = None
                TranslationService._lock = None
                TranslationService._key_path = None
                
                translator = TranslationService("valid_key.json")
                TranslationService._translate_cloud = mock_instance
                TranslationService._use_google_cloud = True
                
                with patch('time.sleep'):
                    result = translator.translate_eng_to_vn("Test")
        
        assert result == TranslationErrorMessage.GOOGLE_CLOUD_FAILED.value


class TestIntegration:
    """Integration tests for TranslationService"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_translate_english_sentence(self) -> None:
        """Test translation of English sentence"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Đây là một câu tiếng Anh"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("This is an English sentence")
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_translate_long_paragraph(self) -> None:
        """Test translation of longer text"""
        translator = TranslationService()
        
        long_text = "The quick brown fox jumps over the lazy dog. " * 5
        
        mock_result = MagicMock()
        mock_result.text = "Con cáo nâu nhanh nhảy qua con chó lười biếng. " * 5
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn(long_text)
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_translate_special_characters(self) -> None:
        """Test translation with special characters"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Xin chào! Bạn khỏe không?"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Hello! How are you?")
        
        assert isinstance(result, str)

    def test_multiple_translations_use_same_instance(self) -> None:
        """Test that multiple translations use same translator instance"""
        translator1 = TranslationService()
        translator2 = TranslationService()
        
        assert translator1 is translator2
        
        mock_result = MagicMock()
        mock_result.text = "Kết quả"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result1 = translator1.translate_eng_to_vn("Result 1")
        result2 = translator2.translate_eng_to_vn("Result 2")
        
        assert result1 == "Kết quả"
        assert result2 == "Kết quả"


class TestEdgeCases:
    """Tests for edge cases"""

    def setup_method(self):
        """Reset singleton before each test"""
        TranslationService._instance = None
        TranslationService._lock = None
        TranslationService._project_id = None
        TranslationService._key_path = None
        TranslationService._use_google_cloud = False
        TranslationService._translate_cloud = None
        TranslationService._googletrans = None

    def test_translate_empty_string(self) -> None:
        """Test translation of empty string"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = ""
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("")
        
        assert isinstance(result, str)

    def test_translate_only_spaces(self) -> None:
        """Test translation of only spaces"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "   "
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("   ")
        
        assert isinstance(result, str)

    def test_translate_with_numbers(self) -> None:
        """Test translation with numbers"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Năm số 2024"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Year 2024")
        
        assert isinstance(result, str)

    def test_translate_with_urls(self) -> None:
        """Test translation with URLs"""
        translator = TranslationService()
        
        mock_result = MagicMock()
        mock_result.text = "Truy cập https://example.com"
        TranslationService._googletrans.translate = MagicMock(return_value=mock_result)
        
        result = translator.translate_eng_to_vn("Visit https://example.com")
        
        assert isinstance(result, str)
