from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ..models.diagnostic_test import DiagnosticTest
from ..models.diagnostic_test_results import DiagnosticTestResult

from ..crud import learning_path as crud_learning_path

from ..database import init_postgres

from datetime import datetime, UTC

router = APIRouter(prefix="/diagnostic_test_result", tags=["diagnostic_test_result"])

# Get a diagnostic test by user ID and learning path ID
@router.get("/user/{user_id}/learning_path/{title}", response_model=DiagnosticTestResult)
async def get_diagnostic_test_results_by_title(user_id: int, title: str, db: Session = Depends(init_postgres)):
    learning_path = crud_learning_path.get_learning_path_by_title(db=db, user_id=user_id, title=title)
    print(learning_path)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found.")
    
    diagnostic_test_result = await DiagnosticTestResult.find_one({"user_id": user_id, "learning_path_id": learning_path.id})
    if not diagnostic_test_result:
        raise HTTPException(status_code=404, detail="Diagnostic Test Result not found.")
    
    print(diagnostic_test_result)
    
    return diagnostic_test_result