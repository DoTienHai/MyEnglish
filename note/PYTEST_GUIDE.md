# Pytest Guide - Ghi chú sử dụng

## � Mục lục

- [Pytest Guide - Ghi chú sử dụng](#pytest-guide---ghi-chú-sử-dụng)
  - [� Mục lục](#-mục-lục)
  - [�📦 Cài đặt Pytest](#-cài-đặt-pytest)
  - [🎯 Cấu trúc cơ bản 1 test](#-cấu-trúc-cơ-bản-1-test)
  - [� conftest.py vs @pytest.fixture](#-conftestpy-vs-pytestfixture)
    - [conftest.py là gì?](#conftestpy-là-gì)
    - [@pytest.fixture là gì?](#pytestfixture-là-gì)
    - [Mối quan hệ](#mối-quan-hệ)
  - [🔍 Pytest tìm conftest.py như thế nào?](#-pytest-tìm-conftestpy-như-thế-nào)
  - [⚠️ Vấn đề: Fixtures trùng tên](#️-vấn-đề-fixtures-trùng-tên)
  - [💡 Khuyến nghị: 1 conftest.py  vs fixtures/ folder](#-khuyến-nghị-1-conftestpy--vs-fixtures-folder)
    - [Option A: Chỉ 1 conftest.py (Đơn giản) ✅ RECOMMENDED](#option-a-chỉ-1-conftestpy-đơn-giản--recommended)
    - [Option B: conftest.py + fixtures/ folder (Modularize)](#option-b-conftestpy--fixtures-folder-modularize)
  - [✅ Import Fixtures - Cần hay không?](#-import-fixtures---cần-hay-không)
    - [Test files: **KHÔNG cần import**](#test-files-không-cần-import)
    - [fixtures/ files được conftest.py: **CÓ cần import**](#fixtures-files-được-conftestpy-có-cần-import)
  - [�🔧 Fixtures - Tái sử dụng dữ liệu](#-fixtures---tái-sử-dụng-dữ-liệu)
    - [Fixture cơ bản](#fixture-cơ-bản)
    - [Fixture scope - Quyết định fixture được tạo bao nhiêu lần](#fixture-scope---quyết-định-fixture-được-tạo-bao-nhiêu-lần)
    - [Fixture dependencies - Fixtures có thể dùng fixtures khác](#fixture-dependencies---fixtures-có-thể-dùng-fixtures-khác)
    - [Fixture cleanup - Dọn dẹp sau test (optional)](#fixture-cleanup---dọn-dẹp-sau-test-optional)
  - [✅ Assertions - Kiểm tra kết quả](#-assertions---kiểm-tra-kết-quả)
    - [Assert cơ bản](#assert-cơ-bản)
    - [Assert với messages](#assert-với-messages)
    - [Assert ngoại lệ (Exception)](#assert-ngoại-lệ-exception)
    - [Assert đối tượng](#assert-đối-tượng)
  - [📊 Mocking - Giả lập dependencies](#-mocking---giả-lập-dependencies)
    - [Mock cơ bản](#mock-cơ-bản)
    - [Mock trong fixture](#mock-trong-fixture)
    - [Patch - Mock class/module](#patch---mock-classmodule)
  - [🎪 Parametrize - Chạy test với nhiều inputs](#-parametrize---chạy-test-với-nhiều-inputs)
  - [🏷️ Markers - Gắn nhãn test](#️-markers---gắn-nhãn-test)
  - [📁 conftest.py - File shared fixtures](#-conftestpy---file-shared-fixtures)
  - [🔄 Áp dụng vào project MyEnglish](#-áp-dụng-vào-project-myenglish)
    - [Example: Test Paragraph Model](#example-test-paragraph-model)
    - [Example: Test Repository](#example-test-repository)
    - [Example: Integration Test](#example-integration-test)
  - [🎯 Best Practices](#-best-practices)
  - [💡 Troubleshooting](#-troubleshooting)

---

## �📦 Cài đặt Pytest

```bash
pip install pytest pytest-cov pytest-watch
```

---

## 🎯 Cấu trúc cơ bản 1 test

```python
import pytest
from model.paragraph import Paragraph

def test_paragraph_to_dict():
    """Test name phải bắt đầu với 'test_'"""
    # Arrange - Chuẩn bị dữ liệu
    para = Paragraph(
        id=1,
        title="Test",
        input_paragraph="Hello",
        reference="Ref",
        machine_translation="Xin chào",
        completed=50.0,
        score=8.0,
        created_at="2026-01-26 12:00:00"
    )
    
    # Act - Thực thi
    result = para.to_dict()
    
    # Assert - Kiểm tra kết quả
    assert result["title"] == "Test"
    assert result["id"] == 1
```

---

## � conftest.py vs @pytest.fixture

### conftest.py là gì?
- **File** có tên bắt buộc (PHẢI đặt tên `conftest.py`)
- Pytest **tự động tìm** file này khi chạy tests
- Dùng để chứa **fixtures, hooks, config chung**

### @pytest.fixture là gì?
- **Decorator** (bộ trang trí hàm)
- Đánh dấu một hàm là fixture
- Có thể define ở conftest.py hoặc file test bất kỳ

### Mối quan hệ
```
conftest.py (file - bắt buộc tên)
    ├── @pytest.fixture (decorator)
    │   def sample_data():  ← fixture (hàm được decorated)
    │       return data
    ├── @pytest.fixture
    │   def db():
    │       return db
    └── pytest hooks (nếu cần)
```

---

## 🔍 Pytest tìm conftest.py như thế nào?

Khi chạy test, Pytest tìm conftest.py theo thứ tự (từ gần đến xa):

```
pytest tests/unit/model/test_paragraph.py
                              ↓
Scan folders:
  1. tests/unit/model/conftest.py       ← Nếu không có
  2. tests/unit/conftest.py             ← Nếu không có
  3. tests/conftest.py                  ✅ Tìm được! Load fixtures
  4. conftest.py (project root)         ← Nếu cần tiếp tục
```

**Lợi ích:**
- ✅ Pytest **tự động tìm parent conftest.py** - không cần config
- ✅ Chạy `pytest tests/unit/` vẫn tìm được `tests/conftest.py`
- ✅ Chạy `pytest tests/integration/` vẫn tìm được `tests/conftest.py`

---

## ⚠️ Vấn đề: Fixtures trùng tên

```python
# tests/conftest.py
@pytest.fixture
def sample_paragraph():
    return Paragraph(id=1, title="Generic")

# tests/unit/conftest.py (Nếu có)
@pytest.fixture
def sample_paragraph():  # ❌ Trùng tên!
    return Paragraph(id=1, title="Unit test")
```

**Vấn đề:**
- Pytest chọn phiên bản gần nhất (confusing)
- Code reviewer khó hiểu fixture nào được dùng
- Dễ có bugs vì fixtures khác nhau

**Giải pháp:**
- ✅ Chỉ dùng **1 conftest.py ở root `tests/`**
- ✅ Nếu có multiple conftest, dùng **tên khác** (VD: `unit_sample_paragraph`)

---

## 💡 Khuyến nghị: 1 conftest.py  vs fixtures/ folder

### Option A: Chỉ 1 conftest.py (Đơn giản) ✅ RECOMMENDED

```
tests/
├── conftest.py          # ← 1 file, tất cả fixtures
├── unit/
├── integration/
└── performance/
```

**Lợi ích:**
- ✅ Đơn giản, không bao giờ trùng
- ✅ Dễ tìm fixtures
- ✅ Pytest tự động tìm

**Bất lợi:**
- ❌ File dài khi fixtures nhiều

### Option B: conftest.py + fixtures/ folder (Modularize)

```
tests/
├── conftest.py                  # ← Import từ fixtures/
│   pytest_plugins = [
│       "fixtures.db_fixtures",
│       "fixtures.model_fixtures",
│   ]
├── fixtures/
│   ├── db_fixtures.py           # Chứa DB fixtures
│   ├── model_fixtures.py        # Chứa model fixtures
│   └── service_mocks.py         # Chứa service mocks
├── unit/
├── integration/
└── performance/
```

**Lợi ích:**
- ✅ Organized, dễ maintain
- ✅ Mỗi file chỉ chứa 1 loại fixtures

**Lưu ý:**
- fixtures/ folder là **optional** - chỉ để modularize
- Pytest **KHÔNG tự động tìm** fixtures/ folder
- Phải được **conftest.py import hoặc đăng ký** mới được dùng

---

## ✅ Import Fixtures - Cần hay không?

### Test files: **KHÔNG cần import**

```python
# tests/unit/model/test_paragraph.py

# ❌ Không cần viết:
# from conftest import sample_paragraph
# from fixtures.model_fixtures import sample_paragraph

# ✅ Chỉ cần dùng trực tiếp:
def test_something(sample_paragraph):
    # Pytest tự động tìm fixture tên "sample_paragraph"
    assert sample_paragraph.title == "Test"
```

### fixtures/ files được conftest.py: **CÓ cần import**

```python
# tests/conftest.py

# Cách 1: Import trực tiếp
from fixtures.db_fixtures import memory_db
from fixtures.model_fixtures import sample_paragraph

# Cách 2: Dùng pytest_plugins (Tự động load)
pytest_plugins = [
    "fixtures.db_fixtures",
    "fixtures.model_fixtures",
    "fixtures.service_mocks",
]
```

---

## �🔧 Fixtures - Tái sử dụng dữ liệu

Fixtures giúp tạo dữ liệu/setup một lần rồi dùng lại nhiều test.

### Fixture cơ bản

```python
import pytest

@pytest.fixture
def sample_paragraph():
    """Hàm fixture - tạo dữ liệu sẵn"""
    from model.paragraph import Paragraph
    return Paragraph(
        id=None,
        title="Test Paragraph",
        input_paragraph="This is a test.",
        reference="Ref",
        machine_translation="Dịch máy",
        completed=50.0,
        score=8.0,
        created_at="2026-01-26 12:00:00"
    )

def test_paragraph_create(sample_paragraph):
    """Sử dụng fixture bằng cách truyền vào param"""
    assert sample_paragraph.title == "Test Paragraph"
```

### Fixture scope - Quyết định fixture được tạo bao nhiêu lần

```python
@pytest.fixture(scope="function")  # Default - tạo lại mỗi test
def sample_data():
    return {"name": "test"}

@pytest.fixture(scope="module")    # Tạo 1 lần cho 1 file test
def database():
    return setup_db()

@pytest.fixture(scope="session")   # Tạo 1 lần cho toàn bộ test run
def config():
    return load_config()
```

### Fixture dependencies - Fixtures có thể dùng fixtures khác

```python
@pytest.fixture
def memory_db():
    """Tạo in-memory database"""
    db = DBConnect(":memory:")
    DBInit(db).create_tables()
    return db

@pytest.fixture
def paragraph_repo(memory_db):
    """Dùng memory_db fixture"""
    return ParagraphRepository(memory_db)

def test_create_paragraph(paragraph_repo):
    """paragraph_repo sẽ có memory_db sẵn"""
    para = Paragraph(title="Test", ...)
    pid = paragraph_repo.create(para)
    assert pid is not None
```

### Fixture cleanup - Dọn dẹp sau test (optional)

```python
@pytest.fixture
def temp_file():
    # Setup
    filepath = "/tmp/test.txt"
    with open(filepath, "w") as f:
        f.write("test")
    
    yield filepath  # Giá trị được truyền vào test
    
    # Cleanup - chạy sau khi test xong
    import os
    os.remove(filepath)

def test_read_file(temp_file):
    with open(temp_file) as f:
        content = f.read()
    assert content == "test"
```

---

## ✅ Assertions - Kiểm tra kết quả

### Assert cơ bản

```python
def test_assertions():
    # Bằng nhau
    assert 5 == 5
    assert "hello" == "hello"
    
    # Không bằng
    assert 5 != 4
    
    # True/False
    assert True
    assert not False
    
    # Thuộc list/dict
    assert "a" in ["a", "b", "c"]
    assert "key" in {"key": "value"}
    
    # So sánh số
    assert 5 > 3
    assert 5 >= 5
    assert 3 < 5
    assert 3 <= 3
```

### Assert với messages

```python
def test_assertions_with_message():
    result = 5 + 2
    assert result == 7, f"Expected 7 but got {result}"
    
    para = Paragraph(title="Test", ...)
    assert para.title == "Test", f"Title không đúng: {para.title}"
```

### Assert ngoại lệ (Exception)

```python
import pytest

def test_division_by_zero():
    """Kiểm tra hàm raise lỗi"""
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0

def test_custom_exception():
    with pytest.raises(ValueError, match="Invalid input"):
        some_function()
```

### Assert đối tượng

```python
def test_paragraph_equality():
    para1 = Paragraph(id=1, title="Test", ...)
    para2 = Paragraph(id=1, title="Test", ...)
    
    # So sánh attributes
    assert para1.title == para2.title
    assert para1.id == para2.id
    
    # Kiểm tra None
    assert para1.id is not None
```

---

## 📊 Mocking - Giả lập dependencies

Dùng `unittest.mock` để giả lập (mock) các dependencies trong unit tests.

### Mock cơ bản

```python
from unittest.mock import Mock

def test_with_mock():
    # Tạo mock object
    mock_repo = Mock()
    
    # Cấu hình return value
    mock_repo.get.return_value = Paragraph(id=1, title="Test")
    
    # Sử dụng
    result = mock_repo.get(1)
    assert result.title == "Test"
    
    # Kiểm tra mock được gọi
    mock_repo.get.assert_called_once_with(1)
```

### Mock trong fixture

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_scoring_service():
    mock = Mock()
    mock.score.return_value = 0.95
    return mock

def test_service_with_mock(mock_scoring_service):
    result = mock_scoring_service.score("Hello", "Hi")
    assert result == 0.95
```

### Patch - Mock class/module

```python
from unittest.mock import patch

@patch('service.scoring_service.ScoringService.score')
def test_with_patch(mock_score):
    # Mock ScoringService.score method
    mock_score.return_value = 0.85
    
    service = ScoringService()
    result = service.score("text1", "text2")
    assert result == 0.85

# Hoặc dùng context manager
def test_with_patch_context():
    with patch('repositories.paragraph_repo.ParagraphRepository.get') as mock_get:
        mock_get.return_value = Paragraph(id=1)
        # Thực thi code
```

---

## 🎪 Parametrize - Chạy test với nhiều inputs

Thay vì viết nhiều test giống nhau, dùng parametrize:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input, expected):
    """Chạy 4 lần với inputs khác nhau"""
    assert input ** 2 == expected

# Hoặc parametrize fixture
@pytest.mark.parametrize("score", [0.5, 0.75, 0.9, 1.0])
def test_scoring_ranges(score):
    assert 0 <= score <= 1
```

---

## 🏷️ Markers - Gắn nhãn test

```python
import pytest

@pytest.mark.slow
def test_large_dataset():
    """Gắn nhãn slow"""
    # Test chạy lâu

@pytest.mark.skip(reason="Chưa implement")
def test_not_implemented():
    assert False

@pytest.mark.skipif(True, reason="Điều kiện không rõ")
def test_conditional_skip():
    assert False

# Chạy chỉ tests có marker slow
# pytest -m slow

# Chạy tất cả TRỪ slow
# pytest -m "not slow"
```

---

## 📁 conftest.py - File shared fixtures

Đặt `conftest.py` ở root `tests/` để các fixtures được tất cả test files sử dụng:

```python
# tests/conftest.py

import pytest
from repositories.db_connect import DBConnect
from repositories.db_init import DBInit

@pytest.fixture(scope="session")
def memory_db():
    """In-memory DB - shared cho toàn session"""
    db = DBConnect(":memory:")
    DBInit(db).create_tables()
    return db

@pytest.fixture
def sample_paragraph():
    from model.paragraph import Paragraph
    return Paragraph(
        id=None,
        title="Test",
        input_paragraph="Test paragraph",
        reference="Ref",
        machine_translation="May dich",
        completed=50.0,
        score=8.0,
        created_at="2026-01-26 12:00:00"
    )
```

Sau đó dùng trong bất kỳ test file:

```python
# tests/unit/model/test_paragraph.py

def test_paragraph(sample_paragraph):
    """Sử dụng fixture từ conftest.py"""
    assert sample_paragraph.title == "Test"
```

---

## 🔄 Áp dụng vào project MyEnglish

### Example: Test Paragraph Model

```python
# tests/unit/model/test_paragraph.py

import pytest
from model.paragraph import Paragraph

@pytest.fixture
def sample_paragraph():
    return Paragraph(
        id=1,
        title="Translation Session",
        input_paragraph="The quick brown fox",
        reference="English Text",
        machine_translation="Con cáo nâu nhanh",
        completed=75.0,
        score=8.5,
        created_at="2026-01-26 12:00:00"
    )

def test_paragraph_to_dict(sample_paragraph):
    result = sample_paragraph.to_dict()
    assert result["title"] == "Translation Session"
    assert result["completed"] == 75.0

def test_paragraph_from_dict():
    data = {
        "id": 1,
        "title": "Test",
        "input_paragraph": "Test",
        "reference": "Ref",
        "machine_translation": "May",
        "completed": 50.0,
        "score": 8.0,
        "created_at": "2026-01-26 12:00:00"
    }
    para = Paragraph.from_dict(data)
    assert para.title == "Test"
    assert para.completed == 50.0
```

### Example: Test Repository

```python
# tests/unit/repository/test_paragraph_repo.py

import pytest
from repositories.paragraph_repo import ParagraphRepository
from model.paragraph import Paragraph

@pytest.fixture
def repo(memory_db):
    """Dùng memory_db từ conftest.py"""
    return ParagraphRepository(memory_db)

@pytest.fixture
def sample_para():
    return Paragraph(
        id=None,
        title="Test Paragraph",
        input_paragraph="This is test.",
        reference="Ref",
        machine_translation="Dich",
        completed=50.0,
        score=8.0,
        created_at="2026-01-26 12:00:00"
    )

def test_create_and_get(repo, sample_para):
    pid = repo.create(sample_para)
    retrieved = repo.get(pid)
    assert retrieved.title == sample_para.title

def test_update(repo, sample_para):
    pid = repo.create(sample_para)
    para = repo.get(pid)
    para.title = "Updated Title"
    repo.update(para)
    updated = repo.get(pid)
    assert updated.title == "Updated Title"

def test_delete(repo, sample_para):
    pid = repo.create(sample_para)
    repo.delete(pid)
    assert repo.get(pid) is None
```

### Example: Integration Test

```python
# tests/integration/test_translation_flow.py

import pytest
from repositories.paragraph_repo import ParagraphRepository
from repositories.sentence_repo import SentenceRepository
from model.paragraph import Paragraph
from model.sentence import Sentence
from service.scoring_service import ScoringService

def test_user_translation_flow(memory_db):
    """E2E: User tạo paragraph → translate → score"""
    
    # 1. Create paragraph
    para_repo = ParagraphRepository(memory_db)
    para = Paragraph(
        title="Test",
        input_paragraph="Hello world",
        reference="Ref",
        machine_translation="May dich",
        completed=0,
        score=0,
        created_at="2026-01-26 12:00:00"
    )
    para_id = para_repo.create(para)
    
    # 2. Create sentence
    sent_repo = SentenceRepository(memory_db)
    sent = Sentence(
        paragraph_id=para_id,
        english_sentence="Hello world",
        user_translation="Xin chào thế giới",
        machine_translation="May: xin chào...",
        ai_score=0
    )
    sent_id = sent_repo.create(sent)
    
    # 3. Score translation
    scorer = ScoringService()
    score = scorer.score(sent.user_translation, sent.machine_translation)
    
    # 4. Update score
    sent.ai_score = score
    sent_repo.update(sent)
    
    # 5. Verify
    updated = sent_repo.get(sent_id)
    assert updated.ai_score is not None
    assert updated.ai_score > 0
```

---

## 🎯 Best Practices

| Best Practice | Lý do |
|---------------|-------|
| **Một assert per test** | Dễ xác định nguyên nhân test fail |
| **Naming rõ ràng** | `test_<feature>_<scenario>` |
| **Setup nhỏ và isolated** | Dùng in-memory DB, mocks |
| **1 conftest.py ở root** | Tránh fixtures trùng tên |
| **Tái sử dụng fixtures** | Dùng conftest.py, không copy-paste |
| **Không test implementation** | Test behavior, không code |
| **Mock external calls** | API, ML model, DB |

---

## � Chạy Tests với Reports

### Cài dependencies
```bash
pip install pytest pytest-cov pytest-html pytest-watch
```

### Lệnh cơ bản
```bash
# Chạy test đơn giản
pytest tests/unit_test/repository/test_paragraph_repo.py

# Chạy với verbose output
pytest tests/unit_test/repository/test_paragraph_repo.py -v
```

### Lệnh đầy đủ: Test Results + Coverage Report
```bash
pytest tests/unit_test/repository/test_paragraph_repo.py -v --tb=short --html=report.html --self-contained-html --cov=repositories --cov-report=html --cov-report=term
```

**Giải thích:**
| Tùy chọn | Ý nghĩa |
|----------|---------|
| `-v` | Verbose - hiển thị chi tiết từng test |
| `--tb=short` | Traceback - hiển thị lỗi ngắn gọn |
| `--html=report.html` | Tạo HTML report cho test results |
| `--self-contained-html` | File HTML độc lập (không cần external files) |
| `--cov=repositories` | Coverage cho module repositories |
| `--cov-report=html` | Tạo HTML coverage report (lưu ở `htmlcov/index.html`) |
| `--cov-report=term` | Hiển thị coverage % trong terminal |

**Output files:**
- `report.html` ← **Test results report** (pass/fail chi tiết) 📊
- `htmlcov/index.html` ← **Coverage report** (% code được test) 📈

### Xem Real-time khi code thay đổi
```bash
pytest-watch tests/unit_test/ -- -v --cov=repositories
```

---

## �💡 Troubleshooting

| Lỗi | Giải pháp |
|-----|----------|
| `ModuleNotFoundError` | Chạy từ root folder: `pytest tests/` |
| `FixtureNotFound` | Kiểm tra conftest.py ở đúng folder |
| `Timeout` | Dùng `@pytest.mark.slow` cho test chậm |
| `DB locked` | Dùng `:memory:` SQLite thay vì file |
