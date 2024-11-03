from sqlalchemy.orm import Session
from app.crud import user as user_crud, learning_path as lp_crud
from app.schemas.user import UserCreate
from app.schemas.learning_path import LearningPathCreate

from datetime import datetime

from pydantic import SecretStr

async def populate_dummy_data(postgres_db: Session):
    user_1 = user_crud.get_user_by_username(username="test123acc", db=postgres_db)
    if not user_1:
        user_1 = user_crud.create_user(
            user=UserCreate(
                email="test123@gmail.com",
                username="test123acc",
                password=SecretStr("password")
            ),
            db = postgres_db
        )

        learning_paths = []

        #Create dummy learning paths
        for title in ["Sliding Window", "Dynamic Programming", "Two Pointers"]:
            lp = lp_crud.create_learning_path(
                db=postgres_db,
                learning_path=LearningPathCreate(
                    user_id = user_1.id,
                    title = title,
                ))
            
            learning_paths.append(lp)