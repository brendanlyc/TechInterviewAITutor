from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import init_postgres
from ..crud import prompt as crud_prompt
from ..schemas import prompt as schemas_prompt

router = APIRouter(prefix="/prompts",tags=["prompts"])


@router.post("/", response_model = schemas_prompt.Prompt)
def create_prompt(prompt: schemas_prompt.PromptCreate, db: Session = Depends(init_postgres)):
    db_prompt = crud_prompt.get_prompt_by_name(db, name= prompt.name)
    if db_prompt:
        raise HTTPException(status_code=400, details="Prompt with this name already exists")

    return crud_prompt.create_prompt(db=db,prompt=prompt)


@router.get("/{prompt_id}", response_model= schemas_prompt.Prompt)
def read_prompt(prompt_id: int, db: Session = Depends(init_postgres)):
    db_prompt = crud_prompt.get_prompt(db, prompt_id= prompt_id)

    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return db_prompt


@router.put("/{prompt_id}", response_model= schemas_prompt.Prompt)
def update_prompt(prompt_id: int, prompt_update: schemas_prompt.PromptUpdate, db: Session = Depends(init_postgres)):
    db_prompt = crud_prompt.update_prompt(db, prompt_id=prompt_id, prompt_update=prompt_update)
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt


@router.delete("/{prompt_id}", response_model = schemas_prompt.Prompt)
def delete_prompt(prompt_id: int, db: Session = Depends(init_postgres)):
    db_prompt = crud_prompt.delete_prompt(db, prompt_id=prompt_id)
    if db_prompt is None:
         raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt
