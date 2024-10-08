from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LearningPathBase(BaseModel):
    user_id: int
    title: str
    total_levels: int

class LearningPathCreate(LearningPathBase):
    pass

class LearningPathUpdate(LearningPathBase):
    title: Optional[str] = None
    total_levels: Optional[str] = None


class LearningPath(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
