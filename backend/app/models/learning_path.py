from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from ..database import PostgresBase
from datetime import datetime,UTC

class LearningPath(PostgresBase):
    __tablename__ = "learning_paths"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    experience_level = Column(String, nullable = False)

    created_at = Column(TIMESTAMP, default=datetime.now(UTC))

    user = relationship("User",back_populates="learning_paths")
    levels = relationship("Level",back_populates="learning_path", cascade="all, delete-orphan")
    progress = relationship("Progress",back_populates="learning_path",cascade="all, delete")



