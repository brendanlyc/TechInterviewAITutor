from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.auth import UserLogin, TokenResponse
from ..schemas.user import ResetPasswordRequest
from ..routers.user import get_user_by_email
from ..crud.auth import authenticate_user
from ..database import init_postgres
from ..utils.auth import create_access_token
from ..utils.email import send_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(user_login: UserLogin, db: Session = Depends(init_postgres)):
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token(data={"sub": user.username})  # JWT token creation
    return {"token": token, "userId": user.id, "username": user.username}


@router.post("/request-reset-password")
def request_reset_password(reset_request: ResetPasswordRequest, db: Session = Depends(init_postgres)):
    user = get_user_by_email(db=db, email=reset_request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Account with email does not exist")
    reset_token = create_access_token(data={"sub": str(user.id)})
    reset_link = f"http://localhost:8080/reset-password/{user.id}/{reset_token}"

    send_reset_email(user.email,reset_link)

    return {"message": "Reset link sent"}




