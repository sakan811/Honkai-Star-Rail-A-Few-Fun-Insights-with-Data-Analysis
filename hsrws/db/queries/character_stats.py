"""SQLAlchemy queries for character statistics."""

from sqlalchemy import Column, Select, func, select
from hsrws.db.models import HsrCharacter


def get_latest_patch_stmt() -> Select[tuple[float]]:
    """
    Returns the statement to get the latest patch version.

    Returns:
        SQLAlchemy SELECT statement.
    """
    version_data: Column[float] = HsrCharacter.Version
    latest_version_data = func.max(version_data)
    return select(latest_version_data.label("latest_version"))


def get_path_distribution_stmt():
    """
    Returns the statement to get Path distribution.

    Returns:
        SQLAlchemy SELECT statement for Path distribution.
    """
    return (
        select(HsrCharacter.Path.label("category"), func.count().label("count"))
        .group_by(HsrCharacter.Path)
        .order_by(func.count().desc())
    )


def get_element_distribution_stmt():
    """
    Returns the statement to get Element distribution.

    Returns:
        SQLAlchemy SELECT statement for Element distribution.
    """
    return (
        select(HsrCharacter.Element.label("category"), func.count().label("count"))
        .group_by(HsrCharacter.Element)
        .order_by(func.count().desc())
    )


def get_rarity_distribution_stmt():
    """
    Returns the statement to get Rarity distribution.

    Returns:
        SQLAlchemy SELECT statement for Rarity distribution.
    """
    return (
        select(HsrCharacter.Rarity.label("category"), func.count().label("count"))
        .group_by(HsrCharacter.Rarity)
        .order_by(func.count().desc())
    )


def get_element_path_heatmap_stmt():
    """
    Returns the statement to get Element-Path distribution for heatmap.

    Returns:
        SQLAlchemy SELECT statement for Element-Path heatmap data.
    """
    return (
        select(HsrCharacter.Element, HsrCharacter.Path, func.count().label("count"))
        .group_by(HsrCharacter.Element, HsrCharacter.Path)
        .order_by(HsrCharacter.Element, HsrCharacter.Path)
    )


def get_rarity_element_distribution_stmt():
    """
    Returns the statement to get Rarity-Element distribution for stacked bar chart.

    Returns:
        SQLAlchemy SELECT statement for Rarity-Element distribution data.
    """
    return (
        select(HsrCharacter.Rarity, HsrCharacter.Element, func.count().label("count"))
        .group_by(HsrCharacter.Rarity, HsrCharacter.Element)
        .order_by(HsrCharacter.Rarity, HsrCharacter.Element)
    )


def get_version_release_timeline_stmt():
    """
    Returns the statement to get character releases by version for timeline plot.

    Returns:
        SQLAlchemy SELECT statement for version release timeline data.
    """
    return (
        select(HsrCharacter.Version, func.count().label("character_count"))
        .group_by(HsrCharacter.Version)
        .order_by(HsrCharacter.Version)
    )


def get_version_element_evolution_stmt():
    """
    Returns the statement to get cumulative elemental balance evolution across versions.

    Returns:
        SQLAlchemy SELECT statement for cumulative elemental balance evolution data.
    """
    # First create a subquery with the count per version and element
    version_element_counts = (
        select(HsrCharacter.Version, HsrCharacter.Element, func.count().label("count"))
        .group_by(HsrCharacter.Version, HsrCharacter.Element)
        .order_by(HsrCharacter.Version, HsrCharacter.Element)
        .subquery()
    )

    # Then use window function to calculate cumulative sum
    return select(
        version_element_counts.c.Version,
        version_element_counts.c.Element,
        func.sum(version_element_counts.c.count)
        .over(
            partition_by=version_element_counts.c.Element,
            order_by=version_element_counts.c.Version,
        )
        .label("count"),
    ).order_by(version_element_counts.c.Version, version_element_counts.c.Element)


def get_path_rarity_distribution_stmt():
    """
    Returns the statement to get Path-Rarity distribution for grouped bar chart.

    Returns:
        SQLAlchemy SELECT statement for Path-Rarity distribution data.
    """
    return (
        select(HsrCharacter.Path, HsrCharacter.Rarity, func.count().label("count"))
        .group_by(HsrCharacter.Path, HsrCharacter.Rarity)
        .order_by(HsrCharacter.Path, HsrCharacter.Rarity)
    )


def get_version_path_evolution_stmt():
    """
    Returns the statement to get cumulative path balance evolution across versions.

    Returns:
        SQLAlchemy SELECT statement for cumulative path balance evolution data.
    """
    # First create a subquery with the count per version and path
    version_path_counts = (
        select(HsrCharacter.Version, HsrCharacter.Path, func.count().label("count"))
        .group_by(HsrCharacter.Version, HsrCharacter.Path)
        .order_by(HsrCharacter.Version, HsrCharacter.Path)
        .subquery()
    )

    # Then use window function to calculate cumulative sum
    return select(
        version_path_counts.c.Version,
        version_path_counts.c.Path,
        func.sum(version_path_counts.c.count)
        .over(
            partition_by=version_path_counts.c.Path,
            order_by=version_path_counts.c.Version,
        )
        .label("count"),
    ).order_by(version_path_counts.c.Version, version_path_counts.c.Path)
