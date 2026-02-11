"""Database fixtures for testing"""
from typing import Generator
import pytest
from repositories.db_connect import DBConnect
from repositories.db_init import DBInit
from repositories.paragraph_repo import ParagraphRepository
from repositories.sentence_repo import SentenceRepository
from repositories.vocabulary_repo import VocabularyRepository


@pytest.fixture(scope="function")
def memory_db() -> Generator[DBConnect, None, None]:
    """In-memory SQLite database for tests
    
    This fixture creates a fresh SQLite database in RAM (":memory:") for each test.
    - Scope: function - Each test gets a new isolated database instance
    - Benefit: Fast (RAM is faster than disk), Clean (auto-deleted after test), Isolated (no cross-test contamination)
    - Data flow: Create DB → Initialize tables → Use in test → Auto cleanup when test ends
    
    Returns:
        Generator[DBConnect, None, None]: Database connection object stored in RAM
    """
    # Reset singleton before creating new instance
    DBConnect._instance = None
    
    # Create in-memory database (data stored in RAM, not disk)
    db = DBConnect(":memory:")
    
    # Initialize database schema (create tables, indexes, etc.)
    DBInit(db).create_tables()
    
    yield db
    
    # Cleanup: Reset singleton after test
    DBConnect._instance = None


@pytest.fixture(scope="function")
def paragraph_repo(memory_db: DBConnect) -> ParagraphRepository:
    """ParagraphRepository với in-memory DB"""
    return ParagraphRepository(memory_db)


@pytest.fixture(scope="function")
def sentence_repo(memory_db: DBConnect) -> SentenceRepository:
    """SentenceRepository với in-memory DB"""
    return SentenceRepository(memory_db)


@pytest.fixture(scope="function")
def vocabulary_repo(memory_db: DBConnect) -> VocabularyRepository:
    """VocabularyRepository với in-memory DB"""
    return VocabularyRepository(memory_db)
