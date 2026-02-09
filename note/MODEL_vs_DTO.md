# 📦 Model vs DTO Pattern

## Sự khác biệt cơ bản

| Aspect | Model | DTO |
|--------|-------|-----|
| **Định nghĩa** | Đại diện entity trong DB | Format dữ liệu giữa các tầng |
| **Fields** | ALL fields từ schema | Chỉ fields cần thiết |
| **Mục đích** | Persist/Query data | Transfer data (View) |
| **Scope** | Toàn codebase | Specific layer (View) |
| **Thay đổi** | Ít (schema stable) | Thường (UI requirements) |
| **Logic** | Domain rules | Dữ liệu thuần |
| **Nơi dùng** | Service, Repository | View, ViewModel, API |

## Ví dụ cụ thể

### Database Table: vocabulary

```sql
CREATE TABLE vocabulary (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL,
    part_of_speech TEXT,
    vi_meaning TEXT NOT NULL,
    eng_description TEXT,       -- Không cần show
    example TEXT NOT NULL,
    note TEXT,                  -- Private notes
    correct_count INTEGER,      -- Dùng cho flashcard
    wrong_count INTEGER,        -- Dùng cho flashcard
    created_at TEXT
);
```

### Model: Vocabulary (đại diện DB)

```python
@dataclass
class Vocabulary:
    id: int
    word: str
    part_of_speech: str
    vi_meaning: str
    eng_description: str  # ← Có trong DB, nhưng View không cần
    example: str
    note: str             # ← Có trong DB, nhưng là private
    correct_count: int    # ← Có trong DB, dùng cho flashcard
    wrong_count: int      # ← Có trong DB, dùng cho flashcard
    created_at: str
```

### DTO for Home Screen (chỉ show table)

#### Cách 1: TypedDict (khuyến nghị) ⭐

```python
# view_model/dtos.py
from typing import TypedDict

class VocabularyTableDTO(TypedDict):
    id: int
    word: str
    vi_meaning: str
    example: str
    # ❌ Không cần: part_of_speech, eng_description, note, correct_count, wrong_count

# view_model/home_vm.py
def get_all_vocabulary(self) -> list[VocabularyTableDTO]:
    all_vocab = self.vocabulary_service.get_all_vocabulary()
    return [
        {
            "id": v.id,
            "word": v.word,
            "vi_meaning": v.vi_meaning,
            "example": v.example,
        }
        for v in all_vocab
    ]
```

**Ưu điểm:**
- ✅ Type hint tốt (IDE autocomplete)
- ✅ Nhẹ (chỉ là type hint, runtime vẫn là dict)
- ✅ Syntax gần dict (bạn gọi nó là TypedDict)

#### Cách 2: Dict plain

```python
def get_all_vocabulary(self) -> list[dict]:
    all_vocab = self.vocabulary_service.get_all_vocabulary()
    return [
        {
            "id": v.id,
            "word": v.word,
            "vi_meaning": v.vi_meaning,
            "example": v.example,
        }
        for v in all_vocab
    ]
```

**Ưu điểm:**
- ✅ Đơn giản nhất
- ✅ Không cần tạo class

**Nhược điểm:**
- ❌ Không có type hint

### DTO for Vocabulary Screen (flashcard)

```python
class VocabularyFlashCardDTO(TypedDict):
    id: int
    word: str
    example: str
    part_of_speech: str
    # ❌ Không cần: vi_meaning (user phải đoán), eng_description, note, created_at
```

## Tại sao cần DTO?

### 1. Separation of Concerns

```python
# ❌ BAD - View biết toàn bộ Model
def render(vocab: Vocabulary):
    text.value = vocab.word  # OK
    if vocab.correct_count > 5:  # ❌ Business logic ở View
        show_badge()

# ✅ GOOD - View chỉ biết DTO
def render(vocab_dto: VocabularyTableDTO):
    text.value = vocab_dto["word"]  # OK
    # ❌ Không thể access correct_count (nó không có trong DTO)
```

### 2. Flexibility (Thay đổi Model không ảnh hưởng View)

```python
# Model thêm field mới
class Vocabulary:
    deleted_at: str  # ← Thêm field

# DTO không cần thay đổi (nếu không cần show deleted_at)
class VocabularyTableDTO(TypedDict):
    id: int
    word: str
    vi_meaning: str
    example: str  # ← Không đổi
```

### 3. Performance (Chỉ serialize fields cần thiết)

```python
# Serialize Model (15 fields)
vocab = Vocabulary(...)
json.dumps(vocab.to_dict())  # Send 15 fields

# Serialize DTO (4 fields)
dto = {"id": 1, "word": "hello", ...}
json.dumps(dto)  # Send 4 fields (nhẹ hơn)
```

### 4. Security (Không expose sensitive data)

```python
# Model có password
class User:
    password_hash: str  # ❌ Không nên expose

# DTO không có password
class UserDTO(TypedDict):
    id: int
    name: str
    email: str  # ✅ Safe to expose
```

### 5. Clear Intent (View biết rõ cần gì)

```python
# ❌ View work với Model - không rõ cần fields nào
def render_table(vocab: Vocabulary):
    # Có bao nhiêu fields để dùng?
    # Nên dùng fields nào?
    
# ✅ View work với DTO - rõ ràng
def render_table(vocab_dto: VocabularyTableDTO):
    # Chỉ có id, word, vi_meaning, example
    # Dùng chúng là tốt
```

## Số lượng DTO cần thiết

**Không cần quá nhiều - chỉ 2-3 cho toàn project:**

```python
# Cho Home Screen
class VocabularyTableDTO(TypedDict):
    id: int
    word: str
    vi_meaning: str
    example: str

# Cho Vocabulary Screen (Flashcard)
class VocabularyFlashCardDTO(TypedDict):
    id: int
    word: str
    example: str
    part_of_speech: str

# Cho Paragraph Screen
class ParagraphCardDTO(TypedDict):
    id: int
    title: str
    completed: int
    score: int
    created_at: str
```

**Tất cả các hàm ViewModel return một trong 3 này thôi.**

## Khi nào dùng Model vs DTO

| Situation | Dùng |
|-----------|------|
| Service cần lấy dữ liệu | Model |
| ViewModel format cho View | DTO |
| Repository persist | Model |
| View display | DTO |
| API response | DTO |
| Component render | DTO |

## Implementation Pattern

```python
# service/vocabulary_service.py
def get_all_vocabulary(self) -> list[Vocabulary]:
    """Return Model từ Service"""
    return self.vocab_repo.all()

# view_model/home_vm.py
def get_all_vocabulary(self) -> list[VocabularyTableDTO]:
    """Transform Model → DTO trong ViewModel"""
    models = self.vocabulary_service.get_all_vocabulary()
    return [
        {
            "id": m.id,
            "word": m.word,
            "vi_meaning": m.vi_meaning,
            "example": m.example,
        }
        for m in models
    ]

# view/components/vocabulary_table.py
def _build_vocabulary_row(self, vocab_dto: VocabularyTableDTO):
    """Render DTO trong Component"""
    return ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(vocab_dto["word"])),
            ft.DataCell(ft.Text(vocab_dto["vi_meaning"])),
            ...
        ]
    )
```

## Summary

- **Model** = Chứa ALL data từ DB, dùng trong Service/Repository
- **DTO** = Chỉ fields cần thiết, dùng trong ViewModel/View
- **Transform** xảy ra ở ViewModel (Model → DTO)
- **Separation** giữa layers rõ ràng
- **2-3 DTOs** đủ cho toàn project
