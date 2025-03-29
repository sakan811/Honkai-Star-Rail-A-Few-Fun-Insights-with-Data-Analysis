"""Tests for payload utilities."""

import pytest
from unittest.mock import patch
import os

from hsrws.utils.payload import get_headers, default_char_data_dict, get_first_value


def test_get_headers():
    """Test get_headers returns the correct headers dictionary."""
    with patch.dict(os.environ, {"USER_AGENT": "test-agent"}):
        headers = get_headers()
        
        assert isinstance(headers, dict)
        assert headers["Origin"] == "https://wiki.hoyolab.com"
        assert headers["Referer"] == "https://wiki.hoyolab.com/"
        assert headers["User-Agent"] == "test-agent"
        assert headers["X-Rpc-Language"] == "en-us"
        assert headers["X-Rpc-Wiki_app"] == "hsr"


def test_default_char_data_dict():
    """Test default_char_data_dict returns a dictionary with expected keys and empty lists."""
    result = default_char_data_dict()
    
    assert isinstance(result, dict)
    assert "Character" in result and isinstance(result["Character"], list)
    assert "Path" in result and isinstance(result["Path"], list)
    assert "Element" in result and isinstance(result["Element"], list)
    assert "Rarity" in result and isinstance(result["Rarity"], list)
    assert "ATK Lvl 80" in result and isinstance(result["ATK Lvl 80"], list)
    assert "DEF Lvl 80" in result and isinstance(result["DEF Lvl 80"], list)
    assert "HP Lvl 80" in result and isinstance(result["HP Lvl 80"], list)
    assert "SPD Lvl 80" in result and isinstance(result["SPD Lvl 80"], list)
    
    # Check all lists are empty
    assert all(len(value) == 0 for value in result.values())


def test_get_first_value_found():
    """Test get_first_value returns the first value when found."""
    test_data = {
        "test_key": {"values": ["test_value"]},
        "other_key": {"values": ["other_value"]}
    }
    
    result = get_first_value(test_data, "test_key")
    assert result == "test_value"


def test_get_first_value_multiple_keys():
    """Test get_first_value with multiple keys returns first found value."""
    test_data = {
        "test_key": {"values": []},
        "other_key": {"values": ["other_value"]}
    }
    
    result = get_first_value(test_data, "test_key", "other_key")
    assert result == "other_value"


def test_get_first_value_default():
    """Test get_first_value returns the default value when no value is found."""
    test_data = {
        "test_key": {"values": []}
    }
    
    result = get_first_value(test_data, "test_key", default="default_value")
    assert result == "default_value"
    
    # Also test with key not in data
    result = get_first_value(test_data, "non_existent_key", default="default_value")
    assert result == "default_value" 