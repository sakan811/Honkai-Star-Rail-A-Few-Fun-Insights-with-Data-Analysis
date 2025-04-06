"""Main script for Honkai Star Rail data analysis."""

import asyncio
import sys
import argparse
from typing import Any

import pandas as pd
from loguru import logger

from hsrws.core.scraper import Scraper
from hsrws.utils.payload import get_headers
from hsrws.data.transformer import (
    transform_char_name,
    clean_path_name,
    add_char_version,
)
from hsrws.db.sqlite import load_to_sqlite
from hsrws.visual.charts import create_advanced_charts

logger.configure(handlers=[{"sink": sys.stderr, "level": "WARNING"}])
logger.add(
    "main.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
    mode="w",
    level="WARNING",
)


def scrape_data() -> pd.DataFrame:
    """
    Function to scrape character data from Honkai Star Rail API.

    Returns:
        Pandas DataFrame with character data.
    """
    url: str = "https://sg-wiki-api.hoyolab.com/hoyowiki/hsr/wapi/get_entry_page_list"
    headers: dict[str, Any] = get_headers()

    scraper: Scraper = Scraper() # type: ignore
    character_data_dataframe: pd.DataFrame = asyncio.run(
        scraper.scrape_hsr_data(url, headers)
    )

    character_data_dataframe["Character"] = character_data_dataframe["Character"].apply( # type: ignore
        transform_char_name
    )
    character_data_dataframe["Path"] = character_data_dataframe["Path"].apply( # type: ignore
        clean_path_name
    )

    add_char_version(character_data_dataframe)

    return character_data_dataframe


def visualize_data() -> None:
    """Create visualization charts from the database."""
    create_advanced_charts()


def main() -> None:
    """
    Main function to parse arguments and run the requested functionality.
    """
    parser = argparse.ArgumentParser(description="Honkai Star Rail Data Analysis Tool")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["all", "scrape", "visualize"],
        default="all",
        help="Operation mode: 'all' runs complete pipeline, 'scrape' only scrapes data, 'visualize' only creates visualizations",
    )

    args = parser.parse_args()

    if args.mode in ["all", "scrape"]:
        logger.info("Starting data scraping")
        char_data_df = scrape_data()
        load_to_sqlite(char_data_df)
        logger.info("Data scraping and storage complete")

    if args.mode in ["all", "visualize"]:
        logger.info("Creating visualizations")
        visualize_data()
        logger.info("Visualization creation complete")

    logger.info(f"Completed requested operation: {args.mode}")


if __name__ == "__main__":
    main()
