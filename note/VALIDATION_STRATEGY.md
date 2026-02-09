# ✅ Data Validation Strategy

## Validation nằm ở đâu?

```
┌──────────────────────────────────┐
│ View/Component                   │  ← UI Validation (nhẹ)
│ - Required fields                │     Not empty, basic format
│ - Basic format check             │
└──────────────────────────────────┘
          ↓ (pass to)
┌──────────────────────────────────┐
│ ViewModel                        │  ← Transform data
│ - Prepare data                   │     (NO validation)
└──────────────────────────────────┘
          ↓ (pass to)
┌──────────────────────────────────┐
│ Service ⭐ MAIN VALIDATION HERE   │  ← Business Logic Validation
│ - Required fields check          │     Domain constraints
│ - Format validation              │     Unique checks
│ - Business rules                 │     Raise ValueError
│ - Data integrity                 │
└──────────────────────────────────┘
          ↓ (if valid)
┌──────────────────────────────────┐
│ Repository                       │  ← CRUD DB
│ - Assume valid, just CRUD        │
└──────────────────────────────────┘
          ↓
┌──────────────────────────────────┐
│ Database                         │  ← Constraint enforcement
│ - UNIQUE, NOT NULL, FK           │
│ - Last line of defense           │
└──────────────────────────────────┘
```

## Ví dụ cụ thể: Create Vocabulary

### ❌ Sai cách (Validation bị tán rác)

```python
# view/components/add_vocabulary_dialog.py
class AddVocabularyDialog:
    def on_save_click(self):
        word = self.word_field.value
        
        # ❌ Validate ở View
        if not word:
            self.show_error("Word required")
            return
        if len(word) < 2:
            self.show_error("Word must be 2+ chars")
            return
        if word.count(" ") > 0:
            self.show_error("Word cannot have spaces")
            return
        if len(word) > 100:
            self.show_error("Word must be < 100 chars")
            return
        
        # ❌ Validation logic bị tán rác ở View
```

**Vấn đề:**
- ❌ Validation logic bị tán rác khắp nơi
- ❌ Khó maintain (thay đổi rule phải sửa View)
- ❌ Không có single source of truth
- ❌ API call trực tiếp không có validation
- ❌ Code duplicate (nhiều View validate cùng một thing)

### ✅ Cách đúng: Try-Catch Pattern

#### **Step 1: View - Nhẹ UI Validation**

```python
# view/components/add_vocabulary_dialog.py
class AddVocabularyDialog:
    def on_save_click(self):
        word = self.word_field.value.strip()
        vi_meaning = self.meaning_field.value.strip()
        
        # ✅ Chỉ validate FORM (required fields)
        if not word or not vi_meaning:
            self.show_error("Please fill all fields")
            return
        
        try:
            # ✅ Pass to ViewModel → Service
            vocab_id = self.home_vm.create_vocabulary(word, vi_meaning)
            self.show_success("Vocabulary added!")
            self.refresh()
            
        except ValueError as e:
            # ✅ Catch Service validation errors
            self.show_error(str(e))  # "Word 'hello' already exists"
        except Exception as e:
            # ✅ Catch DB errors
            self.show_error(f"Error: {str(e)}")
```

#### **Step 2: ViewModel - Transform (NO validation)**

```python
# view_model/home_vm.py
class HomeViewModel:
    def create_vocabulary(self, word: str, vi_meaning: str) -> int:
        """
        ViewModel chỉ transform, không validate
        Gọi Service để handle validation
        """
        # ✅ Pass to Service - Service sẽ validate
        vocab_id = self.vocabulary_service.create_vocabulary(
            word=word,
            part_of_speech="",  # Default
            vi_meaning=vi_meaning,
            eng_description="",  # Default
            example="",  # Default
            note=""  # Default
        )
        return vocab_id
```

#### **Step 3: Service - ⭐ MAIN VALIDATION HERE**

```python
# service/vocabulary_service.py
class VocabularyService:
    def create_vocabulary(self, word: str, part_of_speech: str,
                         vi_meaning: str, eng_description: str,
                         example: str, note: str = "") -> int:
        """
        ✅ ALL business logic validation nằm ở đây
        Raise ValueError nếu invalid
        """
        
        # 1️⃣ Validate: Required fields
        if not word or not word.strip():
            raise ValueError("Word cannot be empty")
        if not vi_meaning or not vi_meaning.strip():
            raise ValueError("Vietnamese meaning cannot be empty")
        
        # Clean data
        word = word.strip()
        vi_meaning = vi_meaning.strip()
        
        # 2️⃣ Validate: Format
        if len(word) < 2:
            raise ValueError("Word must be at least 2 characters")
        if len(word) > 100:
            raise ValueError("Word must be less than 100 characters")
        if " " in word:
            raise ValueError("Word cannot contain spaces")
        
        # 3️⃣ Validate: Business rules (unique check)
        existing = self.vocab_repo.filter("word", word)
        if existing:
            raise ValueError(f"Word '{word}' already exists")
        
        # 4️⃣ Validate: Data integrity
        if len(vi_meaning) < 2:
            raise ValueError("Meaning must be at least 2 characters")
        if len(vi_meaning) > 500:
            raise ValueError("Meaning must be less than 500 characters")
        
        # ✅ Nếu tới đây, data hợp lệ - persist
        now = datetime.now().isoformat()
        new_vocab = Vocabulary(
            id=None,
            word=word,
            part_of_speech=part_of_speech,
            vi_meaning=vi_meaning,
            eng_description=eng_description,
            example=example,
            note=note,
            correct_count=0,
            wrong_count=0,
            created_at=now
        )
        
        vocab_id = self.vocab_repo.create(new_vocab)
        return vocab_id
```

