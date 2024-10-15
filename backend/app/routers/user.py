from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import init_postgres
from ..crud.user import create_user, get_user, get_user_by_email, update_user_password
from ..schemas.user import UserCreate, User, PasswordUpdate, ResetPasswordRequest
from ..utils.auth import verify_access_token

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/", response_model = User)
def create_new_user(user: UserCreate, db: Session = Depends(init_postgres)):
    existing_user = get_user_by_email(user.email,db=db)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    return create_user(user=user,db=db)


@router.get("/{user_id}", response_model= User)
def read_user(user_id: int, db: Session = Depends(init_postgres)):
    user = get_user(user_id=user_id,db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}/password", response_model = User)
def update_password(user_id: int, token: str, password_update: PasswordUpdate, db: Session = Depends(init_postgres)):
    token_user_id = verify_access_token(token)
    print(user_id,token_user_id)
    if token_user_id != user_id:
        raise HTTPException(status_code=403, details="Invalid URL")
    
    updated_user = update_user_password(user_id, password_update, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user