from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, UTC

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer,primary_key=True,index=True)
    learning_path_id = Column(Integer,ForeignKey("learning_paths.id"),nullable=False)
    level_number = Column(Integer,nullable=False)
    content_reference = Column(String, nullable=False)
    review_question_reference = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(UTC))

    learning_path = relationship("LearningPath", back_populates="levels")
