import pytest

from hsrws.hsr_scraper import Scraper, get_headers, get_payload


class MockAsyncContextManager:
    def __init__(self, status, json_data=None):
        self.status = status
        self.json_data = json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def json(self):
        return self.json_data

@pytest.mark.asyncio
async def test_fetch_character_list_success(mocker):
    url = "https://example.com/api"
    headers = get_headers()
    payload_data = await get_payload(1)

    mock_response = MockAsyncContextManager(
        status=200,
        json_data={'data': {'list': [{'name': 'Character1'}, {'name': 'Character2'}]}}
    )

    mocker.patch('aiohttp.ClientSession.post', return_value=mock_response)

    scraper = Scraper()
    char_list = await scraper._fetch_character_list(url, headers, payload_data)

    assert len(char_list) == 2
    assert char_list[0]['name'] == 'Character1'
    assert char_list[1]['name'] == 'Character2'

@pytest.mark.asyncio
async def test_fetch_character_list_failure(mocker):
    url = "https://example.com/api"
    headers = get_headers()
    payload_data = await get_payload(1)

    mock_response = MockAsyncContextManager(status=500)

    mocker.patch('aiohttp.ClientSession.post', return_value=mock_response)

    scraper = Scraper()
    char_list = await scraper._fetch_character_list(url, headers, payload_data)

    assert char_list == []

@pytest.mark.asyncio
async def test_fetch_character_list_empty(mocker):
    url = "https://example.com/api"
    headers = get_headers()
    payload_data = await get_payload(1)

    mock_response = MockAsyncContextManager(
        status=200,
        json_data={'data': {'list': []}}
    )

    mocker.patch('aiohttp.ClientSession.post', return_value=mock_response)

    scraper = Scraper()
    char_list = await scraper._fetch_character_list(url, headers, payload_data)

    assert char_list == []

if __name__ == '__main__':
    pytest.main()