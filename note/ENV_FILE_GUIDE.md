# .env File - Hướng Dẫn & Kiến Thức

## 1. .env là gì?

**.env** (Environment variables file) là file chứa các **biến môi trường** - những cấu hình nhạy cảm chỉ cần ở local.

```
✅ Lưu trữ: API keys, mật khẩu, database credentials, cấu hình địa phương
❌ KHÔNG commit: Bảo vệ secrets không lộ lên GitHub
```

---

## 2. Cấu trúc File .env

**Format cơ bản:**
```env
# Comments bắt đầu với #
KEY=VALUE
GOOGLE_APPLICATION_CREDENTIALS=gg_cloud_key.json
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:password@localhost/mydb
```

**Quy tắc:**
- Format: `KEY=VALUE` (không có dấu ngoặc kép)
- Một dòng = một biến môi trường
- `#` = comment (không xử lý)
- Không có space quanh dấu `=`

---

## 3. Lợi ích của .env

| Lợi ích | Ví dụ |
|---------|-------|
| **Bảo mật** | API keys không visible trong source code |
| **Linh hoạt** | Dev/Staging/Production dùng .env khác nhau |
| **Dễ quản lý** | Thay đổi config mà không cần chỉnh code |
| **Team collaboration** | Mỗi dev tạo .env riêng với credentials của họ |
| **Tránh Hardcode** | Không phải lưu secrets trực tiếp trong code |

---

## 4. So sánh: Hardcode vs .env

### ❌ **Cách sai (Hardcode trong code):**
```python
API_KEY = "sk-12345abcde"  # ⚠️ Bị lộ trên GitHub!
CREDENTIALS = {"user": "admin", "password": "secret123"}
```

**Vấn đề:**
- Secrets visible trên GitHub
- Mọi người thấy credentials
- Khó thay đổi khi deploy
- Bảo mật rất thấp

### ✅ **Cách đúng (dùng .env):**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Đọc từ .env tự động

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "default_value")
```

**Lợi ích:**
- Secrets chỉ ở local
- Code clean và generic
- Dễ bảo mật
- Flexible cho nhiều environment

---

## 5. Cách sử dụng .env trong Python

### **Bước 1: Cài đặt package**
```bash
pip install python-dotenv
```

### **Bước 2: Tạo file .env trong project root**
```env
GOOGLE_APPLICATION_CREDENTIALS=gg_cloud_key.json
LOG_LEVEL=INFO
DATABASE_PATH=app_data.db
DEBUG=True
```

### **Bước 3: Load trong code**
```python
import os
from dotenv import load_dotenv

# Load từ .env tự động
load_dotenv()

# Lấy giá trị
api_key = os.getenv("API_KEY")

# Với default value (nếu key không tồn tại)
log_level = os.getenv("LOG_LEVEL", "INFO")
debug = os.getenv("DEBUG", "False") == "True"

# Validation
if api_key is None:
    raise ValueError("API_KEY not found in .env file")
```

---

## 6. .gitignore - Bảo vệ .env

### **Tại sao phải ignore .env?**

```
❌ .env được commit → Secrets được push lên GitHub
✅ .env trong .gitignore → Secrets an toàn, chỉ local
```

### **Cách setup:**

**File `.gitignore`:**
```
# Environment variables
.env
.env.local
.env.*.local
*.env

# API Keys & Credentials
gg_cloud_key.json
*.key
*.pem
```

### **Git sẽ bỏ qua:**
- `.env` - file environment variables chính
- `gg_cloud_key.json` - Google Cloud credentials
- `*.key`, `*.pem` - tất cả file key/certificate

---

## 7. .env vs .env.example

### **.env (Local - Không commit)**
```env
GOOGLE_APPLICATION_CREDENTIALS=gg_cloud_key.json
API_KEY=sk-12345abcde
DATABASE_URL=postgresql://user:password@localhost/mydb
```

### **.env.example (Template - Commit)**
```env
# Copy file này sang .env và điền giá trị của bạn
GOOGLE_APPLICATION_CREDENTIALS=
API_KEY=
DATABASE_URL=
```

**Quy trình:**
```
1. Dev A commit .env.example
   ↓
2. Dev B clone repository
   ↓
3. Dev B: cp .env.example .env
   ↓
4. Dev B điền credentials riêng của họ
   ↓
5. Dev B: git status → .env không hiện (bị ignore)
```

---

## 8. Ví dụ thực tế: MyEnglish TranslationService

### **Cách hiện tại (Hardcode path):**
```python
class TranslationService:
    def __init__(self, key_path="gg_cloud_key.json"):
        # Chỉ tìm file cứng ở local
        if os.path.exists(key_path):
            # Load credentials
```

### **Cách cải thiện (với .env):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class TranslationService:
    def __init__(self):
        # Đọc path từ .env, nếu không có dùng default
        key_path = os.getenv(
            "GOOGLE_CREDENTIALS_PATH", 
            "gg_cloud_key.json"
        )
        
        if os.path.exists(key_path):
            # Load credentials
        else:
            # Fallback sang googletrans
```

**File .env:**
```env
GOOGLE_CREDENTIALS_PATH=gg_cloud_key.json
LOG_LEVEL=INFO
```

---

## 9. Best Practices

### ✅ **Làm đúng:**
```
1. Tạo .env với secrets
2. Thêm .env vào .gitignore
3. Commit .gitignore và .env.example
4. Các dev tạo .env riêng
5. Load bằng python-dotenv
6. Validation & error handling
7. Git commit: .env (KHÔNG), .env.example (CÓ)
```

### ❌ **Tránh làm:**
```
1. Hardcode secrets trong code
2. Commit .env lên GitHub
3. Sử dụng environment variables không tồn tại mà không check
4. Để .env.example có secrets thực
5. Quên cài python-dotenv
6. Không validation input từ .env
```

---

## 10. Checklist Chuẩn

### **Setup ban đầu:**
- [ ] Cài `pip install python-dotenv`
- [ ] Tạo file `.env` với secrets
- [ ] Tạo file `.env.example` (template)
- [ ] Thêm `.env` vào `.gitignore`
- [ ] Thêm `*.key`, `*.pem`, `gg_cloud_key.json` vào `.gitignore`
- [ ] Load `.env` trong dự án bằng `load_dotenv()`

### **Kiểm tra trước commit:**
```bash
# Xem file sẽ được commit
git status

# .env không được liệt kê (bị ignore) ✅
# .env.example được liệt kê (template) ✅

# Commit
git add .
git commit -m "Cập nhật .env.example"
git push
```

### **Cho team members:**
```bash
# Sau khi clone
cp .env.example .env

# Điền credentials
# Chạy ứng dụng
flet run main.py
```

---

## 11. Tham khảo

- **python-dotenv docs:** https://python-dotenv.readthedocs.io/
- **12 Factor App (Environment config):** https://12factor.net/config
- **Project conventions:** `.github/CONVENTIONS.md`

---

**Cập nhật lần cuối:** Tháng 2, 2026
