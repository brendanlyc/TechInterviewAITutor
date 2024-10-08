from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import init_postgres
from ..schemas import level as schemas_level
from ..crud import level as crud_level

router = APIRouter(prefix="/levels",tags=['levels'])

@router.post("/", response_model=schemas_level.Level)
def create_level(level: schemas_level.LevelCreate, db: Session = Depends(init_postgres)):
    return crud_level.create_level(db=db, level=level)

@router.get("/{level_id}", response_model=schemas_level.Level)
def read_level(level_id: int, db: Session = Depends(init_postgres)):
    db_level = crud_level.get_level(db, level_id=level_id)
    if db_level is None:
        raise HTTPException(status_code=404, detail="Level not found")
    return db_level

@router.get("/", response_model=list[schemas_level.Level])
def read_levels(learning_path_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(init_postgres)):
    return crud_level.get_levels_by_learning_path(db, learning_path_id=learning_path_id, skip=skip, limit=limit)

@router.put("/{level_id}", response_model=schemas_level.Level)
def update_level(level_id: int, level_update: schemas_level.LevelUpdate, db: Session = Depends(init_postgres)):
    db_level = crud_level.update_level(db, level_id=level_id, level_update=level_update)
    if db_level is None:
        raise HTTPException(status_code=404, detail="Level not found")
    return db_level

@router.delete("/{level_id}", response_model=schemas_level.Level)
def delete_level(level_id: int, db: Session = Depends(init_postgres)):
    db_level = crud_level.delete_level(db, level_id=level_id)
    if db_level is None:
        raise HTTPException(status_code=404, detail="Level not found")
    return db_level
