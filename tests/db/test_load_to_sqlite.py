"""Tests for the load_to_sqlite function."""

import sqlite3
from unittest.mock import patch, call, MagicMock

import pytest

from hsrws.db.sqlite import load_to_sqlite


def test_successful_load(sample_character_df, mock_sqlite_connection):
    """Test successful loading of DataFrame to SQLite."""
    # Mock pandas to_sql method
    with patch('pandas.DataFrame.to_sql') as mock_to_sql, \
         patch('sqlite3.connect', return_value=mock_sqlite_connection) as mock_connect, \
         patch('hsrws.db.sqlite.drop_views') as mock_drop_views, \
         patch('hsrws.db.sqlite.create_views') as mock_create_views:
        
        # Set up the mock connection as a context manager
        mock_sqlite_connection.__enter__ = MagicMock(return_value=mock_sqlite_connection)
        mock_sqlite_connection.__exit__ = MagicMock(return_value=None)
        
        # Call the function under test
        load_to_sqlite(sample_character_df)

        # Verify to_sql was called
        mock_to_sql.assert_called_once_with('HsrCharacters', mock_sqlite_connection, if_exists='replace')
        
        # Verify connect was called with the right DB
        mock_connect.assert_called_once_with('hsr.db')
        
        # Verify drop_views and create_views were called
        mock_drop_views.assert_called_once_with(mock_sqlite_connection)
        mock_create_views.assert_called_once_with(mock_sqlite_connection)


def test_operational_error(sample_character_df):
    """Test error handling when SQLite operation fails."""
    with patch("hsrws.db.sqlite.sqlite3.connect") as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            load_to_sqlite(sample_character_df)
