"""Tests for the load_to_sqlite function."""

import sqlite3
from unittest.mock import patch

import pytest

from hsrws.db.sqlite import load_to_sqlite


def test_successful_load(sample_character_df, mock_sqlite_connection):
    """Test successful loading of DataFrame to SQLite."""
    # Mock pandas to_sql method
    with (
        patch("pandas.DataFrame.to_sql") as mock_to_sql,
        patch("sqlite3.connect", return_value=mock_sqlite_connection),
        # Instead of patching non-existent functions, create mock functions
        patch.object(mock_sqlite_connection, "cursor"),
    ):
        # Call the function you're testing
        from hsrws.db.sqlite import load_to_sqlite

        load_to_sqlite(sample_character_df)

        # Assert that to_sql was called with the expected arguments
        mock_to_sql.assert_called_once()


def test_operational_error(sample_character_df):
    """Test error handling when SQLite operation fails."""
    with patch("hsrws.db.sqlite.sqlite3.connect") as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            load_to_sqlite(sample_character_df)
