"""Tests for the core scraper functionality."""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, AsyncMock

from hsrws.core.scraper import (
    fetch_character_list,
    scrape_character_data,
    scrape_hsr_data,
)


@pytest.mark.asyncio
async def test_fetch_character_list():
    """Test fetching the character list."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "list": [
                {"name": "Character1", "icon": "icon1.png"},
                {"name": "Character2", "icon": "icon2.png"},
            ]
        }
    }

    # Mock the aiohttp.ClientSession
    mock_session = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_response

    # Call the function under test
    result = await fetch_character_list(mock_session)

    # Verify results
    assert len(result) == 2
    assert result[0]["name"] == "Character1"
    assert result[1]["name"] == "Character2"


@pytest.mark.asyncio
async def test_scrape_character_data():
    """Test scraping individual character data."""
    # Mock character data
    mock_char = {
        "name": "Test Character",
        "element": {"name": "Fire"},
        "path": {"name": "The Hunt"},
        "rarity": 5,
    }

    # Mock the response for stat requests
    mock_stat_response = MagicMock()
    mock_stat_response.json.return_value = {
        "data": {
            "list": [
                {"stat_name": "ATK", "value": 100},
                {"stat_name": "DEF", "value": 200},
                {"stat_name": "HP", "value": 1000},
                {"stat_name": "SPD", "value": 100},
            ]
        }
    }

    # Mock the aiohttp.ClientSession
    mock_session = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_stat_response

    # Set up character data dict
    char_data_dict = {
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
    await scrape_character_data(mock_session, mock_char, char_data_dict)

    # Verify results
    assert char_data_dict["Character"] == ["Test Character"]
    assert char_data_dict["Path"] == ["The Hunt"]
    assert char_data_dict["Element"] == ["Fire"]
    assert char_data_dict["Rarity"] == [5]
    assert char_data_dict["ATK Lvl 80"] == [100]
    assert char_data_dict["DEF Lvl 80"] == [200]
    assert char_data_dict["HP Lvl 80"] == [1000]
    assert char_data_dict["SPD Lvl 80"] == [100]


@pytest.mark.asyncio
async def test_scrape_hsr_data():
    """Test the main scraper function that coordinates the entire process."""
    # Mock data
    mock_char_list = [
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

    # Mock the fetch_character_list function
    with patch("hsrws.core.scraper.fetch_character_list", return_value=mock_char_list):
        # Mock scrape_character_data to simulate populating character data
        async def mock_scrape_char_data(session, char, data_dict):
            data_dict["Character"].append(char["name"])
            data_dict["Path"].append(char["path"]["name"])
            data_dict["Element"].append(char["element"]["name"])
            data_dict["Rarity"].append(char["rarity"])
            data_dict["ATK Lvl 80"].append(100)
            data_dict["DEF Lvl 80"].append(200)
            data_dict["HP Lvl 80"].append(1000)
            data_dict["SPD Lvl 80"].append(100)

        with patch(
            "hsrws.core.scraper.scrape_character_data",
            side_effect=mock_scrape_char_data,
        ):
            # Call the function under test
            result_df = await scrape_hsr_data()

            # Verify results
            assert isinstance(result_df, pd.DataFrame)
            assert not result_df.empty
            assert len(result_df) == 2
            assert "Character" in result_df.columns
            assert "Path" in result_df.columns
            assert "Element" in result_df.columns
            assert "Rarity" in result_df.columns
            assert "ATK Lvl 80" in result_df.columns
            assert "DEF Lvl 80" in result_df.columns
            assert "HP Lvl 80" in result_df.columns
            assert "SPD Lvl 80" in result_df.columns
