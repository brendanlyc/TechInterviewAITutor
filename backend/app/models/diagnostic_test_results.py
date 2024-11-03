from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class CriterionScore(BaseModel):
    criterion: str
    score: float
    justification: str
    max_score: float

class QuestionResult(BaseModel):
    question_id: int
    student_answer: Optional[str]
    criterion_scores: List[CriterionScore]
    total_score: float = 0.0
    max_score: float = 0.0
    percentage_score: float = 0.0

    def calculate_scores(self):
        self.total_score = sum(criterion.score for criterion in self.criterion_scores)
        self.max_score = sum(criterion.max_score for criterion in self.criterion_scores)
        self.percentage_score = (self.total_score/self.max_score) * 100 if self.max_score > 0 else 0.0

class DiagnosticTestResult(Document):
    user_id: int 
    diagnostic_test_id: str
    learning_path_id: int
    date_taken: datetime
    total_score: float = 0.0
    max_score: float = 0.0
    percentage_score: float = 0.0
    question_results: List[QuestionResult]

    def calculate_scores(self):
        for question in self.question_results:
            question.calculate_scores()

        self.total_score = sum(question.total_score for question in self.question_results)
        self.max_score = sum(question.max_score for quesiton in self.question_results)
        self.percentage_score = (self.total_score/self.max_score) * 100 if self.max_score > 0 else 0.0

    class Settings:
        collection = "diagnostic_test_results"