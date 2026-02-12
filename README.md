# MyEnglish 📚

## Overview

**MyEnglish** is a modern desktop application for English learning, built with Python and [Flet](https://flet.dev/). It provides an interactive platform to practice English through sentence translation, vocabulary tracking, and AI-powered scoring. The project serves as both a practical learning tool and a demonstration of modern desktop app development with clean architecture patterns.
<!-- i want to give user that you can click here to download app exe -->
Download the latest Windows executable (if available): [Download MyEnglish (Windows)](https://drive.google.com/file/d/1MjKpDprdZpvsENBw1uSMLhCFwjrOGEEb/view?usp=drive_link)

## ✨ Key Features

- **Paragraph Management** - Create and track English learning paragraphs with progress monitoring
- **Sentence Translation Practice** - Practice translation with instant AI-powered similarity scoring
- **Vocabulary Tracker** - Build vocabulary lists with daily tracking and statistics visualization
- **Flashcard Practice** - Interactive flashcard mode with multiple-choice questions for vocabulary review
- **Smart Scoring System** - Uses semantic similarity (sentence-transformers) to evaluate translation accuracy
- **Translation Integration** - Quick reference with Google Translate API support
- **Interactive Dashboard** - Visual charts and progress indicators for learning analytics
- **Persistent Storage** - Local SQLite database for offline learning without data loss

---

## 🔑 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **UI Framework** | [Flet](https://flet.dev/) | 0.28.3+ |
| **Language** | Python | 3.8+ |
| **Database** | SQLite3 | (built-in) |
| **ML/AI Scoring** | sentence-transformers | 5.1.2 |
| **Translation** | Google Translate API, googletrans | 4.0.0+ |


**Core Dependencies:**
- `flet` - Desktop UI framework
- `sentence-transformers` - Semantic similarity scoring
- `google-cloud-translate` - Google Cloud Translation API
- `googletrans` - Free translation support (fallback option)

---

## 🚀 Installation

### Step 1: Prerequisites
Ensure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Clone/Download the Repository
```bash
cd MyEnglish
```

### Step 3: Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Create a `.env` file or set the following (if using external APIs):
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/gg_cloud_key.json  # Optional: for Google Translate API
```

---

## ▶️ How to Run & Use

### Running the Application
```bash
flet run main.py
```

The app will:
1. Initialize the SQLite database (`app_data.db`) if it doesn't exist
2. Create all necessary tables automatically
3. Launch the Flet desktop UI

### Building as Standalone Executable
```bash
flet pack main.py
```

---

## 🧪 Testing & Test Reports

### View Test Results
Automated test reports are generated and published to GitHub Pages after each commit:

- **[Test Report](https://dotienhai.github.io/MyEnglish/report.html?sort=result)** - Unit test execution results with detailed pass/fail information
- **[Code Coverage Report](https://dotienhai.github.io/MyEnglish/htmlcov/index.html)** - Coverage analysis showing which code paths are tested

### Running Tests Locally
```bash
# Run all unit tests for repositories
pytest tests/unit_test/repository -v

# Run with coverage report
pytest tests/unit_test/repository -v --cov=repositories --cov-report=html:test_report/htmlcov
```

---

## 📁 Project Structure & Explanation

```
MyEnglish/
├── main.py                          # Application entry point
├── config.py                        # Configuration and constants
├── requirements.txt                 # Python dependencies
├── main.spec                        # PyInstaller configuration
│
├── model/                           # Data models
│   ├── sentence.py                  # Sentence model
│   ├── paragraph.py                 # Paragraph model
│   └── vocabulary.py                # Vocabulary model
│
├── repositories/                    # Data access layer
│   ├── db_connect.py                # SQLite connection (singleton)
│   ├── db_init.py                   # Database initialization
│   ├── repo_base.py                 # Base repository class
│   ├── sentence_repo.py             # Sentence data access
│   ├── paragraph_repo.py            # Paragraph data access
│   └── vocabulary_repo.py           # Vocabulary data access
│
├── service/                         # Business logic layer
│   ├── scoring_service.py           # AI-powered scoring (singleton)
│   ├── translation_service.py       # Translation integration
│   ├── sentence_service.py          # Sentence operations
│   ├── paragraph_service.py         # Paragraph operations
│   └── vocabulary_service.py        # Vocabulary operations
│
├── view/                            # UI components (Flet)
│   ├── main_app_layout.py           # Main application layout
│   ├── components/                  # Reusable UI components
│   │   ├── header.py                # Header component
│   │   ├── navbar.py                # Navigation bar
│   │   ├── footer.py                # Footer component
│   │   ├── flash_card.py            # Flashcard component
│   │   └── loading.py               # Loading indicator
│   └── screens/                     # Application screens
│       ├── home_view.py             # Home dashboard screen
│       ├── translate_practice_view.py # Translation practice screen
│       └── vocabulary_view.py       # Vocabulary management screen
│
├── view_model/                      # ViewModel layer (state management)
│   ├── home_vm.py                   # Home screen logic
│   ├── translate_practice_vm.py     # Translation practice logic
│   └── vocabulary_vm.py             # Vocabulary management logic
│
├── shared/                          # Shared utilities
│   └── observer_base.py             # Observer pattern base class
│
├── storage/                         # Local file storage
│   ├── data/                        # Data storage directory
│   └── temp/                        # Temporary files
│
├── assets/                          # Static resources (images, icons)
│
├── build/                           # PyInstaller build output
│
├── .github/
│   └── copilot-instructions.md      # AI agent development guidance
│
└── README.md                        # This file
```

### Key Directories Explained:

- **model/** - Pure data classes representing domain entities
- **repositories/** - Handles all database operations; uses singleton `DBConnect` for thread-safe connection pooling
- **service/** - Encapsulates business logic and external API calls (scoring, translation)
- **view/** - Flet UI components built as reusable, composable controls
- **view_model/** - Connects UI events to services; manages screen state

---

## 🔧 Environment Variables

### Google Cloud Translation API Setup

The translation feature requires Google Cloud credentials. Follow these steps:

#### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "MyEnglish-Translation")
3. Enable the **Cloud Translation API**

#### Step 2: Create a Service Account
1. In the Cloud Console, navigate to **Service Accounts**
2. Click **Create Service Account**
3. Fill in the service account name and description
4. Click **Create and Continue**
5. Grant the role: **Editor** (or more restrictive: **Cloud Translation API Editor**)
6. Click **Continue** and then **Done**

#### Step 3: Create and Download JSON Key
1. Go to the **Service Accounts** page
2. Click on your created service account
3. Go to the **Keys** tab
4. Click **Add Key** → **Create new key**
5. Select **JSON** format
6. Download the file and rename it to `gg_cloud_key.json`
7. Place it in the project root directory: `MyEnglish/gg_cloud_key.json`

#### Step 4: Set Environment Variable
```bash
# Windows (Command Prompt)
set GOOGLE_APPLICATION_CREDENTIALS=gg_cloud_key.json

# Windows (PowerShell)
$env:GOOGLE_APPLICATION_CREDENTIALS="gg_cloud_key.json"

# macOS/Linux
export GOOGLE_APPLICATION_CREDENTIALS=gg_cloud_key.json
```

Or add to a `.env` file:
```
GOOGLE_APPLICATION_CREDENTIALS=gg_cloud_key.json
```

**⚠️ Security Note:** Never commit `gg_cloud_key.json` to version control. Add it to `.gitignore`:
```
gg_cloud_key.json
.env
```

### Optional Configuration
For other settings:
```
# Database location (optional)
DB_PATH=app_data.db

# Logging level (optional)
LOG_LEVEL=INFO
```

### Configuration File
Edit `config.py` for:
- Application title and version
- Database path
- Default settings
- Color theme definitions
- UI preferences

---

## 🤝 Contribution Guidelines

### Code Standards
1. **Follow MVCS Pattern** - Keep model, view, service, and controller concerns separated
2. **Use Naming Conventions**:
   - `*_service.py` for business logic
   - `*_repo.py` for data access
   - `*_vm.py` for ViewModels
3. **Thread Safety** - Use locks for shared resources (see `db_connect.py` for example)
4. **Type Hints** - Add Python type annotations where possible
5. **Comments** - Explain complex logic, especially business rules

### Development Workflow
1. Create a new branch for your feature: `git checkout -b feature/your-feature`
2. Make changes following the code conventions
3. Test thoroughly before committing
4. Write clear commit messages
5. Submit a pull request with detailed description

---

## 📄 License

**Personal Learning Project** - Educational use only

This project is developed as a personal learning exercise and for demonstration purposes. Feel free to use it as a reference for building desktop applications with Flet and Python.

---

## 📚 Additional Resources

- [Flet Documentation](https://flet.dev/)
- [Sentence Transformers](https://www.sbert.net/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [AI Development Guidance](.github/copilot-instructions.md)

---

## 🚦 Current Status

- ✅ Core MVCS architecture
- ✅ Paragraph and vocabulary management
- ✅ AI-powered sentence scoring
- ✅ Interactive dashboard with charts
- ✅ Database persistence
- 🔄 Continuous improvements and feature additions
