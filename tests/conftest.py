"""Pytest configuration file for hsrws tests."""

import pytest
import os
import sys

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