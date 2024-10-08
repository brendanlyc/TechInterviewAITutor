from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime,UTC

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(UTC))
    total_levels = Column(Integer, nullable=False, default=0)

    user = relationship("User",back_populates="learning_paths")
    levels = relationship("Level",back_populates="learning_path", cascade="all, delete-orphan")
    progress = relationship("Progress",back_populates="learning_path",cascade="all")



