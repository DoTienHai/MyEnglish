# Software Development Lifecycle (SDLC) - Quick Reference

## 7 Giai đoạn của quy trình phát triển phần mềm

### 1️⃣ Planning & Requirements (Lập kế hoạch & Thu thập yêu cầu)
**Mục tiêu:** Xác định scope, requirements, timeline  
**Deliverables:**
- Project Charter
- Requirements Specification
- Project Schedule
- Risk Register

**Ví dụ:** Định nghĩa features (Translation Practice, Vocabulary, Dashboard), chọn tech stack (Flet + Python + SQLite)

---

### 2️⃣ Analysis (Phân tích)
**Mục tiêu:** Phân tích chi tiết, tìm constraints & dependencies  
**Deliverables:**
- Use Case Diagram
- Data Flow Diagram (DFD)
- User Stories
- Domain Model

**Ví dụ:**
```
Use Case 1: User practices translation
  - Input: Paragraph (title, source, text)
  - Process: Split sentences → User translates → AI scores
  - Output: Progress saved

Use Case 2: User practices vocabulary
  - Input: Display random word + example
  - Process: User selects answer → Evaluate
  - Output: Update score
```

---

### 3️⃣ Design (Thiết kế)
**Mục tiêu:** Thiết kế architecture, database, UI, APIs  
**Deliverables:**
- System Architecture Diagram
- Database ER Diagram
- UI/UX Mockups
- API Specifications
- Design Patterns

**Ví dụ - MyEnglish Architecture:**
```
Flet UI (View)
    ↓
ViewModel (State Management)
    ↓
Service (Business Logic)
    ↓
Repository (Data Access)
    ↓
SQLite Database
```

**Database Schema:**
```
Paragraph (id, title, source, input_text, completion%, score)
Sentence (id, paragraph_id, order, user_translation, machine_translation, ai_score)
Vocabulary (id, word, meaning, example, correct_count, wrong_count)
```

---

### 4️⃣ Development/Implementation (Phát triển)
**Mục tiêu:** Code implementation theo design  
**Best Practices:**
- ✅ Code Style: PEP 8
- ✅ Naming: Clear & descriptive
- ✅ DRY: Don't Repeat Yourself
- ✅ SOLID Principles
- ✅ Error Handling & Logging
- ✅ Git Workflow (feature branches, meaningful commits)

**Deliverables:**
- Source Code
- Code Documentation
- Build Scripts
- Configuration Files

---

### 5️⃣ Testing (Kiểm thử)
**Mục tiêu:** Verify code quality, find bugs, ensure reliability  

**Test Types:**

| Loại | Mục tiêu | Tool | Coverage |
|------|----------|------|----------|
| **Unit Test** | Test individual functions (isolated) | pytest | 80%+ |
| **Integration Test** | Test multiple components together | pytest | 60%+ |
| **System/E2E Test** | Test entire workflow end-to-end | pytest | 40%+ |
| **UI Test** | Test Flet components (limited) | - | Manual |

**Test Strategy cho MyEnglish:**
```
tests/
├── unit/
│   ├── test_models.py           # 100% coverage
│   ├── test_repositories.py     # 90%+ coverage
│   └── test_services.py         # 85%+ coverage
├── integration/
│   ├── test_paragraph_flow.py
│   ├── test_translation_flow.py
│   └── test_vocabulary_flow.py
└── conftest.py                  # Shared fixtures
```

**Example Unit Test:**
```python
def test_translate_practice_vm_submit_translation():
    # Arrange
    vm = TranslatePracticeViewModel(mock_services)
    
    # Act
    result = vm.submit_translation(1, "Hello world")
    
    # Assert
    assert 0 <= result['score'] <= 10
```

---

### 6️⃣ Deployment (Triển khai)
**Mục tiêu:** Release to production  
**Deployment Checklist:**
- ✅ All tests passing (100% pass rate)
- ✅ Code review approved
- ✅ Documentation complete
- ✅ Database migrations ready
- ✅ Configuration setup
- ✅ Performance tested
- ✅ Security audit done
- ✅ Backup & recovery plan
- ✅ Rollback plan ready

**MyEnglish Release Process:**
```bash
1. Build: flet pack main.py  → main.exe
2. Tag: git tag v1.0.0
3. Upload: .exe to cloud storage
4. Update: README with download link
5. Notify: Users
```

---

### 7️⃣ Maintenance & Support (Bảo trì & Hỗ trợ)
**Mục tiêu:** Fix bugs, monitor performance, plan next versions  
**Activities:**
- 🐛 Bug Fixes: Issue → Reproduce → Fix → Test → Deploy
- 📊 Monitoring: Performance, errors, user feedback
- 📚 Documentation Updates: FAQ, known issues
- 🔄 Enhancement Planning: Feature requests for v2.0

---

## 📊 SDLC Timeline (3-month MVP)

```
Month 1: Planning & Design (Week 1-4)
├── Requirements & Analysis
├── Architecture & Database Design
└── UI/UX Mockups

Month 2: Development & Unit Testing (Week 5-8)
├── Core features coding
├── Unit tests (80%+ coverage)
└── Code review process

Month 3: Integration Testing & Deployment (Week 9-12)
├── Integration tests
├── User acceptance testing (UAT)
├── Bug fixes
└── v1.0 Release
```

---

## ✅ MyEnglish Project Status

| Phase | Status | Completion |
|-------|--------|-----------|
| 1. Planning | ✅ | 80% |
| 2. Analysis | ✅ | 80% |
| 3. Design | ✅ | 90% |
| 4. Development | ✅ | 85% |
| **5. Testing** | 🔄 | **30%** ← FOCUS HERE |
| 6. Deployment | ⏳ | 0% |
| 7. Maintenance | ⏳ | 0% |

---

## 🎯 Immediate Actions (Priority Order)

1. **🔴 Enhance Unit Tests** (Phase 5)
   - Target: 80%+ code coverage
   - Create test suites for: Models, Repositories, Services, ViewModels
   - Use pytest + mocking

2. **🟠 Create Integration Tests** (Phase 5)
   - Test data flows: Paragraph Creation → Translation → Scoring
   - Test Cross-layer interactions

3. **🟡 Document Test Strategy** (Phase 5)
   - Create TEST_STRATEGY.md
   - Define test coverage targets
   - Setup CI/CD pipeline (optional)

4. **🟢 Prepare Deployment** (Phase 6)
   - Create DEPLOYMENT_GUIDE.md
   - Create RELEASE_NOTES.md
   - Build exe with `flet pack`

---

## 📚 Key Principles

### SOLID Principles
- **S** - Single Responsibility: One class should have one reason to change
- **O** - Open/Closed: Open for extension, closed for modification
- **L** - Liskov Substitution: Subclasses should be substitutable
- **I** - Interface Segregation: Depend on specific interfaces
- **D** - Dependency Inversion: High-level modules shouldn't depend on low-level

### Testing Pyramid 🔺
```
        UI Tests (Manual) ▲
      /        \
    /  E2E Tests  \
  /                \
/  Integration     \
      Tests
      /        \
    / Unit Tests \
  /________________\
  
Focus on Unit Tests (80%), then Integration Tests, then UI Tests
```

### Git Workflow
```
main branch (stable)
    ↑
    ├── Pull Request (code review)
    ↑
feature/xxx branch (development)
    ↑
    └── Local commits (git add, git commit)
```

---

**Last Updated:** February 9, 2026  
**See also:** [docs/requirement.md](../docs/requirement.md) for detailed SDLC phase information
