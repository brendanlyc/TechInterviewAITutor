from pydantic import BaseModel

class ProgressBase(BaseModel):
    user_id: int
    learning_path_id: int
    current_level: int

class ProgressCreate(ProgressBase):
    pass

class ProgressUpdate(ProgressBase):
    current_level: int

class Progress(ProgressBase):
    id: int

    class Config:
        orm_mode = True