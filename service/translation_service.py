from google.cloud import translate_v3 as translate
from google.oauth2 import service_account
import json
import time
import os
from googletrans import Translator
import threading as _threading

class TranslationService:
    _instance = None
    _lock = None  # set later to avoid import-time threading if not needed
    _project_id = None
    _key_path = None
    _use_google_cloud = False
    _translate_cloud = None
    _googletrans = None

    def __new__(cls, key_path="gg_cloud_key.json"):
        # Lazy create a class-level lock
        if cls._lock is None:
            cls._lock = _threading.Lock()
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # Lock in the key_path on the first initialization
                    if cls._key_path is None:
                        cls._key_path = key_path
                    cls._instance = super(TranslationService, cls).__new__(cls)
                    cls._instance._initialize(cls._key_path)
        return cls._instance

    def _initialize(self, key_path="gg_cloud_key.json"):
        # Lock key_path at class-level if not set
        if type(self)._key_path is None:
            type(self)._key_path = key_path
        
        # Try to load Google Cloud credentials first
        try:
            if os.path.exists(type(self)._key_path):
                credentials = service_account.Credentials.from_service_account_file(type(self)._key_path)
                pid = self._get_project_id_from_json(type(self)._key_path)
                # Cache at class level
                type(self)._project_id = pid
                self.project_id = pid
                type(self)._translate_cloud = translate.TranslationServiceClient(credentials=credentials)
                type(self)._use_google_cloud = True
                print("[TranslationService] Using Google Cloud Translation")
            else:
                raise FileNotFoundError(f"Key file not found: {type(self)._key_path}")
        except Exception as e:
            # Fallback to googletrans
            print(f"[TranslationService] Google Cloud initialization failed: {e}")
            print("[TranslationService] Falling back to googletrans (free translation)")
            type(self)._googletrans = Translator()
            type(self)._use_google_cloud = False

    def _get_project_id_from_json(self, key_path):
        with open(key_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("project_id")

    @classmethod
    def get_project_id(cls):
        """Get cached project_id at class-level (may be None before first initialization)."""
        return cls._project_id

    def _translate_google_cloud(self, text, retries=3):
        """Translate using Google Cloud Translation API"""
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
                print(f"Translation error attempt {attempt+1}: {e}")
                time.sleep(1)
        return "[Translation failed]"

    def _translate_googletrans(self, text, retries=3):
        """Translate using googletrans (free translation)"""
        for attempt in range(retries):
            try:
                result = type(self)._googletrans.translate(text, dest_language='vi')
                return result.text
            except Exception as e:
                print(f"Translation error attempt {attempt+1}: {e}")
                time.sleep(1)
        return "[Translation failed]"

    def translate_eng_to_vn(self, text, retries=3):
        """Translate English to Vietnamese using configured provider"""
        if type(self)._use_google_cloud:
            return self._translate_google_cloud(text, retries)
        else:
            return self._translate_googletrans(text, retries)

if __name__ == "__main__":
    translator = TranslationService("gg_cloud_key.json")

    ret = translator.translate_eng_to_vn(
        "A human cell swarms with trillions of molecules, including some 42 million proteins and a plethora of carbohydrates, lipids, and nucleic acids."
    )
    print(ret)
