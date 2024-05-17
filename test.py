import sqlite3

import pytest

import hsrws
import sqlite_pipeline


def test_hsr_scrape_manual():
    url = ['https://www.prydwen.gg/star-rail/characters/aventurine']

    main = hsrws.HonkaiStarRailScrapeStats(urls=url)
    main.hsr_scrape()

    sqlite_pipeline.main()
    database = 'hsr.db'

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM Stats")
        result = cursor.fetchall()  # Fetch all results

        # Assert that there should be records
        assert len(result) > 0

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        query = """
        SELECT
            Character,
            Level
        FROM (
            SELECT
                Character,
                Level,
                ROW_NUMBER() OVER (PARTITION BY Character, Level ORDER BY Level) AS RowNum
            FROM
                Stats
        ) subquery
        WHERE
            RowNum > 1;
        """
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all results

        # Assert that there should be no duplicates in Level for each Character
        assert len(result) == 0


def test_full_process():
    scrape_stat = hsrws.HonkaiStarRailScrapeStats(auto=True)
    scrape_stat.hsr_scrape()

    scrape_others = hsrws.HonkaiStarRailScrapePathAndElement(auto=True)
    scrape_others.hsr_scrape()

    sqlite_pipeline.main()

    database = 'hsr.db'

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM Stats")
        result = cursor.fetchall()  # Fetch all results

        # Assert that there should be records
        assert len(result) > 0

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM Characters")
        result = cursor.fetchall()  # Fetch all results

        # Assert that there should be records
        assert len(result) > 0

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        query = """
        SELECT
            Character,
            Level
        FROM (
            SELECT
                Character,
                Level,
                ROW_NUMBER() OVER (PARTITION BY Character, Level ORDER BY Level) AS RowNum
            FROM
                Stats
        ) subquery
        WHERE
            RowNum > 1;
        """
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all results

        # Assert that there should be no duplicates in Level for each Character
        assert len(result) == 0


if __name__ == '__main__':
    pytest.main()
