# 📚 Quick Reference & Best Practices

## When in Doubt, Ask:

### 1. Đây là Model hay DTO?
```python
# Model: ALL DB fields, persistent
class Vocabulary:
    id, word, part_of_speech, vi_meaning, eng_description, example, note, correct_count, wrong_count, created_at

# DTO: Chỉ fields cần thiết, format cho View
class VocabularyTableDTO(TypedDict):
    id, word, vi_meaning, example
```

### 2. Tầng nào nên handle việc này?

| Task | Layer |
|------|-------|
| Render UI | **View** |
| Get user input | **View** |
| Transform data | **ViewModel** |
| Validate business rules | **Service** ⭐ |
| Unique check | **Service** |
| CRUD DB | **Repository** |
| Format display | **ViewModel** |
| Error handling | **View** (try-catch) |

### 3. Component nên nhận gì?
```python
# ✅ YES
class VocabularyTable(ft.Container):
    def __init__(self, home_vm: HomeViewModel):
        self.home_vm = home_vm

# ❌ NO
class VocabularyTable(ft.Container):
    def __init__(self, vocab_service: VocabularyService):
        self.vocab_service = vocab_service  # Direct access
```

### 4. DTO cần bao nhiêu class?
```python
# Không cần quá nhiều - chỉ 2-4 cho toàn project
class VocabularyTableDTO(TypedDict): ...  # For Home Screen
class VocabularyFlashCardDTO(TypedDict): ...  # For Vocabulary Screen
class ParagraphCardDTO(TypedDict): ...  # For Paragraph Screen
```

## Code Patterns

### ✅ GOOD Pattern: View → ViewModel → Service → Repository

```python
# view/components/add_dialog.py
def on_save_click(self):
    word = self.word_field.value.strip()
    
    # 1. UI validation (form level)
    if not word:
        print("Error: Word required")
        return
    
    try:
        # 2. Call ViewModel
        self.home_vm.create_vocabulary(word, ...)
        print("Added!")
    except ValueError as e:
        # 3. Handle Service error
        print(f"Error: {e}")

# view_model/home_vm.py
def create_vocabulary(self, word: str, ...):
    # ViewModel just calls Service
    return self.vocabulary_service.create_vocabulary(word, ...)

# service/vocabulary_service.py
def create_vocabulary(self, word: str, ...):
    # Service validates
    if len(word) < 2:
        raise ValueError("Word must be 2+ chars")
    
    vocab = Vocabulary(...)
    return self.vocab_repo.create(vocab)

# repositories/vocabulary_repo.py
def create(self, model: Vocabulary):
    # Repo assumes valid, just CRUD
    sql = "INSERT INTO vocabulary ..."
    cursor.execute(sql, model.to_row())
    return cursor.lastrowid
```

### ❌ BAD Pattern: Validation tán rác

```python
# ❌ Validation ở View
if not word:
    return

# ❌ Validation ở ViewModel
if len(word) < 2:
    return

# ❌ Validation ở Component
if word.count(" ") > 0:
    return

# ❌ Validation ở Service
if existing:
    return
```

## Common Mistakes

### ❌ Mistake 1: Component access Service directly
```python
# ❌ BAD
class VocabularyTable:
    def __init__(self, vocab_service):
        self.vocab_service = vocab_service
        self.vocab_service.create_vocabulary(...)

# ✅ GOOD
class VocabularyTable:
    def __init__(self, home_vm):
        self.home_vm = home_vm
        self.home_vm.create_vocabulary(...)
```

### ❌ Mistake 2: ViewModel access Repository
```python
# ❌ BAD
class HomeViewModel:
    def __init__(self, repo):
        self.repo = repo
        self.repo.create(vocab)

# ✅ GOOD
class HomeViewModel:
    def __init__(self, service):
        self.service = service
        self.service.create_vocabulary(...)
```

### ❌ Mistake 3: No validation in Service
```python
# ❌ BAD
class VocabularyService:
    def create_vocabulary(self, word, ...):
        vocab = Vocabulary(word, ...)
        return self.vocab_repo.create(vocab)  # No validation!

# ✅ GOOD
class VocabularyService:
    def create_vocabulary(self, word, ...):
        if not word:
            raise ValueError("Word cannot be empty")
        vocab = Vocabulary(word, ...)
        return self.vocab_repo.create(vocab)
```

