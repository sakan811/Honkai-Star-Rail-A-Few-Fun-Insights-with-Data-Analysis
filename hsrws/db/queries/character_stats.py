"""SQLAlchemy queries for character statistics."""

from sqlalchemy import func, select
from hsrws.db.models import HsrCharacter


def get_latest_patch_stmt():
    """
    Returns the statement to get the latest patch version.
    
    Returns:
        SQLAlchemy SELECT statement.
    """
    return select(func.max(HsrCharacter.Version).label('latest_version'))


def get_path_distribution_stmt():
    """
    Returns the statement to get Path distribution.
    
    Returns:
        SQLAlchemy SELECT statement for Path distribution.
    """
    return select(
        HsrCharacter.Path.label('category'), 
        func.count().label('count')
    ).group_by(
        HsrCharacter.Path
    ).order_by(
        func.count().desc()
    )


def get_element_distribution_stmt():
    """
    Returns the statement to get Element distribution.
    
    Returns:
        SQLAlchemy SELECT statement for Element distribution.
    """
    return select(
        HsrCharacter.Element.label('category'), 
        func.count().label('count')
    ).group_by(
        HsrCharacter.Element
    ).order_by(
        func.count().desc()
    )


def get_rarity_distribution_stmt():
    """
    Returns the statement to get Rarity distribution.
    
    Returns:
        SQLAlchemy SELECT statement for Rarity distribution.
    """
    return select(
        HsrCharacter.Rarity.label('category'), 
        func.count().label('count')
    ).group_by(
        HsrCharacter.Rarity
    ).order_by(
        func.count().desc()
    ) 