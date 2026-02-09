# 🏗️ MVVM-S Architecture Pattern

## Định nghĩa
MVVM-S = Model-View-ViewModel-Service

Kiến trúc phân tầng để tách biệt logic từ UI, dễ maintain và test.

## Sơ Đồ Kiến Trúc

```
┌─────────────────────────────────────────┐
│  View (UI - Flet Components)            │  ← Người dùng thấy
├─────────────────────────────────────────┤
│  ViewModel (Data Transform)             │  ← Format dữ liệu
├─────────────────────────────────────────┤
│  Service (Business Logic)               │  ← Xử lý logic
├─────────────────────────────────────────┤
│  Repository (Database Access)           │  ← CRUD DB
├─────────────────────────────────────────┤
│  Model (Entity)                         │  ← Đại diện DB
└─────────────────────────────────────────┘
```

## 1. Model Layer (`model/vocabulary.py`)

**Trách nhiệm:**
- ✅ Đại diện entity từ database
- ✅ Contain ALL fields từ DB schema
- ✅ Có methods: to_dict(), to_row(), from_dict()
- ❌ Không có business logic phức tạp
- ❌ Không trực tiếp sử dụng trong View

```python
from dataclasses import dataclass

@dataclass
class Vocabulary:
    id: int
    word: str
    part_of_speech: str
    vi_meaning: str
    eng_description: str
    example: str
    note: str
    correct_count: int
    wrong_count: int
    created_at: str
    
    def to_dict(self):
        """Convert thành dict để serialize"""
        return {
            'id': self.id,
            'word': self.word,
            'part_of_speech': self.part_of_speech,
            'vi_meaning': self.vi_meaning,
            'eng_description': self.eng_description,
            'example': self.example,
            'note': self.note,
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count,
            'created_at': self.created_at,
        }
    
    def to_row(self):
        """Convert thành tuple cho DB insert"""
        return (
            self.word,
            self.part_of_speech,
            self.vi_meaning,
            self.eng_description,
            self.example,
            self.note,
            self.correct_count,
            self.wrong_count,
            self.created_at
        )
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create instance từ dict"""
        return cls(**data)
```

## 2. Repository Layer (`repositories/vocabulary_repo.py`)

**Trách nhiệm:**
- ✅ CRUD database
- ✅ Execute SQL queries
- ✅ Convert DB rows → Model objects
- ❌ Không có business logic
- ❌ Không validate dữ liệu

```python
from repositories.repo_base import BaseRepository
from model.vocabulary import Vocabulary

class VocabularyRepository(BaseRepository):
    def __init__(self, db_connect):
        super().__init__(db_connect)
        self.table_name = "vocabulary"
        self.columns = [
            "id", "word", "part_of_speech", "vi_meaning", 
            "eng_description", "example", "note", 
            "correct_count", "wrong_count", "created_at"
        ]
        self.model_class = Vocabulary
    
    # BaseRepository cung cấp:
    # - create(model) → id
    # - get(id) → model
    # - update(model)
    # - delete(id)
    # - all() → [model]
    # - filter(field, value) → [model]
    # - count_all() → int
    # - count_by(field, value) → int
```

## 3. Service Layer (`service/vocabulary_service.py`)

**Trách nhiệm:**
- ✅ Business logic & validation
- ✅ Instantiate Repository
- ✅ Xử lý domain rules
- ✅ Transactions
- ❌ Không biết về UI
- ❌ Không format dữ liệu cho View

```python
from repositories.vocabulary_repo import VocabularyRepository
from model.vocabulary import Vocabulary
from datetime import datetime

class VocabularyService:
    def __init__(self):
        self.vocab_repo = VocabularyRepository(DBConnect())
    
    def create_vocabulary(self, word: str, part_of_speech: str,
                         vi_meaning: str, eng_description: str,
                         example: str, note: str = "") -> int:
        """
        Business logic: tạo vocabulary với validation
        """
        # Validate
        if not word.strip():
            raise ValueError("Word cannot be empty")
        
        # Create model
        vocab = Vocabulary(
            id=None,
            word=word,
            part_of_speech=part_of_speech,
            vi_meaning=vi_meaning,
            eng_description=eng_description,
            example=example,
            note=note,
            correct_count=0,
            wrong_count=0,
            created_at=datetime.now().isoformat()
        )
        
        # Persist
        return self.vocab_repo.create(vocab)
    
    def update_vocabulary(self, vocab_id: int, correct_count: int = None, ...):
        """Business logic: cập nhật vocabulary"""
        vocab = self.vocab_repo.get(vocab_id)
        if not vocab:
            raise ValueError(f"Vocabulary {vocab_id} not found")
        
        # Update logic
        if correct_count is not None:
            vocab.correct_count = correct_count
        ...
        
        self.vocab_repo.update(vocab)
    
    def get_all_vocabulary(self) -> list[Vocabulary]:
        """Get tất cả vocabulary từ DB"""
        return self.vocab_repo.all()
```

