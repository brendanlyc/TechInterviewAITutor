from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..crud import learning_path as crud_learning_path
from ..crud import learning_path_content as crud_learning_path_content
from ..schemas import learning_path as schemas_learning_path
from ..models.learning_path_content import LearningPathContent, ChatMessage
from ..models.diagnostic_test import DiagnosticTest
from ..database import init_postgres
import json
 
from ..services.generative_ai import openai_service

from urllib.parse import unquote

router = APIRouter(prefix="/learning_paths",tags=['learning_paths'])

@router.post("/",response_model=schemas_learning_path.LearningPath)
def create_learning_path(learning_path: schemas_learning_path.LearningPathCreate, db: Session = Depends(init_postgres)):
    """ Create Learning Path Entry in DB"""
    existing_learning_path = crud_learning_path.get_learning_path_by_title(db=db,user_id=learning_path.user_id,title=learning_path.title)

    if existing_learning_path:
        raise HTTPException(status_code=400, detail="Learning path with this title already created. Use another title.")
    
    return crud_learning_path.create_learning_path(db=db,learning_path=learning_path)

@router.get("/user_id/{user_id}/learning_path_title/{title}",response_model=schemas_learning_path.LearningPath)
async def read_learning_path_by_title(user_id: int, title: str, db: Session = Depends(init_postgres)):
    learning_path = crud_learning_path.get_learning_path_by_title(db=db,user_id=user_id,title=unquote(title))
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path with given title not found")
    return learning_path

@router.get("/{learning_path_id}",response_model=schemas_learning_path.LearningPath)
def read_learning_path(learning_path_id: int, db: Session = Depends(init_postgres)):
    db_learning_path = crud_learning_path.get_learning_path(db=db,learning_path_id=learning_path_id)
    if db_learning_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    return db_learning_path

@router.get("/user_id/{user_id}",response_model=list[schemas_learning_path.LearningPath])
def read_learning_paths(user_id: int, db: Session = Depends(init_postgres)):
    learning_paths = crud_learning_path.get_learning_paths(db=db,user_id=user_id)
    if not learning_paths:
        raise HTTPException(status_code=404, detail = "No learning paths found for this user")
    
    return learning_paths

@router.put("/{learning_path_id}",response_model=schemas_learning_path.LearningPath)
def update_learning_path(learning_path_id: int, learning_path_update: schemas_learning_path.LearningPathUpdate, db: Session = Depends(init_postgres)):
    db_learning_path = crud_learning_path.update_learning_path(db=db,learning_path_id=learning_path_id,learning_path_update=learning_path_update)
    if db_learning_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")


@router.delete("/{learning_path_id}",response_model=schemas_learning_path.LearningPath)
def delete_learning_path(learning_path_id: int, db: Session = Depends(init_postgres)):
    db_learning_path = crud_learning_path.delete_learning_path(db=db,learning_path_id=learning_path_id)
    if db_learning_path is None:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return db_learning_path

#Actual learning path content

@router.post("/load/learning_path/{user_id}/{title}", response_model=dict)
async def load_learning_path(user_id: int, title: str, db: Session = Depends(init_postgres)):
    learning_path = crud_learning_path.get_learning_path_by_title(db=db, user_id=user_id, title=title)
    print("Learning Path Located")
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found.")

    learning_path_content = await LearningPathContent.find_one({"user_id": user_id, "learning_path_id": learning_path.id})

    topic = title
    
    #generate learning path content if not available
    if not learning_path_content:
        generated_content = openai_service.generate_learning_path_content(topic)
    #    feedback = openai_service.validate_learning_path_content(topic,str(generated_content['levels'])).get("feedback")

    #    if "no changes needed" not in str(generated_content).lower():
    #        generated_content = openai_service.modify_learning_path_content(topic,str(generated_content['levels']),feedback)

        learning_path_content = LearningPathContent(
            title=title,
            user_id=user_id,
            learning_path_id = learning_path.id,
            levels = generated_content['levels'],
            generation_working = generated_content['generation_working']
        )

        await learning_path_content.insert()
    
    diagnostic_test = await DiagnosticTest.find_one({"user_id": user_id, "learning_path_id": learning_path.id})

    if not diagnostic_test:
        diagnostic_test = openai_service.generate_diagnostic_test(topic,str(learning_path_content.levels))
        #test_feedback = openai_service.validate_diagnostic_test(topic,str(learning_path_content.levels),str(diagnostic_test['questions']))
        #print(diagnostic_test)
        #if "no changes needed" not in test_feedback.lower():
        #    diagnostic_test = openai_service.modify_diagnostic_test(topic,str(learning_path_content.levels),str(diagnostic_test['questions']),test_feedback)
        #    print("Diagnostic test modified")
        diagnostic_test_document = DiagnosticTest(
            user_id = user_id,
            learning_path_id = learning_path.id,
            questions = diagnostic_test['questions']
        )

        await diagnostic_test_document.insert()

    return {
        "learning_path_content": learning_path_content,
        "diagnostic_test": diagnostic_test
    }

@router.post("/save_chat/{user_id}/{title}", response_model=dict)
async def save_chat_history(user_id: int, title: str, chat_message: ChatMessage, db: Session = Depends(init_postgres)):
    learning_path = crud_learning_path.get_learning_path_by_title(db=db, user_id=user_id, title=title)
    print("CHAT MESSAGE: ", chat_message)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found.")
    
    await crud_learning_path_content.save_chat_history(user_id=user_id,
                                                learning_path_id=learning_path.id,
                                                message=chat_message)

    return {"message": "Chat history saved successfully"}

