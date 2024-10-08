from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import PostgresBase

class User(PostgresBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255),unique=True,nullable=False)
    username = Column(String(255),unique=True,nullable=False)
    hashed_password = Column(String(255),nullable=False)

    learning_paths = relationship("LearningPath", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress",back_populates="user",cascade="all, delete-orphan")