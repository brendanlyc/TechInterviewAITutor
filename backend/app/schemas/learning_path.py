from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LearningPathBase(BaseModel):
    user_id: int
    title: str
    completed: Optional[bool] = False

class LearningPathCreate(LearningPathBase):
    pass

class LearningPathUpdate(LearningPathBase):
    title: Optional[str] = None
    completed: Optional[bool] = False
    diagnostic_test_attempted: Optional[bool] = False

class LearningPath(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    completed: bool

    class Config:
        orm_mode = True
