from sqlalchemy.orm import Session
from ..models.learning_path import LearningPath
from ..schemas.learning_path import LearningPathCreate, LearningPathUpdate

def get_learning_path(db: Session, learning_path_id: int):
    return db.query(LearningPath).filter(LearningPath.id == learning_path_id).first()

def get_learning_path_by_title(db: Session, user_id: int, title: str):
    response = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()
    return db.query(LearningPath).filter_by(user_id=user_id,title=title).first()

def get_learning_paths(db: Session, user_id: int):
    return db.query(LearningPath).filter(LearningPath.user_id == user_id)\
        .order_by(LearningPath.created_at.desc()).all()

def create_learning_path(db: Session, learning_path: LearningPathCreate):
    db_learning_path = LearningPath(**learning_path.dict())
    db.add(db_learning_path)
    db.commit()
    db.refresh(db_learning_path)
    return db_learning_path

def update_learning_path(db: Session, learning_path_id: int, learning_path_update: LearningPathUpdate):
    db_learning_path = get_learning_path(db=db,learning_path_id=learning_path_id)
    if db_learning_path:
        update_data = learning_path_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_learning_path, key, value)
        db.commit()
        db.refresh(db_learning_path)
    
    return db_learning_path

def delete_learning_path(db: Session, learning_path_id: int):
    db_learning_path = get_learning_path(db=db,learning_path_id=learning_path_id)
    if db_learning_path:
        db.delete(db_learning_path)
        db.commit()
    return db_learning_path

