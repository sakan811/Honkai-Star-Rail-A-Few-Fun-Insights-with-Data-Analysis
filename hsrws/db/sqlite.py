"""SQLite database functionality."""

import sqlite3
import traceback

import pandas as pd
from loguru import logger


def load_to_sqlite(df: pd.DataFrame) -> None:
    """
    Loads dataframe to SQLite database.

    Args:
        df: Dataframe to load.

    Raises:
        sqlite3.OperationalError: If there's an issue with the SQLite operation.
    """
    logger.info("Loading dataframe to SQLite database...")
    try:
        with sqlite3.connect("hsr.db") as conn:
            df.to_sql("HsrCharacters", conn, if_exists="replace")
    except sqlite3.OperationalError as e:
        logger.error(f"OperationalError: {e}")
        logger.error(traceback.format_exc())
        raise
