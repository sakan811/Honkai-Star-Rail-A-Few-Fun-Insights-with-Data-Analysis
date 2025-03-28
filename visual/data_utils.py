import pandas as pd
from database import get_session
from queries import (
    get_latest_patch_stmt,
    get_path_distribution_stmt,
    get_element_distribution_stmt,
    get_rarity_distribution_stmt
)


def fetch_data_orm(stmt):
    """Fetch data from the database using SQLAlchemy ORM."""
    with get_session() as session:
        result = session.execute(stmt).all()
        # Convert to pandas DataFrame with column names
        column_names = stmt.columns.keys() if hasattr(stmt, 'columns') else [c['name'] for c in stmt.column_descriptions]
        return pd.DataFrame(result, columns=column_names)


def get_latest_patch():
    """Get the latest patch version from the database using SQLAlchemy ORM."""
    result = fetch_data_orm(get_latest_patch_stmt())
    return result.iloc[0]['latest_version']


def get_path_distribution():
    """Get the Path distribution data."""
    return fetch_data_orm(get_path_distribution_stmt())


def get_element_distribution():
    """Get the Element distribution data."""
    return fetch_data_orm(get_element_distribution_stmt())


def get_rarity_distribution():
    """Get the Rarity distribution data."""
    return fetch_data_orm(get_rarity_distribution_stmt()) 