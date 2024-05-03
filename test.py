import pytest

import hsrws
from sqlite_pipeline import SQLitePipeline


def test_hsr_scrape():
    # Given
    url = ['https://www.prydwen.gg/star-rail/characters/aventurine']

    # When
    main = hsrws.HonkaiStarRailScrapeStats(urls=url)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_hsr_scrape_auto():
    # Given
    auto = True

    # When
    main = hsrws.HonkaiStarRailScrapeStats(auto=auto)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_scrape_paths_elements_rarities():
    # Given
    auto = True

    # When
    main = hsrws.HonkaiStarRailScrapePathAndElement(auto=auto)
    main.hsr_scrape()

    # Then
    # No errors should be raised


def test_sqlite_pipeline():
    database = 'hsr.db'
    sqlite_pipeline = SQLitePipeline(database)
    version_dict = sqlite_pipeline.version_dict

    df = sqlite_pipeline.add_version(version_dict)
    sqlite_pipeline.create_characters_table(df)
    sqlite_pipeline.create_stats_table()
    sqlite_pipeline.create_views()


if __name__ == '__main__':
    pytest.main()
