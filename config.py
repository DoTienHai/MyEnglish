import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# Application Configuration
# ============================================
APP_NAME = "MyEnglish"
APP_VERSION = "1.0.0"

# ============================================
# Database Configuration
# ============================================
DATABASE_PATH = os.getenv("DB_PATH", "app_data.db")

# ============================================
# Logging Configuration
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================
# Translation Configuration
# Loaded from .env (no default fallback)
# ============================================
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

# ============================================
# Application Settings
# ============================================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ============================================
# Screen Navigation Enum
# ============================================
class Screen(Enum):
    HOME = "home"
    TRANSLATE = "translate practice"
    VOCABULARY = "vocabulary"