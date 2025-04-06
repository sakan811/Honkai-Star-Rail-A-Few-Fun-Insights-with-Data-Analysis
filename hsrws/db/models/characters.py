"""SQLAlchemy models for the HSR characters database."""

from sqlalchemy.orm import declarative_base  # Updated import path
from sqlalchemy import Column, String, Float

Base = declarative_base()


class HsrCharacter(Base):
    """
    SQLAlchemy model for HsrCharacters table.

    Attributes:
        Character: Character name (primary key).
        Path: Character's path.
        Element: Character's element.
        Rarity: Character's rarity.
        Version: Version the character was released in.
    """

    __tablename__ = "HsrCharacters"

    Character = Column(String, primary_key=True)
    Path = Column(String)
    Element = Column(String)
    Rarity = Column(String)
    Version: Column[float] = Column(Float)
