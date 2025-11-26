import re
import threading
from model.db_manager import DatabaseManager
from service.translator import TranslationService
from service.scored import *

class TranslatePracticeController:
    def __init__(self):
        self.translator = TranslationService()
        self.db_manager = DatabaseManager()
        
        self.session_id = None
        self.title = None
        self.ref_source = None
        self.input_text = None
        self.input_translated = None
        self.session_completed = False
        
        self.sentences_id = []
        self.sentences = []
        self.user_translations = []
        self.cloud_translations = []  
        self.scores = []
        self.new_words = []
    
    def process_input(self, title:str, ref_source:str,input_text:str):
        self.title = title
        self.ref_source = ref_source
        self.input_text = input_text
        
        self.session_id = self.db_manager.create_session(self.title, self.input_text, self.ref_source)
        split_input = re.split(r'(?<=[.!?])[\s\n]+', self.input_text.strip())
        for sentence in split_input:
            sentence = sentence.strip()
            if not sentence:
                continue
            self.sentences.append(sentence)
            
        def _translate_input_text(input_text):
            self.input_translated = self.translator.translate_eng_to_vn(input_text)
            self.db_manager.update_session(session_id=self.session_id, translated_text=self.input_translated)
        threading.Thread(target=_translate_input_text, args=(input_text,)).start()
        
        def _translate_sentences(sentences):
            for sentence_index, sentence in enumerate(sentences, start=1):
                cloud_translation = self.translator.translate_eng_to_vn(sentence, free=True)
                self.cloud_translations.append(cloud_translation)
                sentence_id = self.db_manager.create_sentence(session_id=self.session_id, sentence_index=sentence_index, source_sentence=sentence)
                self.sentences_id.append(sentence_id)
                self.db_manager.update_sentence(sentence_id=sentence_id,cloud_translation=cloud_translation)
        threading.Thread(target=_translate_sentences, args=(self.sentences,)).start()
        return self.sentences
        
    def get_sentences(self):
        return self.sentences    
    
    def number_of_sentences(self):
        return len(self.sentences)
    
    def get_cloud_translations(self):
        return self.cloud_translations
    
    def process_translations(self, translations:list[str]):
        self.user_translations = translations
        un_complete = 0
        for idx, translation in enumerate(translations, start=1):
            if translation.strip() == "" or translation is None:
                un_complete += 1
                score = 0
            else:
                score = scored(translation, self.cloud_translations[idx-1])
            self.scores.append(score)
            self.db_manager.update_sentence(sentence_id=self.sentences_id[idx-1],translation_sentence=translation, score=score)
        session_scored = round(sum(self.scores)/len(self.scores), 2)
        session_complete = round((self.number_of_sentences() - un_complete)*100/self.number_of_sentences() , 2)
        self.db_manager.update_session(session_id=self.session_id, score=session_scored, completed=session_complete)
        return self.scores

    def get_user_translations(self):
        return self.user_translations
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
                word_id = self.db_manager.create_vocabulary(word=new_word)
                self.db_manager.update_vocabulary(vocab_id=word_id, example=sentence_example, meaning=meaning)
            self.new_words.append(new_words_in_sentence)
        return self.new_words
# The sun was setting behind the mountains, casting a golden glow across the valley. Birds chirped softly as they returned to their nests. A gentle breeze rustled the leaves, carrying the scent of blooming flowers. In the distance, a small river reflected the fading light, shimmering like liquid gold.
# Mặt trời đang lặt phía sau những ngọn núi, ánh sáng vàng đang trải dài khắp thung lũng.


# ở khoảng cách này, một dòng sông nhỏ đã phản chiếu ánh sáng mờ, óng ánh như một chất lỏng vàng.
        
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
    