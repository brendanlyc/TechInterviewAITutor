from pydantic import BaseModel

class PromptBase(BaseModel):
    name: str
    content: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    content: str


class Prompt(PromptBase):
    id: int
    
    class Config:
        orm_mode = True
