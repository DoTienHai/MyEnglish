class Sentence:
    def __init__(self,
            id: int,
            session_id: int,
            sentence_index: int,
            source_sentence: str,
            translated_sentence: str,
            cloud_translated_sentence: str,
            score: float,
            note: str,
            created_at: str):
        self.id = id
        self.session_id = session_id
        self.sentence_index = sentence_index
        self.source_sentence = source_sentence
        self.translated_sentence = translated_sentence
        self.cloud_translated_sentence = cloud_translated_sentence
        self.score = score
        self.note = note
        self.created_at = created_at

        
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "sentence_index": self.sentence_index,
            "source_sentence": self.source_sentence,
            "translated_sentence": self.translated_sentence,
            "cloud_translated_sentence": self.cloud_translated_sentence,
            "score": self.score,
            "note": self.note,
            "created_at": self.created_at
        }
        
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            session_id=data.get("session_id"),
            sentence_index=data.get("sentence_index"),
            source_sentence=data.get("source_sentence"),
            translated_sentence=data.get("translated_sentence"),
            cloud_translated_sentence=data.get("cloud_translated_sentence"),
            score=data.get("score"),
            note=data.get("note"),
            created_at=data.get("created_at")
        )
        
    def to_row(self):
        return [
            self.id,
            self.session_id,
            self.sentence_index,
            self.source_sentence,
            self.translated_sentence,
            self.cloud_translated_sentence,
            self.score,
            self.note,
            self.created_at
        ]
    
    
    def __repr__(self):
        return f"<Sentence id={self.id} session_id={self.session_id} sentence_index={self.sentence_index}>"