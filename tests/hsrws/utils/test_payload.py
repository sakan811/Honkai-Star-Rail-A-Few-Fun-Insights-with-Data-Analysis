"""Tests for the payload utility functions."""

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


def test_get_payload():
    """Test that get_payload returns the correct payload structure."""
    expected_payload = {
        "filters": [],
        "page_num": 1,
        "page_size": 100,
        "use_default_keywords": True,
        "need_count": True,
    }

    payload = get_payload()
    assert payload == expected_payload


def test_get_first_value():
    """Test that get_first_value extracts the first value correctly."""
    test_data = {"data": {"list": [{"test_field": "test_value"}]}}

    # Test with valid path
    result = get_first_value(test_data, ["data", "list", 0, "test_field"])
    assert result == "test_value"

    # Test with invalid path
    result = get_first_value(test_data, ["data", "invalid", 0])
    assert result is None

    # Test with default value
    result = get_first_value(test_data, ["data", "invalid"], default="default_value")
    assert result == "default_value"
