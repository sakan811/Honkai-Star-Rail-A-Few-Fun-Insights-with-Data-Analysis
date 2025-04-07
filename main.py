"""Main script for Honkai Star Rail data analysis."""

import asyncio
import os
import sys
from typing import Any

import pandas as pd
from loguru import logger
from flask import Flask, jsonify

from hsrws.core.scraper import Scraper
from hsrws.utils.payload import get_headers
from hsrws.data.transformer import (
    transform_char_name,
    clean_path_name,
    add_char_version,
)
from hsrws.db.sqlite import load_to_sqlite
from hsrws.visual.charts import create_advanced_charts

# Configure logger
logger.configure(handlers=[{"sink": sys.stderr, "level": "WARNING"}])
logger.add(
    "main.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
    mode="w",
    level="WARNING",
)

# Initialize Flask application
app = Flask(__name__)


def scrape_data() -> pd.DataFrame:
    """
    Function to scrape character data from Honkai Star Rail API.

    Returns:
        Pandas DataFrame with character data.
    """
    url: str = "https://sg-wiki-api.hoyolab.com/hoyowiki/hsr/wapi/get_entry_page_list"
    headers: dict[str, Any] = get_headers()

    scraper: Scraper = Scraper()  # type: ignore
    character_data_dataframe: pd.DataFrame = asyncio.run(
        scraper.scrape_hsr_data(url, headers)
    )

    character_data_dataframe["Character"] = character_data_dataframe["Character"].apply(  # type: ignore
        transform_char_name
    )
    character_data_dataframe["Path"] = character_data_dataframe["Path"].apply(  # type: ignore
        clean_path_name
    )

    add_char_version(character_data_dataframe)

    return character_data_dataframe


def visualize_data() -> None:
    """Create visualization charts from the database."""
    create_advanced_charts()


# Flask routes
@app.route("/scrape", methods=["GET"])
def api_scrape():
    """API endpoint for scraping data."""
    try:
        logger.info("Starting data scraping via API")
        char_data_df = scrape_data()
        load_to_sqlite(char_data_df)
        logger.info("Data scraping and storage complete")
        return jsonify(
            {
                "status": "success",
                "message": "Data scraping complete",
                "data_shape": char_data_df.shape,
            }
        )
    except Exception as e:
        logger.error(f"Error during data scraping: {e}")
        return jsonify(
            {"status": "error", "message": "An internal error has occurred."}
        ), 500


@app.route("/visualize", methods=["GET"])
def api_visualize():
    """API endpoint for visualization generation."""
    try:
        logger.info("Creating visualizations via API")
        visualize_data()
        logger.info("Visualization creation complete")
        return jsonify(
            {"status": "success", "message": "Visualization creation complete"}
        )
    except Exception as e:
        logger.error(f"Error during visualization: {e}")
        return jsonify(
            {"status": "error", "message": "An internal error has occurred."}
        ), 500


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(debug=debug_mode, host="0.0.0.0", port=1234)
