from googletrans import Translator
from google.cloud import translate_v2 as translate
import time


class TranslationService:
    def __init__(self):
        self.translator_free = Translator()
        self.translate_cloud = translate.Client.from_service_account_json("gg_cloud_key.json")

    def translate_eng_to_vn(self, text, free=True, retries=3):
            for attempt in range(retries):
                try:
                    if free:
                        return self.translator_free.translate(text, src='en', dest='vi').text
                    else:
                        print("cloud translator")
                        return self.translate_cloud.translate(text, source_language='en',target_language='vi')["translatedText"]
                except Exception as e:
                    print(f"Lỗi dịch lần {attempt+1}: {e}")
                    time.sleep(1)  # đợi 1s rồi thử lại
            return "[Translation failed]"

if __name__ == "__main__":
    translator =TranslationService()
    ret = translator.translate_eng_to_vn("A human cell swarms with trillions of molecules, including some 42 million proteins and a plethora of carbohydrates, lipids, and nucleic acids.", free=False)
    print(ret)