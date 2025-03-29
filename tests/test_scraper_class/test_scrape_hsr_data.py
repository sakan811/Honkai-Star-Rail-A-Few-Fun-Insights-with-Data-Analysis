from unittest.mock import patch, AsyncMock

import pandas as pd
import pytest

from hsrws.core.scraper import Scraper


@pytest.fixture
def scraper():
    return Scraper()


@pytest.mark.asyncio
async def test_scrape_hsr_data_success(scraper):
    url = "http://test.com"
    headers = {"User-Agent": "Test"}

    mock_char_list = [{"name": "Char1"}, {"name": "Char2"}]
    mock_df = pd.DataFrame({"name": ["Char1", "Char2"]})

    with (
        patch(
            "hsrws.utils.payload.get_payload", new_callable=AsyncMock
        ) as mock_get_payload,
        patch.object(
            scraper, "_fetch_character_list", new_callable=AsyncMock
        ) as mock_fetch,
        patch(
            "hsrws.core.character.process_character_list", new_callable=AsyncMock
        ) as mock_process,
    ):
        mock_get_payload.return_value = {"some": "payload"}
        mock_fetch.side_effect = [mock_char_list, mock_char_list, []]
        scraper.char_data_dict = {"name": ["Char1", "Char2"]}

        result = await scraper.scrape_hsr_data(url, headers)

        assert isinstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, mock_df)
        assert mock_get_payload.call_count == 3
        assert mock_fetch.call_count == 3
        assert mock_process.call_count == 2


@pytest.mark.asyncio
async def test_scrape_hsr_data_empty_first_page(scraper):
    url = "http://test.com"
    headers = {"User-Agent": "Test"}

    with (
        patch(
            "hsrws.utils.payload.get_payload", new_callable=AsyncMock
        ) as mock_get_payload,
        patch.object(
            scraper, "_fetch_character_list", new_callable=AsyncMock
        ) as mock_fetch,
        patch(
            "hsrws.core.character.process_character_list", new_callable=AsyncMock
        ) as mock_process,
    ):
        mock_get_payload.return_value = {"some": "payload"}
        mock_fetch.return_value = []
        scraper.char_data_dict = {}

        result = await scraper.scrape_hsr_data(url, headers)

        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert mock_get_payload.call_count == 1
        assert mock_fetch.call_count == 1
        assert mock_process.call_count == 0


@pytest.mark.asyncio
async def test_scrape_hsr_data_exception(scraper):
    url = "http://test.com"
    headers = {"User-Agent": "Test"}

    with (
        patch(
            "hsrws.utils.payload.get_payload", new_callable=AsyncMock
        ) as mock_get_payload,
        patch.object(
            scraper, "_fetch_character_list", new_callable=AsyncMock
        ) as mock_fetch,
        patch(
            "hsrws.core.character.process_character_list", new_callable=AsyncMock
        ) as mock_process,
    ):
        mock_get_payload.side_effect = Exception("Test error")

        with pytest.raises(Exception):
            await scraper.scrape_hsr_data(url, headers)

        assert mock_get_payload.call_count == 1
        assert mock_fetch.call_count == 0
        assert mock_process.call_count == 0


@pytest.mark.asyncio
async def test_scrape_hsr_data_logging(scraper):
    url = "http://test.com"
    headers = {"User-Agent": "Test"}

    mock_char_list = [{"name": "Char1"}]

    with (
        patch(
            "hsrws.utils.payload.get_payload", new_callable=AsyncMock
        ) as mock_get_payload,
        patch.object(
            scraper, "_fetch_character_list", new_callable=AsyncMock
        ) as mock_fetch,
        patch("hsrws.core.character.process_character_list", new_callable=AsyncMock),
    ):
        mock_get_payload.return_value = {"some": "payload"}
        mock_fetch.side_effect = [mock_char_list, []]
        scraper.char_data_dict = {"name": ["Char1"]}

        await scraper.scrape_hsr_data(url, headers)
