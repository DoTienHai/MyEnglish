import re
import threading
from core.db_manager import DatabaseManager
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
        self.scores = []
        self.cloud_translations = []  
        self.new_words = []
    
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
    
    def number_of_sentences(self):
        return len(self.sentences)
    
    def get_cloud_translations(self):
        return self.cloud_translations
    
    def process_translations(self, translations:list[str]):
        for idx, translation in enumerate(translations, start=1):
            score = scored(translation, self.cloud_translations[idx-1])
            self.scores.append(score)
            self.db_manager.update_sentence(session_id=self.session_id, sentence_id=idx, translation=translation, score=score)
        self.db_manager.update_score_session(self.session_id, round(sum(self.scores)/len(self.scores), 2))
        return self.scores

    def get_scores(self):
        return self.scores

    def process_new_words(self, new_word_list:list[list[str]]):
        for idx, new_words in enumerate(new_word_list, start=1):
            sentence_example = self.sentences[idx-1]
            new_words_in_sentence = [] 
            for new_word in new_words.split(","):
                new_word = new_word.strip()
                if new_word.strip() == "" or new_word is None:
                    continue
                new_words_in_sentence.append(new_word)
                meaning = self.translator.translate_eng_to_vn(new_word, free=True)
                self.db_manager.add_vocabulary(word=new_word, example=sentence_example, meaning=meaning)
            self.new_words.append(new_words_in_sentence)
    
    # def auto_translate_sentences(self):
    #     for idx, sentence in enumerate(self.sentences, start=1):
    #         translated = self.translator.translate_eng_to_vn(sentence, free=True)
    #         self.db_manager.update_translation(session_id=self.session_id, index=idx,
    #                                            cloud_translation=translated)
         
        
if __name__ == "__main__":
    db = DatabaseManager(db_path="data\\app_data.db")
    input_text = "Fueled by sugar and caffeine, Cairo is a late-night city, and the energy in both its ancient heart and wealthy ‘New’ Cairo is boundless. A city with layers of history; the top drawcards are its most ancient: the Nile River and the Pyramids of Giza, which have towered over this frenetic megalopolis for millennia. And documented stories of Egypt’s empires and eras are on display in a collection of museums spearheaded by the new Grand Egyptian Museum. Our essential guide will help you plan your trip to Cairo to see the highly anticipated museum."
    controller = TranslatePracticeController()
    controller.process_input("test", "test", input_text)
    sentences = controller.sentences
    new_words = [["wealthy"], ["drawcards", "towered", "frenetic", "megalopolis"], ["essential", "anticipated"]]
    print(controller.cloud_translations)
    controller.process_translations(sentences)
    controller.process_new_words(new_words)
    