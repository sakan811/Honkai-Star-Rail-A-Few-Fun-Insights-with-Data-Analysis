"""Tests for the payload utility functions."""

import pytest
from hsrws.utils.payload import get_headers, get_payload, get_first_value


def test_get_headers(mock_environment_variables):
    """Test that get_headers returns the correct headers with environment variables."""
    expected_headers = {
        "Origin": "https://wiki.hoyolab.com",
        "Referer": "https://wiki.hoyolab.com/",
        "User-Agent": "test-agent",
        "X-Rpc-Language": "en-us",
        "X-Rpc-Wiki_app": "hsr",
    }

    headers = get_headers()
    assert headers == expected_headers


@pytest.mark.asyncio
async def test_get_payload():
    """Test that get_payload returns the correct payload structure."""
    page_num = 1
    expected_payload = {
        "filters": [],
        "menu_id": "104",
        "page_num": page_num,
        "page_size": 30,
        "use_es": True,
    }

    payload = await get_payload(page_num)
    assert payload == expected_payload


def test_get_first_value():
    """Test that get_first_value extracts the first value correctly."""
    # Test with valid data having values key
    test_data = {
        "character_paths": {"values": ["Path1"]},
        "character_combat_type": {"values": ["Element1"]},
        "empty_field": {"values": []}
    }

    # Test with valid key
    result = get_first_value(test_data, "character_paths")
    assert result == "Path1"

    # Test with another valid key
    result = get_first_value(test_data, "character_combat_type")
    assert result == "Element1"

    # Test with empty values list
    result = get_first_value(test_data, "empty_field")
    assert result is None

    # Test with missing key
    result = get_first_value(test_data, "not_existing")
    assert result is None

    # Test with default value
    result = get_first_value(test_data, "not_existing", default="default_value")
    assert result == "default_value"
