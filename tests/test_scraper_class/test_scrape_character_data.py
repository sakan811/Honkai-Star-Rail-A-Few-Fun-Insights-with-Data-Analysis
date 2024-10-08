import pytest
from unittest.mock import AsyncMock, patch
import json
from hsrws.hsr_scraper import Scraper


def setup_test():
    scraper = Scraper()
    scraper.char_data_dict = {
        'Character': [],
        'ATK Lvl 80': [],
        'DEF Lvl 80': [],
        'HP Lvl 80': [],
        'SPD Lvl 80': []
    }
    return scraper


@pytest.mark.asyncio
async def test_scrape_character_data():
    scraper = setup_test()
    # Mock the _append_char_type_data method
    with patch.object(Scraper, '_append_char_type_data', new_callable=AsyncMock) as mock_append:
        # Test case 1: Character with stats
        character_data_with_stats = {
            'name': 'Test Character',
            'display_field': {
                'attr_level_80': json.dumps({
                    'base_atk': 100,
                    'base_def': 200,
                    'base_hp': 300,
                    'base_speed': 400
                })
            }
        }

        await scraper._scrape_character_data(character_data_with_stats)

        assert scraper.char_data_dict['Character'] == ['Test Character']
        assert scraper.char_data_dict['ATK Lvl 80'] == [100]
        assert scraper.char_data_dict['DEF Lvl 80'] == [200]
        assert scraper.char_data_dict['HP Lvl 80'] == [300]
        assert scraper.char_data_dict['SPD Lvl 80'] == [400]
        mock_append.assert_called_once_with(character_data_with_stats)


@pytest.mark.asyncio
async def test_scrape_char_with_no_stat():
    scraper = setup_test()
    # Mock the _append_char_type_data method
    with patch.object(Scraper, '_append_char_type_data', new_callable=AsyncMock) as mock_append:
        # Test case 2: Character without stats
        character_data_without_stats = {
            'name': 'No Stats Character',
            'display_field': {}
        }

        await scraper._scrape_character_data(character_data_without_stats)

        assert scraper.char_data_dict['Character'] == ['No Stats Character']
        assert scraper.char_data_dict['ATK Lvl 80'] == [0]
        assert scraper.char_data_dict['DEF Lvl 80'] == [0]
        assert scraper.char_data_dict['HP Lvl 80'] == [0]
        assert scraper.char_data_dict['SPD Lvl 80'] == [0]
        mock_append.assert_called_once_with(character_data_without_stats)


@pytest.mark.asyncio
async def test_key_error_handling():
    scraper = setup_test()
    # Test case 3: Check if KeyError is handled
    invalid_character_data = {}
    with pytest.raises(KeyError):
        await scraper._scrape_character_data(invalid_character_data)
