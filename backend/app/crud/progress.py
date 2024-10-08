from sqlalchemy.orm import Session
from ..models.progress import Progress
from ..schemas.progress import ProgressCreate, ProgressUpdate

def get_progress(db: Session, progress_id: int):
    return db.query(Progress).filter(Progress.id == progress_id).first()

def get_user_progress(db: Session, user_id: int, learning_path_id: int):
    return db.query(Progress).filter(Progress.user_id == user_id, Progress.learning_path_id == learning_path_id).first()

def create_progress(db: Session, progress: ProgressCreate):
    db_progress = Progress(**progress.dict())
    if db_progress:
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
    return db_progress

def update_progress(db: Session, progress_id: int, progress_update: ProgressUpdate):
    db_progress = get_progress(db,progress_id)
    if db_progress:
        db_progress.current_level = progress_update.current_level
        db.commit()
        db.refresh(db_progress)
    
    return db_progress
