from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LearningPathBase(BaseModel):
    user_id: int
    title: str
    experience_level: str

class LearningPathCreate(LearningPathBase):
    pass

class LearningPathUpdate(LearningPathBase):
    title: Optional[str] = None

class LearningPath(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
