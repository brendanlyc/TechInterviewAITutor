from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class ReviewQuestion(Document):
    level_reference: str
    question: Optional[str] = None
    created_at: Optional[datetime] = None

    class Settings:
        collection = "review_questions"
