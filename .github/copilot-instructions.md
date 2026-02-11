# MyEnglish - AI Coding Agent Instructions

## Project Overview

Flet-based desktop app for English learning with AI-powered semantic scoring. Data flow: **UI (Flet) → ViewModel → Service → Repository → SQLite**.

## Current Features

### 1. Home Dashboard (`view/screens/home_view.py`)
- **Session Summary Chart**: Pie chart showing Completed/In-Progress/Open sessions with average score
- **Vocabulary Summary Chart**: Bar chart displaying vocabulary learned per day (last 10 days)
- **Session Cards**: List of incomplete sessions with "Continue Session" button
- **Vocabulary Table**: DataTable listing all words with word/meaning/example columns

### 2. Translation Practice (`view/screens/translate_practice_view.py`)
- **Step 1 - Input**: Enter session title, reference source, and English paragraph
- **Step 2 - Translate**: Sentence-by-sentence translation input with optional new words field
- **Step 3 - Review**: Side-by-side comparison of user vs machine translation with AI similarity score
- Uses `ScoringService` to compute semantic similarity between translations

### 3. Vocabulary Flashcard (`view/screens/vocabulary_view.py`)
- **Question Mode**: Shows word + example sentence, user picks correct meaning from multiple choices
- **Answer Result**: Displays correct/incorrect feedback with ✔/✘ indicators
- Tracks `correct_count` and `wrong_count` per vocabulary item

## Architecture (MVVM-S)

| Layer | Location | Responsibility |
|-------|----------|----------------|
| **Model** | `model/` | Data classes with `to_dict()`, `from_dict()`, `to_row()`, `__repr__()` |
| **View** | `view/screens/`, `view/components/` | Flet UI; screens are full pages, components are reusable widgets |
| **ViewModel** | `view_model/` | Bridges UI↔Service; handles formatting/aggregation, no UI code |
| **Service** | `service/` | Business logic; instantiates repositories internally |
| **Repository** | `repositories/` | DB access via `BaseRepository` (CRUD: `create`, `get`, `update`, `delete`, `all`, `filter`) |

## Key Design Patterns

- **Singleton (thread-safe)**: `DBConnect` and `ScoringService` use `_lock` + `__new__()` pattern
- **Base Repository**: Subclass `BaseRepository`, define `table_name`, `columns`, `model_class`
- **Service Injection**: `MainAppLayout.__init__()` instantiates all services → passes to ViewModels
- **Observer**: `shared/observer_base.py` provides `ObserverBase` for reactive state

## Core Entities

- **Paragraph** (`model/paragraph.py`): Learning session container with title, input text, completion %, score
- **Sentence** (`model/sentence.py`): Individual sentence within paragraph; stores user/machine translations and AI score
- **Vocabulary** (`model/vocabulary.py`): Word entries with meaning, example, correct/wrong counts

## Data Flow Example: Translation Scoring

1. User submits translation in `TranslatePracticeScreen`
2. `TranslatePracticeViewModel` → `SentenceService.update_sentence()`
3. `ScoringService.score(user_text, machine_text)` computes semantic similarity
4. Score persisted via `SentenceRepository.update()`

## Development Commands

```bash
flet run main.py          # Dev mode with hot-reload
flet pack main.py         # Build standalone .exe
pytest tests/             # Run tests (uses in-memory SQLite)
```

## Project Conventions

- **Navigation**: `config.py` defines `Screen` enum (HOME, TRANSLATE, VOCABULARY)
- **Database**: SQLite with `PRAGMA foreign_keys = ON`; schema in `repositories/db_init.py`
- **ML Model**: `paraphrase-multilingual-MiniLM-L12-v2` loaded lazily in `ScoringService._get_model()`
- **Vietnamese comments**: Preserve when editing; codebase is bilingual

## Adding a New Feature

1. **Model**: Add fields to class, update `to_row()` order to match DB columns
2. **Repository**: Extend `BaseRepository`; add custom queries if needed
3. **Service**: Create service class, instantiate repo internally
4. **ViewModel**: Add data transformation methods
5. **View**: Create screen/component, inject ViewModel
6. **Wire up**: Add to `MainAppLayout.__init__()` and `switch_screen()`

## Common Pitfalls

- **Model↔DB sync**: `to_row()` column order must match `columns` list in repository
- **Foreign keys**: Deleting `Paragraph` cascades to delete child `Sentence` records
- **Thread safety**: `DBConnect._lock` guards all DB operations; `ScoringService._model_lock` guards ML model
- **UI freeze**: ML scoring is synchronous; large batch operations may block

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point; initializes DB, launches Flet |
| `view/main_app_layout.py` | Main orchestrator; service injection point |
| `repositories/repo_base.py` | Generic CRUD base class |
| `service/scoring_service.py` | ML similarity scoring (singleton) |
| `repositories/db_init.py` | Database schema definitions |
| `tests/test_paragraph_repo.py` | Test pattern example using in-memory DB |
