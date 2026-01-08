import random
from enum import Enum
from shared.observer_base import ObserverBase
from service.vocabulary_service import VocabularyService
from model.vocabulary import Vocabulary

class VOCABULARY_STEP(Enum):
    QUESTION = 1
    ANSWER_RESULT = 2

class VocabularyViewModel:
    def __init__(self, vocabulary_service:VocabularyService):
        self.vocabulary_service = vocabulary_service
        self.step = ObserverBase(VOCABULARY_STEP.QUESTION)
        self.current_vocabulary = self.vocabulary_service.random_vocabulary()
        self.current_answers = self.get_answers()
    
    def switch_step(self, new_step: VOCABULARY_STEP):
        self.step.value = new_step
        self.step.notify(new_step)
    
    def next(self):
        self.current_vocabulary = self.vocabulary_service.random_vocabulary()
        self.current_answers = self.get_answers()
        self.switch_step(VOCABULARY_STEP.QUESTION)
        
    def get_answers(self) -> list[str]:
        correct = self.current_vocabulary.meaning

        wrong_meanings = set()

        while len(wrong_meanings) < 3:
            vocab = self.vocabulary_service.random_vocabulary()
            if vocab.meaning != correct:
                wrong_meanings.add(vocab.meaning)

        answers = list(wrong_meanings) + [correct]
        random.shuffle(answers)
        return answers
    def check_answer(self, selected_meaning: str) -> bool:
        if selected_meaning == self.current_vocabulary.meaning:
            self.vocabulary_service.update_vocabulary(self.current_vocabulary.id, 
                                                      correct_count = self.current_vocabulary.correct_count + 1,
                                                      wrong_count = self.current_vocabulary.wrong_count)
        else:
            self.vocabulary_service.update_vocabulary(self.current_vocabulary.id, 
                                                      correct_count = self.current_vocabulary.correct_count,
                                                      wrong_count = self.current_vocabulary.wrong_count + 1)
        self.switch_step(VOCABULARY_STEP.ANSWER_RESULT)