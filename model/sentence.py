class Sentence:
    def __init__(self,
            id: int,
            paragraph_id: int,
            sentence_index: int,
            input_sentence: str,
            user_translation: str,
            machine_translation: str,
            score: float,
            note: str,
            created_at: str):
        # Validate critical fields
        if not isinstance(paragraph_id, int):
            raise TypeError(
                f"Paragraph ID must be an integer, got {type(paragraph_id).__name__}"
            )
        
        if paragraph_id <= 0:
            raise ValueError(
                f"Paragraph ID must be positive: {paragraph_id}"
            )
        
        if not isinstance(sentence_index, int):
            raise TypeError(
                f"Sentence index must be an integer, got {type(sentence_index).__name__}"
            )
        
        if sentence_index < 0:
            raise ValueError(
                f"Sentence index cannot be negative: {sentence_index}"
            )
        
        if not isinstance(input_sentence, str):
            raise TypeError(
                f"Input sentence must be a string, got {type(input_sentence).__name__}"
            )
        
        if not input_sentence or not input_sentence.strip():
            raise ValueError(
                "Input sentence cannot be empty"
            )
        
        self.id = id
        self.paragraph_id = paragraph_id
        self.sentence_index = sentence_index
        self.input_sentence = input_sentence.strip()
        self.user_translation = user_translation
        self.machine_translation = machine_translation
        
        # Initialize private attribute for validation
        self._score = None
        
        # Use property setter to trigger validation
        self.score = score
        self.note = note
        self.created_at = created_at
    
    @property
    def score(self) -> float:
        """Score value (0-10)
        
        Returns:
            float: Score value
        """
        return self._score
    
    @score.setter
    def score(self, value: float) -> None:
        """Validate and set score
        
        Args:
            value: Score value (must be 0-10)
            
        Raises:
            TypeError: If value is not numeric
            ValueError: If value is outside valid range [0, 10]
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Score must be numeric, got {type(value).__name__}"
            )
        
        if value < 0:
            raise ValueError(
                f"Score cannot be negative: {value}. "
                f"Must be between 0 and 10."
            )
        
        if value > 10:
            raise ValueError(
                f"Score cannot exceed 10: {value}. "
                f"Must be between 0 and 10."
            )
        
        self._score = float(value)

    def to_dict(self):
        return {
            "id": self.id,
            "paragraph_id": self.paragraph_id,
            "sentence_index": self.sentence_index,
            "input_sentence": self.input_sentence,
            "user_translation": self.user_translation,
            "machine_translation": self.machine_translation,
            "score": self.score,
            "note": self.note,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            paragraph_id=data.get("paragraph_id"),
            sentence_index=data.get("sentence_index"),
            input_sentence=data.get("input_sentence"),
            user_translation=data.get("user_translation"),
            machine_translation=data.get("machine_translation"),
            score=data.get("score"),
            note=data.get("note"),
            created_at=data.get("created_at")
        )

    def to_row(self):
        return [
            self.id,
            self.paragraph_id,
            self.sentence_index,
            self.input_sentence,
            self.user_translation,
            self.machine_translation,
            self.score,
            self.note,
            self.created_at
        ]