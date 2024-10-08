from fastapi import APIRouter, HTTPException
from ..models.review_question import ReviewQuestion

router = APIRouter(prefix="/review_question", tags=['review_question'])

@router.post("/", response_model=ReviewQuestion)
async def create_review_question(review_question: ReviewQuestion):
    await review_question.insert()
    return review_question

@router.get("/{review_question_id}", response_model=ReviewQuestion)
async def get_review_question(review_question_id: str):
    review_question = await ReviewQuestion.get(review_question_id)
    if review_question is None:
        raise HTTPException(status_code=404, detail="Review question not found")
    return review_question

@router.put("/{review_question_id}", response_model=ReviewQuestion)
async def update_review_question(review_question_id: str, updated_data: dict):
    review_question = await ReviewQuestion.get(review_question_id)
    if review_question is None:
        raise HTTPException(status_code=404, detail="Review question not found")
    await review_question.set(updated_data)
    return review_question

@router.delete("/{review_question_id}", response_model=ReviewQuestion)
async def delete_review_question(review_question_id: str):
    review_question = await ReviewQuestion.get(review_question_id)
    if review_question is None:
        raise HTTPException(status_code=404, detail="Review question not found")
    await review_question.delete()
    return review_question