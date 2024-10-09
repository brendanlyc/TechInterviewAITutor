from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.auth import UserLogin, TokenResponse
from ..crud.auth import authenticate_user
from ..database import init_postgres
from ..utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(user_login: UserLogin, db: Session = Depends(init_postgres)):
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token(data={"sub": user.username})  # JWT token creation
    return {"token": token, "userId": user.id, "username": user.username}