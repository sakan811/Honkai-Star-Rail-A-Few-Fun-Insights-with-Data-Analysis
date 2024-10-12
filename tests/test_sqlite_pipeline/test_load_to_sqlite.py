import sqlite3
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from hsrws.sqlite_pipeline import load_to_sqlite


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Character': ['Char1', 'Char2'],
        'Element': ['Fire', 'Ice'],
        'Path': ['Destruction', 'Harmony']
    })


@pytest.fixture
def mock_sqlite3():
    with patch('hsrws.sqlite_pipeline.sqlite3') as mock_sqlite:
        mock_conn = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        yield mock_sqlite


def test_successful_load(sample_df, mock_sqlite3):
    load_to_sqlite(sample_df)

    mock_sqlite3.connect.assert_called_once_with('hsr.db')
    mock_conn = mock_sqlite3.connect.return_value.__enter__.return_value
    mock_conn.execute.assert_called()


def test_operational_error(sample_df):
    with patch('hsrws.sqlite_pipeline.sqlite3.connect') as mock_connect:
        mock_connect.side_effect = sqlite3.OperationalError("Test error")

        with pytest.raises(sqlite3.OperationalError):
            load_to_sqlite(sample_df)