# MyEnglish - Architecture & Design Documentation

**Document Version:** 1.0  
**Date:** February 9, 2026  
**Status:** Draft (Review Required)  
**Phase:** SDLC Phase 3 - Design

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Database Design](#database-design)
4. [UI Architecture & Navigation](#ui-architecture--navigation)
5. [Layer Architecture (MVVM-S)](#layer-architecture-mvvm-s)
6. [Component Design](#component-design)
7. [Data Flow Diagrams](#data-flow-diagrams)
8. [API & Interface Specifications](#api--interface-specifications)
9. [Design Patterns & Principles](#design-patterns--principles)
10. [Implementation Guidelines](#implementation-guidelines)

---

## Executive Summary

**MyEnglish** uses a **layered MVVM-S (Model-View-ViewModel-Service)** architecture with clear separation of concerns. The system is designed for:
- **Single-user desktop app** (Flet-based UI)
- **Local data persistence** (SQLite)
- **Responsive UI** with real-time updates
- **AI-powered scoring** (ML model as reusable service)
- **Offline capability** (no required cloud calls)

**Key Design Principles:**
- ✅ **Separation of Concerns** - Each layer has single responsibility
- ✅ **Dependency Injection** - Services injected, not instantiated
- ✅ **Reusability** - Components & services reusable across screens
- ✅ **Testability** - No hard-coded dependencies, easy to mock
- ✅ **Maintainability** - Clear code structure, minimal coupling

---

## System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    UI LAYER (Flet)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Screens & Views                                  │   │
│  │  - home_view (Dashboard)                          │   │
│  │  - translate_practice_view (Translation UI)       │   │
│  │  - vocabulary_view (Flashcard UI)                 │   │
│  └──────────────────────────────────────────────────┘   │
│                           ↑↓                             │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Components (Reusable UI Widgets)                │   │
│  │  - session_summary_chart (Pie chart)             │   │
│  │  - vocabulary_summary_chart (Bar chart)          │   │
│  │  - paragraph_table (DataTable)                   │   │
│  │  - vocabulary_table (DataTable)                  │   │
│  │  - loading.py, navbar.py, footer.py              │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────┐
│               VIEW MODEL LAYER (State & Logic)           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  ViewModels (Format & Aggregate Data)            │   │
│  │  - home_vm.py                                    │   │
│  │  - translate_practice_vm.py                      │   │
│  │  - vocabulary_vm.py                              │   │
│  │  (No UI code, no direct DB access)               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────┐
│               SERVICE LAYER (Business Logic)             │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Services (Orchestrate Repositories)             │   │
│  │  - paragraph_service                             │   │
│  │  - sentence_service                              │   │
│  │  - vocabulary_service                            │   │
│  │  - translation_service (Google Translate)        │   │
│  │  - scoring_service (ML Similarity Score)         │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────┐
│              REPOSITORY LAYER (Data Access)              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Repositories (CRUD Operations)                  │   │
│  │  - repo_base.py (Abstract base class)            │   │
│  │  - paragraph_repo.py                             │   │
│  │  - sentence_repo.py                              │   │
│  │  - vocabulary_repo.py                            │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────┐
│              MODEL LAYER (Data Classes)                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Data Models (Entity Classes)                    │   │
│  │  - paragraph.py (Paragraph entity)               │   │
│  │  - sentence.py (Sentence entity)                 │   │
│  │  - vocabulary.py (Vocabulary item)                │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────┐
│                  DATABASE LAYER (SQLite)                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  - paragraph, sentence, vocabulary tables        │   │
│  │  - Auto-increment IDs, timestamps, FK constraints│   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Architecture Layers

| Layer | Responsibility | Examples |
|-------|----------------|----------|
| **UI (View)** | Display data, capture user input | Flet screens & components |
| **ViewModel** | Format data, aggregate, prepare for UI | Format dates, calculate percentages |
| **Service** | Business logic, orchestrate repos | Create paragraph, score translation |
| **Repository** | CRUD operations, database queries | `get()`, `create()`, `update()`, `delete()` |
| **Model** | Data structures, domain objects | Paragraph, Sentence, Vocabulary classes |
| **Database** | Persistent storage | SQLite tables with constraints |

---

## Database Design

### Entity Relationship Diagram (ER Diagram)

```
┌──────────────────────┐         ┌──────────────────────┐
│     Paragraph        │         │     Vocabulary       │
├──────────────────────┤         ├──────────────────────┤
│ id (PK)              │    ┌────│ id (PK)              │
│ title                │    │    │ word_en              │
│ source               │    │    │ word_vn              │
│ input_text           │    │    │ example              │
│ completion_percent   │    │    │ correct_count        │
│ average_score        │    │    │ wrong_count          │
│ status               │    │    │ date_created         │
│ date_created         │    │    │ date_updated         │
└──────────────────────┘    │    └──────────────────────┘
         │                  │
         │ 1:N              │
         │ (has many)       │
         │                  │
┌────────▼──────────────────┼──┐
│      Sentence             │  │
├───────────────────────────┤──│
│ id (PK)                   │  │
│ paragraph_id (FK)─────────┘  │
│ sentence_text                │
│ english_text                 │
│ machine_translation          │
│ user_translation             │
│ ai_score                     │
│ sequence_order               │
│ date_created                 │
└──────────────────────────────┘

Relationships:
  Paragraph 1:N Sentence (one paragraph has many sentences)
  Vocabulary is independent (no FK to Paragraph/Sentence)
```

### Database Schema (SQL)

```sql
-- Paragraph Table
CREATE TABLE paragraph (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    source TEXT,
    input_text TEXT NOT NULL,
    completion_percent REAL DEFAULT 0.0,
    average_score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'IN_PROGRESS', 'COMPLETED')),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sentence Table
CREATE TABLE sentence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paragraph_id INTEGER NOT NULL,
    sentence_text TEXT NOT NULL,
    english_text TEXT NOT NULL,
    machine_translation TEXT,
    user_translation TEXT,
    ai_score REAL,
    sequence_order INTEGER NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paragraph_id) REFERENCES paragraph(id) ON DELETE CASCADE
);

-- Vocabulary Table
CREATE TABLE vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_en TEXT NOT NULL UNIQUE,
    word_vn TEXT NOT NULL,
    example TEXT,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_sentence_paragraph_id ON sentence(paragraph_id);
CREATE INDEX idx_paragraph_status ON paragraph(status);
CREATE INDEX idx_vocabulary_word_en ON vocabulary(word_en);
```

### Data Model Classes

#### Paragraph Model
```python
class Paragraph:
    id: int
    title: str
    source: str
    input_text: str
    completion_percent: float  # 0-100%
    average_score: float       # 0-10
    status: str                # OPEN, IN_PROGRESS, COMPLETED
    date_created: datetime
    date_updated: datetime
    
    Methods:
    - to_dict() → dict
    - from_dict(data: dict) → Paragraph
    - to_row() → tuple (for DB insertion)
    - __repr__()
```

#### Sentence Model
```python
class Sentence:
    id: int
    paragraph_id: int
    sentence_text: str
    english_text: str
    machine_translation: str
    user_translation: str
    ai_score: float            # 0-10
    sequence_order: int        # 1, 2, 3...
    date_created: datetime
    
    Methods:
    - to_dict() → dict
    - from_dict(data: dict) → Sentence
    - to_row() → tuple
    - __repr__()
```

#### Vocabulary Model
```python
class Vocabulary:
    id: int
    word_en: str
    word_vn: str
    example: str
    correct_count: int
    wrong_count: int
    accuracy: float            # calculated: correct/(correct+wrong)
    date_created: datetime
    date_updated: datetime
    
    Methods:
    - to_dict() → dict
    - from_dict(data: dict) → Vocabulary
    - to_row() → tuple
    - __repr__()
```

---

## UI Architecture & Navigation

### Screen Navigation Flow

```
┌─────────────┐
│   Home      │  ← Default screen on app launch
│  (Dashboard)│
└──────┬──────┘
       │
   ┌───┴────┬──────────┐
   ▼        ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Translate│ │Vocab  │ │ Other  │
│Practice │ │Flash  │ │ Screens│
└────────┘ └────────┘ └────────┘
   │          │
   ▼          ▼
 Details   Editor
```

### Screen & Component Structure

#### 1. Home Screen (`view/screens/home_view.py`)
**Purpose:** Display dashboard with charts, tables, summary statistics

**Components:**
- Header (navbar, title)
- Paragraph Summary Chart (pie chart)
- Vocabulary Summary Chart (bar chart)
- Paragraph Table (cards/list of incomplete paragraphs)
- Vocabulary Table (all words with stats)
- Footer

**Interactions:**
- Click "Continue" on paragraph → navigate to TranslatePracticeScreen
- Click "Flashcard" → navigate to VocabularyScreen
- Chart slice click → filter paragraph table

#### 2. Translation Practice Screen (`view/screens/translate_practice_view.py`)
**Purpose:** Multi-step translation workflow

**Step 1: Input**
- Text fields: Title, Source, English Text
- Validation: max 2000 chars, min 2 sentences
- Button: "Next" → Step 2

**Step 2: Translate**
- Display current sentence
- Machine translation (read-only)
- User input field (translation)
- Optional: New words field
- Navigation: Previous / Next / Review
- Progress bar: X of Y sentences

**Step 3: Review**
- Side-by-side: User vs Machine translation
- AI Score display (0-10)
- Option to edit & rescore
- Button: "Save & Complete"

**Data Flow:**
```
Input → Create Paragraph + Sentences → Step 2 → 
Step 3 (Score) → Save → Home
```

#### 3. Vocabulary Screen (`view/screens/vocabulary_view.py`)
**Purpose:** Flashcard-based vocabulary learning

**Question Display:**
- Word (large)
- Example sentence
- 4 multiple-choice buttons (A, B, C, D)
- Statistics (correct %, attempts)

**Answer Display:**
- ✔ Correct! or ✘ Incorrect
- Correct meaning highlighted
- "Next Word" button
- Auto-advance after 2 seconds (optional)

### Component Architecture

```
view/
├── screens/
│   ├── home_view.py
│   ├── translate_practice_view.py
│   └── vocabulary_view.py
│
└── components/
    ├── header.py (Top navigation bar)
    ├── navbar.py (Side menu)
    ├── footer.py (Bottom bar)
    ├── loading.py (Loading spinner)
    ├── session_summary_chart.py (Pie chart)
    ├── vocabulary_summary_chart.py (Bar chart)
    ├── paragraph_cards.py (Reusable card)
    ├── paragraph_table.py (DataTable)
    └── vocabulary_table.py (DataTable)
```

**Component Design Strategy:**
- **Dumb Components:** Only receive props & emit events
- **Smart Components:** Connected to ViewModel, manage state
- **Reusable:** Same component used in multiple screens if applicable

---

## Layer Architecture (MVVM-S)

### Model Layer (`model/`)

**Responsibility:** Define data structures

```python
# model/paragraph.py
class Paragraph:
    def __init__(self, id, title, source, input_text, ...):
        self.id = id
        self.title = title
        ...
    
    def to_dict(self):
        """Convert to dictionary for JSON"""
    
    def to_row(self):
        """Convert to tuple for DB insert"""
    
    @classmethod
    def from_dict(cls, data):
        """Create instance from dict"""
```

**Characteristics:**
- ✅ Pure data structures
- ✅ No business logic
- ✅ Implement `to_dict()`, `from_dict()`, `to_row()`
- ✅ Have `__repr__()` for debugging

### Repository Layer (`repositories/`)

**Responsibility:** CRUD operations, database queries

```python
# repositories/repo_base.py
class BaseRepository:
    def __init__(self, db_connect):
        self.db = db_connect
    
    def create(self, model: Model) → int:
        """Insert and return ID"""
    
    def get(self, id: int) → Model:
        """Get by ID"""
    
    def update(self, model: Model) → bool:
        """Update record"""
    
    def delete(self, id: int) → bool:
        """Delete record"""
    
    def all(self) → List[Model]:
        """Get all records"""
    
    def filter(self, **kwargs) → List[Model]:
        """Filter by conditions"""
```

**Characteristics:**
- ✅ Generic base class `BaseRepository`
- ✅ Subclass for each entity (ParagraphRepository, etc.)
- ✅ No business logic, only DB queries
- ✅ Transaction-safe (use context managers)
- ✅ Connection pooling/singleton

### Service Layer (`service/`)

**Responsibility:** Business logic, orchestrate repositories

```python
# service/paragraph_service.py
class ParagraphService:
    def __init__(self, paragraph_repo, sentence_repo):
        self.para_repo = paragraph_repo
        self.sent_repo = sentence_repo
    
    def create_with_sentences(self, title, source, text):
        """
        Business Logic:
        1. Create paragraph
        2. Split text into sentences
        3. Create sentence records
        4. Return paragraph with sentences
        """
        para = Paragraph(title=title, source=source, ...)
        para_id = self.para_repo.create(para)
        
        sentences = text.split('.')  # Simple split
        for i, sent in enumerate(sentences):
            s = Sentence(paragraph_id=para_id, text=sent, ...)
            self.sent_repo.create(s)
        
        return self.para_repo.get(para_id)
```

**Characteristics:**
- ✅ Orchestrate multiple repositories
- ✅ Complex business logic
- ✅ No UI code, no database code
- ✅ Easy to test (mock repositories)
- ✅ Single responsibility per service

### ViewModel Layer (`view_model/`)

**Responsibility:** Format data for UI, handle UI logic

```python
# view_model/home_vm.py
class HomeViewModel(ObserverBase):
    def __init__(self, paragraph_service, vocabulary_service):
        super().__init__()
        self.para_service = paragraph_service
        self.vocab_service = vocabulary_service
    
    @property
    def paragraph_stats(self):
        """Formatted paragraph statistics"""
        paras = self.para_service.get_all()
        return {
            'completed': len([p for p in paras if p.status == 'COMPLETED']),
            'in_progress': len([...]),
            'open': len([...])
        }
    
    @property
    def chart_data(self):
        """Prepare pie chart data"""
        stats = self.paragraph_stats
        return [
            {'name': 'Completed', 'value': stats['completed']},
            ...
        ]
```

**Characteristics:**
- ✅ Formats data (dates, percentages, currency, etc.)
- ✅ Aggregates multiple service calls
- ✅ No direct database access
- ✅ No UI code (no Flet imports)
- ✅ Observable: notify UI on data changes

### View Layer (`view/screens/`, `view/components/`)

**Responsibility:** Display UI, capture user input

```python
# view/screens/home_view.py
class HomeScreen(UserControl):
    def __init__(self, home_vm: HomeViewModel):
        super().__init__()
        self.vm = home_vm
        self.vm.attach(self.on_vm_changed)  # Observer pattern
    
    def build(self):
        return Column([
            ParagraphSummaryChart(self.vm),
            VocabularySummaryChart(self.vm),
            ParagraphTable(self.vm),
            VocabularyTable(self.vm)
        ])
    
    def on_vm_changed(self):
        """Called when ViewModel data changes"""
        self.update()
```

**Characteristics:**
- ✅ Pure UI code (Flet components)
- ✅ Read-only from ViewModel
- ✅ Cannot modify ViewModel directly
- ✅ All data flows through ViewModel
- ✅ Observable (updates on ViewModel change)

---

## Component Design

### Chart Components

#### Paragraph Summary Chart (Pie Chart)
```
Data Input:
  {
    completed: 3,
    in_progress: 2,
    open: 1,
    average_score: 7.5
  }

Display:
  Pie chart with 3 slices
  - Completed (green, 50%)
  - In-progress (yellow, 33%)
  - Open (gray, 17%)
  
  Legend: "Average Score: 7.5/10"
```

#### Vocabulary Summary Chart (Bar Chart)
```
Data Input:
  {
    Feb 9: 5 words,
    Feb 8: 12 words,
    Feb 7: 8 words,
    ...
  }

Display:
  Bar chart, X-axis: dates, Y-axis: word count
  Hover tooltip: Date + count
  
  Summary: "Total: 127 words"
```

### Table Components

#### Paragraph Table
```
Columns:
  - Title (searchable)
  - Source (sortable)
  - Completion % (sortable, numeric)
  - Average Score (sortable, numeric)
  - Date Created (sortable)
  - Action (button)

Interactions:
  - Click column header → sort
  - Type in search field → filter by title
  - Click "Continue" → navigate to TranslatePracticeScreen

Data Format:
  List[{title, source, completion_percent, average_score, date_created, id}]
```

#### Vocabulary Table
```
Columns:
  - Word (English, searchable)
  - Meaning (Vietnamese)
  - Example (truncated if long)
  - Correct (numeric)
  - Wrong (numeric)
  - Accuracy % (calculated)

Interactions:
  - Click column header → sort
  - Type in search → filter by word
  - Click row → edit form (modal)
  - Delete button → confirm & delete

Data Format:
  List[{word_en, word_vn, example, correct_count, wrong_count, accuracy}]
```

---

## Data Flow Diagrams

### Translation Practice Data Flow

```
User Input (Title, Source, Text)
    ↓
TranslatePracticeScreen
    ↓
TranslatePracticeViewModel.create_paragraph()
    ↓
ParagraphService.create_with_sentences()
    ├→ ParagraphRepository.create()
    └→ SentenceRepository.create() × N
    ↓
Return Paragraph with Sentences
    ↓
Display Step 2 (Translate sentences)
    ↓
User inputs translation for each sentence
    ↓
Click "Review Translations"
    ↓
Display Step 3 with AI Scores
    ├→ For each sentence:
    │   ScoringService.score(user_text, machine_text)
    │   ↓ returns 0-10 score
    ↓
User clicks "Save & Complete"
    ↓
Update Paragraphs & Sentences
    ├→ SentenceRepository.update() × N
    └→ ParagraphRepository.update()
    ↓
Add New Vocabulary Words
    ├→ VocabularyService.add_words()
    └→ VocabularyRepository.create() × M
    ↓
Update Dashboard
    ↓
Navigate to Home Screen
```

### Vocabulary Flashcard Data Flow

```
User clicks "Vocabulary Flashcard"
    ↓
VocabularyScreen.build()
    ↓
VocabularyViewModel.get_random_word()
    ├→ VocabularyRepository.get_all()
    └→ Random selection + shuffle options
    ↓
Display question (word + meaning options)
    ↓
User selects answer
    ↓
VocabularyScreen.on_answer_selected()
    ↓
VocabularyService.record_answer()
    ├→ Check if correct
    └→ VocabularyRepository.update(correct_count or wrong_count)
    ↓
Display feedback (✔ or ✘)
    ↓
Auto-advance after 2 seconds
    ↓
Repeat from "Display question"
```

### Dashboard Data Flow

```
User navigates to Home Screen
    ↓
HomeScreen.build()
    ↓
HomeViewModel loads all data:
    ├→ ParagraphService.get_all()
    ├→ VocabularyService.get_all()
    ├→ ParagraphService.get_stats() (for charts)
    └→ VocabularyService.get_daily_stats()
    ↓
ViewModel aggregates data:
    ├→ Calculate completion percentages
    ├→ Calculate accuracy percentages
    ├→ Format dates
    └→ Prepare chart data
    ↓
Render components:
    ├→ ParagraphSummaryChart
    ├→ VocabularySummaryChart
    ├→ ParagraphTable
    └→ VocabularyTable
    ↓
Dashboard displayed
    ↓
ObserverBase notifies View on any ViewModel change
```

---

## API & Interface Specifications

### Service Interfaces

#### IParagraphService
```python
class ParagraphService:
    def create_with_sentences(title: str, source: str, text: str) → Paragraph
    def get_all() → List[Paragraph]
    def get_by_id(id: int) → Paragraph
    def update(paragraph: Paragraph) → bool
    def delete(id: int) → bool
    def get_incomplete() → List[Paragraph]
    def get_stats() → Dict[str, int]  # {completed, in_progress, open}
```

#### ISentenceService
```python
class SentenceService:
    def get_by_paragraph(paragraph_id: int) → List[Sentence]
    def update_translation(sentence_id: int, translation: str) → bool
    def update_score(sentence_id: int, score: float) → bool
```

#### IVocabularyService
```python
class VocabularyService:
    def create(word_en: str, word_vn: str, example: str) → Vocabulary
    def get_all() → List[Vocabulary]
    def get_random(count: int = 1) → List[Vocabulary]
    def record_correct_answer(vocabulary_id: int) → bool
    def record_wrong_answer(vocabulary_id: int) → bool
    def search(keyword: str) → List[Vocabulary]
    def get_daily_stats(days: int = 10) → Dict[date, int]
```

#### IScoringService
```python
class ScoringService:
    def score(user_text: str, reference_text: str) → float  # 0-10
    # Singleton: Score is computationally expensive (ML model)
```

#### ITranslationService
```python
class TranslationService:
    def translate(text: str, src_lang: str = 'en', dst_lang: str = 'vi') → str
    # Note: May fail gracefully (returns empty string or original text)
```

### Repository Interfaces

#### IBaseRepository (Generic)
```python
class BaseRepository:
    def create(model: Model) → int  # Returns inserted ID
    def get(id: int) → Optional[Model]
    def get_or_raise(id: int) → Model  # Raises exception if not found
    def update(model: Model) → bool
    def delete(id: int) → bool
    def all() → List[Model]
    def filter(**kwargs) → List[Model]  # e.g., filter(status='COMPLETED')
    def count() → int
```

#### IParagraphRepository
```python
class ParagraphRepository(BaseRepository):
    # Inherited: create, get, update, delete, all, filter, count
    # Custom:
    def get_incomplete() → List[Paragraph]
    def get_by_status(status: str) → List[Paragraph]
```

#### ISentenceRepository
```python
class SentenceRepository(BaseRepository):
    def get_by_paragraph(paragraph_id: int) → List[Sentence]
    def delete_by_paragraph(paragraph_id: int) → int  # Returns count deleted
```

#### IVocabularyRepository
```python
class VocabularyRepository(BaseRepository):
    def get_by_word(word_en: str) → Optional[Vocabulary]
    def search(keyword: str) → List[Vocabulary]
```

---

## Design Patterns & Principles

### 1. **Repository Pattern**
**Purpose:** Encapsulate data access logic

```python
# Instead of:
db = sqlite3.connect('app.db')
db.execute("SELECT * FROM paragraph WHERE id = ?", (1,))

# Use:
para_repo = ParagraphRepository(db_connect)
para = para_repo.get(1)  # Clean API
```

**Benefits:** Easy to mock for testing, swap implementations

---

### 2. **Service Layer Pattern**
**Purpose:** Orchestrate complex business logic

```python
# Instead of spreading logic across the UI:
# Use a service to encapsulate logic:

class ParagraphService:
    def create_with_sentences(self, title, source, text):
        # 1. Validate input
        # 2. Create paragraph
        # 3. Split sentences
        # 4. Create sentence records
        # 5. Return result
```

**Benefits:** Reusable, testable, single responsibility

---

### 3. **Dependency Injection**
**Purpose:** Decouple components, enable testing

```python
# BAD: Hard-coded dependencies
class TranslatePracticeViewModel:
    def __init__(self):
        self.para_service = ParagraphService()  # Can't test easily

# GOOD: Injected dependencies
class TranslatePracticeViewModel:
    def __init__(self, para_service: ParagraphService):
        self.para_service = para_service  # Easy to mock
```

**Benefits:** Testable, flexible, prevents tight coupling

---

### 4. **Observer Pattern**
**Purpose:** Notify UI when ViewModel data changes

```python
# ViewModel extends ObserverBase
class HomeViewModel(ObserverBase):
    def load_data(self):
        self.data = ...
        self.notify_observers()  # Notify UI to refresh

# View attaches itself as observer
class HomeScreen(UserControl):
    def __init__(self, vm):
        self.vm = vm
        self.vm.attach(self.on_vm_changed)
    
    def on_vm_changed(self):
        self.update()  # Re-render
```

**Benefits:** Reactive UI, decoupled, real-time updates

---

### 5. **Singleton Pattern (Thread-Safe)**
**Purpose:** Ensure only one instance of expensive resources

```python
# DBConnect singleton (thread-safe)
class DBConnect:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

# ScoringService singleton (ML model is expensive)
class ScoringService:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_model(self):
        # Load model only once
        if self._model is None:
            self._model = load_transformer_model()
        return self._model
```

**Benefits:** Memory efficient, thread-safe, consistent state

---

### 6. **Model-to-Row Consistency**
**Purpose:** Ensure data integrity between model and database

```python
class Paragraph:
    def __init__(self, ...):
        self.id = id
        self.title = title
        self.source = source
    
    def to_row(self):
        # MUST match column order in repository!
        return (self.id, self.title, self.source, ...)

class ParagraphRepository(BaseRepository):
    columns = ['id', 'title', 'source', ...]  # MUST match to_row()!
    
    def create(self, para: Paragraph):
        row = para.to_row()  # Ensure order matches
        self.db.execute(f"INSERT INTO paragraph VALUES {row}")
```

**Benefits:** Prevents silent data corruption, easy debugging

---

## Implementation Guidelines

### Code Organization Best Practices

#### 1. **Imports Organization**
```python
# Standard library first
import sqlite3
import threading
from datetime import datetime

# Third-party libraries
from flet import *

# Local imports
from repository.paragraph_repo import ParagraphRepository
from model.paragraph import Paragraph
```

#### 2. **File Structure**
```
project/
├── model/              # Data classes (pure data)
│   ├── paragraph.py
│   ├── sentence.py
│   └── vocabulary.py
│
├── repositories/       # Data access (CRUD)
│   ├── repo_base.py
│   ├── paragraph_repo.py
│   ├── sentence_repo.py
│   └── vocabulary_repo.py
│
├── service/           # Business logic
│   ├── paragraph_service.py
│   ├── sentence_service.py
│   ├── vocabulary_service.py
│   ├── translation_service.py
│   └── scoring_service.py
│
├── view_model/        # UI logic (data formatting)
│   ├── home_vm.py
│   ├── translate_practice_vm.py
│   └── vocabulary_vm.py
│
└── view/             # UI (Flet)
    ├── screens/
    │   ├── home_view.py
    │   ├── translate_practice_view.py
    │   └── vocabulary_view.py
    └── components/
        ├── paragraph_table.py
        └── vocabulary_table.py
```

#### 3. **Error Handling Strategy**
```python
# Repository layer: Raise exceptions (propagate DB errors)
def get(self, id: int) -> Optional[Model]:
    try:
        cursor = self.db.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception(f"Record not found: {self.table_name}.id={id}")
        return self.model_class.from_row(row)
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise

# Service layer: Handle exceptions, provide user-friendly messages
def create_with_sentences(self, title, source, text):
    try:
        # Business logic
    except ValueError as e:
        return {'success': False, 'error': f"Invalid input: {e}"}
    except Exception as e:
        return {'success': False, 'error': 'Server error. Try again.'}

# ViewModel: Format error messages for UI
def on_create_error(self, error: str):
    self.error_message = error
    self.notify_observers()
```

#### 4. **Testing Strategy**
```python
# Unit test: Test service with mocked repository
@mock('repositories.paragraph_repo.ParagraphRepository')
def test_create_with_sentences(mock_repo):
    service = ParagraphService(mock_repo)
    result = service.create_with_sentences('Title', 'Source', 'Sent1. Sent2.')
    
    assert result.title == 'Title'
    mock_repo.create.assert_called()

# Integration test: Test with in-memory SQLite
def test_paragraph_flow():
    db = sqlite3.connect(':memory:')  # In-memory DB
    repo = ParagraphRepository(db)
    
    para = Paragraph(title='Test', ...)
    id = repo.create(para)
    result = repo.get(id)
    
    assert result.title == 'Test'
```

#### 5. **Performance Considerations**
```python
# Query optimization
class VocabularyRepository:
    def get_all(self):
        # Bad: N+1 query problem
        words = self.db.execute("SELECT * FROM vocabulary")
        for word in words:
            accuracy = self.db.execute(...)  # Repeated queries!
        
        # Good: Single query with calculated field
        words = self.db.execute("""
            SELECT id, word_en, correct_count, wrong_count,
                   CAST(correct_count AS FLOAT) / 
                   (correct_count + wrong_count) as accuracy
            FROM vocabulary
        """)

# Lazy loading (Model loading)
class ScoringService:
    def __init__(self):
        self._model = None  # Not loaded yet
    
    def _get_model(self):
        # Load only when needed
        if self._model is None:
            print("Loading ML model... (first time only)")
            self._model = SentenceTransformer('...')
        return self._model
    
    def score(self, text1, text2):
        model = self._get_model()  # Lazy load
        return model.similarity(text1, text2)
```

#### 6. **Documentation Requirements**
```python
class ParagraphService:
    """Service for managing translation practice paragraphs.
    
    Responsibilities:
    - Create paragraphs with automatic sentence splitting
    - Orchestrate paragraph and sentence repositories
    - Calculate paragraph statistics
    
    Example:
        service = ParagraphService(para_repo, sent_repo)
        para = service.create_with_sentences(
            title='BBC Article',
            source='BBC News',
            text='Climate change affects... The world needs...'
        )
        para.completion_percent  # 0.0 (no translations yet)
    """
    
    def create_with_sentences(self, title: str, source: str, text: str) -> Paragraph:
        """Create a paragraph with automatic sentence splitting.
        
        Args:
            title: Paragraph title (max 200 chars)
            source: Reference source (optional)
            text: English paragraph (min 2 sentences)
        
        Returns:
            Paragraph instance with sentences populated
        
        Raises:
            ValueError: If text has < 2 sentences
        """
```

---

## Summary & Next Steps

### Design Strengths
- ✅ Clear layering: UI → ViewModel → Service → Repository → DB
- ✅ Loose coupling: Easy to test, modify, extend
- ✅ MVVM-S pattern: Industry-standard, scalable
- ✅ Reusable components: Chart, table components shared across screens
- ✅ Observer pattern: Reactive UI updates on data changes
- ✅ Singleton pattern: Efficient resource management

### Ready for Phase 4 Development
- ✅ Database schema defined
- ✅ Data models specified
- ✅ Service interfaces documented
- ✅ UI navigation flows planned
- ✅ Data flows diagrammed
- ✅ Design patterns identified
- ✅ Code organization guidelines provided

### Key Implementation Checklist
- [ ] Create BaseRepository (abstract class)
- [ ] Implement ParagraphRepository, SentenceRepository, VocabularyRepository
- [ ] Create Paragraph, Sentence, Vocabulary models
- [ ] Implement services (ParagraphService, VocabularyService, etc.)
- [ ] Create ViewModels (HomeViewModel, TranslatePracticeViewModel, etc.)
- [ ] Build UI screens (HomeScreen, TranslatePracticeScreen, etc.)
- [ ] Hook up Observer pattern (ViewModel → View)
- [ ] Test each layer in isolation
- [ ] Integration testing (end-to-end flows)

---

**END OF ARCHITECTURE & DESIGN DOCUMENTATION**

*Date Created: February 9, 2026*  
*SDLC Phase: Phase 3 - Design (Draft)*  
*Next Phase: Phase 4 - Development (Implementation)*
