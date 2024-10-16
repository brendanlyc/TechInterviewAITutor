from pydantic import BaseModel
from typing import Optional

class LearningPathRequest(BaseModel):
    topic: str
    experience: str
    feedback: Optional[str]
    prior_content: Optional[str]

class LearningPathResponse(BaseModel):
    content: str