from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    sender: str  # "user" or "tutor"
    message: str
    timestamp: Optional[datetime] = None

class LearningObjective(BaseModel):
    objective_text: str
    learning_objective_chat_summary: Optional[str] = None
    learning_objective_chat_history: List[ChatMessage] = []
    is_completed: bool = False

class Level(BaseModel):
    concept_name: str
    learning_objectives: List[LearningObjective]
    level_chat_summary: Optional[str] = None
    is_completed: bool = False

class LearningPathContent(Document):
    title: str
    user_id: int
    learning_path_id: int
    levels: List[Level] = [] 
    current_level_index: int = 0
    current_learning_objective_index: int = 0
    chat_summary: Optional[str] = None
    chat_history: List[ChatMessage] = []
    generation_working: str

    class Settings:
        collection = "learning_path_contents"
