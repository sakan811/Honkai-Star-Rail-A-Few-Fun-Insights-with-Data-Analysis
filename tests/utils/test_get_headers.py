"""Tests for the get_headers utility function."""

import pytest

from hsrws.utils.payload import get_headers


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


if __name__ == "__main__":
    pytest.main()
