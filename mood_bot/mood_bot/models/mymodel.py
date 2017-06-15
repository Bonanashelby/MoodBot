"""Our models structure."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Float,
    ForeignKey
)

from .meta import Base


class Moodbot(Base):
    """The class for our database structure for our results."""

    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    body = Column(Unicode)
    score = Column(Float)
    explain_score = Column(Unicode)


class User(Base):
    """Model for our users."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode, unique=True)
    password = Column(Unicode)


class Sentiments(Base):
    """Mode for storing sentiments per user."""

    __tablename__ = 'sentiments'
    id = Column(Integer, primary_key=True)
    body = Column(Unicode)
    sentiment = Column(Unicode)
    user_id = Column(Unicode, ForeignKey('users.id'), nullable=False)
