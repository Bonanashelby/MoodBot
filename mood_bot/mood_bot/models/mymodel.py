"""Our models structure."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Float
)

from .meta import Base


class Moodbot(Base):
    """The class for our database structure for our results."""

    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    body = Column(Unicode)
    score = Column(Float)
    explain_score = Column(Unicode)
