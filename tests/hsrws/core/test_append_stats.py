import pytest
from hsrws.hsr_scraper import Scraper


@pytest.fixture
def scraper():
    return Scraper()


def test_append_stats_valid(scraper):
    char_stats_lvl_80 = {
        "base_atk": 100,
        "base_def": 200,
        "base_hp": 300,
        "base_speed": 400,
    }
    scraper._append_stats(char_stats_lvl_80)
    assert scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert scraper.char_data_dict["HP Lvl 80"] == [300]
    assert scraper.char_data_dict["SPD Lvl 80"] == [400]


def test_append_stats_missing(scraper):
    scraper._append_stats()
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
    scraper._append_stats(char_stats_lvl_80)
    assert scraper.char_data_dict["ATK Lvl 80"] == [100]
    assert scraper.char_data_dict["DEF Lvl 80"] == [200]
    assert scraper.char_data_dict["HP Lvl 80"] == [300]
    assert scraper.char_data_dict["SPD Lvl 80"] == [0]
