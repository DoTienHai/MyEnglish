class Vocabulary:
    def __init__(self, 
                 id: int, 
                 word: str, 
                 part_of_speech: str, 
                 meaning: str, 
                 description: str, 
                 example: str, 
                 correct_count: int, 
                 wrong_count: int, 
                 created_at: str):
        self.id = id
        self.word = word
        self.part_of_speech = part_of_speech
        self.meaning = meaning
        self.description = description
        self.example = example
        self.correct_count = correct_count
        self.wrong_count = wrong_count
        self.created_at = created_at
        
    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "part_of_speech": self.part_of_speech,
            "meaning": self.meaning,
            "description": self.description,
            "example": self.example,
            "correct_count": self.correct_count,
            "wrong_count": self.wrong_count,
            "created_at": self.created_at
        }   
        
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            word=data.get("word"),
            part_of_speech=data.get("part_of_speech"),
            meaning=data.get("meaning"),
            description=data.get("description"),
            example=data.get("example"),
            correct_count=data.get("correct_count"),
            wrong_count=data.get("wrong_count"),
            created_at=data.get("created_at")
        )
        
    def to_row(self):
        return [
            self.id,
            self.word,
            self.part_of_speech,
            self.meaning,
            self.description,
            self.example,
            self.correct_count,
            self.wrong_count,
            self.created_at
        ]
        
    def __repr__(self):
        return f"Vocabulary(id={self.id}, word='{self.word}', part_of_speech='{self.part_of_speech}', meaning='{self.meaning}', correct_count={self.correct_count}, wrong_count={self.wrong_count}, created_at='{self.created_at}')"