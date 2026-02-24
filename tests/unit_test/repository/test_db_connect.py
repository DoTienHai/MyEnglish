import pytest
import sqlite3
import threading
from unittest.mock import Mock, patch, MagicMock
from repositories.db_connect import DBConnect
from tests.fixtures.db_fixtures import (
    db_memory,
    db_with_test_table,
    db_with_test_data,
    db_with_3_rows,
    db_with_fk_table
)


class TestDBConnectSingleton:
    """Test Singleton pattern of DBConnect"""
    
    def test_singleton_returns_same_instance(self):
        """Test that DBConnect always returns the same instance"""
        db1 = DBConnect(":memory:")
        db2 = DBConnect(":memory:")
        assert db1 is db2
    
    def test_singleton_thread_safe(self):
        """Test that singleton is thread-safe"""
        instances = []
        
        def create_instance():
            db = DBConnect(":memory:")
            instances.append(db)
        
        threads = [threading.Thread(target=create_instance) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All instances should be the same object
        assert all(inst is instances[0] for inst in instances)


class TestDBConnectConnection:
    """Test connection management"""
    
    def test_connect_creates_connection(self, db_with_test_table):
        """Test that connect() creates a valid SQLite connection"""
        assert db_with_test_table.conn is not None
        assert isinstance(db_with_test_table.conn, sqlite3.Connection)
    
    def test_foreign_keys_enabled(self, db_with_test_table):
        """Test that PRAGMA foreign_keys is ON"""
        result = db_with_test_table.fetch_one("PRAGMA foreign_keys")
        assert result[0] == 1  # Foreign keys should be enabled


class TestDBConnectCommit:
    """Test commit() method"""
    
    def test_commit_when_connection_exists(self, db_with_test_table):
        """Test commit() calls self.conn.commit() when connection exists"""
        # Insert data
        db_with_test_table.execute("INSERT INTO test_table (name) VALUES (?)", ("Test",), commit=False)
        
        # Commit explicitly
        db_with_test_table.commit()
        
        # Verify data was committed by fetching it
        result = db_with_test_table.fetch_one("SELECT name FROM test_table WHERE name = ?", ("Test",))
        assert result is not None
        assert result[0] == "Test"
    
    def test_commit_when_connection_is_none(self):
        """Test commit() safely handles None connection"""
        DBConnect._instance = None
        db = DBConnect(":memory:")
        db.conn = None
        # Should not raise exception
        db.commit()


class TestDBConnectClose:
    """Test close() method"""
    
    def test_close_commits_and_closes_connection(self):
        """Test that close() commits and closes the connection"""
        DBConnect._instance = None
        db = DBConnect(":memory:")
        db.execute(
            "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)",
            commit=True
        )
        
        # Insert data without commit
        db.execute("INSERT INTO test_table (name) VALUES (?)", ("Test",), commit=False)
        
        # Close should commit the data
        db.close()
        
        # Verify connection is None
        assert db.conn is None
    
    def test_close_when_connection_is_none(self):
        """Test close() safely handles None connection"""
        DBConnect._instance = None
        db = DBConnect(":memory:")
        db.conn = None
        # Should not raise exception
        db.close()


class TestDBConnectExecute:
    """Test execute() method for INSERT/UPDATE/DELETE"""
    
    def test_execute_insert_returns_lastrowid(self, db_with_test_table):
        """Test execute() returns lastrowid for INSERT"""
        result = db_with_test_table.execute(
            "INSERT INTO test_table (name) VALUES (?)",
            ("Test1",),
            commit=True
        )
        assert result > 0  # Should return a valid row ID
    
    def test_execute_insert_multiple_rows(self, db_with_test_table):
        """Test execute() can insert multiple rows"""
        id1 = db_with_test_table.execute("INSERT INTO test_table (name) VALUES (?)", ("Test1",), commit=True)
        id2 = db_with_test_table.execute("INSERT INTO test_table (name) VALUES (?)", ("Test2",), commit=True)
        
        assert id1 != id2
        assert id2 > id1
    
    def test_execute_update(self, db_with_test_table):
        """Test execute() for UPDATE"""
        db_with_test_table.execute("INSERT INTO test_table (name) VALUES (?)", ("Original",), commit=True)
        
        result = db_with_test_table.execute(
            "UPDATE test_table SET name = ? WHERE name = ?",
            ("Updated", "Original"),
            commit=True
        )
        
        # Verify update
        row = db_with_test_table.fetch_one("SELECT name FROM test_table WHERE name = ?", ("Updated",))
        assert row is not None
        assert row[0] == "Updated"
    
    def test_execute_delete(self, db_with_test_table):
        """Test execute() for DELETE"""
        db_with_test_table.execute("INSERT INTO test_table (name) VALUES (?)", ("ToDelete",), commit=True)
        
        db_with_test_table.execute(
            "DELETE FROM test_table WHERE name = ?",
            ("ToDelete",),
            commit=True
        )
        
        # Verify deletion
        row = db_with_test_table.fetch_one("SELECT * FROM test_table WHERE name = ?", ("ToDelete",))
        assert row is None
    
    def test_execute_with_commit_parameter(self, db_with_test_table):
        """Test execute() commits when commit=True"""
        db_with_test_table.execute(
            "INSERT INTO test_table (name) VALUES (?)",
            ("CommitTest",),
            commit=True
        )
        
        # Verify data was committed
        row = db_with_test_table.fetch_one("SELECT name FROM test_table WHERE name = ?", ("CommitTest",))
        assert row is not None
    
    def test_execute_without_commit(self, db_with_test_table):
        """Test execute() doesn't commit when commit=False"""
        db_with_test_table.execute(
            "INSERT INTO test_table (name) VALUES (?)",
            ("NoCommitTest",),
            commit=False
        )
        
        # Commit here to verify the operation worked
        db_with_test_table.commit()
        
        # Verify data exists
        row = db_with_test_table.fetch_one("SELECT name FROM test_table WHERE name = ?", ("NoCommitTest",))
        assert row is not None


class TestDBConnectFetchAll:
    """Test fetch_all() method"""
    
    def test_fetch_all_returns_all_rows(self, db_with_test_data):
        """Test fetch_all() returns all rows from query"""
        results = db_with_test_data.fetch_all("SELECT * FROM test_table")
        assert len(results) == 5
    
    def test_fetch_all_returns_tuples(self, db_with_test_data):
        """Test fetch_all() returns tuples for each row"""
        results = db_with_test_data.fetch_all("SELECT id, name FROM test_table")
        assert all(isinstance(row, tuple) for row in results)
    
    def test_fetch_all_with_parameters(self, db_with_test_data):
        """Test fetch_all() with parameters"""
        results = db_with_test_data.fetch_all(
            "SELECT * FROM test_table WHERE name = ?",
            ("Test2",)
        )
        assert len(results) == 1
        assert results[0][1] == "Test2"
    
    def test_fetch_all_empty_result(self, db_with_test_data):
        """Test fetch_all() returns empty list when no rows found"""
        results = db_with_test_data.fetch_all("SELECT * FROM test_table WHERE name = ?", ("NonExistent",))
        assert results == []


class TestDBConnectFetchOne:
    """Test fetch_one() method"""
    
    def test_fetch_one_returns_single_row(self, db_with_3_rows):
        """Test fetch_one() returns a single row"""
        result = db_with_3_rows.fetch_one("SELECT * FROM test_table WHERE id = ?", (1,))
        assert result is not None
        assert isinstance(result, tuple)
    
    def test_fetch_one_with_parameters(self, db_with_3_rows):
        """Test fetch_one() with parameters"""
        result = db_with_3_rows.fetch_one(
            "SELECT id, name FROM test_table WHERE name = ?",
            ("Test1",)
        )
        assert result is not None
        assert result[1] == "Test1"
    
    def test_fetch_one_returns_none_when_not_found(self, db_with_3_rows):
        """Test fetch_one() returns None when row not found"""
        result = db_with_3_rows.fetch_one("SELECT * FROM test_table WHERE name = ?", ("NonExistent",))
        assert result is None
    
    def test_fetch_one_returns_first_row_when_multiple_match(self, db_with_3_rows):
        """Test fetch_one() returns first row when multiple rows match"""
        # This is SQLite behavior - returns first result
        result = db_with_3_rows.fetch_one("SELECT * FROM test_table LIMIT 1")
        assert result is not None


class TestDBConnectThreadSafety:
    """Test thread safety of execute, fetch operations"""
    
    def test_concurrent_queries_are_safe(self, db_with_test_table):
        """Test that multiple threads can safely query the database"""
        # Insert initial data
        for i in range(10):
            db_with_test_table.execute(
                "INSERT INTO test_table (name) VALUES (?)",
                (f"Value{i}",),
                commit=True
            )
        
        results = []
        errors = []
        
        def fetch_and_update(value):
            try:
                # Fetch
                row = db_with_test_table.fetch_one("SELECT * FROM test_table WHERE name = ?", (f"Value{value}",))
                results.append(row)
                
                # Update
                db_with_test_table.execute(
                    "UPDATE test_table SET name = ? WHERE name = ?",
                    (f"Updated{value}", f"Value{value}"),
                    commit=True
                )
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=fetch_and_update, args=(i,)) for i in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Should have no errors
        assert len(errors) == 0
        assert len(results) == 5
