import pytest

from src.hsrws.scrape_stats import HonkaiStarRailScrapeStats
from src.hsrws.scrape_paths_elements_rarities import HonkaiStarRailScrapePathAndElement
from src.hsrws.get_urls_auto import GetUrlAuto


def test_hsr_scrape():
    # Given
    url = ['https://www.prydwen.gg/star-rail/characters/aventurine']

    # When
    main = HonkaiStarRailScrapeStats(urls=url)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_scrape_paths_elements_rarities():
    # Given
    auto = True

    # When
    main = HonkaiStarRailScrapePathAndElement(auto=auto)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_get_url_auto():
    # Given
    main = GetUrlAuto()

    # When
    main.get_urls_auto()

    # Then
    # No errors should be raised


if __name__ == '__main__':
    pytest.main()
