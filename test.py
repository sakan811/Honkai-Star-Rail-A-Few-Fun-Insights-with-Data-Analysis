import pytest

from hsrws.scrape_stats import HonkaiStarRailScrapeStats
from hsrws.scrape_paths_elements_rarities import HonkaiStarRailScrapePathAndElement
from hsrws.get_urls_auto import GetUrlAuto


def test_hsr_scrape():
    # Given
    url = ['https://www.prydwen.gg/star-rail/characters/aventurine']

    # When
    main = HonkaiStarRailScrapeStats(urls=url)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_hsr_scrape_auto():
    # Given
    auto = True

    # When
    main = HonkaiStarRailScrapeStats(auto=auto)
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


if __name__ == '__main__':
    pytest.main()
