# 🔄 Data Flow & Dependency Injection

## Complete Data Flow: Edit Vocabulary

```
┌─────────────────────────────────────────────────────────┐
│ 1. USER INTERACTION                                     │
│    Click Edit button → vocabulary_table.on_edit_click() │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 2. COMPONENT (View Layer)                               │
│    - Set editing_vocab_id = vocab_id                    │
│    - refresh() → rebuild table                          │
│    - Show TextFields with current values                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 3. USER MODIFIES + SAVES                                │
│    - User type new word → TextField.value = "new_word"  │
│    - Click Save → on_save_click()                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 4. VALIDATION (Component - UI Level)                    │
│    - Get values from TextFields                         │
│    - Strip whitespace, validate not empty               │
│    - If invalid, print error & return                   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 5. VIEWMODEL LAYER                                      │
│    Call: home_vm.save_vocabulary_edit(                  │
│        vocab_id, new_word, new_vi_meaning, new_example)│
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 6. SERVICE LAYER - ⭐ MAIN VALIDATION                    │
│    - Fetch vocab từ vocab_repo.get(vocab_id)            │
│    - Validate: format, unique check, business rules     │
│    - If invalid, raise ValueError                       │
│    - Update object properties                           │
│    - Call vocab_repo.update(vocab)                      │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 7. REPOSITORY LAYER (assume valid)                      │
│    - Convert Model → DB row                             │
│    - Execute UPDATE SQL                                 │
│    - Commit transaction                                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 8. DATABASE                                             │
│    UPDATE vocabulary SET word = 'new' WHERE id = 5      │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ 9. BACK TO COMPONENT (Error Handling)                   │
│    - Try-catch block catches ValueError from Service    │
│    - If error: print error message & stop               │
│    - If success:                                        │
│      - Clear edit state (editing_vocab_id = None)       │
│      - refresh() → rebuild table                        │
│      - Fetch fresh data: home_vm.get_all_vocabulary()   │
│      - Show updated table in VIEW mode                  │
└─────────────────────────────────────────────────────────┘
```

## Code Example: Complete Flow

### Component Layer

```python
# view/components/vocabulary_table.py
class VocabularyTable(ft.Container):
    def _on_save_click(self, vocab_id: int):
        try:
            fields = self.edit_fields.get(vocab_id, {})
            
            # Step 4: Validate (UI level)
            new_word = fields['word'].value.strip()
            new_vi_meaning = fields['vi_meaning'].value.strip()
            new_example = fields['example'].value.strip()
            
            if not new_word or not new_vi_meaning:
                print("Error: Fields cannot be empty")
                return
            
            # Step 5: Call ViewModel
            self.home_vm.save_vocabulary_edit(
                vocab_id, new_word, new_vi_meaning, new_example
            )
            
            # Step 9: Success handling
            self.editing_vocab_id = None
            self.edit_fields.clear()
            self.refresh()
            print("Updated successfully!")
            
        except ValueError as e:
            # Step 9: Service validation error
            print(f"Error: {e}")
        except Exception as e:
            # Step 9: Unexpected error
            print(f"Error: {e}")
```

### ViewModel Layer

```python
# view_model/home_vm.py
class HomeViewModel:
    def save_vocabulary_edit(self, vocab_id: int, new_word: str, 
                            new_vi_meaning: str, new_example: str):
        """Step 5: ViewModel - Transform & call Service"""
        
        # Call Service with cleaned data
        vocab = self.vocabulary_service.vocab_repo.get(vocab_id)
        if not vocab:
            raise ValueError(f"Vocabulary {vocab_id} not found")
        
        # Update
        vocab.word = new_word
        vocab.vi_meaning = new_vi_meaning
        vocab.example = new_example
        
        # Step 6: Call Service (validation happens here)
        self.vocabulary_service.vocab_repo.update(vocab)
```

### Service Layer

```python
# service/vocabulary_service.py
class VocabularyService:
    def update_vocabulary(self, vocab: Vocabulary):
        """Step 6: Service - MAIN VALIDATION"""
        
        # Validate format
        if " " in vocab.word:
            raise ValueError("Word cannot contain spaces")
        
        # Validate unique (exclude self)
        existing = self.vocab_repo.filter("word", vocab.word)
        if existing and existing[0].id != vocab.id:
            raise ValueError(f"Word '{vocab.word}' already exists")
        
        # If valid, persist
        self.vocab_repo.update(vocab)
```

### Repository Layer

