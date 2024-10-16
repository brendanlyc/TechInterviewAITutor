from pydantic import BaseModel

class PromptBase(BaseModel):
    name: str
    system_content: str
    user_content: str
    temperature: float

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    system_content: str
    user_content: str
    temperature: float


class Prompt(PromptBase):
    id: int
    
    class Config:
        orm_mode = True
