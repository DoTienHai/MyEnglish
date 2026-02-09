# Refactoring: Environment Variables Architecture

## 📋 Tổng Quan

Dự án **MyEnglish** đã được refactor để theo cấu trúc **Centralized Configuration**:

```
.env (Secrets - Local only, in .gitignore)
  ↓
config.py (Load & Centralize - duy nhất 1 chỗ)
  ↓
main.py, services, models (Import & Use)
```

---

## 🔄 Những Thay Đổi

### **1️⃣ config.py (Centralized Source Of Truth)**

**Trước:** `service/translation_service.py` load `.env` riêng
```python
# ❌ Cũ: Mỗi class load .env riêng
from dotenv import load_dotenv
load_dotenv()
```

**Sau:** Tất cả config load ở `config.py` **duy nhất 1 lần**
```python
# ✅ Mới: config.py
from dotenv import load_dotenv
load_dotenv()  # Load 1 lần duy nhất

# Centralize configuration
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")  # No default fallback
DATABASE_PATH = os.getenv("DB_PATH", "app_data.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

---

### **2️⃣ TranslationService (Import từ config)**

**Trước:**
```python
# ❌ Cũ: Đọc .env trực tiếp + throw exception nếu None
import os
from dotenv import load_dotenv  # Load lại?

load_dotenv()
key_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
```

**Sau:**
```python
# ✅ Mới: Import từ config.py
from config import GOOGLE_CREDENTIALS_PATH

class TranslationService:
    def __new__(cls, key_path=None):
        if key_path is None:
            key_path = GOOGLE_CREDENTIALS_PATH  # From config.py
        
        if key_path is None:
            raise ValueError("GOOGLE_CREDENTIALS_PATH not found in config")
```

**Lợi ích:**
- ✅ Không load `.env` lại (performance)
- ✅ Centralized (dễ thay đổi)
- ✅ Dễ test (mock config.py)

---

### **3️⃣ main.py (Clean Entry Point)**

**Trước:**
```python
# ❌ Các import rắc rối
```

**Sau:**
```python
# ✅ Mới: Import config FIRST (nó load .env)
from config import DATABASE_PATH  # This loads .env!

def main():
    db = DBConnect(db_path=DATABASE_PATH)
    # ...
```

---

## 🎯 Kiến Trúc Mới

```
┌─────────────────────────────────────┐
│  main.py (Entry Point)              │
│  ├─ import config (loads .env)      │
│  ├─ use DATABASE_PATH from config   │
│  └─ initialize services             │
└─────────────────┬───────────────────┘
                  │
                  ↓
┌─────────────────────────────────────┐
│  config.py (Centralized Config)     │
│  ├─ load_dotenv() - 1 lần duy nhất  │
│  ├─ GOOGLE_CREDENTIALS_PATH         │
│  ├─ DATABASE_PATH                   │
│  ├─ LOG_LEVEL                       │
│  └─ DEBUG                           │
└─────────────────┬───────────────────┘
                  │
                  ↓
  ┌───────────────┴────────────────┐
  ↓                               ↓
┌──────────────────┐    ┌─────────────────┐
│ Services         │    │ Models/Repos    │
│ ├─ Translation   │    │ ├─ Paragraph    │
│ ├─ Scoring       │    │ ├─ Sentence     │
│ └─ Sentence      │    │ └─ Vocabulary   │
│                  │    │                 │
│ import config    │    │ use from config │
└──────────────────┘    └─────────────────┘
```

---

## ✅ Best Practices Tuân Thủ

| Tiêu Chí | Status | Chi Tiết |
|---------|--------|----------|
| **Single load .env** | ✅ | Chỉ ở config.py, 1 lần |
| **Centralized config** | ✅ | Tất cả ở config.py |
| **No direct .env access** | ✅ | Services import từ config |
| **Type safety** | ✅ | config.py có type hints (optional) |
| **Testability** | ✅ | Mock config.py dễ hơn |
| **Maintainability** | ✅ | Thay config ở 1 chỗ |

---

## 🚀 Ứng Dụng Thực Tế

### **Scenario 1: Thêm Biến Config Mới**

**Trước:** Phải edit nhiều files (translation_service, scoring_service, v.v.)

**Sau:** Chỉ edit `config.py`:
```python
# config.py
NEW_VARIABLE = os.getenv("NEW_VARIABLE", "default_value")

