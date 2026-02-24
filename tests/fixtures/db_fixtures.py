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


# Additional fixtures for db_connect specific tests

@pytest.fixture
def db_memory():
    """Create a fresh DBConnect instance with in-memory database"""
    DBConnect._instance = None
    db = DBConnect(":memory:")
    yield db
    
    if db.conn:
        db.close()


@pytest.fixture
def db_with_test_table():
    """Create a DBConnect instance with a test table"""
    DBConnect._instance = None
    db = DBConnect(":memory:")
    
    # Create test table
    db.execute(
        "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)",
        commit=True
    )
    
    yield db
    
    if db.conn:
        db.close()


@pytest.fixture
def db_with_test_data():
    """Create a DBConnect instance with test table and sample data (5 rows)"""
    DBConnect._instance = None
    db = DBConnect(":memory:")
    
    # Create test table
    db.execute(
        "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)",
        commit=True
    )
    
    # Insert test data
    for i in range(5):
        db.execute(
            "INSERT INTO test_table (name) VALUES (?)",
            (f"Test{i}",),
            commit=True
        )
    
    yield db
    
    if db.conn:
        db.close()


@pytest.fixture
def db_with_3_rows():
    """Create a DBConnect instance with test table and 3 sample rows"""
    DBConnect._instance = None
    db = DBConnect(":memory:")
    
    # Create test table
    db.execute(
        "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)",
        commit=True
    )
    
    # Insert test data
    for i in range(3):
        db.execute(
            "INSERT INTO test_table (name) VALUES (?)",
            (f"Test{i}",),
            commit=True
        )
    
    yield db
    
    if db.conn:
        db.close()


@pytest.fixture
def db_with_fk_table():
    """Create a DBConnect instance with foreign key constraints enabled"""
    DBConnect._instance = None
    db = DBConnect(":memory:")
    
    # Create parent table
    db.execute(
        "CREATE TABLE parent (id INTEGER PRIMARY KEY, name TEXT)",
        commit=True
    )
    
    # Create child table with foreign key
    db.execute(
        "CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER, value TEXT, "
        "FOREIGN KEY (parent_id) REFERENCES parent(id))",
        commit=True
    )
    
    # Insert parent data
    db.execute("INSERT INTO parent (name) VALUES (?)", ("Parent1",), commit=True)
    db.execute("INSERT INTO parent (name) VALUES (?)", ("Parent2",), commit=True)
    
    # Insert child data
    db.execute(
        "INSERT INTO child (parent_id, value) VALUES (?, ?)",
        (1, "Child1"),
        commit=True
    )
    db.execute(
        "INSERT INTO child (parent_id, value) VALUES (?, ?)",
        (1, "Child2"),
        commit=True
    )
    db.execute(
        "INSERT INTO child (parent_id, value) VALUES (?, ?)",
        (2, "Child3"),
        commit=True
    )
    
    yield db
    
    if db.conn:
        db.close()
