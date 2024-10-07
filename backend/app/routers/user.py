from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import init_postgres
from ..crud.user import create_user, get_user, get_user_by_username, update_user_password
from ..schemas.user import UserCreate, User, UserUpdate

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/", response_model = User)
def create_new_user(user: UserCreate, db: Session = Depends(init_postgres)):
    existing_user = get_user_by_username(user.username,db=db)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return create_user(user=user,db=db)

@router.get("/{user_id}", response_model= User)
def read_user(user_id: int, db: Session = Depends(init_postgres)):
    user = get_user(user_id=user_id,db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/password", response_model = User)
def update_password(user_id: int, user_update: UserUpdate, db: Session = Depends(init_postgres)):
    updated_user = update_user_password(user_id, user_update, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

