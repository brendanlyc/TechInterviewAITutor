from pydantic import BaseModel, SecretStr

class UserLogin(BaseModel):
    username: str
    password: SecretStr

class TokenResponse(BaseModel):
    token: str
    userId: int
    username: str