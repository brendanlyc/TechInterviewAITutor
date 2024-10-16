from sqlalchemy import Column, Integer, String, Float
from ..database import PostgresBase

class Prompt(PostgresBase):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String,unique=True, index=True, nullable=False)
    system_content = Column(String, nullable=False)
    user_content = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
