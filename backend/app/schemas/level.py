from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LevelBase(BaseModel):
    learning_path_id: int
    level_number: int
    title: str
    content_reference: Optional[str] = None
    review_question_reference: Optional[str] = None

class LevelCreate(LevelBase):
    pass

class LevelUpdate(LevelBase):
    content_reference: Optional[str] = None
    review_question_reference: Optional[str] = None

class Level(LevelBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True