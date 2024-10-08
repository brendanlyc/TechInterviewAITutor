from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"),nullable=False)
    current_level = Column(Integer, nullable=False, default=1)

    user = relationship("User", back_populates="progress")
    learning_path = relationship("LearningPath", back_populates="progress")

