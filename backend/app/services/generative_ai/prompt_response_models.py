from pydantic import BaseModel, Field
from beanie import Document
from typing import List, Union, Optional, Dict, Any
from datetime import datetime

#LearningPath

class ContentValidatorResponse(BaseModel):
    analysis: str
    feedback: str

class LearningObjectivesResponse(BaseModel):
    objective_text: str

class LevelResponse(BaseModel):
    concept_name: str
    learning_objectives: List[LearningObjectivesResponse]

class LearningPathGeneratorResponse(BaseModel):
    levels: list[LevelResponse]
    generation_working: str

#DiagnosticTest

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

class DiagnosticTestResponse(BaseModel):
    working: str
    questions: List[Question]

#Diagnostic Test Evaluation
class CriterionScoreResponse(BaseModel):
    criterion: str
    score: float
    justification: str
    max_score: float

class QuestionResultResponse(BaseModel):
    missing_concepts: List[str]
    existing_concepts: List[str]
    student_answer: Optional[str]
    criterion_scores: List[CriterionScoreResponse]

class DiagnosticTestResultResponse(BaseModel):
    question_results: List[QuestionResultResponse]
    working: str

#AI Tutor Response
class AITutorResponseOutput(BaseModel):
    response: str
    working: str

#Student Response Evaluator
class ResponseEvaluatorOutput(BaseModel):
    concept_mastery_evaluation: Optional[Dict[str,int]] = None
    new_concepts: List[str]
    progress: bool
    analysis: str
    working: str