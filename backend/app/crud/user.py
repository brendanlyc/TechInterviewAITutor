
from sqlalchemy.orm import Session
from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserUpdate
from ..utils.auth import hash_password

def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password.get_secret_value())

    new_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_password(user_id: int, user_update: UserUpdate, db: Session):
    user = get_user(user_id=user_id, db=db)
    if user is None:
        return None
    
    hashed_password = hash_password(user_update.password.get_secret_value())
    user.hashed_password = hashed_password
    db.commit()
    return user

def get_user(user_id: int, db: Session):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_username(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_email(email: str, db: Session):
    return db.query(UserModel).filter(UserModel.email == email).first()