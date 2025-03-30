"""Database functionality for HSR web scraper."""

from hsrws.db.sqlite import load_to_sqlite, create_views, drop_views
from hsrws.db.database import get_engine, get_session
from hsrws.db.models import HsrCharacter, Base
from hsrws.db.queries import (
    get_latest_patch_stmt,
    get_path_distribution_stmt,
    get_element_distribution_stmt,
    get_rarity_distribution_stmt,
)

__all__ = [
    "load_to_sqlite",
    "create_views",
    "drop_views",
    "get_engine",
    "get_session",
    "HsrCharacter",
    "Base",
    "get_latest_patch_stmt",
    "get_path_distribution_stmt",
    "get_element_distribution_stmt",
    "get_rarity_distribution_stmt",
]
