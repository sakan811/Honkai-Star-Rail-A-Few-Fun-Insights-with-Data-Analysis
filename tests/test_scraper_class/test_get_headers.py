import pytest

from hsrws.hsr_scraper import get_headers


def test_get_headers(monkeypatch):
    # Set environment variable for testing
    monkeypatch.setenv('USER_AGENT', 'test-agent')

    expected_headers = {
        'Origin': 'https://wiki.hoyolab.com',
        'Referer': 'https://wiki.hoyolab.com/',
        'User-Agent': 'test-agent',
        'X-Rpc-Language': 'en-us',
        'X-Rpc-Wiki_app': 'hsr'
    }

    headers = get_headers()
    assert headers == expected_headers

if __name__ == '__main__':
    pytest.main()