"""Character statistic queries for the HSR application."""

from hsrws.db.queries.character_stats import (
    get_latest_patch_stmt,
    get_path_distribution_stmt,
    get_element_distribution_stmt,
    get_rarity_distribution_stmt
)

from hsrws.db.queries.sql_views import (
    get_element_char_count_by_ver,
    get_path_char_count_by_ver,
    get_rarity_char_count_by_ver
)

__all__ = [
    "get_latest_patch_stmt",
    "get_path_distribution_stmt",
    "get_element_distribution_stmt",
    "get_rarity_distribution_stmt",
    "get_element_char_count_by_ver",
    "get_path_char_count_by_ver",
    "get_rarity_char_count_by_ver"
] 