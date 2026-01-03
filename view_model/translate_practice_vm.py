import threading
from enum import Enum
from service.session_service import SessionService
from service.sentence_service import SentenceService
from service.vocabulary_service import VocabularyService
from service.translation_service import TranslationService
from service.scoring_service import ScoringService
from shared.observer_base import ObserverBase
class TRANSLATE_PRACTICE_STEP(Enum):
    STEP_1_INPUT_TEXT = 1
    STEP_2_TRANSLATE_TEXT = 2
    STEP_3_REVIEW_TRANSLATION = 3
    LOADING = 4


class TranslatePracticeViewModel:
    def __init__(self, 
                 session_service:SessionService,
                 sentence_service:SentenceService,
                 vocabulary_service:VocabularyService,
                 translator:TranslationService,
                 score_service:ScoringService,):
        
        self.session_service = session_service
        self.sentence_service = sentence_service
        self.vocabulary_service = vocabulary_service
        self.translator = translator
        self.score_service = score_service
        
        self.step = ObserverBase(TRANSLATE_PRACTICE_STEP.STEP_1_INPUT_TEXT)
        self.step_1_done = threading.Event()
        
        self.title = ""
        self.input_text = ""
        self.ref_source = ""
        self.session_id = None
        
        self.text_translated_by_translator = ""
        self.input_sentences = []
        self.sentences_translated_by_translator = []
        self.sentence_translations = []
        self.new_words = []
        
    def switch_step(self, new_step: TRANSLATE_PRACTICE_STEP):
        self.step.value = new_step
        self.step.notify(new_step)
        
    def handle_step_1(self, title: str, ref_source: str, input_text: str, ):
        self.step_1_done.clear()
        self.title = title
        self.ref_source = ref_source
        self.input_text = input_text
        # add session to db
        self.session_id = self.session_service.create_session(title, input_text, ref_source)
        # split into sentences
        self.input_sentences = self.sentence_service.split_into_sentences(input_text) 
        self.switch_step(TRANSLATE_PRACTICE_STEP.STEP_2_TRANSLATE_TEXT)
        # cần nghiên cứu và triển khai các biện pháp quản lý data và lỗi trong khi chạy thread
        def handling():
            # translate full text and sentences. update translations to db 
            self.text_translated_by_translator = self.translator.translate_eng_to_vn(input_text)
            self.session_service.update_session(session_id=self.session_id, translated_text=self.text_translated_by_translator)
            for sentence_index, sentence in enumerate(self.input_sentences, start=1):
                sentence_translation = self.translator.translate_eng_to_vn(sentence)
                self.sentences_translated_by_translator.append(sentence_translation)
                self.sentence_service.create_sentence(session_id=self.session_id, 
                                                      sentence_index=sentence_index, 
                                                      source_sentence=sentence, 
                                                      cloud_translation=sentence_translation)
            self.step_1_done.set()
        threading.Thread(target=handling, args=()).start()
        
    def handle_step_2(self, sentence_translations: list[str], new_words_list: list[str]):
        if self.step_1_done.is_set() == False:
            self.switch_step(TRANSLATE_PRACTICE_STEP.LOADING)
            self.step_1_done.wait()
        self.sentence_translations = sentence_translations
        self.new_words = new_words_list
        self.switch_step(TRANSLATE_PRACTICE_STEP.LOADING)
        self.process_translations()
        self.process_new_words()
        self.switch_step(TRANSLATE_PRACTICE_STEP.STEP_3_REVIEW_TRANSLATION)
        
    def process_translations(self):
        un_complete = 0
        scores = []
        for idx, translation in enumerate(self.sentence_translations, start=1):
            if translation.strip() == "" or translation is None:
                un_complete += 1
                score = 0
            else:
                score = self.score_service.score(translation, self.sentences_translated_by_translator[idx-1])
            scores.append(score)
            self.sentence_service.update_sentence(sentence_id=idx-1,translated_sentence=translation, score=score)
        session_scored = round(sum(scores)/len(scores), 2)
        session_complete = round((len(self.input_sentences) - un_complete)*100/len(self.input_sentences) , 2)
        self.session_service.update_session(session_id=self.session_id, score=session_scored, completed=session_complete)
        return scores

    def process_new_words(self):
        for idx, new_words in enumerate(self.new_words, start=1):
            sentence_example = self.input_sentences[idx-1]
            for new_word in new_words.split(","):
                new_word = new_word.strip()
                if new_word.strip() == "" or new_word is None:
                    continue
                meaning = self.translator.translate_eng_to_vn(new_word)
                self.vocabulary_service.create_vocabulary(word=new_word, part_of_speech="", meaning=meaning, description="", example=sentence_example)
                
        
    def handle_step_3(self):
        # reset all data
        self.step_1_done.clear()
        self.title = ""
        self.input_text = ""
        self.ref_source = ""
        self.session_id = None
        self.text_translated_by_translator = ""
        self.input_sentences = []
        self.sentences_translated_by_translator = []
        self.sentence_translations = []
        self.new_words = []
        self.switch_step(TRANSLATE_PRACTICE_STEP.STEP_1_INPUT_TEXT)
    
        