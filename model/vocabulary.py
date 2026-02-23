class Vocabulary:
    def __init__(self, 
                 id: int, 
                 word: str, 
                 part_of_speech: str, 
                 vi_meaning: str, 
                 eng_description: str, 
                 example: str, 
                 note: str,
                 correct_count: int, 
                 wrong_count: int, 
                 created_at: str):
        # Validate critical fields
        if not isinstance(word, str):
            raise TypeError(
                f"Word must be a string, got {type(word).__name__}"
            )
        
        if not word or not word.strip():
            raise ValueError(
                "Word cannot be empty"
            )
        
        self.id = id
        self.word = word.strip()
        self.part_of_speech = part_of_speech
        self.vi_meaning = vi_meaning
        self.eng_description = eng_description
        self.example = example
        self.note = note
        
        # Initialize private attributes for validation
        self._correct_count = None
        self._wrong_count = None
        
        # Use property setters to trigger validation
        self.correct_count = correct_count
        self.wrong_count = wrong_count
        self.created_at = created_at
    
    @property
    def correct_count(self) -> int:
        """Number of correct answers (>= 0)
        
        Returns:
            int: Correct count
        """
        return self._correct_count
    
    @correct_count.setter
    def correct_count(self, value: int) -> None:
        """Validate and set correct count
        
        Args:
            value: Correct count (must be >= 0)
            
        Raises:
            TypeError: If value is not an integer
            ValueError: If value is negative
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Correct count must be an integer, got {type(value).__name__}"
            )
        
        if value < 0:
            raise ValueError(
                f"Correct count cannot be negative: {value}. "
                f"Must be >= 0."
            )
        
        self._correct_count = value
    
    @property
    def wrong_count(self) -> int:
        """Number of wrong answers (>= 0)
        
        Returns:
            int: Wrong count
        """
        return self._wrong_count
    
    @wrong_count.setter
    def wrong_count(self, value: int) -> None:
        """Validate and set wrong count
        
        Args:
            value: Wrong count (must be >= 0)
            
        Raises:
            TypeError: If value is not an integer
            ValueError: If value is negative
        """
        if not isinstance(value, int):
            raise TypeError(
                f"Wrong count must be an integer, got {type(value).__name__}"
            )
        
        if value < 0:
            raise ValueError(
                f"Wrong count cannot be negative: {value}. "
                f"Must be >= 0."
            )
        
        self._wrong_count = value
        
    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "part_of_speech": self.part_of_speech,
            "vi_meaning": self.vi_meaning,
            "eng_description": self.eng_description,
            "example": self.example,
            "note": self.note,
            "correct_count": self.correct_count,
            "wrong_count": self.wrong_count,
            "created_at": self.created_at
        }   
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            word=data.get("word"),
            part_of_speech=data.get("part_of_speech"),
            vi_meaning=data.get("vi_meaning"),
            eng_description=data.get("eng_description"),
            example=data.get("example"),
            note=data.get("note"),
            correct_count=data.get("correct_count"),
            wrong_count=data.get("wrong_count"),
            created_at=data.get("created_at")
        )
        
    def to_row(self):
        return [
            self.id,
            self.word,
            self.part_of_speech,
            self.vi_meaning,
            self.eng_description,
            self.example,
            self.note,
            self.correct_count,
            self.wrong_count,
            self.created_at
        ]