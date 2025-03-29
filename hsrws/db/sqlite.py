"""SQLite database functionality."""

import sqlite3
import traceback

import pandas as pd
from loguru import logger

# Import from the queries package which now correctly exposes these functions
from hsrws.db.queries import (
    get_element_char_count_by_ver,
    get_path_char_count_by_ver,
    get_rarity_char_count_by_ver,
)


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
            drop_views(conn)
            create_views(conn)
    except sqlite3.OperationalError as e:
        logger.error(f"OperationalError: {e}")
        logger.error(traceback.format_exc())
        raise


def create_views(conn: sqlite3.Connection) -> None:
    """
    Creates Views in the database.
    
    Args:
        conn: SQLite connection.
    """
    logger.info("Creating Views...")
    query = get_element_char_count_by_ver()
    conn.execute(query)
    query = get_path_char_count_by_ver()
    conn.execute(query)
    query = get_rarity_char_count_by_ver()
    conn.execute(query)


def drop_views(conn: sqlite3.Connection) -> None:
    """
    Drops Views in the database if they exist.
    
    Args:
        conn: SQLite connection
    """
    logger.info("Dropping Views if exist...")
    query = "DROP VIEW IF EXISTS ElementCharacterCountByVersion"
    conn.execute(query)

    query = "DROP VIEW IF EXISTS PathCharacterCountByVersion"
    conn.execute(query)

    query = "DROP VIEW IF EXISTS RarityCharacterCountByVersion"
    conn.execute(query) 