"""Tests for the SQLite database functions."""

import pytest
import sqlite3
from unittest.mock import patch, MagicMock


from hsrws.db.sqlite import load_to_sqlite


def test_connection_error_handling(sample_character_df):
    """Test error handling when connection fails."""
    with patch("sqlite3.connect") as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            # Attempt to connect and perform an operation
            load_to_sqlite(sample_character_df)


def test_load_to_sqlite(sample_character_df):
    """Test loading dataframe to SQLite database."""
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        # Mock the to_sql method on the DataFrame class, not the instance
        with patch("pandas.DataFrame.to_sql") as mock_to_sql:
            # Call the function
            load_to_sqlite(sample_character_df)

            # Verify that to_sql was called with the correct arguments
            mock_to_sql.assert_called_once_with(
                "HsrCharacters", mock_conn, if_exists="replace"
            )
