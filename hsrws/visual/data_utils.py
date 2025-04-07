"""Data utility functions for visualization."""

from typing import Any
import pandas as pd
from sqlalchemy import Select
from hsrws.db import get_session
from hsrws.db.queries import (
    get_latest_patch_stmt,
    get_element_path_heatmap_stmt,
    get_rarity_element_distribution_stmt,
    get_version_release_timeline_stmt,
    get_version_element_evolution_stmt,
    get_path_rarity_distribution_stmt,
    get_version_path_evolution_stmt,
)


def fetch_data_orm(stmt: Select[tuple[Any, ...]]):
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


def get_latest_patch():
    """
    Gets the latest patch version from the database.

    Returns:
        Latest patch version number formatted as "Patch (X.X)".
    """
    result = fetch_data_orm(get_latest_patch_stmt())
    version: float = result.iloc[0]["latest_version"]  # type: ignore
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
    return fetch_data_orm(get_version_element_evolution_stmt())


def get_path_rarity_distribution_data():
    """
    Gets the Path-Rarity distribution data for grouped bar chart.

    Returns:
        DataFrame with Path-Rarity distribution data.
    """
    return fetch_data_orm(get_path_rarity_distribution_stmt())


def get_path_balance_evolution_data():
    """
    Gets the path balance evolution data across versions.

    Returns:
        DataFrame with path balance evolution data.
    """
    return fetch_data_orm(get_version_path_evolution_stmt())


def get_element_colors():
    """
    Gets a mapping of elements to their display colors.

    Returns:
        Dictionary mapping element names to color values.
    """
    return {
        "Fire": "red",
        "Lightning": "purple",
        "Quantum": "darkblue",
        "Ice": "lightblue",
        "Imaginary": "yellow",
        "Wind": "green",
        "Physical": "gray",
    }


def get_path_colors():
    """
    Gets a mapping of paths to their display colors.

    Returns:
        Dictionary mapping path names to color values.
    """
    return {
        "Destruction": "grey",
        "Preservation": "blue",
        "Remembrance": "cyan",
        "Nihility": "purple",
        "Abundance": "yellow",
        "Hunt": "green",
        "Erudition": "pink",
        "Harmony": "orange",
    }


def get_rarity_colors():
    """
    Gets a mapping of rarity levels to their display colors.

    Returns:
        Dictionary mapping rarity levels to color values.
    """
    return {
        "4": "purple",
        "5": "gold",
    }
