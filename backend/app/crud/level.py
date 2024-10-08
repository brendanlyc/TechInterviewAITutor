from sqlalchemy.orm import Session
from ..models.level import Level
from ..schemas.level import LevelCreate, LevelUpdate

def get_level(db: Session, level_id: int):
    return db.query(Level).filter(Level.id == level_id).first()

def get_levels_by_learning_path(db: Session, learning_path_id: int, skip: int = 0, limit: int = 10):
    return db.query(Level).filter(Level.learning_path_id == learning_path_id).order_by(Level.level_number).offset(skip).limit(limit).all()

def create_level(db: Session, level: LevelCreate):
    db_level = Level(**level.dict())
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level

def update_level(db: Session, level_id: int, level_update: LevelUpdate):
    db_level = get_level(db=db,level_id=level_id)
    if db_level:
        update_data = level_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_level,key,value)
        db.commit()
        db.refresh(db_level)
    return db_level

def delete_level(db: Session, level_id: int):
    db_level = get_level(db, level_id)
    if db_level:
        db.delete(db_level)
        db.commit()
    return db_level