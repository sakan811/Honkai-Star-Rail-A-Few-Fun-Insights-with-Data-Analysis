import pytest
from hsrws.core.scraper import Scraper
from hsrws.core.character import append_char_stats


@pytest.fixture
def scraper():
    scraper = Scraper()
    # Initialize char_data_dict with the required keys
    scraper.char_data_dict = {
        "ATK Lvl 80": [],
        "DEF Lvl 80": [],
        "HP Lvl 80": [],
        "SPD Lvl 80": [],
    }
    return scraper


def test_append_char_stats_valid(scraper):
    character_data = {
        "display_field": {
            "attr_level_80": '{"base_atk": 100, "base_def": 200, "base_hp": 300, "base_speed": 400}'
        }
    }
    append_char_stats(scraper, character_data)
    assert scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert scraper.char_data_dict["HP Lvl 80"] == [300]
    assert scraper.char_data_dict["SPD Lvl 80"] == [400]


def test_append_char_stats_no_stats(scraper):
    character_data = {"display_field": {}}
    append_char_stats(scraper, character_data)
    assert scraper.char_data_dict["ATK Lvl 80"] == [0]
    assert scraper.char_data_dict["DEF Lvl 80"] == [0]
    assert scraper.char_data_dict["HP Lvl 80"] == [0]
    assert scraper.char_data_dict["SPD Lvl 80"] == [0]


def test_append_char_stats_empty_dict(scraper):
    character_data = {}
    append_char_stats(scraper, character_data)
    assert scraper.char_data_dict["ATK Lvl 80"] == [0]
    assert scraper.char_data_dict["DEF Lvl 80"] == [0]
    assert scraper.char_data_dict["HP Lvl 80"] == [0]
    assert scraper.char_data_dict["SPD Lvl 80"] == [0]
