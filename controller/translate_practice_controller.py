import re
import threading
from core.sqlite3 import DatabaseManager
from core.translator import TranslationService
from core.scored import *

class TranslatePracticeController:
    def __init__(self):
        self.translator = TranslationService()
        self.db_manager = DatabaseManager()
        self.title = None
        self.ref_source = None
        self.input_text = None
        self.session_id = None
        self.sentences = []
        self.cloud_translations = []  
    
    def process_input(self, title:str, ref_source:str,input_text:str):
        self.title = title
        self.ref_source = ref_source
        self.input_text = input_text

        self.session_id = self.db_manager.add_session(self.title, self.input_text, self.ref_source)
        split_input = re.split(r'(?<=[.!?])\s+', self.input_text.strip())
        count = 0
        for sentence in split_input:
            sentence = sentence.strip()
            if not sentence:
                continue
            count += 1
            self.sentences.append(sentence)
            cloud_translation = self.translator.translate_eng_to_vn(sentence, free=True)
            self.cloud_translations.append(cloud_translation)
            
            self.db_manager.add_sentence(session_id=self.session_id, sentence_index=count, source=sentence, cloud_translation=cloud_translation)
            
        return self.sentences
        
    def get_sentences(self):
        return self.sentences    
    
    def get_cloud_translations(self):
        return self.cloud_translations
    
    def process_translations(self, translations:list[str], new_words:list):
        scores = []
        for idx, translation in enumerate(translations, start=1):
            print(translation, self.cloud_translations[idx-1])
            score = scored(translation, self.cloud_translations[idx-1])
            scores.append(score)
            self.db_manager.update_sentence(session_id=self.session_id, sentence_id=idx, translation=translation, score=score)
        return scores
        # for idx, new_word in enumerate(new_words, start=1):
        #     self.db_manager.add_vocabulary(session_id=self.session_id, sentence_id=idx, note=new_word)
    
    # def auto_translate_sentences(self):
    #     for idx, sentence in enumerate(self.sentences, start=1):
    #         translated = self.translator.translate_eng_to_vn(sentence, free=True)
    #         self.db_manager.update_translation(session_id=self.session_id, index=idx,
    #                                            cloud_translation=translated)
         
        
    