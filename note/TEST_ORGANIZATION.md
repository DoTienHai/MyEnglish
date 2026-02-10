# Test Organization Structure

## 📁 Cấu trúc folder Test

```
tests/
├── conftest.py                      # Shared fixtures cho toàn project
├── fixtures/
│   ├── __init__.py
│   ├── db_fixtures.py               # DB setup, in-memory instance
│   ├── model_fixtures.py            # Sample data (paragraph, sentence, vocab)
│   └── service_mocks.py             # Mocks cho services
├── unit/                            # Unit tests - test từng layer riêng biệt
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── test_paragraph.py        # Test Paragraph model (✓ có rồi)
│   │   ├── test_sentence.py
│   │   └── test_vocabulary.py
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── test_paragraph_repo.py   # Test ParagraphRepository (✓ có rồi)
│   │   ├── test_sentence_repo.py
│   │   └── test_vocabulary_repo.py
│   ├── service/
│   │   ├── __init__.py
│   │   ├── test_paragraph_service.py
│   │   ├── test_sentence_service.py
│   │   ├── test_vocabulary_service.py
│   │   ├── test_translation_service.py
│   │   └── test_scoring_service.py
│   └── viewmodel/
│       ├── __init__.py
│       ├── test_home_vm.py
│       ├── test_translate_practice_vm.py
│       └── test_vocabulary_vm.py
├── integration/
│   ├── __init__.py
│   ├── test_translation_flow.py     # E2E: User input → Score
│   ├── test_vocabulary_flow.py      # E2E: Learn word → Track
│   └── test_home_dashboard.py       # Dashboard aggregation
└── performance/
    ├── __init__.py
    └── test_scoring_performance.py  # ML model benchmarking
```

---

## 📋 Ý nghĩa các folder

| Folder | Mục đích |
|--------|---------|
| **conftest.py** | Định nghĩa __shared fixtures__ dùng chung cho toàn bộ tests (DB setup, sample data, mocks) |
| **fixtures/** | Tập trung __fixtures__ + __sample data__ để tái sử dụng (model_fixtures, db_fixtures, service_mocks) |
| **unit/** | Test __từng layer riêng biệt__ với mock dependencies - **nhanh, isolation** |
| **integration/** | Test __end-to-end flow__ giữa các layers - **kiểm tra real flow** |
| **performance/** | Test __tốc độ, load lớn__ (ML scoring, large dataset queries) |

---

## 🚀 Câu lệnh chạy Test

```bash
# Chạy toàn bộ tests
pytest tests/ -v

# Chạy unit tests (nhanh)
pytest tests/unit/ -v

# Chạy integration tests
pytest tests/integration/ -v

# Chạy performance tests
pytest tests/performance/ -v

# Chạy test cụ thể
pytest tests/unit/model/test_paragraph.py -v

# Chạy test với coverage report
pytest tests/ --cov=. --cov-report=html

# Chạy test và dừng ở lỗi đầu tiên
pytest tests/ -x

# Chạy test verbose với output
pytest tests/ -vv -s

# ⭐ Đầy đủ: Test Results + Coverage Report (RECOMMENDED)
pytest tests/unit_test/repository/test_paragraph_repo.py -v --tb=short --html=report.html --self-contained-html --cov=repositories --cov-report=html --cov-report=term
```

**Lệnh cuối chi tiết:**
- `-v` : Hiển thị chi tiết từng test
- `--tb=short` : Lỗi ngắn gọn
- `--html=report.html` : Tạo test results report
- `--self-contained-html` : File HTML độc lập
- `--cov=repositories` : Coverage cho module repositories
- `--cov-report=html` : HTML coverage (xem ở `htmlcov/index.html`)
- `--cov-report=term` : Hiển thị coverage % trong terminal

**Output:**
- `report.html` ← Test results (pass/fail) 
- `htmlcov/index.html` ← Coverage % (code coverage)

### Chi tiết từng test subfolder:

- **unit/model/** → Test data classes (to_dict, from_dict, validation)
- **unit/repository/** → Test CRUD operations, custom queries
- **unit/service/** → Test business logic (mocking repositories)
- **unit/viewmodel/** → Test formatting, aggregation (mocking services)

---

## 🎯 Khi nào dùng loại test nào?

| Loại Test | Khi nào viết | Ví dụ |
|-----------|-------------|-------|
| **Unit** | Test logic của 1 function/method riêng lẻ | `test_paragraph_to_dict()` - test Paragraph model |
| **Integration** | Test flow hoàn chỉnh qua nhiều layers | User submit translation → Score được lưu trong DB |
| **Performance** | Test khả năng chịu tải, tốc độ | Load 1000 sentences cùng lúc, ML scoring speed |
