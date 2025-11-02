from googletrans import Translator

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_eng_to_vn(self, text : str) -> str:

        translation = self.translator.translate(text, src='en', dest='vi')
        return translation.text