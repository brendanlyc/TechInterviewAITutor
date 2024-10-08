from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..crud import learning_path as crud_learning_path
from ..schemas import learning_path as schemas_learning_path
from ..database import init_postgres

router = APIRouter(prefix="/learning_paths",tags=['learning_paths'])

@router.post("/",response_model=schemas_learning_path.LearningPath)
def create_learning_path(learning_path: schemas_learning_path.LearningPathCreate, db: Session = Depends(init_postgres)):
    return crud_learning_path.create_learning_path(db=db,learning_path=learning_path)


@router.get("/{learning_path_id}",response_model=schemas_learning_path.LearningPath)
def read_learning_path(learning_path_id: int, db: Session = Depends(init_postgres)):
    db_learning_path = crud_learning_path.get_learning_path(db=db,learning_path_id=learning_path_id)
    if db_learning_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    return db_learning_path


@router.get("/",response_model=list[schemas_learning_path.LearningPath])
def read_learning_paths(user_id: int, skip: int = 0, limit: int = 0, db: Session = Depends(init_postgres)):
    return crud_learning_path.get_learning_paths(db=db,user_id=user_id,skip=skip,limit=limit)


@router.put("/{learning_path_id}",response_model=schemas_learning_path.LearningPath)
def update_learning_path(learning_path_id: int, learning_path_update: schemas_learning_path.LearningPathUpdate, db: Session = Depends(init_postgres)):
    db_learning_path = crud_learning_path.update_learning_path(db=db,learning_path_id=learning_path_id,learning_path_update=learning_path_update)
    if db_learning_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")


@router.delete("/{learning_path_id}",response_model=schemas_learning_path.LearningPath)
def delete_learning_path(learning_path_id: int, db: Session = Depends(init_postgres)):
    db_learning_path = crud_learning_path.delete_learning_path(db=db,learning_path_id=learning_path_id)
    if db_learning_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return db_learning_path