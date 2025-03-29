"""Data utility functions for visualization."""

import pandas as pd
from sqlalchemy import text
from loguru import logger
from hsrws.db import get_session
from hsrws.db.queries import (
    get_latest_patch_stmt,
    get_element_path_heatmap_stmt,
    get_rarity_element_distribution_stmt,
    get_version_release_timeline_stmt,
    get_version_element_evolution_stmt,
    get_path_rarity_distribution_stmt,
)


def fetch_data_orm(stmt):
    """
    Fetches data from the database using SQLAlchemy ORM.

    Args:
        stmt: SQLAlchemy statement to execute.

    Returns:
        DataFrame with query results.
    """
    with get_session() as session:
        result = session.execute(stmt).all()
        # Convert to pandas DataFrame with column names
        column_names = (
            stmt.columns.keys()
            if hasattr(stmt, "columns")
            else [c["name"] for c in stmt.column_descriptions]
        )
        return pd.DataFrame(result, columns=column_names)


def fetch_view_data(view_name):
    """
    Fetches data from a SQL view.

    Args:
        view_name: Name of the SQL view to query.

    Returns:
        DataFrame with query results.
    """
    with get_session() as session:
        # Use text() to properly create a SQL text object
        sql_query = text(f"SELECT * FROM {view_name}")
        result = session.execute(sql_query)
        
        # Get column names from the result's keys method
        if result.returns_rows:
            # Get result as a list of dictionaries for pandas
            rows = [dict(row._mapping) for row in result]
            if rows:
                return pd.DataFrame(rows)
        
        # Return empty DataFrame if no results
        return pd.DataFrame()


def get_latest_patch():
    """
    Gets the latest patch version from the database.

    Returns:
        Latest patch version number formatted as "Patch (X.X)".
    """
    result = fetch_data_orm(get_latest_patch_stmt())
    version = result.iloc[0]["latest_version"]
    return f"Patch ({version})"


def get_element_path_heatmap_data():
    """
    Gets the Element-Path distribution data for heatmap.

    Returns:
        DataFrame with Element-Path distribution data.
    """
    return fetch_data_orm(get_element_path_heatmap_stmt())


def get_rarity_element_distribution_data():
    """
    Gets the Rarity-Element distribution data for stacked bar chart.

    Returns:
        DataFrame with Rarity-Element distribution data.
    """
    return fetch_data_orm(get_rarity_element_distribution_stmt())


def get_version_release_timeline_data():
    """
    Gets the character releases by version data for timeline plot.

    Returns:
        DataFrame with version release timeline data.
    """
    return fetch_data_orm(get_version_release_timeline_stmt())


def get_element_balance_evolution_data():
    """
    Gets the elemental balance evolution data across versions.

    Returns:
        DataFrame with elemental balance evolution data.
    """
    try:
        # Use the SQL view for this complex query
        return fetch_view_data("ElementCharacterCountByVersion")
    except Exception as e:
        # Fallback: If view doesn't exist, use the direct query
        logger.warning(f"View query failed: {e}. Using direct query instead.")
        return fetch_data_orm(get_version_element_evolution_stmt())


def get_path_rarity_distribution_data():
    """
    Gets the Path-Rarity distribution data for grouped bar chart.

    Returns:
        DataFrame with Path-Rarity distribution data.
    """
    return fetch_data_orm(get_path_rarity_distribution_stmt())
