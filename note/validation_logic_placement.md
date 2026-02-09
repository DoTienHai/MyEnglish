# Ghi chú: Nơi Đặt Validation Logic trong Kiến Trúc MVCS

## Câu Hỏi
Trong class Repository có vẻ chưa check các điều kiện hợp lệ để đưa vào database. Phần logic này nên được để ở đâu?

## 📌 Câu Trả Lời: SERVICE LAYER

Validation logic **NÊN ĐẶT Ở SERVICE LAYER**, không phải ở Repository.

---

## 🏗️ Dòng Dữ Liệu Trong MVCS:

```
UI/View
  ↓
ViewModel (định dạng dữ liệu, truy vấn service)
  ↓
Service (✅ VALIDATION & Business Logic)  ← Kiểm tra điều kiện hợp lệ
  ↓
Repository (chỉ CRUD)  ← Không kiểm tra, chỉ lưu trữ dữ liệu
  ↓
Database
```

---

## 💼 Chi Tiết Từng Tầng:

### 1. **Service Layer** (✅ RECOMMENDED - Nơi Cần Đặt Validation)
- Chịu trách nhiệm kiểm tra logic business
- Validate dữ liệu trước khi gửi xuống Repository
- Ví dụ:
  ```python
  # service/sentence_service.py
  class SentenceService:
      def __init__(self, sentence_repo: SentenceRepository):
          self.repo = sentence_repo
      
      def create_sentence(self, paragraph_id: int, sentence_index: int, 
                         input_sentence: str, user_translation: str, 
                         machine_translation: str, score: float):
          # ✅ VALIDATION Ở ĐÂY
          if not input_sentence or len(input_sentence.strip()) == 0:
              raise ValueError("input_sentence không được để trống")
          if not user_translation or len(user_translation.strip()) == 0:
              raise ValueError("user_translation không được để trống")
          if not (0 <= score <= 10):
              raise ValueError("score phải từ 0-10")
          if sentence_index < 0:
              raise ValueError("sentence_index không được âm")
          
          # Sau khi validation xong, tạo model
          sentence = Sentence(
              id=None,
              paragraph_id=paragraph_id,
              sentence_index=sentence_index,
              input_sentence=input_sentence,
              user_translation=user_translation,
              machine_translation=machine_translation,
              score=score,
              note="",
              created_at=""
          )
          # Đưa vào repository
          return self.repo.create(sentence)
  ```

### 2. **Model Layer** (Optional - Validation Cơ Bản)
- Có thể thêm validation cơ bản trong `__init__()` của Model
- Ví dụ:
  ```python
  # model/sentence.py
  class Sentence:
      def __init__(self, id, paragraph_id, ..., score, ...):
          # Validation cơ bản
          if score < 0 or score > 10:
              raise ValueError("score phải từ 0-10")
          self.score = score
          # ...
  ```

### 3. **Repository Layer** (❌ KHÔNG NÊN)
- Repository **chỉ là Data Access Layer (DAL)**
- Nhận dữ liệu đã validate từ Service
- **Chỉ chịu trách nhiệm**: CRUD (Create, Read, Update, Delete)
- Không nên kiểm tra logic business ở đây

---

## 🎯 Tóm Lại:

| Tầng | Chức Năng | Validation? |
|------|-----------|------------|
| **Service** | Business logic, điều phối | ✅ YES (Nên đặt ở đây) |
| **Model** | Dữ liệu, conversion | ✅ Optional (cơ bản) |
| **Repository** | CRUD database | ❌ NO (chỉ lưu trữ) |

---

## 📝 Ví Dụ Cụ Thể - Tạo Sentence:

1. **ViewModel** gọi Service:
   ```python
   sentence_id = self.sentence_service.create_sentence(
       paragraph_id=1,
       sentence_index=1,
       input_sentence="Hello world",
       user_translation="Xin chào thế giới",
       machine_translation="Xin chào thế giới",
       score=8.5
   )
   ```

2. **Service** kiểm tra điều kiện:
   ```python
   # service/sentence_service.py
   if not input_sentence.strip():
       raise ValueError("Câu không được để trống")
   if not (0 <= score <= 10):
       raise ValueError("Điểm phải từ 0-10")
   ```

3. **Repository** chỉ lưu:
   ```python
   # repositories/sentence_repo.py
   def create(self, sentence: Sentence):
       # Không kiểm tra gì, chỉ INSERT vào DB
       ...
   ```

---

## 💡 Lợi Ích:

- **Tách biệt trách nhiệm**: Mỗi tầng làm một việc
- **Dễ test**: Service có thể test validation độc lập
- **Dễ bảo trì**: Logic business ở một chỗ duy nhất
- **Bảo mật**: Đảm bảo dữ liệu hợp lệ trước khi lưu vào DB
