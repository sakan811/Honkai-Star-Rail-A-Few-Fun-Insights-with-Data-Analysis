from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PATH = "hsr.db"


def get_engine():
    """Get SQLAlchemy engine for the database."""
    return create_engine(f"sqlite:///{DB_PATH}")


def get_session():
    """Get a SQLAlchemy session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session() 