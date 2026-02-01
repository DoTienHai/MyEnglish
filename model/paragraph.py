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
        self.id = id
        self.title = title
        self.input_paragraph = input_paragraph
        self.reference = reference
        self.machine_translation = machine_translation
        self.completed = completed
        self.score = score
        self.created_at = created_at
        
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
    
    def __repr__(self):
        return f"Paragraph(id={self.id}, title='{self.title}', completed={self.completed}, score={self.score}, created_at='{self.created_at}')"
