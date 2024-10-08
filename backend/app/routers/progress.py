from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..crud import progress as crud_progress
from ..schemas import progress as schemas_progress
from ..database import init_postgres

router = APIRouter(prefix="/progress",tags=['progress'])

@router.post("/", response_model=schemas_progress.Progress)
def create_progress(progress: schemas_progress.ProgressCreate, db: Session = Depends(init_postgres)):
    db_progress = crud_progress.get_user_progress(db,progress.user_id,progress.learning_path_id)

    if db_progress:
        raise HTTPException(status_code=400, detail="Progress for this user and learning path already exists")
    return crud_progress.create_progress(db=db, progress=progress)


@router.get("/{progress_id}", response_model=schemas_progress.Progress)
def read_progress(progress_id: int, db: Session = Depends(init_postgres)):
    db_progress = crud_progress.get_progress(db=db, progress_id=progress_id)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    return db_progress


@router.put("/{progress_id}", response_model=schemas_progress.Progress)
def update_progress(progress_id: int, progress_update: schemas_progress.ProgressUpdate, db: Session = Depends(init_postgres)):
    db_progress = crud_progress.update_progress(db=db,progress_id=progress_id,progress_update=progress_update)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    return db_progress
