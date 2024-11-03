from beanie import Document
from datetime import datetime, UTC
from typing import List, Optional
from pydantic import BaseModel

class Concept(BaseModel):
    concept_name: str
    mastery_score: float
    last_updated: datetime = datetime.now(UTC)

class UserConceptMastery(Document):
    user_id: int 
    concepts: List[Concept] 

    class Settings:
        collection = "user_concept_mastery"
