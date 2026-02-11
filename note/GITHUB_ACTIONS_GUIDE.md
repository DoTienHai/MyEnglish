# GitHub Actions Hướng Dẫn Tích Hợp

## � Mục Lục

- [GitHub Actions Hướng Dẫn Tích Hợp](#github-actions-hướng-dẫn-tích-hợp)
  - [� Mục Lục](#-mục-lục)
  - [�📌 GitHub Actions Là Gì?](#-github-actions-là-gì)
  - [💰 GitHub Actions Có Free Không?](#-github-actions-có-free-không)
  - [🚀 Cách Tích Hợp Cho MyEnglish Project](#-cách-tích-hợp-cho-myenglish-project)
    - [⚠️ Quy Tắc Bắt Buộc](#️-quy-tắc-bắt-buộc)
    - [Bước 1: Tạo Thư Mục `.github/workflows`](#bước-1-tạo-thư-mục-githubworkflows)
    - [Bước 2: File Cấu Hình Workflow](#bước-2-file-cấu-hình-workflow)
      - [**File 1: `.github/workflows/test.yml`** (Chạy Tests)](#file-1-githubworkflowstestyml-chạy-tests)
      - [**File 2: `.github/workflows/test-report.yml`** (Tạo Test Report)](#file-2-githubworkflowstest-reportyml-tạo-test-report)
  - [� Giải Thích Chi Tiết Files](#-giải-thích-chi-tiết-files)
    - [**File 1: `test.yml` - Chạy Tests Trên Nhiều Python Versions**](#file-1-testyml---chạy-tests-trên-nhiều-python-versions)
    - [**File 2: `test-report.yml` - Tạo HTML Report Chi Tiết**](#file-2-test-reportyml---tạo-html-report-chi-tiết)
    - [**So Sánh 2 Files**](#so-sánh-2-files)
    - [**Quy Trình Thực Tế**](#quy-trình-thực-tế)
  - [�📦 Cài Đặt Thêm Packages](#-cài-đặt-thêm-packages)
  - [🔧 Hướng Dẫn Chi Tiết Các Bước](#-hướng-dẫn-chi-tiết-các-bước)
    - [**Bước 1: Push `.github/workflows` lên GitHub**](#bước-1-push-githubworkflows-lên-github)
    - [**Bước 2: Kiểm Tra Workflows**](#bước-2-kiểm-tra-workflows)
    - [**Bước 3: Badge Status (Optional)**](#bước-3-badge-status-optional)
  - [🎯 Cấu Trúc Workflow Chi Tiết](#-cấu-trúc-workflow-chi-tiết)
    - [**Kiến Thức Cơ Bản**](#kiến-thức-cơ-bản)
    - [**Events (Sự Kiện Kích Hoạt)**](#events-sự-kiện-kích-hoạt)
    - [**Matrix Testing**](#matrix-testing)
  - [📊 Sử Dụng Codecov Cho Coverage Report](#-sử-dụng-codecov-cho-coverage-report)
    - [**1. Tại Account Trên Codecov**](#1-tại-account-trên-codecov)
    - [**2. Thêm Badge Vào README**](#2-thêm-badge-vào-readme)
  - [🔒 Secret Variables (Nếu Cần)](#-secret-variables-nếu-cần)
  - [⚙️ Workflows Khác Hữu Ích](#️-workflows-khác-hữu-ích)
    - [**Auto Format Code**](#auto-format-code)
    - [**Auto Build Executable**](#auto-build-executable)
  - [🐛 Troubleshooting](#-troubleshooting)
  - [📝 Ví Dụ Hoàn Chỉnh Cho MyEnglish](#-ví-dụ-hoàn-chỉnh-cho-myenglish)
    - [**.github/workflows/myenglish-ci.yml**](#githubworkflowsmyenglish-ciyml)
  - [🎓 Lệnh Chạy Tests Cục Bộ (Trước Khi Push)](#-lệnh-chạy-tests-cục-bộ-trước-khi-push)
  - [📚 Tài Liệu Tham Khảo](#-tài-liệu-tham-khảo)
  - [✅ Checklist Tích Hợp](#-checklist-tích-hợp)

---

## �📌 GitHub Actions Là Gì?

GitHub Actions là dịch vụ tự động hóa (CI/CD) do GitHub cung cấp, cho phép bạn tự động chạy các tác vụ khi có sự kiện xảy ra như:
- Đẩy code (push)
- Tạo pull request
- Tạo release
- Theo lịch định kỳ

## 💰 GitHub Actions Có Free Không?

**CÓ! GitHub Actions HOÀN TOÀN MIỄN PHÍ** cho các public repository và private repository với giới hạn:

| Loại Repository | Giới hạn | Chi phí |
|---|---|---|
| **Public** | Unlimited | **MIỄN PHÍ** |
| **Private** | 2,000 phút/tháng | **MIỄN PHÍ** (vượt quá sẽ tính phí) |

👉 **Lưu ý**: Nếu vượt quá 2,000 phút/tháng, GitHub sẽ tính phí $0.24 per 1,000 phút.

---

## 🚀 Cách Tích Hợp Cho MyEnglish Project

### ⚠️ Quy Tắc Bắt Buộc

| Tiêu Chí | Bắt Buộc | Chi Tiết |
|---|---|---|
| **Thư mục** | ✅ Yes | **`.github/workflows/`** (GitHub chỉ quét folder này) |
| **Extension** | ✅ Yes | `.yml` hoặc `.yaml` |
| **YAML syntax** | ✅ Yes | Phải valid YAML (indentation, colon, etc.) |
| **Tên file** | ❌ No | Convention tùy ý (`test.yml`, `ci.yml`, `build.yml`, etc.) |
| **Nội dung tối thiểu** | ✅ Yes | Phải có: `name`, `on` (event), `jobs` |

**Ví dụ hợp lệ:**
```
✅ .github/workflows/test.yml         → GitHub sẽ detect
❌ .github/test.yml                   → GitHub sẽ KHÔNG detect
❌ workflows/test.yml                 → GitHub sẽ KHÔNG detect
```

### Bước 1: Tạo Thư Mục `.github/workflows`

```bash
.github/
└── workflows/
    ├── test.yml
    └── test-report.yml
```

### Bước 2: File Cấu Hình Workflow

#### **File 1: `.github/workflows/test.yml`** (Chạy Tests)

```yaml
name: Run Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=. --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

#### **File 2: `.github/workflows/test-report.yml`** (Tạo Test Report)

```yaml
name: Generate Test Report

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-report:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-html pytest-cov
    
    - name: Run tests with HTML report
      run: |
        pytest tests/ \
          --html=report.html \
          --cov=. \
          --cov-report=html:htmlcov \
          --cov-report=term-missing
    
    - name: Upload HTML report as artifact
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-report
        path: report.html
    
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: coverage-report
        path: htmlcov/
```

---

## � Giải Thích Chi Tiết Files

### **File 1: `test.yml` - Chạy Tests Trên Nhiều Python Versions**

```yaml
name: Run Tests                        # Tên workflow hiển thị trên Actions tab
```
- **Mục đích**: Kiểm tra code tương thích với Python 3.9, 3.10, 3.11
- **Kích hoạt**: Mỗi lần push hoặc tạo PR

```yaml
on:
  push:
    branches: [ main, develop ]        # Khi push đến main hoặc develop
  pull_request:
    branches: [ main, develop ]        # Khi tạo PR đến main hoặc develop
```

```yaml
jobs:
  test:
    runs-on: ubuntu-latest             # Chạy trên máy Linux (miễn phí, nhanh)
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']  # Chạy 3 lần + 3 Python versions
        # Nếu 1 version fail → những version khác vẫn tiếp tục chạy
```

```yaml
    steps:
    - uses: actions/checkout@v3        # Tải code từ GitHub repo
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4    # Cài đặt Python (từ matrix)
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip        # Cập nhật pip
        pip install -r requirements.txt            # Cài packages dự án
        pip install pytest pytest-cov              # Cài test tools
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=. --cov-report=xml --cov-report=html
        # -v = verbose (hiển thị chi tiết từng test)
        # --cov=. = tính coverage cho toàn project (folder hiện tại)
        # --cov-report=xml = tạo coverage.xml (cho Codecov upload)
        # --cov-report=html = tạo htmlcov/ folder (view report cục bộ)
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3           # Action Codecov cung cấp
      with:
        file: ./coverage.xml                    # File XML của pytest
        fail_ci_if_error: true                  # CI fail nếu upload lỗi
```

**Kết quả:**
- ✅ Tests pass/fail trên Python 3.9, 3.10, 3.11
- 📊 Coverage report gửi lên Codecov

---

### **File 2: `test-report.yml` - Tạo HTML Report Chi Tiết**

```yaml
name: Generate Test Report

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]                 # Chỉ PR vào main (khác file 1)
```

```yaml
jobs:
  test-report:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'         # Chỉ 1 version (nhanh hơn file 1)
    
    - name: Install dependencies
      run: |
        ...
        pip install pytest pytest-html pytest-cov  # pytest-html tạo HTML report
    
    - name: Run tests with HTML report
      run: |
        pytest tests/ \
          --html=report.html \              # Tạo report.html (HTML report)
          --cov=. \                         # Coverage calculation
          --cov-report=html:htmlcov \       # Tạo folder htmlcov/ (HTML coverage)
          --cov-report=term-missing         # In missing coverage vào terminal
    
    - name: Upload HTML report as artifact
      uses: actions/upload-artifact@v3      # Lưu trữ output file
      if: always()                          # Chạy dù test fail
      with:
        name: test-report                   # Tên artifact
        path: report.html                   # File report.html
    
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: coverage-report
        path: htmlcov/                      # Folder chứa coverage report HTML
```

**Kết quả:**
- 📄 report.html = Test report (xem passed/failed tests)
- 📊 htmlcov/ = Coverage HTML (xem % code được test)
- 💾 Artifacts = Download từ GitHub Actions tab

---

### **So Sánh 2 Files**

| Tính Năng | test.yml | test-report.yml |
|---|---|---|
| **Python Versions** | 3 versions (matrix) | 1 version (nhanh) |
| **HTML Report** | ❌ Không | ✅ report.html |
| **Coverage HTML** | ❌ Không | ✅ htmlcov/ folder |
| **Upload Codecov** | ✅ Có | ❌ Không |
| **Tốc độ** | ~5-10 phút | ~2-3 phút |
| **Lưu trữ** | Codecov online | GitHub Artifacts |

---

### **Quy Trình Thực Tế**

```
Bạn push code lên GitHub
  ↓
GitHub Actions kích hoạt CÙNG LÚC:
  ├─ test.yml chạy:
  │   ├─ Python 3.9 test
  │   ├─ Python 3.10 test
  │   ├─ Python 3.11 test
  │   └─ Upload coverage.xml → Codecov
  │
  └─ test-report.yml chạy:
      ├─ Python 3.11 test 1 lần
      ├─ Tạo report.html
      ├─ Tạo htmlcov/
      └─ Save artifacts
  ↓
Kết quả: Trên GitHub Actions tab
  - Xem test results
  - Download report.html, htmlcov/
  - Xem Codecov dashboard
```

---

## �📦 Cài Đặt Thêm Packages

Thêm vào `requirements.txt` để chạy test reports:

```txt
pytest>=7.0
pytest-cov>=4.0
pytest-html>=3.1
```

---

## 🔧 Hướng Dẫn Chi Tiết Các Bước

### **Bước 1: Push `.github/workflows` lên GitHub**

```bash
# 1. Tạo thư mục
mkdir -p .github/workflows

# 2. Tạo files YAML (xem bên dưới)

# 3. Push lên GitHub
git add .github/
git commit -m "Add GitHub Actions workflows"
git push origin main
```

### **Bước 2: Kiểm Tra Workflows**

Trên GitHub:
1. Vào **Actions** tab
2. Chọn workflow để xem chi tiết
3. Xem logs của từng job

### **Bước 3: Badge Status (Optional)**

Thêm badge vào `README.md` để hiển thị status:

```markdown
![Tests](https://github.com/YOUR_USERNAME/MyEnglish/actions/workflows/test.yml/badge.svg)
```

---

## 🎯 Cấu Trúc Workflow Chi Tiết

### **Kiến Thức Cơ Bản**

```yaml
name: Tên Workflow                    # Tên hiển thị
on: [push, pull_request]              # Sự kiện kích hoạt
jobs:                                 # Danh sách công việc
  test:                               # Tên job
    runs-on: ubuntu-latest            # OS chạy
    steps:                            # Các bước
      - uses: actions/checkout@v3     # Action có sẵn
      - run: echo "Hello"             # Lệnh shell
```

### **Events (Sự Kiện Kích Hoạt)**

```yaml
on:
  push:
    branches: [ main, develop ]       # Khi push đến branches này
  pull_request:
    branches: [ main ]                # Khi tạo PR đến main
  schedule:
    - cron: '0 0 * * 0'              # Hàng tuần (0h Chủ nhật UTC)
```

### **Matrix Testing**

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    os: [ubuntu-latest, windows-latest]
```

Sẽ chạy test trên tất cả tổ hợp (3 versions × 2 OS = 6 job).

---

## 📊 Sử Dụng Codecov Cho Coverage Report

### **1. Tại Account Trên Codecov**

- Truy cập [codecov.io](https://codecov.io)
- Kết nối GitHub account
- Escolha repositories muốn theo dõi

### **2. Thêm Badge Vào README**

```markdown
[![codecov](https://codecov.io/gh/YOUR_USERNAME/MyEnglish/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/MyEnglish)
```

---

## 🔒 Secret Variables (Nếu Cần)

Nếu cần token hoặc key bí mật (ví dụ: API key, database password):

1. **GitHub** → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Sử dụng trong workflow:

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: python deploy.py
```

---

## ⚙️ Workflows Khác Hữu Ích

### **Auto Format Code**

```yaml
name: Code Format Check

on: [push, pull_request]

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install black flake8
      - run: black --check .
      - run: flake8 .
```

### **Auto Build Executable**

```yaml
name: Build Executable

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: pyinstaller main.spec
      - uses: actions/upload-artifact@v3
        with:
          name: myenglish-app
          path: dist/main.exe
```

---

## 🐛 Troubleshooting

| Vấn Đề | Giải Pháp |
|---|---|
| ❌ ImportError: module not found | Thêm vào requirements.txt |
| ❌ Workflow không chạy | Kiểm tra branch name & syntax YAML |
| ❌ Timeout (>360 phút) | Tối ưu tests hoặc chia nhỏ jobs |
| ❌ Permission denied | Kiểm tra GitHub token permissions |

---

## 📝 Ví Dụ Hoàn Chỉnh Cho MyEnglish

### **.github/workflows/myenglish-ci.yml**

```yaml
name: MyEnglish CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-and-report:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-html
    
    - name: Run linters (optional)
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      continue-on-error: true
    
    - name: Run tests and generate reports
      run: |
        pytest tests/ \
          -v \
          --html=report.html \
          --cov=. \
          --cov-report=xml \
          --cov-report=html:htmlcov \
          --cov-report=term-missing
    
    - name: Upload test report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-report
        path: report.html
        retention-days: 30
    
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: coverage-report
        path: htmlcov/
        retention-days: 30
    
    - name: Comment PR with coverage
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const coverage = fs.readFileSync('htmlcov/status.json', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `📊 **Test Report**: [View Report](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})`
          });
```

---

## 🎓 Lệnh Chạy Tests Cục Bộ (Trước Khi Push)

```bash
# Cài đặt test packages
pip install pytest pytest-cov pytest-html

# Chạy tests và tạo reports
pytest tests/ \
  -v \
  --html=report.html \
  --cov=. \
  --cov-report=html:htmlcov \
  --cov-report=term-missing

# Xem HTML report
# Windows
start report.html

# Linux/Mac
open report.html
```

---

## 📚 Tài Liệu Tham Khảo

- [GitHub Actions Official Docs](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.io/)

---

## ✅ Checklist Tích Hợp

- [ ] Tạo thư mục `.github/workflows/`
- [ ] Tạo file `test.yml`
- [ ] Tạo file `test-report.yml`
- [ ] Cập nhật `requirements.txt` với pytest packages
- [ ] Push lên GitHub
- [ ] Kiểm tra Actions tab trên GitHub
- [ ] Thêm badges vào README.md
- [ ] (Optional) Tạo Codecov account

---

**Created**: February 11, 2026
**Updated**: Latest
