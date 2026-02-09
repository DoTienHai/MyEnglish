# Triển Khai .env - Hướng Dẫn Setup & Thereon

## 📋 Tổng Quan Thay Đổi

Dự án **MyEnglish** đã được triển khai lại để sử dụng **biến môi trường từ file `.env`** thay vì hardcode:

```
✅ Bảo mật credentials
✅ Dễ thay đổi config (Dev/Prod khác nhau)
✅ Giấu secrets khỏi GitHub
✅ Linh hoạt cho team development
```

---

## 🔄 Những File Đã Được Cập Nhật

### **1. requirements.txt**
- ✅ Thêm `python-dotenv==1.0.0` để load file `.env`

### **2. main.py**
- ✅ Import `load_dotenv` từ `python-dotenv`
- ✅ Gọi `load_dotenv()` ở startup để load biến môi trường

### **3. config.py**
- ✅ Thêm load dotenv tại top level
- ✅ Chuyển tất cả settings thành environment variables
- ✅ Hỗ trợ default values nếu env var không tồn tại

### **4. service/translation_service.py**
- ✅ Import `load_dotenv`
- ✅ Đọc `GOOGLE_CREDENTIALS_PATH` từ `.env`
- ✅ Fallback sang `gg_cloud_key.json` nếu không có env var

### **5. .env.example** (newly created)
- ✅ Template file cho team members
- ✅ Hướng dẫn các biến cần setup

### **6. .gitignore**
- ✅ Đã có `.env` (được ignore)
- ✅ Thêm `.env.local`, `.env.*.local`, `gg_cloud_key.json`, `*.key`, `*.pem` (credentials)

---

## 🚀 Hướng Dẫn Setup

### **Bước 1: Cài Đặt Dependencies**
```bash
pip install -r requirements.txt
```

Hoặc nếu đã cài trước, chỉ cần:
```bash
pip install python-dotenv==1.0.0
```

### **Bước 2: Tạo File .env Từ Template**

**Trên Windows (Command Prompt):**
```bash
copy .env.example .env
```

**Trên Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Trên macOS/Linux:**
```bash
cp .env.example .env
```

### **Bước 3: Điền Giá Trị Vào .env**

**File `.env` (bạn tạo):**
```env
# Google Cloud Translation API Configuration
GOOGLE_CREDENTIALS_PATH=gg_cloud_key.json

# Database Configuration
DB_PATH=app_data.db

# Logging Configuration
LOG_LEVEL=INFO

# Application Settings
DEBUG=False
```

### **Bước 4: Đặt Google Cloud Credentials (Nếu Dùng)**

1. Download file `gg_cloud_key.json` từ Google Cloud Console
2. Đặt vào project root: `MyEnglish/gg_cloud_key.json`
3. Hoặc chỉ định path khác trong `.env`:
   ```env
   GOOGLE_CREDENTIALS_PATH=/path/to/your/gg_cloud_key.json
   ```

### **Bước 5: Chạy Ứng Dụng**
```bash
flet run main.py
```

---

## 🔐 Cách Các Biến Được Sử Dụng

### **config.py** - Truy Cập Centralized
```python
from config import DATABASE_PATH, GOOGLE_CREDENTIALS_PATH, LOG_LEVEL

# DATABASE_PATH = "app_data.db" (từ .env hoặc default)
# GOOGLE_CREDENTIALS_PATH = "gg_cloud_key.json" (từ .env hoặc default)
# LOG_LEVEL = "INFO" (từ .env hoặc default)
```

### **TranslationService** - Tự Động Load
```python
# TranslationService sẽ:
# 1. Đọc GOOGLE_CREDENTIALS_PATH từ .env
# 2. Nếu không tìm thấy, dùng default "gg_cloud_key.json"
# 3. Nếu file không tồn tại, fallback sang googletrans (free)
```

---

## 📝 Biến Môi Trường Có Sẵn