```python
# repositories/vocabulary_repo.py
class VocabularyRepository(BaseRepository):
    def update(self, model: Vocabulary):
        """Step 7: Repository - CRUD (assume valid)"""
        row = model.to_row()
        sql = f"UPDATE {self.table_name} SET ... WHERE id = ?"
        cursor = self.db_connect.connection.cursor()
        cursor.execute(sql, row + (model.id,))
        self.db_connect.connection.commit()
```

## Dependency Injection Pattern

### Inject từ trên xuống (Top-Down)

```python
# main.py - Application Entry Point
from service.vocabulary_service import VocabularyService
from view_model.home_vm import HomeViewModel
from view.screens.home_view import HomeScreen

# 1. Create Service (bottom layer)
vocabulary_service = VocabularyService()

# 2. Create ViewModel (middle layer)
home_vm = HomeViewModel(vocabulary_service)

# 3. Create Screen (top layer)
home_screen = HomeScreen(home_vm)

# 4. Use Screen
page.content = home_screen
```

### Dependency Chain

```
Screen
  ↓
  └─→ Inject ViewModel
      ↓
      ├─→ Inject ViewModel to Component
      │   ↓
      │   Component
      │   (call: home_vm.create_vocabulary())
      │
      └─→ ViewModel has Services
          ↓
          ├─→ VocabularyService
          │   ├─→ Use VocabularyRepository
          │   │   └─→ CRUD operations
          │   └─→ Business logic
          │
          ├─→ ParagraphService
          └─→ SentenceService
```

### Code: Dependency Injection

```python
# 1. HomeScreen gets HomeViewModel
class HomeScreen(ft.Container):
    def __init__(self, home_vm: HomeViewModel):  # ← Injected
        self.home_vm = home_vm
        self.vocabulary_table = VocabularyTable(home_vm)  # ← Re-inject

# 2. VocabularyTable gets HomeViewModel (same instance)
class VocabularyTable(ft.Container):
    def __init__(self, home_vm: HomeViewModel):  # ← Injected
        self.home_vm = home_vm
        # Use it
        self.home_vm.create_vocabulary(...)

# 3. HomeViewModel gets Services
class HomeViewModel:
    def __init__(self, vocabulary_service: VocabularyService):  # ← Injected
        self.vocabulary_service = vocabulary_service

# 4. Services create Repositories
class VocabularyService:
    def __init__(self):
        self.vocab_repo = VocabularyRepository(DBConnect())

# 5. DBConnect is Singleton (thread-safe)
class DBConnect:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

## Lợi ích của Dependency Injection

✅ **Testable**
```python
# Test với mock Service
mock_service = MockVocabularyService()
home_vm = HomeViewModel(mock_service)
# Test logic mà không cần DB
```

✅ **Flexible**
```python
# Swap implementation dễ dàng
home_vm = HomeViewModel(MockVocabularyService())  # Test
home_vm = HomeViewModel(RealVocabularyService())  # Production
```

✅ **Loose Coupling**
```python
# HomeScreen không biết về Service/Repository
# Chỉ cần ViewModel
class HomeScreen:
    def __init__(self, home_vm):  # ← Generic
        self.home_vm = home_vm
```

✅ **Reusable**
```python
# Cùng một ViewModel instance dùng cho nhiều Components
vocabulary_table = VocabularyTable(home_vm)
vocabulary_stats = VocabularyStats(home_vm)
# Cùng data source
```

## Error Propagation

```
Component
  ↓ (try-catch)
    ↓
ViewModel
  ↓ (pass through)
    ↓
Service (raise ValueError)
  ↓
Component (catch ValueError)
  ↓
Show error to user
```

### Code

```python
# Component
try:
    self.home_vm.save_vocabulary_edit(...)  # ← Call ViewModel
except ValueError as e:  # ← Catch Service error
    print(f"Error: {e}")  # ← Show to user
except Exception as e:  # ← Catch unexpected
    print(f"Unexpected error: {e}")

# ViewModel
def save_vocabulary_edit(self, ...):
    # No try-catch here, let exception propagate
    vocab = self.vocabulary_service.vocab_repo.get(vocab_id)
    # ... update ...
    self.vocabulary_service.vocab_repo.update(vocab)

# Service
def update_vocabulary(self, vocab):
    if " " in vocab.word:
        raise ValueError("Word cannot contain spaces")  # ← Raise here
    # ... persist ...
```

## Summary

- **Data flows**: View → ViewModel → Service → Repository → DB
- **Errors propagate** back to View (try-catch)
- **Validation** happens ở Service (main) + View (UI level)
- **Dependencies** inject từ trên xuống
- **Loose coupling**: Each layer only knows what it needs
- **Single responsibility**: Each layer has one job
