import pytest

import hsrws
import sqlite_pipeline


def test_hsr_scrape_manual():
    # Given
    url = ['https://www.prydwen.gg/star-rail/characters/aventurine']

    # When
    main = hsrws.HonkaiStarRailScrapeStats(urls=url)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_full_process():
    scrape_stat = hsrws.HonkaiStarRailScrapeStats(auto=True)
    scrape_stat.hsr_scrape()

    scrape_others = hsrws.HonkaiStarRailScrapePathAndElement(auto=True)
    scrape_others.hsr_scrape()

    sqlite_pipeline.main()


if __name__ == '__main__':
    pytest.main()