## 4. ViewModel Layer (`view_model/home_vm.py`)

**Trách nhiệm:**
- ✅ Bridge giữa View ↔ Service
- ✅ Transform Model → DTO/dict
- ✅ Data aggregation & formatting
- ✅ State management
- ❌ Không vẽ UI
- ❌ Không trực tiếp access Repository

```python
from service.vocabulary_service import VocabularyService
from model.vocabulary import Vocabulary

class HomeViewModel:
    def __init__(self, vocabulary_service: VocabularyService):
        self.vocabulary_service = vocabulary_service
    
    def get_all_vocabulary(self) -> list[dict]:
        """
        Lấy dữ liệu từ Service, 
        TRANSFORM thành format cho View cần
        """
        all_vocab = self.vocabulary_service.get_all_vocabulary()
        
        # Transform: Lọc fields, format dữ liệu
        return [
            {
                "id": v.id,
                "word": v.word,
                "vi_meaning": v.vi_meaning,
                "example": v.example,
                # ❌ Bỏ: eng_description, note, correct_count, ...
            }
            for v in all_vocab
        ]
    
    def save_vocabulary_edit(self, vocab_id: int, new_word: str, 
                            new_vi_meaning: str, new_example: str):
        """
        Lấy input từ View,
        Gọi Service để update
        """
        vocab = self.vocabulary_service.vocab_repo.get(vocab_id)
        if not vocab:
            raise ValueError(f"Vocabulary {vocab_id} not found")
        
        # Update
        vocab.word = new_word.strip()
        vocab.vi_meaning = new_vi_meaning.strip()
        vocab.example = new_example.strip()
        
        # Persist
        self.vocabulary_service.vocab_repo.update(vocab)
```

## 5. View Layer (`view/screens/home_view.py`)

**Trách nhiệm:**
- ✅ Render UI (Flet widgets)
- ✅ Handle user interactions
- ✅ Call ViewModel methods
- ❌ Không contain business logic
- ❌ Không direct access Service/Repository
- ❌ Không trực tiếp manipulate Model

```python
import flet as ft
from view.components.vocabulary_table import VocabularyTable

class HomeScreen(ft.Container):
    def __init__(self, home_vm: HomeViewModel, switcher=None):
        super().__init__(expand=True, padding=20)
        self.home_vm = home_vm
        self.vocabulary_table_component = None
        self.render()
    
    def build_vocabulary_table(self):
        """Render UI component"""
        if self.vocabulary_table_component is None:
            self.vocabulary_table_component = VocabularyTable(self.home_vm)
        return self.vocabulary_table_component
    
    def render(self):
        """Build entire UI"""
        self.content = ft.Column(
            controls=[
                self.build_vocabulary_table(),
                # ... more UI
            ]
        )
        self.update()
```

## Data Flow Example: Edit Vocabulary

```
User Input (View)
    ↓ (value from TextField)
Component.on_save_click()
    ↓ (vocab_id, new_word, new_meaning, ...)
ViewModel.save_vocabulary_edit()
    ↓ (update object)
Service (through vocab_repo)
    ↓
Repository.update(vocab)
    ↓
Database (UPDATE)
    ↓
Component.refresh()
    ↓ (rebuild table)
View renders updated data
```

## Best Practices

✅ **DO:**
- Follow layer separation strictly
- Inject dependencies (ViewModel to View)
- Validate in Service, not View
- Catch exceptions at View level
- Transform data in ViewModel

❌ **DON'T:**
- Access Repository from View
- Put business logic in View
- Modify Model in View
- Direct Service calls from Component
- Validate in multiple layers
