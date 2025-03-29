"""Tests for character data processing logic."""

import pytest
from unittest.mock import MagicMock, patch

from hsrws.core.character import (
    process_character_list,
    scrape_character_data,
    append_char_stats,
    append_stats,
    append_char_type_data
)
from hsrws.core.scraper import Scraper


@pytest.fixture
def mock_scraper():
    """Create a mock scraper with default char_data_dict."""
    scraper = MagicMock(spec=Scraper)
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
    return scraper


@pytest.mark.asyncio
async def test_process_character_list(mock_scraper):
    """Test process_character_list processes all characters in the list."""
    with patch("hsrws.core.character.scrape_character_data") as mock_scrape:
        char_list = [{"name": "Character1"}, {"name": "Character2"}]
        await process_character_list(mock_scraper, char_list)
        
        assert mock_scrape.call_count == 2
        mock_scrape.assert_any_call(mock_scraper, {"name": "Character1"})
        mock_scrape.assert_any_call(mock_scraper, {"name": "Character2"})


@pytest.mark.asyncio
async def test_scrape_character_data_success(mock_scraper):
    """Test scrape_character_data successfully processes character data."""
    with patch("hsrws.core.character.append_char_type_data") as mock_type:
        with patch("hsrws.core.character.append_char_stats") as mock_stats:
            # Test with valid character data
            character_data = {"name": "TestChar"}
            await scrape_character_data(mock_scraper, character_data)
            
            assert mock_scraper.char_data_dict["Character"] == ["TestChar"]
            mock_type.assert_called_once_with(mock_scraper, character_data)
            mock_stats.assert_called_once_with(mock_scraper, character_data)


@pytest.mark.asyncio
async def test_scrape_character_data_missing_name(mock_scraper):
    """Test scrape_character_data raises KeyError when name is missing."""
    with pytest.raises(KeyError):
        await scrape_character_data(mock_scraper, {})


def test_append_stats_with_data(mock_scraper):
    """Test append_stats correctly appends character stats when data is available."""
    char_stats = {
        "base_atk": "100",
        "base_def": "200",
        "base_hp": "1000",
        "base_speed": "120"
    }
    
    append_stats(mock_scraper, char_stats)
    
    assert mock_scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert mock_scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert mock_scraper.char_data_dict["HP Lvl 80"] == [1000]
    assert mock_scraper.char_data_dict["SPD Lvl 80"] == [120]


def test_append_stats_with_missing_data(mock_scraper):
    """Test append_stats correctly handles missing stats by adding zeros."""
    # Missing all stats
    append_stats(mock_scraper, {})
    
    assert mock_scraper.char_data_dict["ATK Lvl 80"] == [0]
    assert mock_scraper.char_data_dict["DEF Lvl 80"] == [0]
    assert mock_scraper.char_data_dict["HP Lvl 80"] == [0]
    assert mock_scraper.char_data_dict["SPD Lvl 80"] == [0]


def test_append_stats_with_no_data(mock_scraper):
    """Test append_stats correctly handles None input by adding zeros."""
    append_stats(mock_scraper, None)
    
    assert mock_scraper.char_data_dict["ATK Lvl 80"] == [0]
    assert mock_scraper.char_data_dict["DEF Lvl 80"] == [0]
    assert mock_scraper.char_data_dict["HP Lvl 80"] == [0]
    assert mock_scraper.char_data_dict["SPD Lvl 80"] == [0] 