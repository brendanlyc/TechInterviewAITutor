from sqlalchemy.orm import Session
from app.crud import user as user_crud, learning_path as lp_crud, level as lvl_crud, progress as progress_crud, prompt as prompt_crud
from app.schemas.user import UserCreate
from app.schemas.learning_path import LearningPathCreate
from app.schemas.level import LevelCreate
from app.schemas.progress import ProgressCreate
from app.schemas.prompt import PromptCreate
from app.models.content import Content
from app.models.review_question import ReviewQuestion

from datetime import datetime

from pydantic import SecretStr


async def create_mongodb_content_for_level(level_reference: str):
    content_doc = Content(level_reference=level_reference,
                          content_date={"text": f"Content data for {level_reference}"},
                          created_at=datetime.now())
    await content_doc.insert()
    return content_doc

async def create_mongodb_review_question_for_level(level_reference: str):
    review_question_doc = ReviewQuestion(level_reference=level_reference,
                                         question=f"Review question for {level_reference}",
                                         created_at=datetime.now())
    await review_question_doc.insert()
    return review_question_doc

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
                    experience_level = "Completed basic data structures and algorithms course in university"
                ))
            
            learning_paths.append(lp)
        
        #create levels for each learning path
        for learning_path in learning_paths:
            for i in range(1,4):
                level_reference = f"lp_{learning_path.title}_level_{i}"
                content_doc = await create_mongodb_content_for_level(level_reference=level_reference)
                review_question_doc = await create_mongodb_review_question_for_level(level_reference=level_reference)

                lvl_crud.create_level(
                    db=postgres_db,
                    level=LevelCreate(
                        learning_path_id=lp.id,
                        level_number=i,
                        title=f"Level {i}",
                        goal="",
                        concepts=[],
                        content_reference=str(content_doc.id),
                        review_question_reference=str(review_question_doc.id)
                ))
            
        progress_crud.create_progress(
            db = postgres_db,
            progress = ProgressCreate(
                user_id = user_1.id,
                learning_path_id = learning_paths[0].id,
                current_level = 1
            )
        )

        progress_crud.create_progress(
            db = postgres_db,
            progress = ProgressCreate(
                user_id = user_1.id,
                learning_path_id = learning_paths[1].id,
                current_level = 2
            )
        )

        progress_crud.create_progress(
            db = postgres_db,
            progress = ProgressCreate(
                user_id = user_1.id,
                learning_path_id = learning_paths[2].id,
                current_level = 4
            )
        )
