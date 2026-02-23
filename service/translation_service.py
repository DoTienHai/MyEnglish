import os
import json
import time
import threading as _threading
from enum import Enum
from googletrans import Translator
from google.oauth2 import service_account
from google.cloud import translate_v3 as translate


class TranslationErrorMessage(str, Enum):
    """Translation error status messages"""
    GOOGLE_CLOUD_FAILED = "[Google cloud: Translation failed]"
    GOOGLETRANS_FAILED = "[Googletrans: Translation failed]"

class TranslationService:
    """Singleton: 1 instance, 2 backends (Google Cloud or googletrans)"""
    
    _instance = None
    _lock = None
    _project_id = None
    _key_path = None
    _use_google_cloud = False
    _translate_cloud = None
    _googletrans = None

    def __new__(cls, key_path=None):
        """Singleton: create once, reuse next time (thread-safe)"""
        if cls._lock is None:
            cls._lock = _threading.Lock()
        
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if cls._key_path is None:
                        cls._key_path = key_path
                    cls._instance = super(TranslationService, cls).__new__(cls)
                    cls._instance._initialize(cls._key_path)
        
        return cls._instance

    def _initialize(self, key_path=None):
        """Setup backend: Google Cloud or googletrans (free)"""
        if type(self)._key_path is None:
            type(self)._key_path = key_path
        
        # No key: use googletrans
        if type(self)._key_path is None:
            print("[TranslationService] Using googletrans (free)")
            type(self)._googletrans = Translator()
            type(self)._use_google_cloud = False
            return
        
        # Has key: try Google Cloud
        try:
            if os.path.exists(type(self)._key_path):
                credentials = service_account.Credentials.from_service_account_file(
                    type(self)._key_path
                )
                pid = self._get_project_id_from_json(type(self)._key_path)
                type(self)._project_id = pid
                self.project_id = pid
                type(self)._translate_cloud = translate.TranslationServiceClient(
                    credentials=credentials
                )
                type(self)._use_google_cloud = True
                print("[TranslationService] Using Google Cloud")
            else:
                raise FileNotFoundError(f"Key not found: {type(self)._key_path}")
        except Exception as e:
            print(f"[TranslationService] Google Cloud failed: {e}")
            print("[TranslationService] Fallback to googletrans")
            type(self)._googletrans = Translator()
            type(self)._use_google_cloud = False

    def _get_project_id_from_json(self, key_path):
        """Extract project_id from JSON credentials"""
        with open(key_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("project_id")

    @classmethod
    def get_project_id(cls):
        """Return cached project_id (or None)"""
        return cls._project_id

    def _translate_google_cloud(self, text, retries=3):
        """Google Cloud Translation API (retry 3 times)"""
        parent = f"projects/{self.project_id}/locations/global"
        
        for attempt in range(retries):
            try:
                response = type(self)._translate_cloud.translate_text(
                    request={
                        "parent": parent,
                        "contents": [text],
                        "mime_type": "text/plain",
                        "source_language_code": "en",
                        "target_language_code": "vi",
                    }
                )
                return response.translations[0].translated_text
            except Exception as e:
                print(f"Error attempt {attempt+1}: {e}")
                time.sleep(1)
        
        return TranslationErrorMessage.GOOGLE_CLOUD_FAILED.value

    def _translate_googletrans(self, text, retries=3):
        """Googletrans free translation (retry 3 times)"""
        for attempt in range(retries):
            try:
                result = type(self)._googletrans.translate(text, dest='vi')
                return result.text
            except Exception as e:
                print(f"Error attempt {attempt+1}: {e}")
                time.sleep(1)
        
        return TranslationErrorMessage.GOOGLETRANS_FAILED.value

    def translate_eng_to_vn(self, text, retries=3):
        """Translate EN→VI: choose Google Cloud or googletrans"""
        if type(self)._use_google_cloud:
            return self._translate_google_cloud(text, retries)
        else:
            return self._translate_googletrans(text, retries)

if __name__ == "__main__":  # pragma: no cover
    translator = TranslationService("gg_cloud_key.json")
    ret = translator.translate_eng_to_vn(
        "A human cell swarms with trillions of molecules, including some 42 million proteins and a plethora of carbohydrates, lipids, and nucleic acids."
    )
    print(ret)
