import threading
from enum import Enum
from model.sentence import Sentence
from service.paragraph_service import ParagraphService
from service.sentence_service import SentenceService
from service.vocabulary_service import VocabularyService
from service.translation_service import TranslationService
from service.scoring_service import ScoringService
from shared.observer_base import ObserverBase
from shared.text_utils import split_into_sentences
class TRANSLATE_PRACTICE_STEP(Enum):
    STEP_1_INPUT_TEXT = 1
    STEP_2_TRANSLATE_TEXT = 2
    STEP_3_REVIEW_TRANSLATION = 3
    LOADING = 4


class TranslatePracticeViewModel:
    def __init__(self, 
                 paragraph_service:ParagraphService,
                 sentence_service:SentenceService,
                 vocabulary_service:VocabularyService,
                 translator:TranslationService,
                 score_service:ScoringService,):
        
        self.paragraph_service = paragraph_service
        self.sentence_service = sentence_service
        self.vocabulary_service = vocabulary_service
        self.translator = translator
        self.score_service = score_service
        
        self.step = ObserverBase(TRANSLATE_PRACTICE_STEP.STEP_1_INPUT_TEXT)
        self.step_1_done = threading.Event()
        
        self.title = ""
        self.input_text = ""
        self.ref_source = ""
        self.paragraph_id = None
        
        self.text_translated_by_translator = ""
        self.input_sentences = []
        self.sentences_translated_by_translator = []
        self.sentence_translations = []
        self.new_words = []
        self.scores = []
    
    def load_paragraph(self, paragraph_id: int):
        paragraph = self.paragraph_service.get_paragraph_by_id(paragraph_id)
        if paragraph is None:
            return False
        self.title = paragraph.title
        self.input_text = paragraph.input_paragraph
        self.ref_source = paragraph.reference
        self.paragraph_id = paragraph.id
        self.input_sentences = [sentence.input_sentence for sentence in self.sentence_service.get_sentences_by_paragraph_id(paragraph_id)]
        self.sentences_translated_by_translator = [sentence.machine_translation for sentence in self.sentence_service.get_sentences_by_paragraph_id(paragraph_id)]
        self.sentence_translations = [sentence.user_translation for sentence in self.sentence_service.get_sentences_by_paragraph_id(paragraph_id)]
        self.step_1_done.set()
        return True

    def switch_step(self, new_step: TRANSLATE_PRACTICE_STEP):
        self.step.value = new_step
        self.step.notify(new_step)
        
    def handle_step_1(self, title: str, ref_source: str, input_text: str, ):
        self.step_1_done.clear()
        self.title = title
        self.ref_source = ref_source
        self.input_text = input_text
        # Add paragraph to database
        self.paragraph_id = self.paragraph_service.create_paragraph(title, input_text, ref_source)
        # Split into sentences
        self.input_sentences = split_into_sentences(input_text)
        self.switch_step(TRANSLATE_PRACTICE_STEP.STEP_2_TRANSLATE_TEXT)
        # TODO: Research and implement data management and error handling for threaded operations
        def handling():
            # Translate full text and sentences, update translations to database 
            self.text_translated_by_translator = self.translator.translate_eng_to_vn(input_text)
            self.paragraph_service.update_paragraph(paragraph_id=self.paragraph_id, machine_translation=self.text_translated_by_translator)
            for sentence_index, sentence in enumerate(self.input_sentences, start=1):
                sentence_translation = self.translator.translate_eng_to_vn(sentence)
                self.sentences_translated_by_translator.append(sentence_translation)
                self.sentence_service.create_sentence(paragraph_id=self.paragraph_id, 
                                                      sentence_index=sentence_index, 
                                                      input_sentence=sentence, 
                                                      machine_translation=sentence_translation)
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
        for idx, translation in enumerate(self.sentence_translations, start=1):
            if translation.strip() == "" or translation is None:
                un_complete += 1
                score = 0
            else:
                score = self.score_service.score(translation, self.sentences_translated_by_translator[idx-1])
            self.scores.append(score)
            sentence = self.sentence_service.get_sentence_by_paragraph_and_index(self.paragraph_id, idx)
            self.sentence_service.update_sentence(sentence_id=sentence.id, user_translation=translation, score=score)
        paragraph_scored = round(sum(self.scores)/len(self.scores), 2)
        paragraph_complete = round((len(self.input_sentences) - un_complete)*100/len(self.input_sentences) , 2)
        self.paragraph_service.update_paragraph(paragraph_id=self.paragraph_id, score=paragraph_scored, completed=paragraph_complete)
        return self.scores

    def process_new_words(self):
        for idx, new_words in enumerate(self.new_words, start=1):
            sentence_example = self.input_sentences[idx-1]
            for new_word in new_words.split(","):
                new_word = new_word.strip()
                if new_word.strip() == "" or new_word is None:
                    continue
                vi_meaning = self.translator.translate_eng_to_vn(new_word)
                self.vocabulary_service.create_vocabulary(word=new_word, part_of_speech="", vi_meaning=vi_meaning, eng_description="", example=sentence_example, note="")
                
        
    def handle_step_3(self):
        # reset all data
        self.step_1_done.clear()
        self.title = ""
        self.input_text = ""
        self.ref_source = ""
        self.paragraph_id = None
        self.text_translated_by_translator = ""
        self.input_sentences.clear()
        self.sentences_translated_by_translator.clear()
        self.sentence_translations.clear()
        self.new_words.clear()
        self.scores.clear()
        self.switch_step(TRANSLATE_PRACTICE_STEP.STEP_1_INPUT_TEXT)
    
        