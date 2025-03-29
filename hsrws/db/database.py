"""Database connectivity for the HSR application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PATH = "hsr.db"


def get_engine():
    """
    Gets SQLAlchemy engine for the database.

    Returns:
        SQLAlchemy engine object.
    """
    return create_engine(f"sqlite:///{DB_PATH}")


def get_session():
    """
    Gets a SQLAlchemy session.

    Returns:
        SQLAlchemy session object.
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
