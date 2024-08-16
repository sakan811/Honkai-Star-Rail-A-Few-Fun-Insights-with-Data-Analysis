import pytest

from hsrws.hsr_scraper import Scraper


@pytest.mark.asyncio
async def test_append_char_type_data_success():
    # Create an instance of the class
    scraper = Scraper()

    # Mock character_data with valid values
    character_data = {
        'filter_values': {
            'character_paths': {'values': ['Path1']},
            'character_elements': {'values': ['Element1']},
            'character_rarity': {'values': ['Rarity1']}
        }
    }

    # Mock the char_data_dict to append values
    scraper.char_data_dict = {'Path': [], 'Element': [], 'Rarity': []}

    # Call the method
    await scraper._append_char_type_data(character_data)

    # Assert that the data has been correctly appended
    assert scraper.char_data_dict['Path'] == ['Path1']
    assert scraper.char_data_dict['Element'] == ['Element1']
    assert scraper.char_data_dict['Rarity'] == ['Rarity1']


@pytest.mark.asyncio
async def test_append_char_type_data_key_error():
    # Create an instance of the class
    scraper = Scraper()

    # Mock character_data missing the required keys
    character_data = {
        'filter_values': {
            'character_paths': {},  # Missing 'values'
            'character_elements': {},  # Missing 'values'
            'character_rarity': {}  # Missing 'values'
        }
    }

    # Mock the char_data_dict to append values
    scraper.char_data_dict = {'Path': [], 'Element': [], 'Rarity': []}

    with pytest.raises(KeyError):
        await scraper._append_char_type_data(character_data)


@pytest.mark.asyncio
async def test_append_char_type_data_index_error():
    # Create an instance of the class
    scraper = Scraper()
    # Mock character_data with an empty list for 'values'
    character_data = {
        'filter_values': {
            'character_paths': {'values': []},
            'character_elements': {'values': []},
            'character_rarity': {'values': []}
        }
    }

    # Mock the char_data_dict to append values
    scraper.char_data_dict = {'Path': [], 'Element': [], 'Rarity': []}

    with pytest.raises(KeyError):
        await scraper._append_char_type_data(character_data)
