import pytest
from hsrws.hsr_scraper import Scraper

@pytest.fixture
def scraper():
    return Scraper()

def test_append_char_stats_valid(scraper):
    character_data = {
        'display_field': {
            'attr_level_80': '{"base_atk": 100, "base_def": 200, "base_hp": 300, "base_speed": 400}'
        }
    }
    scraper._append_char_stats(character_data)
    assert scraper.char_data_dict['ATK Lvl 80'] == [100]
    assert scraper.char_data_dict['DEF Lvl 80'] == [200]
    assert scraper.char_data_dict['HP Lvl 80'] == [300]
    assert scraper.char_data_dict['SPD Lvl 80'] == [400]

def test_append_char_stats_no_stats(scraper):
    character_data = {
        'display_field': {}
    }
    scraper._append_char_stats(character_data)
    assert scraper.char_data_dict['ATK Lvl 80'] == [0]
    assert scraper.char_data_dict['DEF Lvl 80'] == [0]
    assert scraper.char_data_dict['HP Lvl 80'] == [0]
    assert scraper.char_data_dict['SPD Lvl 80'] == [0]

def test_append_char_stats_empty_dict(scraper):
    character_data = {}
    scraper._append_char_stats(character_data)
    assert scraper.char_data_dict['ATK Lvl 80'] == [0]
    assert scraper.char_data_dict['DEF Lvl 80'] == [0]
    assert scraper.char_data_dict['HP Lvl 80'] == [0]
    assert scraper.char_data_dict['SPD Lvl 80'] == [0]