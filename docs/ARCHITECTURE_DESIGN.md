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
8. [Summary & Next Steps](#summary--next-steps)

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
│                    UI LAYER (Flet)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Screens & Views                                 │   │
│  │  - home_view (Dashboard)                         │   │
│  │  - translate_practice_view (Translation UI)      │   │
│  │  - vocabulary_view (Flashcard UI)                │   │
│  └──────────────────────────────────────────────────┘   │
│                           ↑↓                            │
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
│               VIEW MODEL LAYER (State & Logic)          │
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
│               SERVICE LAYER (Business Logic)            │
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
│              REPOSITORY LAYER (Data Access)             │
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
│              MODEL LAYER (Data Classes)                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Data Models (Entity Classes)                    │   │
│  │  - paragraph.py (Paragraph entity)               │   │
│  │  - sentence.py (Sentence entity)                 │   │
│  │  - vocabulary.py (Vocabulary item)               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↑↓
┌─────────────────────────────────────────────────────────┐
│                  DATABASE LAYER (SQLite)                │
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

**Database Notes:**
- 3 tables: Paragraph, Sentence, Vocabulary
- Paragraph ↔ Sentence: 1:N relationship (CASCADE delete)
- Vocabulary: Independent table
- Detailed schema will be implemented in Phase 4

---

## UI Architecture & Navigation

### Screen Navigation Flow

```
┌─────────────┐
│   Home      │  ← Default screen on app launch
│  (Dashboard)│
└──────┬──────┘
       │
   ┌───┴──────┬──────────┐
   ▼          ▼          ▼
┌─────────┐ ┌────────┐ ┌────────┐
│Translate│ │Vocab   │ │ Other  │
│Practice │ │Flash   │ │ Screens│
└─────────┘ └────────┘ └────────┘
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
