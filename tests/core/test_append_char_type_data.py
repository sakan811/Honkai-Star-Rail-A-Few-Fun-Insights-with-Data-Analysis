import pytest
from hsrws.core.scraper import Scraper
from hsrws.core.character import append_char_type_data


@pytest.mark.asyncio
async def test_append_char_type_data_success():
    # Create an instance of the class
    scraper = Scraper()

    # Mock character_data with valid values
    character_data = {
        "filter_values": {
            "character_paths": {"values": ["Path1"]},
            "character_combat_type": {"values": ["Element1"]},
            "character_rarity": {"values": ["4-Star"]},
        }
    }

    # Mock the char_data_dict to append values
    scraper.char_data_dict = {"Path": [], "Element": [], "Rarity": []}

    # Call the function with scraper and character_data
    await append_char_type_data(scraper, character_data)

    # Assert that the data has been correctly appended
    assert scraper.char_data_dict["Path"] == ["Path1"]
    assert scraper.char_data_dict["Element"] == ["Element1"]
    assert scraper.char_data_dict["Rarity"] == ["4"]


@pytest.mark.asyncio
async def test_append_char_type_data_empty_values():
    # Create an instance of the class
    scraper = Scraper()
    # Mock character_data with an empty list for 'values'
    character_data = {
        "filter_values": {
            "character_paths": {"values": []},
            "character_combat_type": {"values": []},
            "character_rarity": {"values": []},
        }
    }

    # Mock the char_data_dict to append values
    scraper.char_data_dict = {"Path": [], "Element": [], "Rarity": []}

    # Call the function with scraper and character_data
    await append_char_type_data(scraper, character_data)

    # Assert that 'Unknown' values have been appended
    assert scraper.char_data_dict["Path"] == ["Unknown"]
    assert scraper.char_data_dict["Element"] == ["Unknown"]
    assert scraper.char_data_dict["Rarity"] == ["Unknown"]


@pytest.mark.asyncio
async def test_append_char_type_data_missing_values_key():
    # Create an instance of the class
    scraper = Scraper()

    # Mock character_data missing the 'values' key
    character_data = {
        "filter_values": {
            "character_paths": {},
            "character_combat_type": {},
            "character_rarity": {},
        }
    }

    # Mock the char_data_dict to append values
    scraper.char_data_dict = {"Path": [], "Element": [], "Rarity": []}

    # Call the method and expect KeyError to be handled internally
    await append_char_type_data(scraper, character_data)

    # Assert that 'Unknown' values have been appended
    assert scraper.char_data_dict["Path"] == ["Unknown"]
    assert scraper.char_data_dict["Element"] == ["Unknown"]
    assert scraper.char_data_dict["Rarity"] == ["Unknown"]
