class Session:
    def __init__(self, 
                 id: int, 
                 title: str, 
                 source_text: str, 
                 source_reference: str, 
                 translated_text: str, 
                 completed: float, 
                 score: float, 
                 created_at: str):
        self.id = id
        self.title = title
        self.source_text = source_text
        self.source_reference = source_reference
        self.translated_text = translated_text
        self.completed = completed
        self.score = score
        self.created_at = created_at
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "source_text": self.source_text,
            "source_reference": self.source_reference,
            "translated_text": self.translated_text,
            "completed": self.completed,
            "score": self.score,
            "created_at": self.created_at
        }
        
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            source_text=data.get("source_text"),
            source_reference=data.get("source_reference"),
            translated_text=data.get("translated_text"),
            completed=data.get("completed"),
            score=data.get("score"),
            created_at=data.get("created_at")
        )
        
    def to_row(self):
        return [
            self.id,
            self.title,
            self.source_text,
            self.source_reference,
            self.translated_text,
            self.completed,
            self.score,
            self.created_at
        ]
        
    def __repr__(self):
        return f"Session(id={self.id}, title='{self.title}', completed={self.completed}, score={self.score}, created_at='{self.created_at}')"