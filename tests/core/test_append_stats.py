import pytest
from hsrws.core.scraper import Scraper
from hsrws.core.character import append_stats


@pytest.fixture
def scraper():
    scraper = Scraper()
    # Initialize char_data_dict with the required keys
    scraper.char_data_dict = {
        "ATK Lvl 80": [],
        "DEF Lvl 80": [],
        "HP Lvl 80": [],
        "SPD Lvl 80": []
    }
    return scraper


def test_append_stats_valid(scraper):
    char_stats_lvl_80 = {
        "base_atk": 100,
        "base_def": 200,
        "base_hp": 300,
        "base_speed": 400,
    }
    append_stats(scraper, char_stats_lvl_80)
    assert scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert scraper.char_data_dict["HP Lvl 80"] == [300]
    assert scraper.char_data_dict["SPD Lvl 80"] == [400]


def test_append_stats_missing(scraper):
    append_stats(scraper)
    assert scraper.char_data_dict["ATK Lvl 80"] == [0]
    assert scraper.char_data_dict["DEF Lvl 80"] == [0]
    assert scraper.char_data_dict["HP Lvl 80"] == [0]
    assert scraper.char_data_dict["SPD Lvl 80"] == [0]


def test_append_stats_key_error(scraper):
    char_stats_lvl_80 = {
        "base_atk": 100,
        "base_def": 200,
        "base_hp": 300,
        # 'base_speed' is missing to simulate KeyError
    }
    append_stats(scraper, char_stats_lvl_80)
    assert scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert scraper.char_data_dict["HP Lvl 80"] == [300]
    assert scraper.char_data_dict["SPD Lvl 80"] == [0]
