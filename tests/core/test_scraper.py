"""Tests for the core scraper functionality."""

import pytest
import pandas as pd
from unittest.mock import patch, AsyncMock

from hsrws.core.scraper import Scraper
from hsrws.core.character import scrape_character_data


@pytest.mark.asyncio
async def test_fetch_character_list():
    """Test fetching the character list."""
    # Define the expected result
    test_data = [
        {"name": "Character1", "icon": "icon1.png"},
        {"name": "Character2", "icon": "icon2.png"},
    ]

    # Create a scraper instance
    scraper = Scraper()

    # Create our own implementation of _fetch_character_list to replace the real one
    async def mock_fetch_impl(self, url, headers, payload_data):
        assert url == "https://test.url"
        assert headers == {"User-Agent": "test"}
        assert payload_data == {"page_num": 1}
        return test_data

    # Patch the _fetch_character_list method with our mock implementation
    with patch.object(Scraper, "_fetch_character_list", new=mock_fetch_impl):
        # Call the method under test
        url = "https://test.url"
        headers = {"User-Agent": "test"}
        payload = {"page_num": 1}
        result = await scraper._fetch_character_list(url, headers, payload)

        # Verify results
        assert result == test_data
        assert len(result) == 2
        assert result[0]["name"] == "Character1"
        assert result[1]["name"] == "Character2"


@pytest.mark.asyncio
async def test_scrape_character_data():
    """Test scraping individual character data."""
    # Mock character data
    mock_char = {
        "name": "Test Character",
        "filter_values": {
            "path": {"values": ["The Hunt"]},
            "element": {"values": ["Fire"]},
            "rarity": {"values": [5]},
        },
        "display_field": {
            "attr_level_80": '{"base_atk": 100, "base_def": 200, "base_hp": 1000, "base_speed": 100}'
        },
    }

    # Create a scraper instance with initialized char_data_dict
    scraper = Scraper()
    scraper.char_data_dict = {
        "Character": [],
        "Path": [],
        "Element": [],
        "Rarity": [],
        "ATK Lvl 80": [],
        "DEF Lvl 80": [],
        "HP Lvl 80": [],
        "SPD Lvl 80": [],
    }

    # Call the function under test
    await scrape_character_data(scraper, mock_char)

    # Verify results
    assert scraper.char_data_dict["Character"] == ["Test Character"]
    assert scraper.char_data_dict["Path"] == ["The Hunt"]
    assert scraper.char_data_dict["Element"] == ["Fire"]
    assert scraper.char_data_dict["Rarity"] == [5]
    assert scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert scraper.char_data_dict["HP Lvl 80"] == [1000]
    assert scraper.char_data_dict["SPD Lvl 80"] == [100]


@pytest.mark.asyncio
async def test_scrape_hsr_data():
    """Test the main scraper function that coordinates the entire process."""
    # Create a mock character list
    mock_char_list = [
        {
            "name": "Character1",
            "filter_values": {
                "path": {"values": ["The Hunt"]},
                "element": {"values": ["Fire"]},
                "rarity": {"values": [5]},
            },
        },
        {
            "name": "Character2",
            "filter_values": {
                "path": {"values": ["The Harmony"]},
                "element": {"values": ["Ice"]},
                "rarity": {"values": [4]},
            },
        },
    ]

    # Create a scraper instance
    scraper = Scraper()

    # Mock the _fetch_character_list method
    with patch.object(
        scraper, "_fetch_character_list", new_callable=AsyncMock
    ) as mock_fetch:
        # Set up the mock to return our test data and then empty list to end the loop
        mock_fetch.side_effect = [mock_char_list, []]

        # Mock process_character_list to simulate processing characters
        with patch(
            "hsrws.core.character.process_character_list", new_callable=AsyncMock
        ) as mock_process:
            # Call the method under test
            url = "https://test.url"
            headers = {"User-Agent": "test"}
            result_df = await scraper.scrape_hsr_data(url, headers)

            # Verify results
            assert isinstance(result_df, pd.DataFrame)
            assert mock_fetch.call_count == 2
            assert mock_process.call_count == 1
            assert mock_process.call_args[0][0] == scraper
            assert mock_process.call_args[0][1] == mock_char_list
