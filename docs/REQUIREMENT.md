# MyEnglish - Software Requirements Specification (SRS)

**Document Version:** 1.0  
**Date:** February 9, 2026  
**Status:** Approved ✅  
**Phase:** SDLC Phase 1 - Planning & Requirements

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Charter](#project-charter)
3. [Stakeholders & Vision](#stakeholders--vision)
4. [Scope & Objectives](#scope--objectives)
5. [Functional Requirements](#functional-requirements)
6. [Use Cases](#use-cases)
7. [Non-Functional Requirements](#non-functional-requirements)
8. [Constraints & Assumptions](#constraints--assumptions)
9. [Risk Register](#risk-register)
10. [Future Development](#future-development)
11. [Glossary](#glossary)

---

## Executive Summary

**MyEnglish** is a desktop application designed to help **individual English learners** practice translation and vocabulary building through an interactive, AI-powered learning system.

The MVP (Minimum Viable Product) will focus on **3 core features**:
1. **Translation Practice** - Paragraph-based translation with semantic AI scoring
2. **Vocabulary Flashcard** - Multiple-choice vocabulary learning
3. **Dashboard & Statistics** - Progress tracking and learning analytics

**Target Release:** v1.0 (Stable, production-ready)  
**Timeline:** 1 developer, flexible duration (learning project)  
**Tech Stack:** Python + Flet + SQLite + sentence-transformers

---

## Project Charter

### Project Name
**MyEnglish - AI-Powered English Learning Desktop Application**

### Project Purpose
Enable individual English learners to:
- Practice translation with immediate AI-powered feedback
- Build vocabulary through interactive flashcards
- Track learning progress with visual statistics

### Project Vision
*"Make English learning accessible, interactive, and measurable through AI-powered feedback and personalized practice."*

### Project Objectives (SMART)

| # | Objective | Success Measure |
|---|-----------|-----------------|
| 1 | Deliver v1.0 stable release | Zero critical bugs, all tests pass |
| 2 | Implement 3 core features | Translation, Vocabulary, Dashboard working |
| 3 | Achieve 80%+ test coverage | All layers tested (Model, Repo, Service, VM) |
| 4 | Enable offline learning | App works without internet |
| 5 | Support progress tracking | Users can see learning statistics |

### Project Authority
- **Project Owner/Product Owner:** HaiDT
- **Development Team:** 1 developer
- **Stakeholders:** Individual English learners

---

## Stakeholders & Vision

### Primary Stakeholders

| Stakeholder | Role | Interest | Influence |
|------------|------|---------|-----------|
| **Individual English Learner** | End User | Learn English effectively, see progress | HIGH |
| **Project Owner** | Product Manager | Deliver high-quality, complete product | HIGH |
| **Developer** | Implementation, Quality | Code quality, SDLC compliance | HIGH |

### User Persona: "Linh - Determined English Learner"

```
Name: Linh (25 years old)
Goal: Improve English translation skills for career advancement
Pain Points:
  - Want real-time feedback on translation accuracy
  - Need to track vocabulary learning progress
  - Prefer offline learning (can't always connect internet)
  - Wants professional, easy-to-use interface

Expected Behaviors:
  - Uses app 3-4 times per week for 30-45 minutes
  - Practices translation with news articles or business materials
  - Reviews vocabulary before sleep
  - Likes seeing progress charts & statistics
```

---

## Scope & Objectives

### MVP Features

#### Feature 1: Translation Practice Module
- User inputs English paragraph (title, source reference, text)
- System automatically splits text into sentences
- User translates each sentence to Vietnamese
- System uses ML (sentence-transformers) to score semantic similarity (0-10)
- User reviews all translations with AI scores
- Paragraph progress saved (completion %, average score)
- User can continue incomplete paragraphs

#### Feature 2: Vocabulary Flashcard Module
- Display random vocabulary word with example sentence
- User selects correct meaning from 4 multiple choice options
  - 1 correct answer
  - 3 randomly selected distractors
- System provides immediate feedback (✔ Correct / ✘ Incorrect)
- Track per-word statistics: correct_count, wrong_count
- User can review vocabulary learned

#### Feature 3: Dashboard & Statistics
**Home Screen Components:**
- **Paragraph Summary Chart** (Pie chart)
  - Completed paragraphs
  - In-progress paragraphs
  - Open paragraphs
  - Average score across all paragraphs

- **Vocabulary Summary Chart** (Bar chart)
  - Words learned per day (last 10 days)
  - Total words in system

- **Paragraph Table**
  - Table displaying all incomplete paragraphs
  - Columns: Title, Source, Completion %, Average Score, Date Created
  - "Continue" button for each paragraph
  - Sortable and searchable columns

- **Vocabulary Table**
  - All vocabulary entries (word, meaning, example)
  - Correct/wrong counts
  - Option to edit/delete vocabulary items

## Functional Requirements

### FR-1: Translation Practice

#### FR-1.1: Create New Paragraph
**User Story:**  
*"As a learner, I want to start a new translation practice paragraph so that I can practice translating English texts."*

**Acceptance Criteria:**
- [ ] User can input paragraph title (text input, required)
- [ ] User can input reference source (text input, optional)
- [ ] User can paste/input English text (large text area, required)
- [ ] Text must contain at least 2 sentences
- [ ] Input form validates data before submission
- [ ] Paragraph saved to SQLite with timestamp

**Functional Details:**
```
Input:
  - Title: "Business Email Translation"
  - Source: "Harvard Business Review"
  - Text: "Dear Mr. Johnson. Thank you for your interest. 
           We are excited to work with you."

Process:
  1. Split text into sentences
  2. Create Paragraph record (status=IN_PROGRESS)
  3. Create Sentence records (one per sentence)

Output:
  - Paragraph created with 2 sentences
  - User redirected to Step 2 (Translation input) for that paragraph
```

#### FR-1.2: Translate Sentences
**User Story:**  
*"As a learner, I want to translate each sentence one by one so that I can work at my own pace."*

**Acceptance Criteria:**
- [ ] Display original English sentence
- [ ] Display Vietnamese translation (auto-generated by Google Translate)
- [ ] Text area for user to input their own translation
- [ ] Optional field for new vocabulary encountered
- [ ] User can move to next/previous sentence
- [ ] User can skip sentence & continue later
- [ ] Progress bar shows completion percentage
- [ ] "Review Translations" button moves to Step 3

**Functional Details:**
```
Display (for each sentence):
  - English sentence: "Thank you for your interest."
  - Machine translation: "Cảm ơn bạn quan tâm."
  - Input field: [User enters Vietnamese translation]
  - New words field: [comma-separated list, optional]

Navigation:
  - Previous / Next buttons
  - Skip & continue
  - Progress: 1 of 3 sentences
```

#### FR-1.3: AI Scoring & Review
**User Story:**  
*"As a learner, I want to see AI feedback on my translation so that I can understand accuracy."*

**Acceptance Criteria:**
- [ ] Display user translation, machine translation, and AI score (0-10)
- [ ] User can edit translation & rescore
- [ ] Paragraph completion percentage updated
- [ ] Average paragraph score calculated
- [ ] "Save & Exit" or "Continue Practicing" button
- [ ] Paragraph marked as COMPLETED when all translated

**Functional Details:**
```
Scoring Algorithm:
  score = SemanticSimilarity(user_translation, machine_translation)
  returns: float 0.0 to 10.0
  
  Example:
    User: "Cảm ơn bạn để quan tâm"
    Machine: "Cảm ơn bạn quan tâm"
    Score: 8.5/10 (Minor grammar difference)
```

#### FR-1.4: New Words Auto-Addition
**User Story:**  
*"As a learner, I want to add new words I encounter to my vocabulary so that I can study them later."*

**Acceptance Criteria:**
- [ ] During Step 2, user can input new words (optional field)
- [ ] On review (Step 3), system extracts new words
- [ ] System auto-translates words using Google Translate
- [ ] Words added to Vocabulary table automatically
- [ ] Avoid duplicates (check if word already exists)
- [ ] User notified: "3 new words added!"

**Functional Details:**
```
Input: "proficiency, leverage, stakeholder"

Process:
  1. Split by comma
  2. For each word:
     - Check if exists in Vocabulary
     - If new: auto-translate to Vietnamese
     - Create Vocabulary record

Output: 3 new vocabulary items created
```

---

### FR-2: Vocabulary Flashcard

#### FR-2.1: Display Flashcard Question
**User Story:**  
*"As a learner, I want to see a vocabulary word with an example so that I can understand context."*

**Acceptance Criteria:**
- [ ] Randomly select vocabulary word from database
- [ ] Display word (large, prominent)
- [ ] Display example sentence (showing word usage)
- [ ] Display 4 multiple choice options:
  - 1 correct meaning
  - 3 random incorrect meanings (distractors)
- [ ] Options labeled: A, B, C, D
- [ ] "Skip" button (move to next word without answering)
- [ ] Word statistics displayed (correct %, attempted count)

**Functional Details:**
```
Example Display:

WORD: "proficiency"

EXAMPLE: "Her proficiency in English helped her get the job."

Which meaning is correct?
A) Lack of knowledge
B) High level of skill
C) Slow progress
D) Lack of confidence

Stats: Correct: 5/7 attempts (71%)
```

#### FR-2.2: Answer & Feedback
**User Story:**  
*"As a learner, I want immediate feedback on my answer so that I learn from mistakes."*

**Acceptance Criteria:**
- [ ] User selects an answer (A, B, C, or D)
- [ ] System checks if correct
- [ ] Show feedback:
  - ✔ Green highlight: Correct!
  - ✘ Red highlight: Incorrect
- [ ] Display correct answer (even if wrong)
- [ ] Display correct_count & wrong_count update
- [ ] "Next Word" button appears
- [ ] System auto-advances after 2 seconds (optional)

**Functional Details:**
```
User selects: B) High level of skill
Response: ✔ CORRECT! Proficiency means expert skill.

Stats Updated:
  - correct_count: 6 (was 5)
  - wrong_count: 1 (same)
  - Accuracy: 6/7 = 85.7%
```

#### FR-2.3: Statistics Tracking
**User Story:**  
*"As a learner, I want to see my vocabulary learning statistics so that I can track progress."*

**Acceptance Criteria:**
- [ ] For each vocabulary item, track:
  - correct_count (integer)
  - wrong_count (integer)
  - accuracy = correct_count / (correct_count + wrong_count) %
- [ ] Statistics persist in database
- [ ] Statistics updated immediately on answer
- [ ] Statistics visible in Dashboard (summary chart)

---

### FR-3: Dashboard & Statistics

#### FR-3.1: Paragraph Summary Chart
**User Story:**  
*"As a learner, I want to see a pie chart of my paragraphs so that I can track progress."*

**Acceptance Criteria:**
- [ ] Pie chart displaying:
  - Completed paragraphs (count & %)
  - In-progress paragraphs (count & %)
  - Open paragraphs (count & %)
- [ ] Show average score across all completed paragraphs
- [ ] Color coding:
  - 🟢 Green: Completed
  - 🟡 Yellow: In-progress
  - 🔴 Gray: Open (not started)
- [ ] Click on slice → filter paragraph list
- [ ] Update in real-time as paragraphs progress

#### FR-3.2: Vocabulary Summary Chart
**User Story:**  
*"As a learner, I want to see a bar chart of vocabulary learned per day so that I can see trends."*

**Acceptance Criteria:**
- [ ] Bar chart showing:
  - X-axis: Last 10 days
  - Y-axis: Number of new words added that day
- [ ] Each bar labeled with date & count
- [ ] Quick view: "Total words: 127"
- [ ] Update daily as words are added
- [ ] Responsive to window sizing

#### FR-3.3: Paragraph Table
**User Story:**  
*"As a learner, I want to see all my incomplete paragraphs in a table so that I can easily find and continue where I left off."*

**Acceptance Criteria:**
- [ ] Display table for all IN_PROGRESS & OPEN paragraphs
- [ ] Table columns:
  - Paragraph title (clickable/searchable)
  - Source reference
  - Completion percentage (visual progress bar or number)
  - Average score (if any)
  - Date created
  - Action button: "Continue"
- [ ] "Continue" button → jump to paragraph
- [ ] Sort by: Title, Source, Completion %, Score, Date
- [ ] Search/filter by paragraph title
- [ ] Pagination if many paragraphs (e.g., 10 per page, next/previous buttons)

#### FR-3.4: Vocabulary Table
**User Story:**  
*"As a learner, I want to see all my vocabulary words so that I can manage them."*

**Acceptance Criteria:**
- [ ] DataTable with columns:
  - Word (English)
  - Meaning (Vietnamese)
  - Example sentence
  - Correct count
  - Wrong count
  - Accuracy %
- [ ] Sortable columns (click header)
- [ ] Searchable (search by word)
- [ ] Inline edit & delete:
  - Edit: Click row → edit form
  - Delete: Confirm dialog → delete
- [ ] Create new: "Add New Word" button
- [ ] Total count: "Total: 127 words"

---

## Use Cases

### Use Case 1: Complete a Translation Practice Paragraph

```
Actor: Linh (English Learner)
Precondition: App is open, database initialized
Main Flow:

1. Linh clicks "Start Translation Practice"
2. Linh enters:
   - Title: "BBC News Article"
   - Source: "BBC Learning English"
   - Text: "Climate change is affecting global weather patterns..."
3. System creates paragraph, splits sentences
4. System displays Step 2: "Translate Sentences"
5. Linh translates Sentence 1: "Thay đổi khí hậu ảnh hưởng..."
6. Linh adds new word: "ecosystem, biodiversity"
7. Linh moves to Sentence 2, 3, ... until all translated
8. Linh clicks "Review Translations"
9. System displays Step 3 with AI scores:
   - Sentence 1: 8.5/10
   - Sentence 2: 6.2/10
   - Sentence 3: 9.1/10
10. Linh sees average: 7.9/10
11. Linh clicks "Save & Complete"
12. System marks paragraph COMPLETED, saves all data
13. New words added: "ecosystem, biodiversity"
14. Dashboard updates: +1 completed paragraph, +2 words
15. Linh returns to home screen

Postcondition:
  - Paragraph saved in database (status=COMPLETED)
  - All translations & scores persisted
  - New words in vocabulary table
  - Statistics updated
```

### Use Case 2: Practice Vocabulary Flashcard

```
Actor: Linh (English Learner)
Precondition: App is open, vocabulary items exist (min 5)
Main Flow:

1. Linh clicks "Vocabulary Flashcard"
2. System randomly selects "proficiency"
3. Display shown:
   - Word: PROFICIENCY
   - Example: "Her high proficiency in English impressed the interview panel."
   - Options: A) Lack of knowledge
             B) High level of skill
             C) Slow progress
             D) Lack of confidence
4. Linh reads & thinks (5 seconds)
5. Linh selects: B) High level of skill
6. System responds: ✔ CORRECT!
7. System updates: correct_count: 5 → 6
8. Linh clicks "Next Word"
9. Flow repeats for 10+ words
10. Linh clicks "Done" or closes app

Postcondition:
  - Vocabulary statistics updated
  - Accuracy % recalculated
  - Learning paragraph tracked
  - Data persisted to database
```

### Use Case 3: Review Dashboard Statistics

```
Actor: Linh (English Learner)
Precondition: App is open, user has completed paragraphs & vocabulary
Main Flow:

1. Linh opens MyEnglish app
2. Home screen loads
3. Linh sees:
   - Pie chart: 3 completed, 2 in-progress, 1 open paragraph
   - Bar chart: 5 words today, 12 yesterday, 3 day before...
   - Paragraph table: 2 in-progress paragraphs with "Continue" buttons
   - Vocabulary table: 127 words with search & sort
4. Linh takes note of:
   - Overall learning trend (bar chart)
   - Paragraph completions (pie chart)
   - Favorite/struggle words (from table)
5. Linh decides: "I want to complete the in-progress BBC article paragraph"
6. Linh clicks "Continue Paragraph" on BBC card
7. System loads that paragraph in Step 2-3 review mode
8. Linh can edit translations & rescore

Postcondition:
  - Dashboard statistics accurate & up-to-date
  - User has clear visibility into learning progress
```

---

## Non-Functional Requirements

### NFR-1: Performance
- **Requirement:** App should respond to user actions within acceptable time
- **Acceptance Criteria:**
  - ✅ App startup time: < 3 seconds
  - ✅ Loading sentences: < 500ms
  - ✅ AI scoring calculation: < 2 seconds per sentence
  - ✅ Dashboard chart rendering: < 1 second
  - ✅ Database queries: < 200ms

### NFR-2: Reliability & Data Integrity
- **Requirement:** Data must be safe & consistent
- **Acceptance Criteria:**
  - ✅ All database writes atomic (all-or-nothing)
  - ✅ Foreign key constraints enforced
  - ✅ Data persists across app restarts
  - ✅ Zero data loss on crash
  - ✅ Graceful error handling (no crashes on invalid input)

### NFR-3: Usability
- **Requirement:** UI should be intuitive & easy to navigate
- **Acceptance Criteria:**
  - ✅ Maximum 3 clicks to access any feature
  - ✅ Clear button labels & instructions
  - ✅ Consistent color scheme & typography
  - ✅ Loading spinners & progress indicators
  - ✅ Helpful error messages (not cryptic)

### NFR-4: Offline Capability
- **Requirement:** App works without internet connection
- **Acceptance Criteria:**
  - ✅ Google Translate can fail gracefully (warning message)
  - ✅ AI scoring works offline (transformers loaded locally)
  - ✅ All data saved locally in SQLite
  - ✅ No required cloud API calls (optional for new translations)

### NFR-5: Compatibility
- **Requirement:** App works on Windows systems
- **Acceptance Criteria:**
  - ✅ Tested on Windows 10 / 11
  - ✅ Python 3.8+
  - ✅ Flet 0.20+
  - ✅ All dependencies listed in requirements.txt

### NFR-6: Security
- **Requirement:** Local data protected from casual access
- **Acceptance Criteria:**
  - ✅ SQLite database not world-readable
  - ✅ No sensitive data in logs
  - ✅ Input validation (SQL injection prevention)
  - ✅ Local storage only (no cloud)

### NFR-7: Maintainability
- **Requirement:** Code easy to understand & modify
- **Acceptance Criteria:**
  - ✅ MVVM-S architecture followed
  - ✅ Code comments explain "why", not "what"
  - ✅ Functions < 30 lines
  - ✅ Unit tests for all core logic (80%+ coverage)

---

## Constraints & Assumptions

### Constraints

| Type | Constraint | Impact |
|------|-----------|--------|
| **Technology** | Python 3.8+ required | Limits older system compatibility |
| **Technology** | Flet UI framework | Limited to Flet capabilities |
| **Time** | 1 developer, flexible | May take weeks/months depending on effort |
| **ML Model** | sentence-transformers locally | Large model file (~100-200MB) |
| **Translation** | Google Translate optional | May fail without internet (graceful fallback) |
| **Database** | SQLite (local only) | No multi-user access, no cloud |
| **Language** | English → Vietnamese (MVP) | Can extend to other languages in v2.0 |

### Assumptions

| Assumption | Rationale |
|-----------|-----------|
| Users have Windows PC | Target platform is Windows desktop |
| Learners have English-Vietnamese bilingual ability | Translating to Vietnamese assumes user knows Vietnamese |
| Internet available for initial ML model download | sentence-transformers needs internet on first run |
| Users motivated to learn (self-study) | No gamification in MVP |
| Single user per app instance | No multi-user/cloud sync in MVP |
| English text is well-formed | Assume proper English paragraphs, not speech-to-text |

---

## Risk Register

### Risk 1: ML Model Size & Performance
**Risk:** sentence-transformers model is large (~200MB), may slow startup

**Likelihood:** Medium | **Impact:** Medium  
**Priority:** 🟡 Medium

**Mitigation:**
- [ ] Load model only when scoring (lazy loading) ← IMPLEMENTED
- [ ] Implement model caching (load once, reuse)
- [ ] Singleton pattern for model ← IMPLEMENTED
- [ ] Monitor startup time in testing

**Contingency:**
- If startup > 3 seconds, optimize loading or show progress spinner

---

### Risk 2: Database Corruption
**Risk:** SQLite database may corrupt if app crashes during write

**Likelihood:** Low | **Impact:** High  
**Priority:** 🔴 High

**Mitigation:**
- [ ] Use transactions (atomic writes)
- [ ] Enable PRAGMA foreign_keys
- [ ] Test crash scenarios
- [ ] Regular backups

**Contingency:**
- Backup database before each paragraph
- Provide recovery option (rollback to last checkpoint)

---

### Risk 3: Google Translate API Failures
**Risk:** If Google Translate unavailable, auto-translation of new words fails

**Likelihood:** Low | **Impact:** Low  
**Priority:** 🟢 Low

**Mitigation:**
- [ ] Implement graceful fallback (warning message)
- [ ] Store translations locally (avoid repeated calls)
- [ ] Offline mode doesn't require translation
- [ ] Manual translation entry as fallback

**Contingency:**
- Users can manually enter translations instead

---

### Risk 4: Test Coverage Gaps
**Risk:** Some code paths not tested, bugs found in production

**Likelihood:** Medium | **Impact:** High  
**Priority:** 🔴 High

**Mitigation:**
- [ ] Target 80%+ code coverage
- [ ] Write tests BEFORE committing code
- [ ] Code review for test quality
- [ ] Use pytest coverage reports

**Contingency:**
- Post-launch hotfix process for bugs found by users

---

### Risk 5: Scope Creep
**Risk:** Adding v2.0 features during MVP development delays release

**Likelihood:** High | **Impact:** Medium  
**Priority:** 🟡 Medium

**Mitigation:**
- [ ] Clear feature list in this document (OUT OF SCOPE section)
- [ ] Discipline: v2.0 features = defer to next sprint
- [ ] Focus on MVP quality, not quantity
- [ ] Regular sprint reviews to assess scope

**Contingency:**
- Prioritize: Functionality > UI > Documentation > Optimization

---

### Risk 6: Requirements Misunderstanding
**Risk:** Vague requirements lead to building wrong features

**Likelihood:** Low | **Impact:** High  
**Priority:** 🟡 Medium

**Mitigation:**
- [ ] This detailed SRS document
- [ ] Regular feedback & validation (this document verified by user)
- [ ] User acceptance testing (UAT) before release
- [ ] Clear acceptance criteria for each feature

**Contingency:**
- Bi-weekly sprint reviews with user feedback

---

## Future Development

The following features are **explicitly deferred** for v2.0 and later releases:

### User Management & Cloud (v2.0)
- User authentication (login/registration)
- Cloud synchronization & backup
- Multi-device sync
- Cloud-based storage

### Mobile & Platform Expansion (v2.0)
- Android/iOS mobile app
- Web browser version
- MacOS/Linux support (currently Windows only)

### Advanced Learning Features (v2.0+)
- Word pronunciation & audio playback
- Spaced repetition algorithm
- Dialogue conversation practice
- Listening comprehension exercises
- Writing corrections & grammar feedback

### Gamification & Motivation (v2.0+)
- Achievement badges
- Leaderboards
- Streaks counter
- Points & rewards
- Level progression

### Content & Customization (v2.0+)
- Built-in article library
- Custom difficulty levels
- Topic-based learning paths
- AI-powered personalized recommendations

### Monetization (v2.0+)
- Premium features
- Subscription model
- Payment processing
- Analytics dashboard

---

## Glossary

| Term | Definition |
|------|-----------|
| **Paragraph** | A learning activity with English text split into sentences for translation practice (status: OPEN, IN_PROGRESS, COMPLETED) |
| **Sentence** | Individual sentence within a paragraph |
| **Translation** | Vietnamese translation of English sentence, either user-provided or machine-generated |
| **Semantic Similarity** | AI score (0-10) comparing how similar user translation is to machine translation in meaning |
| **Vocabulary Item** | A single word with meaning & example sentence |
| **Flashcard** | Interactive card showing word + example, user selects correct meaning (multiple choice) |
| **MVP** | Minimum Viable Product - smallest feature set for release |
| **SDLC** | Software Development Lifecycle - formal phases of software development |
| **Sprint** | 1-4 week development cycle (Agile/Scrum methodology) |
| **User Story** | Description of feature from user perspective ("As a learner, I want...") |
| **Acceptance Criteria** | Specific, testable conditions for feature to be considered "done" |
| **Machine Translation** | Computer-generated translation (Google Translate) |
| **AI Scoring** | Semantic similarity calculation using sentence-transformers ML model |
| **Test Coverage** | Percentage of code executed by tests (target: 80%+) |
| **Unit Test** | Test of single function/method in isolation |
| **Integration Test** | Test of multiple components working together |
| **ER Diagram** | Entity-Relationship diagram showing database design |
| **Foreign Key** | Database constraint linking records across tables |

---

## Document Control

| Version | Date | Author | Status | Changes |
|---------|------|--------|--------|---------|
| 1.0 | Feb 9, 2026 | HaiDT | ✅ Approved | Initial SRS for MyEnglish MVP |

---

## Approval & Sign-off

- [x] **Product Owner (HaiDT)** - Approved ✅
- [x] **Developer** - Reviewed & Understood ✅
- [ ] **QA Lead** - To review in Phase 5 (Testing)
- [ ] **Project Manager** - To review before release

---

## Related Documents

- [`note/SDLC_PHASES.md`](../note/SDLC_PHASES.md) - Overview of 7 SDLC phases
- [`note/SDLC_METHODOLOGIES.md`](../note/SDLC_METHODOLOGIES.md) - Agile, Scrum, Waterfall comparison
- [`FEATURES_ROADMAP.md`](../FEATURES_ROADMAP.md) - Feature completion status
- [`note/MVVM_S_ARCHITECTURE.md`](../note/MVVM_S_ARCHITECTURE.md) - System architecture
- [`note/DATA_FLOW.md`](../note/DATA_FLOW.md) - Data flow diagrams

---

**END OF REQUIREMENTS SPECIFICATION**

---

*This Software Requirements Specification (SRS) document defines the complete scope, objectives, functional & non-functional requirements for MyEnglish MVP v1.0.*

*Date Created: February 9, 2026*  

