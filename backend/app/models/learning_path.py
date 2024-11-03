from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from ..database import PostgresBase
from datetime import datetime,UTC

class LearningPath(PostgresBase):
    __tablename__ = "learning_paths"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    completed = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, default=datetime.now(UTC))

    user = relationship("User",back_populates="learning_paths")

    __table_args__ = (
        UniqueConstraint('user_id', 'title', name='unique_user_title'),
    )
