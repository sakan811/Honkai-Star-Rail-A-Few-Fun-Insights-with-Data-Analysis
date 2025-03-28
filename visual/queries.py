from sqlalchemy import func, select
from models import HsrCharacter


def get_latest_patch_stmt():
    """Return the statement to get the latest patch version."""
    return select(func.max(HsrCharacter.Version).label('latest_version'))


def get_path_distribution_stmt():
    """Return the statement to get Path distribution."""
    return select(
        HsrCharacter.Path.label('category'), 
        func.count().label('count')
    ).group_by(
        HsrCharacter.Path
    ).order_by(
        func.count().desc()
    )


def get_element_distribution_stmt():
    """Return the statement to get Element distribution."""
    return select(
        HsrCharacter.Element.label('category'), 
        func.count().label('count')
    ).group_by(
        HsrCharacter.Element
    ).order_by(
        func.count().desc()
    )


def get_rarity_distribution_stmt():
    """Return the statement to get Rarity distribution."""
    return select(
        HsrCharacter.Rarity.label('category'), 
        func.count().label('count')
    ).group_by(
        HsrCharacter.Rarity
    ).order_by(
        func.count().desc()
    ) 