### ❌ Mistake 4: View don't catch exceptions
```python
# ❌ BAD
def on_save_click(self):
    self.home_vm.create_vocabulary(word, ...)  # No try-catch!

# ✅ GOOD
def on_save_click(self):
    try:
        self.home_vm.create_vocabulary(word, ...)
    except ValueError as e:
        print(f"Error: {e}")
```

### ❌ Mistake 5: Component state not isolated
```python
# ❌ BAD
class VocabularyTable:
    editing_vocab_id = None  # Class variable - shared!

# ✅ GOOD
class VocabularyTable:
    def __init__(self, home_vm):
        self.editing_vocab_id = None  # Instance variable - isolated
```

## Validation Checklist

Before calling `repo.create()`, Service must check:

- [ ] Required fields not empty
- [ ] String lengths within limits
- [ ] Format is correct (no spaces, special chars, etc.)
- [ ] Unique constraints (not duplicate)
- [ ] Business rules (e.g., age > 18)
- [ ] Data integrity (related data exists)

Example:
```python
def create_vocabulary(self, word, vi_meaning, ...):
    # Check 1: Required
    if not word or not word.strip():
        raise ValueError("Word cannot be empty")
    
    # Check 2: Length
    word = word.strip()
    if len(word) < 2 or len(word) > 100:
        raise ValueError("Word length must be 2-100 chars")
    
    # Check 3: Format
    if " " in word:
        raise ValueError("Word cannot contain spaces")
    
    # Check 4: Unique
    if self.vocab_repo.filter("word", word):
        raise ValueError(f"Word '{word}' already exists")
    
    # ✅ All valid, persist
    return self.vocab_repo.create(Vocabulary(word, vi_meaning, ...))
```

## File Structure

```
MyEnglish/
├── model/
│   ├── vocabulary.py  (Model: ALL fields from DB)
│   ├── paragraph.py
│   └── sentence.py
├── repositories/
│   ├── vocabulary_repo.py  (Repository: CRUD)
│   ├── paragraph_repo.py
│   └── repo_base.py
├── service/
│   ├── vocabulary_service.py  (Service: Validation + Business Logic)
│   ├── paragraph_service.py
│   └── scoring_service.py
├── view_model/
│   ├── home_vm.py  (ViewModel: Transform Model → DTO)
│   ├── translate_practice_vm.py
│   └── vocabulary_vm.py
└── view/
    ├── screens/
    │   ├── home_view.py  (View: Render UI)
    │   ├── translate_practice_view.py
    │   └── vocabulary_view.py
    └── components/
        ├── vocabulary_table.py  (Component: Reusable widget)
        ├── flash_card.py
        └── footer.py
```

## Testing Quick Tips

```python
# Test Service independently (without DB)
class MockVocabularyRepository:
    def __init__(self):
        self.items = {}
    
    def create(self, vocab):
        self.items[vocab.id] = vocab
        return vocab.id
    
    def filter(self, field, value):
        return [v for v in self.items.values() if getattr(v, field) == value]

# Use in test
mock_repo = MockVocabularyRepository()
service = VocabularyService()
service.vocab_repo = mock_repo

# Test validation
try:
    service.create_vocabulary("", ...)
    assert False, "Should raise ValueError"
except ValueError as e:
    assert "cannot be empty" in str(e)
```

## Summary for Quick Reference

| Component | Input | Output | Error Handling |
|-----------|-------|--------|-----------------|
| **View** | User action | Call ViewModel | try-catch |
| **ViewModel** | ViewModel call | Call Service | Pass through |
| **Service** | Service call | Validate, then CRUD | Raise ValueError |
| **Repository** | Model | DB operations | Assume valid |

**Remember:**
- ✅ One-way dependency: View → ViewModel → Service → Repository
- ✅ Validation ở Service (main) + View (UI level)
- ✅ Error handling ở View (try-catch)
- ✅ Data transform ở ViewModel
- ✅ Business logic ở Service