# Services tự động có biến này nếu cần
from config import NEW_VARIABLE
```

### **Scenario 2: Chuyển sang Environment Variables System Khác**

**Trước:** Phải thay từng file

**Sau:** Chỉ thay logic ở `config.py`:
```python
# Có thể thay sang dynaconf, pydantic, v.v.
from dynaconf import settings
GOOGLE_CREDENTIALS_PATH = settings.GOOGLE_CREDENTIALS_PATH
```

---

## 📊 So Sánh Trước-Sau

| Tính Năng | Trước ❌ | Sau ✅ |
|----------|---------|--------|
| **Load .env** | Nhiều chỗ (N services) | 1 chỗ (config.py) |
| **Centralized** | Scattered | Một chỗ duy nhất |
| **Mock test** | Khó (phải mock N services) | Dễ (mock config.py) |
| **Thay config** | N files | 1 file |
| **Performance** | .env loaded N lần | .env loaded 1 lần |
| **Coupling** | Chặt (mỗi service-dotenv) | Lỏng (service-config) |

---

## 🔒 Security

### ✅ Đã Bảo Vệ

- `.env` trong `.gitignore` ✅
- `gg_cloud_key.json` trong `.gitignore` ✅
- `.env.example` là template (commit được) ✅
- Validation ở config.py (fail fast) ✅

### 📋 Nguyên Tắc

```
Local Dev:
├─ .env (secrets, không commit)
├─ gg_cloud_key.json (API key, không commit)
└─ code imports từ config.py

Production:
├─ Environment variables từ OS (không có .env)
├─ config.py vẫn hoạt động (đọc từ OS)
└─ code imports từ config.py (không thay)
```

---

## 🧪 Testing

### **Ví dụ: Mock config.py**

```python
import pytest
from unittest.mock import patch

def test_translation_service():
    # Mock config
    with patch("config.GOOGLE_CREDENTIALS_PATH", "mock_key.json"):
        service = TranslationService()
        # test...
```

### **Ví dụ: Test validation**

```python
def test_config_validation():
    # Config sẽ validate GOOGLE_CREDENTIALS_PATH
    with patch("config.GOOGLE_CREDENTIALS_PATH", None):
        # Sẽ raise ValueError
        with pytest.raises(ValueError):
            from service.translation_service import TranslationService
```

---

## 📚 Quy Trình Setup

### **Cho New Developer**

```bash
# 1. Clone repo
git clone <repo>

# 2. Copy template
cp .env.example .env

# 3. Điền credentials
# Edit .env:
GOOGLE_CREDENTIALS_PATH=path/to/gg_cloud_key.json

# 4. Run
python main.py
```

### **Tại Sao Nó Hoạt Động**

1. `main.py` import `config`
2. `config.py` chạy `load_dotenv()` → đọc `.env`
3. `config.py` set `GOOGLE_CREDENTIALS_PATH = os.getenv(...)`
4. Services import từ `config` → nhận giá trị đã load

---

## ⚠️ Lưu Ý

### **Không Nên**

```python
# ❌ Không load .env ở các service
from dotenv import load_dotenv
load_dotenv()
```

```python
# ❌ Không os.getenv() trực tiếp
key_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
```

### **Nên**

```python
# ✅ Import từ config
from config import GOOGLE_CREDENTIALS_PATH
```

```python
# ✅ Hoặc import config module
import config
key_path = config.GOOGLE_CREDENTIALS_PATH
```

---

## 🎓 File Liên Quan

- **config.py** - Centralized configuration
- **main.py** - Entry point, imports config
- **service/translation_service.py** - ví dụ imports từ config
- **.env.example** - Template cho .env
- **.gitignore** - Ignore secrets

---

**Cập nhật lần cuối:** Tháng 2, 2026
