"""Tests for the load_to_sqlite function."""

import sqlite3
from unittest.mock import patch

import pytest

from hsrws.sqlite_pipeline import load_to_sqlite


def test_successful_load(sample_character_df, mock_sqlite_connection):
    """Test successful loading of DataFrame to SQLite."""
    load_to_sqlite(sample_character_df)

    # Verify connection and execution occurred
    mock_sqlite_connection.execute.assert_called()

    # Verify commit was called
    mock_sqlite_connection.commit.assert_called_once()


def test_operational_error(sample_character_df):
    """Test error handling when SQLite operation fails."""
    with patch("hsrws.sqlite_pipeline.sqlite3.connect") as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            load_to_sqlite(sample_character_df)
