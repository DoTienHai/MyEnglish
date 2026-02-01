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
        self.id = id
        self.word = word
        self.part_of_speech = part_of_speech
        self.vi_meaning = vi_meaning
        self.eng_description = eng_description
        self.example = example
        self.note = note
        self.correct_count = correct_count
        self.wrong_count = wrong_count
        self.created_at = created_at
        
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
        
    def __repr__(self):
        return f"Vocabulary(id={self.id}, word='{self.word}', part_of_speech='{self.part_of_speech}', vi_meaning='{self.vi_meaning}', correct_count={self.correct_count}, wrong_count={self.wrong_count}, created_at='{self.created_at}')"