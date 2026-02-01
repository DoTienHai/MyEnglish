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
        self.id = id
        self.paragraph_id = paragraph_id
        self.sentence_index = sentence_index
        self.input_sentence = input_sentence
        self.user_translation = user_translation
        self.machine_translation = machine_translation
        self.score = score
        self.note = note
        self.created_at = created_at

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

    def __repr__(self):
        return f"<Sentence id={self.id} paragraph_id={self.paragraph_id} sentence_index={self.sentence_index}>"