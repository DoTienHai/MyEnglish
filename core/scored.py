from sentence_transformers import SentenceTransformer, util

# Load model đa ngôn ngữ (hỗ trợ tiếng Việt)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def scored(vn_sentence1, vn_sentence2, max_score=10):
    """
    So sánh 2 câu tiếng Việt và trả về điểm similarity
    max_score: số điểm tối đa
    """
    # Encode 2 câu thành embedding
    emb1 = model.encode(vn_sentence1, convert_to_tensor=True)
    emb2 = model.encode(vn_sentence2, convert_to_tensor=True)
    
    # Tính cosine similarity
    similarity = util.pytorch_cos_sim(emb1, emb2).item()  # giá trị 0→1
    
    # Quy đổi sang điểm (0 → max_score)
    score = round(similarity * max_score, 2)
    return score


if __name__ == "__main__":
    # Ví dụ
    import time
    cau1 = "Tôi thích lập trình."
    cau2 = "bạn không yêu lập trình."
    cau3 = "tôi không yêu lập trình"
    cau4 = "bạn thích lập trình"
    cau5 = "tôi thấy lập trình không khó lắm đâu"
    all_cau = [cau1, cau2, cau3, cau4, cau5]
    starts = time.time()
    for x in all_cau:
        for y in all_cau:
            print(f"{x} vs {y}: {scored(x, y)}. Thời gian: {round(time.time() - starts, 2)}s")
            starts = time.time()

