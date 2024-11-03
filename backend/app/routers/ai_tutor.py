from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ..models.diagnostic_test import DiagnosticTest
from ..models.diagnostic_test_results import DiagnosticTestResult
from ..models.learning_path_content import LearningPathContent
from ..models.user_concept_mastery import UserConceptMastery, Concept

from datetime import datetime, UTC

from ..crud import learning_path as crud_learning_path
from ..crud import learning_path_content as crud_learning_path_content

from ..services.generative_ai import openai_service

from ..database import init_postgres

from ..utils.mastery import adjust_mastery_from_feedback

from datetime import datetime, UTC

router = APIRouter(prefix="/ai_tutor", tags=["ai_tutor"])

@router.get("/{user_id}/{topic}")
async def get_ai_tutor_response(user_id: int, topic: str, db: Session = Depends(init_postgres)):

    first_message = False

    learning_path = crud_learning_path.get_learning_path_by_title(db=db, user_id=user_id, title=topic)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found.")
    
    learning_path_content = await LearningPathContent.find_one({"user_id": user_id, "learning_path_id": learning_path.id})

    if not learning_path_content:
        raise HTTPException(status_code=404, detail="Learning path content not found.")
    
    if learning_path_content.current_level_index != -1:
        #get current level and objective
        current_level = learning_path_content.levels[learning_path_content.current_level_index]
        current_objective = current_level.learning_objectives[learning_path_content.current_learning_objective_index]

        #Get prior exchanges
        recent_chat = current_objective.learning_objective_chat_history[-10:] if current_objective.learning_objective_chat_history else []
        
        prior_exchanges = [{"sender": chat.sender, "message": chat.message} for chat in recent_chat]

        if recent_chat == []:
            first_message = True

        #Get conversation history summary
        conversation_history_summary = learning_path_content.chat_summary if learning_path_content.chat_summary else ""
        level_chat_summary = current_level.level_chat_summary if current_level.level_chat_summary else ""
        learning_objective_summary = current_objective.learning_objective_chat_summary if current_objective.learning_objective_chat_summary else ""
    
    else:
        prior_exchanges = []
        learning_objective_summary = "No summary available"
        

    #Fetch mastery scores
    user_concept_mastery = await UserConceptMastery.find_one({"user_id": user_id})
    if not user_concept_mastery:
        raise HTTPException(status_code=404, detail="User concept mastery data not found.")
    
    if not first_message:
        mastery_scores = {concept.concept_name: concept.mastery_score for concept in user_concept_mastery.concepts}

        evaluation_response = openai_service.response_evaluator(
            prior_exchanges=prior_exchanges,
            learning_objective_conversation_summary=learning_objective_summary,
            mastery_scores=mastery_scores,
            topic=topic,
            learning_objective=current_objective.objective_text if learning_path_content.current_level_index != -1 else "The student has completed the learning tree. Review a student's weak points in the level and reinforce them."
        )

        print(evaluation_response)

        #update current learning objective summary
        if learning_path_content.current_level_index != -1:
            updated_learning_objective_summary = openai_service.content_summarizer(
                old_summary=learning_objective_summary,
                new_information=evaluation_response['analysis']
            ) if learning_objective_summary else evaluation_response['analysis']

            current_objective.learning_objective_chat_summary = updated_learning_objective_summary

        #Update current level and learning objective if student ready to move on
        if evaluation_response['progress'] and learning_path_content.current_level_index != -1:
            if learning_path_content.current_learning_objective_index + 1 < len(current_level.learning_objectives):
                #Update learning objective only
                learning_path_content.current_learning_objective_index += 1
                current_objective = current_level.learning_objectives[learning_path_content.current_learning_objective_index]
                
                #update level summary
                updated_level_chat_summary = openai_service.content_summarizer(
                    old_summary=level_chat_summary,
                    new_information=learning_objective_summary
                ) if level_chat_summary else learning_objective_summary
                current_level.level_chat_summary = updated_level_chat_summary

            elif learning_path_content.current_level_index + 1 < len(learning_path_content.levels):
                #Update level to next level, retrieve first learning objective
                learning_path_content.current_learning_objective_index = 0
                learning_path_content.current_level_index += 1
                current_level = learning_path_content.levels[learning_path_content.current_level_index]
                current_objective = current_level.learning_objectives[learning_path_content.current_learning_objective_index]

                #update level summary
                updated_level_chat_summary = openai_service.content_summarizer(
                    old_summary=level_chat_summary,
                    new_information=learning_objective_summary
                ) if level_chat_summary else level_chat_summary
                current_level.level_chat_summary = updated_level_chat_summary

                #update overall summary
                updated_conversation_history_summary = openai_service.content_summarizer(
                    old_summary=conversation_history_summary,
                    new_information=updated_level_chat_summary
                ) if conversation_history_summary else updated_level_chat_summary

                learning_path_content.chat_summary = updated_conversation_history_summary

            else:
                learning_path_content.current_learning_objective_index = -1
                learning_path_content.current_level_index = -1

        existing_concepts_dict = {concept.concept_name: concept for concept in user_concept_mastery.concepts}

        for concept_name in evaluation_response['new_concepts']:
            if concept_name not in existing_concepts_dict:
                new_concept= Concept(
                concept_name=concept_name,
                mastery_score=0.38,
                last_updated=datetime.now(UTC)
                )
                
                user_concept_mastery.concepts.append(new_concept)
                existing_concepts_dict[concept_name] = new_concept
        
        for concept_name, mastery_evaluation in evaluation_response['concept_mastery_evaluation'].items():
            if concept_name in existing_concepts_dict:
                existing_concept = existing_concepts_dict[concept_name]
                existing_concept.mastery_score = adjust_mastery_from_feedback(existing_concept.mastery_score,mastery_evaluation)
        
        await user_concept_mastery.save()
    
    updated_mastery_scores = {concept.concept_name: concept.mastery_score for concept in user_concept_mastery.concepts}

    
    await learning_path_content.save()

    #Get conversation history summary
    conversation_history_summary = learning_path_content.chat_summary if learning_path_content.chat_summary else "No summary available."

    if learning_path_content.current_level_index != -1:
        level_chat_summary = current_level.level_chat_summary if current_level.level_chat_summary else "No summary available"
        learning_objective_summary = current_objective.learning_objective_chat_summary if current_objective.learning_objective_chat_summary else "No summary available"
        current_objective_text = current_objective.objective_text
    else:
        level_chat_summary = "No summary available"
        learning_objective_summary = "No summary available"
        current_objective_text = "The student has completed the learning tree. Review a student's weak points in the level and reinforce them."

    ai_response = openai_service.ai_tutor(
        prior_exchanges= prior_exchanges,
        conversation_history_summary=conversation_history_summary,
        level_chat_summary=level_chat_summary,
        learning_objective_summary=learning_objective_summary,
        mastery_scores=updated_mastery_scores,
        topic=topic,
        current_learning_objective=current_objective_text,
        progress=evaluation_response['progress']
    )

    print(ai_response)

    await crud_learning_path_content.save_chat_history(user_id=user_id,
                                                 learning_path_id=learning_path.id,
                                                 message={"sender":"tutor","message":ai_response["response"]})

    #output
    return ai_response["response"]


