import math
import threading
from sentence_transformers import SentenceTransformer, util

class ScoringService:
    _instance = None
    _lock = threading.Lock()
    _model = None
    _model_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ScoringService, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            with cls._model_lock:
                if cls._model is None:
                    cls._model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        return cls._model

    def exp_score(self, similarity, max_score=10, k=1):
        """
        similarity: giá trị từ 0 -> 1
        max_score: điểm tối đa
        k: độ cong của hàm exponential
        """
        # giới hạn similarity trong [0,1]
        if similarity < 0:
            similarity = 0
        if similarity > 1:
            similarity = 1

        # tính score theo công thức chuẩn hóa exponential
        normalized = (math.exp(k * similarity) - 1) / (math.exp(k) - 1)
        score = round(normalized * max_score, 2)
        return score

    def score(self, sentence1: str, sentence2: str, max_score=10) -> float:
        """
        Trả về điểm similarity giữa 2 câu (0 → max_score)
        """
        if not sentence1 or not sentence2:
            return 0.0

        model = type(self)._get_model()
        emb1 = model.encode(sentence1, convert_to_tensor=True)
        emb2 = model.encode(sentence2, convert_to_tensor=True)

        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        # print(f"Sentence 1: {sentence1}\nSentence 2: {sentence2}\nSimilarity: {similarity}")Nước được tạo thành từ hydro và oxy.
        score = self.exp_score(similarity=max(similarity, 0), max_score=max_score, k=0.25)
        # score = similarity
        return score



if __name__ == "__main__":
    scorer = ScoringService()
    sentence_a = "This is a test sentence."
    sentence_b = "Đây là 1 câu thử."
    sentence_c = "This is my test sentence."
    sentence_d = "Đây là câu thử của tôi."
    
    score = scorer.score(sentence_a, sentence_b, max_score=10)
    print(f"Score between sentences: {score}")
    score_similar = scorer.score(sentence_a, sentence_c, max_score=10)
    print(f"Score between similar sentences: {score_similar}")
    score_similar_vn = scorer.score(sentence_b, sentence_d, max_score=10)
    print(f"Score between similar Vietnamese sentences: {score_similar_vn}")

