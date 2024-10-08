from sqlalchemy import Column, Integer, String
from ..database import Base

class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String,unique=True, index=True, nullable=False)
    content = Column(String,unique=True,nullable=False)
