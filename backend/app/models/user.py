from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255),unique=True,nullable=False)
    username = Column(String(255),unique=True,nullable=False)
    hashed_password = Column(String(255),nullable=False)