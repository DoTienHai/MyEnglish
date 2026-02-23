class Paragraph:
    def __init__(self, 
                 id: int, 
                 title: str, 
                 input_paragraph: str, 
                 reference: str, 
                 machine_translation: str, 
                 completed: float, 
                 score: float, 
                 created_at: str):
        # Validate critical fields
        if not isinstance(title, str):
            raise TypeError(
                f"Title must be a string, got {type(title).__name__}"
            )
        
        if not title or not title.strip():
            raise ValueError(
                "Title cannot be empty"
            )
        
        if not isinstance(input_paragraph, str):
            raise TypeError(
                f"Input paragraph must be a string, got {type(input_paragraph).__name__}"
            )
        
        if not input_paragraph or not input_paragraph.strip():
            raise ValueError(
                "Input paragraph cannot be empty"
            )
        
        self.id = id
        self.title = title.strip()
        self.input_paragraph = input_paragraph.strip()
        self.reference = reference
        self.machine_translation = machine_translation
        
        # Initialize private attributes for validation
        self._completed = None
        self._score = None
        
        # Use property setters to trigger validation
        self.completed = completed
        self.score = score
        self.created_at = created_at
    
    @property
    def completed(self) -> float:
        """Completion percentage (0-100)
        
        Returns:
            float: Completion percentage
        """
        return self._completed
    
    @completed.setter
    def completed(self, value: float) -> None:
        """Validate and set completion percentage
        
        Args:
            value: Completion percentage (must be 0-100)
            
        Raises:
            TypeError: If value is not numeric
            ValueError: If value is outside valid range [0, 100]
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Completed must be numeric, got {type(value).__name__}"
            )
        
        if value < 0:
            raise ValueError(
                f"Completed percentage cannot be negative: {value}. "
                f"Must be between 0 and 100."
            )
        
        if value > 100:
            raise ValueError(
                f"Completed percentage cannot exceed 100: {value}. "
                f"Must be between 0 and 100."
            )
        
        self._completed = float(value)
    
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
            "title": self.title,
            "input_paragraph": self.input_paragraph,
            "reference": self.reference,
            "machine_translation": self.machine_translation,
            "completed": self.completed,
            "score": self.score,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            input_paragraph=data.get("input_paragraph"),
            reference=data.get("reference"),
            machine_translation=data.get("machine_translation"),
            completed=data.get("completed"),
            score=data.get("score"),
            created_at=data.get("created_at")
        )
    
    def to_row(self):
        return [
            self.id,
            self.title,
            self.input_paragraph,
            self.reference,
            self.machine_translation,
            self.completed,
            self.score,
            self.created_at
        ]