#### **Step 4: Repository - CRUD (Assume valid)**

```python
# repositories/vocabulary_repo.py
class VocabularyRepository(BaseRepository):
    def create(self, model: Vocabulary) -> int:
        """
        ❌ KHÔNG validate
        Assume data đã valid từ Service
        Chỉ CRUD
        """
        row = model.to_row()
        
        sql = f"""
            INSERT INTO {self.table_name} 
            (word, part_of_speech, vi_meaning, eng_description, example, note, correct_count, wrong_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor = self.db_connect.connection.cursor()
        cursor.execute(sql, row)
        self.db_connect.connection.commit()
        
        return cursor.lastrowid
```

## Validation Types & Locations

| Type | Where | Example | Raises |
|------|-------|---------|--------|
| **Form Level** | View | `if not field.value` | - (show error) |
| **Required** | Service | `if not word.strip()` | ValueError |
| **Format** | Service | `if " " in word` | ValueError |
| **Length** | Service | `if len(word) < 2` | ValueError |
| **Unique** | Service | `if repo.filter("word", word)` | ValueError |
| **Business Rules** | Service | `if user.role != "admin"` | ValueError |
| **Database Constraints** | DB | `UNIQUE(word)`, `NOT NULL` | DB Error |

## Error Handling Pattern

```python
# view/components/add_vocabulary_dialog.py
def on_save_click(self):
    word = self.word_field.value.strip()
    vi_meaning = self.meaning_field.value.strip()
    
    # UI Level
    if not word or not vi_meaning:
        self.show_error("Please fill all fields")
        return
    
    try:
        # Business Logic (Service) + Persist (Repo)
        self.home_vm.create_vocabulary(word, vi_meaning)
        self.show_success("Added successfully!")
        self.refresh()
        
    except ValueError as e:
        # Business validation error từ Service
        self.show_error(str(e))
        # Example messages:
        # - "Word 'hello' already exists"
        # - "Word must be at least 2 characters"
        # - "Meaning cannot be empty"
        
    except Exception as e:
        # Unexpected error (DB issue, etc.)
        self.show_error(f"Error: {str(e)}")
        print(f"Error creating vocabulary: {e}")  # Log
```

## Validation Best Practices

✅ **DO:**
- Validate ở Service trước persist
- Raise ValueError with clear message
- Catch exceptions ở Component
- Show error messages to user
- Single source of truth (Service)
- Validate in order (required → format → business rules)

❌ **DON'T:**
- Validate logic ở View (chỉ form level)
- Allow invalid data reach Repository
- Silent failures (always raise or return)
- Duplicate validation logic
- Trust client-side validation only
- Validate ở Repository

## Complete Example: Edit Vocabulary

```python
# service/vocabulary_service.py
def update_vocabulary(self, vocab_id: int, new_word: str, 
                     new_vi_meaning: str, new_example: str):
    """Update with validation"""
    # Validate inputs
    if not new_word or not new_word.strip():
        raise ValueError("Word cannot be empty")
    if not new_vi_meaning or not new_vi_meaning.strip():
        raise ValueError("Meaning cannot be empty")
    
    # Check unique (excluding self)
    existing = self.vocab_repo.filter("word", new_word.strip())
    if existing and existing[0].id != vocab_id:
        raise ValueError(f"Word '{new_word}' already exists")
    
    # Get and update
    vocab = self.vocab_repo.get(vocab_id)
    if not vocab:
        raise ValueError(f"Vocabulary {vocab_id} not found")
    
    vocab.word = new_word.strip()
    vocab.vi_meaning = new_vi_meaning.strip()
    vocab.example = new_example.strip()
    
    self.vocab_repo.update(vocab)

# view/components/vocabulary_table.py
def _on_save_click(self, vocab_id: int):
    try:
        fields = self.edit_fields.get(vocab_id, {})
        
        # UI validation
        new_word = fields['word'].value.strip()
        new_vi_meaning = fields['vi_meaning'].value.strip()
        new_example = fields['example'].value.strip()
        
        if not new_word or not new_vi_meaning:
            print("Error: Fields cannot be empty")
            return
        
        # Service validation + update
        self.home_vm.save_vocabulary_edit(
            vocab_id, new_word, new_vi_meaning, new_example
        )
        
        # Success
        self.editing_vocab_id = None
        self.edit_fields.clear()
        self.refresh()
        
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error: {e}")
```

## Summary

- **View**: Validate form (required fields only)
- **ViewModel**: Transform data (no validation)
- **Service**: ⭐ Main validation (all business rules)
- **Repository**: Trust valid data, only CRUD
- **Database**: Last line of defense (constraints)
- **Error handling**: Try-catch, show to user
