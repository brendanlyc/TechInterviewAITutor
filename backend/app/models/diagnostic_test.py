from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ScoringCriterion(BaseModel):
    description: str
    max_score: float

class ScoringRubrics(BaseModel):
    understanding: Optional[ScoringCriterion] = None
    application: Optional[ScoringCriterion] = None
    analysis: Optional[ScoringCriterion] = None
    efficiency: Optional[ScoringCriterion] = None
    accuracy: Optional[ScoringCriterion] = None

class ProvidedDataSchemas(BaseModel):
    example_input: Optional[str] = None  
    example_output: Optional[str] = None 

class Question(BaseModel):
    question: str
    provided_data_schemas: Optional[ProvidedDataSchemas] = None
    difficulty: str
    learning_objectives: List[str]
    estimated_time: str
    scoring_rubrics: ScoringRubrics
    total_max_score: float
    answer: str

class DiagnosticTest(Document):
    user_id: int 
    learning_path_id: int
    questions: List[Question]

    class Settings:
        collection = "diagnostic_tests"
