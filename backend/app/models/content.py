from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Content(Document):
    level_reference: str
    content_data: Optional[dict] = None
    created_at: Optional[datetime] = None

    class Settings:
        collection = "content"




