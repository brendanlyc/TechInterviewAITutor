from pydantic import BaseModel, EmailStr, SecretStr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: SecretStr


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    password: SecretStr