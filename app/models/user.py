from datetime import datetime
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String(128))
    created_at = Column(DateTime, default=datetime.now)


class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(228), index=True)
    user = Column(Integer, ForeignKey("users.id"), nullable=True)
    token_data = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
