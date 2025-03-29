"""Data utility functions for visualization."""

import pandas as pd
from hsrws.db import get_session
from hsrws.db.queries import (
    get_latest_patch_stmt,
    get_path_distribution_stmt,
    get_element_distribution_stmt,
    get_rarity_distribution_stmt
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
        column_names = stmt.columns.keys() if hasattr(stmt, 'columns') else [c['name'] for c in stmt.column_descriptions]
        return pd.DataFrame(result, columns=column_names)


def get_latest_patch():
    """
    Gets the latest patch version from the database.
    
    Returns:
        Latest patch version number.
    """
    result = fetch_data_orm(get_latest_patch_stmt())
    return result.iloc[0]['latest_version']


def get_path_distribution():
    """
    Gets the Path distribution data.
    
    Returns:
        DataFrame with Path distribution data.
    """
    return fetch_data_orm(get_path_distribution_stmt())


def get_element_distribution():
    """
    Gets the Element distribution data.
    
    Returns:
        DataFrame with Element distribution data.
    """
    return fetch_data_orm(get_element_distribution_stmt())


def get_rarity_distribution():
    """
    Gets the Rarity distribution data.
    
    Returns:
        DataFrame with Rarity distribution data.
    """
    return fetch_data_orm(get_rarity_distribution_stmt()) 