from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..crud import learning_path as crud_learning_path
from ..crud import progress as crud_progress
from ..crud import level as crud_levels
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


@router.get("/{user_id}",response_model=list[schemas_learning_path.LearningPath])
def read_learning_paths(user_id: int, skip: int = 0, limit: int = 0, db: Session = Depends(init_postgres)):
    learning_paths = crud_learning_path.get_learning_paths(db=db,user_id=user_id,skip=skip,limit=limit)

    if not learning_paths:
        raise HTTPException(status_code=404, detail = "No learning paths found for this user")
    
    user_learning_paths = []
    for path in learning_paths:
        progress = crud_progress.get_user_progress(db=db,user_id=user_id,learning_path_id=path.id)
        levels = crud_levels.get_levels_by_learning_path(db=db,learning_path_id=path.id)

        current_level = progress.current_level if progress else 0
        total_levels = len(levels)

        if not path.is_completed:
            current_level_title = levels[current_level-1]

        user_learning_paths.append({
            "id": path.id,
            "title": path.title,
            "created_at": path.created_at,
            "current_level": current_level,
            "total_levels": total_levels,
            "current_level_title": current_level_title
        })

        return user_learning_paths


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