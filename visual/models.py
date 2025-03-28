from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HsrCharacter(Base):
    """SQLAlchemy model for HsrCharacters table."""
    __tablename__ = "HsrCharacters"
    
    Character = Column(String, primary_key=True)
    Path = Column(String)
    Element = Column(String)
    Rarity = Column(String)
    Version = Column(String) 