### **GOOGLE_CREDENTIALS_PATH**
```
Mục đích: Đường dẫn đến Google Cloud credentials JSON file
Mặc định: gg_cloud_key.json
Ví dụ:  GOOGLE_CREDENTIALS_PATH=/home/user/credentials/gg_key.json
```

### **DB_PATH**
```
Mục đích: Đường dẫn đến SQLite database file
Mặc định: app_data.db
Ví dụ: DB_PATH=/var/myapp/database.db
```

### **LOG_LEVEL**
```
Mục đích: Mức độ logging
Mặc định: INFO
Giá trị: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### **DEBUG**
```
Mục đích: Bật/tắt debug mode
Mặc định: False
Giá trị: True hoặc False
```

---

## 👥 Quy Trình Team Development

### **Người tạo repo (Developer 1):**
```bash
# 1. Đã có .env.example
# 2. Commit .env.example lên GitHub
# 3. .env không commit (bị ignore)
```

### **Người khác clone (Developer 2):**
```bash
# 1. Clone repository
git clone <repo>

# 2. Tạo .env từ template
cp .env.example .env

# 3. Điền credentials riêng
# (Edit .env với Google Cloud key path của Developer 2)

# 4. Chạy ứng dụng
flet run main.py
```

**Kết quả:**
```
GitHub: ✅ .env.example (template)
        ❌ .env (bị ignore)
        ❌ gg_cloud_key.json (bị ignore)

Dev 1 Local: .env (credentials)
             gg_cloud_key.json (API key)

Dev 2 Local: .env (credentials khác)
             gg_cloud_key.json (API key khác)
```

---

## ✅ Checklist Chuẩn

- [ ] Cài `pip install -r requirements.txt`
- [ ] Tạo `.env` từ `.env.example`
- [ ] Điền `GOOGLE_CREDENTIALS_PATH` (nếu dùng Google Cloud)
- [ ] Đặt `gg_cloud_key.json` trong project root (nếu có)
- [ ] Chạy `flet run main.py` để test
- [ ] Kiểm tra `git status` → `.env` không hiện (bị ignore)
- [ ] Commit `.env.example` lên GitHub
- [ ] `.env` và `gg_cloud_key.json` KHÔNG commit

---

## 🚨 Thường Gặp Lỗi

### **Lỗi 1: `ModuleNotFoundError: No module named 'dotenv'`**
**Giải pháp:**
```bash
pip install python-dotenv==1.0.0
```

### **Lỗi 2: `[TranslationService] Google Cloud initialization failed`**
**Nguyên nhân:** File `gg_cloud_key.json` không tìm thấy hoặc path sai

**Giải pháp:**
```
1. Check .env → GOOGLE_CREDENTIALS_PATH đúng không?
2. Check file tồn tại chưa?
3. Kiểm tra permission truy cập file
4. App sẽ fallback sang googletrans (free) nếu không có
```

### **Lỗi 3: `.env` bị commit lên GitHub**
**Nguyên nhân:** `.env` không trong `.gitignore`

**Giải pháp:**
```
1. Check .gitignore → có .env chưa?
2. Nếu đã commit trước đó:
   git rm --cached .env
   git commit -m "Remove .env from git history"
```

---

## 🔄 Migration từ Config Cũ

Nếu bạn đã setup trước và đổi vị trí credentials:

**Trước (hardcode):**
```python
key_path = "gg_cloud_key.json"  # Cứng trong code
```

**Bây giờ:**
```env
# Trong .env
GOOGLE_CREDENTIALS_PATH=gg_cloud_key.json
```

**Lợi ích:**
- ✅ Dễ thay đổi (chỉ edit `.env`, không cần code)
- ✅ Production có thể dùng path khác
- ✅ Bảo mật tốt hơn

---

## 📚 Tham Khảo

- **ENV_FILE_GUIDE.md** - Kiến thức chi tiết về .env
- **CONVENTIONS.md** - Quy ước dự án
- **python-dotenv docs:** https://python-dotenv.readthedocs.io/
- **12 Factor App:** https://12factor.net/config

---

**Cập nhật lần cuối:** Tháng 2, 2026
