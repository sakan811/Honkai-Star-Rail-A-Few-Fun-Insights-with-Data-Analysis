"""Tests for the SQLite database functions."""

import pytest
import sqlite3
from unittest.mock import patch, MagicMock, call


from hsrws.db.sqlite import create_views, drop_views, load_to_sqlite


def test_create_views(mock_sqlite_connection):
    """Test creating database views."""
    # Mock the get query functions to return SQL strings with CREATE VIEW
    with (
        patch(
            "hsrws.db.sqlite.get_element_char_count_by_ver",
            return_value="CREATE VIEW ElementCharacterCountByVersion AS SELECT...",
        ),
        patch(
            "hsrws.db.sqlite.get_path_char_count_by_ver",
            return_value="CREATE VIEW PathCharacterCountByVersion AS SELECT...",
        ),
        patch(
            "hsrws.db.sqlite.get_rarity_char_count_by_ver",
            return_value="CREATE VIEW RarityCharacterCountByVersion AS SELECT...",
        ),
    ):
        create_views(mock_sqlite_connection)

        # Verify execute was called for each view
        assert mock_sqlite_connection.execute.call_count == 3

        # Check that all calls to execute contained CREATE VIEW
        for call_args in mock_sqlite_connection.execute.call_args_list:
            assert "CREATE VIEW" in call_args[0][0]


def test_drop_views(mock_sqlite_connection):
    """Test dropping database views."""
    drop_views(mock_sqlite_connection)

    # Verify connection execute was called with DROP VIEW SQL
    assert mock_sqlite_connection.execute.call_count == 3

    # Expected calls
    expected_calls = [
        call("DROP VIEW IF EXISTS ElementCharacterCountByVersion"),
        call("DROP VIEW IF EXISTS PathCharacterCountByVersion"),
        call("DROP VIEW IF EXISTS RarityCharacterCountByVersion"),
    ]

    # Verify all expected calls were made
    for expected in expected_calls:
        assert expected in mock_sqlite_connection.execute.call_args_list


def test_connection_error_handling(sample_character_df):
    """Test error handling when connection fails."""
    with patch("sqlite3.connect") as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            # Attempt to connect and perform an operation
            load_to_sqlite(sample_character_df)


# Test function for load_to_sqlite
def test_load_to_sqlite(sample_character_df):
    """Test loading dataframe to SQLite database."""
    # Mock the to_sql method on the DataFrame
    sample_character_df.to_sql = MagicMock()

    with patch("sqlite3.connect") as mock_connect:
        mock_conn = mock_connect.return_value
        mock_conn.__enter__.return_value = mock_conn

        # Also patch drop_views and create_views to isolate the test
        with patch("hsrws.db.sqlite.drop_views") as mock_drop_views:
            with patch("hsrws.db.sqlite.create_views") as mock_create_views:
                # Call the function under test
                load_to_sqlite(sample_character_df)

                # Verify connection was established
                mock_connect.assert_called_once_with("hsr.db")

                # Verify that to_sql was called on the dataframe
                sample_character_df.to_sql.assert_called_once_with(
                    "HsrCharacters", mock_conn, if_exists="replace"
                )

                # Verify views were managed
                mock_drop_views.assert_called_once_with(mock_conn)
                mock_create_views.assert_called_once_with(mock_conn)
