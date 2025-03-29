"""Pytest configuration file for hsrws tests."""

import os
import sys
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Configure pytest
def pytest_configure(config):
    """Configure pytest for hsrws tests."""
    # Register markers
    config.addinivalue_line("markers", "db: mark tests that require database")
    config.addinivalue_line("markers", "scraper: mark tests that use scraper")
    config.addinivalue_line("markers", "asyncio: mark tests that use asyncio")
    config.addinivalue_line("markers", "visual: mark tests that generate visuals")


# Common fixtures that can be used across multiple test modules


@pytest.fixture
def sample_character_df():
    """Return a sample character DataFrame for testing."""
    return pd.DataFrame(
        {
            "Character": ["Test Character", "Another Character"],
            "Path": ["Test Path", "Another Path"],
            "Element": ["Test Element", "Another Element"],
            "Rarity": [5, 4],
            "ATK Lvl 80": [100, 120],
            "DEF Lvl 80": [200, 180],
            "HP Lvl 80": [1000, 1200],
            "SPD Lvl 80": [100, 110],
        }
    )


@pytest.fixture
def mock_sqlite_connection():
    """Return a mock SQLite connection."""
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_conn


@pytest.fixture
def mock_environment_variables(monkeypatch):
    """Set mock environment variables for testing."""
    monkeypatch.setenv("USER_AGENT", "test-agent")
    return {"USER_AGENT": "test-agent"}


@pytest.fixture
def mock_character_list():
    """Return a mock character list for testing."""
    return [
        {
            "name": "Character1",
            "element": {"name": "Fire"},
            "path": {"name": "The Hunt"},
            "rarity": 5,
        },
        {
            "name": "Character2",
            "element": {"name": "Ice"},
            "path": {"name": "The Harmony"},
            "rarity": 4,
        },
    ]
