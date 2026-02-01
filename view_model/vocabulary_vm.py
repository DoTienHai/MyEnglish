import random
from enum import Enum
from shared.observer_base import ObserverBase
from service.vocabulary_service import VocabularyService
from model.vocabulary import Vocabulary

NUMBER_OF_ANSWER_CHOICES = 4
NUMBER_OF_MINIMUM_VOCABULARY = 10
class VOCABULARY_STEP(Enum):
    NOT_ENOUGH_VOCABULARY = 0
    QUESTION = 1
    ANSWER_RESULT = 2

class VocabularyViewModel:
    def __init__(self, vocabulary_service:VocabularyService):
        self.vocabulary_service = vocabulary_service
        self.step = ObserverBase(VOCABULARY_STEP.QUESTION)
        self.current_vocabulary: Vocabulary = None
        self.current_answers: list[str] = []
        self.refresh()
    
    def switch_step(self, new_step: VOCABULARY_STEP):
        self.step.value = new_step
        self.step.notify(new_step)
    
    def get_answers(self) -> list[str]:
        correct = self.current_vocabulary.vi_meaning
        wrong_meanings = set()

        while len(wrong_meanings) < NUMBER_OF_ANSWER_CHOICES - 1:
            vocab = self.vocabulary_service.get_random_vocabulary()
            if vocab.vi_meaning != correct:
                wrong_meanings.add(vocab.vi_meaning)

        answers = list(wrong_meanings) + [correct]
        random.shuffle(answers)
        return answers
    
    def check_answer(self, selected_meaning: str) -> bool:
        if selected_meaning == self.current_vocabulary.vi_meaning:
            self.vocabulary_service.update_vocabulary(self.current_vocabulary.id, 
                                                      correct_count = self.current_vocabulary.correct_count + 1,
                                                      wrong_count = self.current_vocabulary.wrong_count)
        else:
            self.vocabulary_service.update_vocabulary(self.current_vocabulary.id, 
                                                      correct_count = self.current_vocabulary.correct_count,
                                                      wrong_count = self.current_vocabulary.wrong_count + 1)
        self.switch_step(VOCABULARY_STEP.ANSWER_RESULT) 
        
    def get_vocabulary_count(self) -> int:
        return self.vocabulary_service.total_vocabulary()

    def refresh(self):
        # check number of vocabulary entries in database, if less than 4, set step to NOT_ENOUGH_VOCABULARY
        if self.vocabulary_service.total_vocabulary() < NUMBER_OF_MINIMUM_VOCABULARY:
            self.switch_step(VOCABULARY_STEP.NOT_ENOUGH_VOCABULARY)
        else:
            self.current_vocabulary = self.vocabulary_service.get_random_vocabulary()
            self.current_answers = self.get_answers()
            self.switch_step(VOCABULARY_STEP.QUESTION)