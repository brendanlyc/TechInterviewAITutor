from sqlalchemy.orm import Session
from ..models.prompt import Prompt
from ..schemas.prompt import PromptCreate, PromptUpdate

def get_prompt(db: Session, prompt_id: int):
    return db.query(Prompt).filter(Prompt.id==prompt_id).first()

def get_prompt_by_name(db: Session, name: str):
    return db.query(Prompt).filter(Prompt.name==name).first()

def create_prompt(db: Session, prompt: PromptCreate):
    db_prompt = Prompt(name=prompt.name, 
                       system_content=prompt.system_content,
                       user_content=prompt.user_content,
                       temperature=prompt.temperature)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def update_prompt(db: Session, prompt_id: int, prompt_update: PromptUpdate):
    db_prompt = get_prompt(db,prompt_id)
    if db_prompt:
        db_prompt.system_content = prompt_update.system_content
        db_prompt.user_content = prompt_update.user_content
        db_prompt.temperature = prompt_update.temperature
        db.commit()
        db.refresh(db_prompt)
    return db_prompt

def delete_prompt(db: Session, prompt_id: int):
    db_prompt = get_prompt(db,prompt_id)
    if db_prompt:
        db.delete(db_prompt)
        db.commit()
    return db_prompt

