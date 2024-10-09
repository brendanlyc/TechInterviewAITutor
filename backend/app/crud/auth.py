from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.auth import verify_password

from pydantic import SecretStr

def authenticate_user(db: Session, username: str, password: SecretStr):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(user.hashed_password,password.get_secret_value()):
        return user
    return None