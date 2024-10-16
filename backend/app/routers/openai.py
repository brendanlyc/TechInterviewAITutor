from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import init_postgres
from app.external_services.openai_service import generate_learning_path, regenerate_learning_path
from app.schemas.openai import LearningPathRequest, LearningPathResponse
from app.crud import learning_path as lp_crud, level as lvl_crud, progress as progress_crud

router = APIRouter(prefix="/openai",tags=['openai'])

@router.post("/generate-path", response_model=LearningPathResponse)
async def create_learning_path(request: LearningPathRequest, db: Session=Depends(init_postgres)):
    try:
        path_content = generate_learning_path(request.topic, request.experience, db=db)
        return {"content": path_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate-path", response_model=LearningPathResponse)
async def recreate_learning_path(request: LearningPathRequest, db: Session=Depends(init_postgres)):
    try:
        regenerated_content = regenerate_learning_path(request.topic, request.experience, request.feedback, db=db)
        return {"content": regenerated_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
