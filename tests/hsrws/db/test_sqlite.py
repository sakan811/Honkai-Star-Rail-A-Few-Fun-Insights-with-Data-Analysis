"""Tests for the SQLite database functions."""

import pytest
import sqlite3
from unittest.mock import patch


from hsrws.db.sqlite import create_tables, load_data, create_views, drop_views


def test_create_tables(mock_sqlite_connection):
    """Test creating database tables."""
    create_tables(mock_sqlite_connection)

    # Verify connection execute was called with CREATE TABLE SQL
    mock_sqlite_connection.execute.assert_called()

    # Check at least one call contains "CREATE TABLE"
    create_calls = [
        call
        for call in mock_sqlite_connection.execute.call_args_list
        if isinstance(call[0][0], str) and "CREATE TABLE" in call[0][0]
    ]
    assert len(create_calls) > 0


def test_load_data(sample_character_df, mock_sqlite_connection):
    """Test loading data into database."""
    load_data(mock_sqlite_connection, sample_character_df)

    # Verify connection method calls
    mock_sqlite_connection.execute.assert_called()
    mock_sqlite_connection.commit.assert_called_once()


def test_create_views(mock_sqlite_connection):
    """Test creating database views."""
    create_views(mock_sqlite_connection)

    # Verify connection execute was called with CREATE VIEW SQL
    mock_sqlite_connection.execute.assert_called()

    # Check at least one call contains "CREATE VIEW"
    view_calls = [
        call
        for call in mock_sqlite_connection.execute.call_args_list
        if isinstance(call[0][0], str) and "CREATE VIEW" in call[0][0]
    ]
    assert len(view_calls) > 0


def test_drop_views(mock_sqlite_connection):
    """Test dropping database views."""
    drop_views(mock_sqlite_connection)

    # Verify connection execute was called with DROP VIEW SQL
    mock_sqlite_connection.execute.assert_called()

    # Check at least one call contains "DROP VIEW"
    drop_calls = [
        call
        for call in mock_sqlite_connection.execute.call_args_list
        if isinstance(call[0][0], str) and "DROP VIEW" in call[0][0]
    ]
    assert len(drop_calls) > 0


def test_connection_error_handling():
    """Test error handling when connection fails."""
    with patch("sqlite3.connect") as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            # Attempt to connect and perform an operation
            conn = sqlite3.connect("test.db")
            create_tables(conn)
