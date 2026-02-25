import pytest
from tests.fixtures.db_fixtures import *
from tests.fixtures.paragraph_model_fixtures import *
from tests.fixtures.sentence_model_fixtures import *
from tests.fixtures.vocabulary_model_fixtures import *
from repositories.db_connect import DBConnect
from repositories.db_init import DBInit


@pytest.fixture(scope="function", autouse=True)
def reset_database_before_each_test():
    """Autouse fixture: Reset DBConnect singleton to in-memory database for each test
    
    Automatically runs before every test to ensure:
    - Fresh, isolated in-memory SQLite database for each test
    - No shared state between tests
    - No interference from local database
    
    Yields control to test, then cleanup after test completes
    """
    # Reset singleton before test starts
    DBConnect._instance = None
    
    # Create fresh in-memory database with initialized schema
    db = DBConnect(":memory:")
    DBInit(db).create_tables()
    
    yield  # Run the test with clean in-memory DB
    
    # Cleanup: Reset singleton after test completes
    DBConnect._instance = None
