from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ..models.diagnostic_test import DiagnosticTest
from ..models.diagnostic_test_results import DiagnosticTestResult, CriterionScore, QuestionResult
from ..models.user_concept_mastery import UserConceptMastery, Concept

from ..crud import learning_path as crud_learning_path

from ..database import init_postgres

from datetime import datetime, UTC

from ..services.generative_ai import openai_service

from ..utils.mastery import update_mastery_from_diagnostic_performance

router = APIRouter(prefix="/diagnostic_test", tags=["diagnostic_test"])

# Get a diagnostic test by user ID and learning path ID
@router.get("/user/{user_id}/learning_path/{learning_path_id}", response_model=DiagnosticTest)
async def get_diagnostic_test(user_id: int, learning_path_id: int):
    diagnostic_test = await DiagnosticTest.find_one({"user_id": user_id, "learning_path_id": learning_path_id})
    if diagnostic_test is None:
        raise HTTPException(status_code=404, detail="Diagnostic test not found")
    return diagnostic_test

# Delete a diagnostic test by ID
@router.delete("/{diagnostic_test_id}", response_model=DiagnosticTest)
async def delete_diagnostic_test(diagnostic_test_id: str):
    diagnostic_test = await DiagnosticTest.get(diagnostic_test_id)
    if diagnostic_test is None:
        raise HTTPException(status_code=404, detail="Diagnostic test not found")
    await diagnostic_test.delete()
    return diagnostic_test

@router.post("/evaluate/user/{user_id}/learning_path/{title}")
async def process_diagnostic_test_answer(user_id: int, title: str, user_answers: Dict[str,str], db: Session = Depends(init_postgres)):
    learning_path = crud_learning_path.get_learning_path_by_title(db=db, user_id=user_id, title=title)
    if not learning_path:
        raise HTTPException(status_code=404, detail="Learning path not found.")
    #Retrieve diagnostic test
    diagnostic_test = await DiagnosticTest.find_one({"user_id": user_id, "learning_path_id": learning_path.id})
    if diagnostic_test is None:
        raise HTTPException(status_code=404, detail="Diagnostic test not found")

    test_details = [
        {
            "questions": q.question,
            "learning_objectives": q.learning_objectives,
            "scoring_rubrics": q.scoring_rubrics.dict(),
            "answer": q.answer
        }
        for q in diagnostic_test.questions
    ]

    #Add student's response
    sorted_answers = dict(sorted(user_answers.items(), key=lambda item: int(item[0])))

    for i, (qn_id, answer) in enumerate(sorted_answers.items()):
        if i < len(test_details):
            test_details[i]["student_answer"] = answer

    test_details_str = str(test_details)

    #obtain user concept mastery information
    user_concept_mastery = await UserConceptMastery.find_one({"user_id": user_id})
    if user_concept_mastery is None:
        concept_names_str = "[]"
    else:
        concept_names = [concept.concept_name for concept in user_concept_mastery.concepts]
        concept_names_str = str(concept_names)

    generated_content = openai_service.evaluate_diagnostic_test(test_details_str,concept_names_str)

    print(generated_content['question_results'])

    transformed_question_results = []
    
    for idx, question in enumerate(generated_content['question_results'], start=1):
        transformed_criterion_scores = [
            CriterionScore(
                criterion = score['criterion'],
                score = score['score'],
                justification = score['justification'],
                max_score = score['max_score']
            )
            for score in question['criterion_scores']
        ]

        transformed_question_results.append(
            QuestionResult(
                question_id = idx,
                student_answer = question['student_answer'],
                criterion_scores = transformed_criterion_scores
            )
        )

    diagnostic_test_results = DiagnosticTestResult(
                                user_id= user_id,
                                diagnostic_test_id= str(diagnostic_test.id),
                                learning_path_id= learning_path.id,
                                date_taken= datetime.now(UTC),
                                question_results = transformed_question_results
                            )
    
    diagnostic_test_results.calculate_scores()

    await diagnostic_test_results.insert()

    user_concept_mastery = await UserConceptMastery.find_one({"user_id": user_id})
    
    if not user_concept_mastery:
        # Initialize if it doesn't exist
        user_concept_mastery = UserConceptMastery(user_id=user_id, concepts=[])

    concept_scores: Dict[str, List[float]] = {}

    for question_result in generated_content['question_results']:
        missing_concepts = question_result["missing_concepts"]
        existing_concepts = question_result["existing_concepts"]
        question_percentage_score = (
            sum(score['score'] for score in question_result['criterion_scores']) / 
            sum(score['max_score'] for score in question_result['criterion_scores'])
        ) * 100

        for concept_name in existing_concepts:
            if concept_name not in concept_scores:
                concept_scores[concept_name] = []
            concept_scores[concept_name].append(question_percentage_score)

        for concept_name in missing_concepts:
            if concept_name not in concept_scores:
                concept_scores[concept_name] = [50]
            concept_scores[concept_name].append(question_percentage_score)

        existing_concepts_dict = {concept.concept_name: concept for concept in user_concept_mastery.concepts}
        
        for concept_name, scores in concept_scores.items():
            prior_mastery = existing_concepts_dict[concept_name].mastery_score if concept_name in existing_concepts else 0.5

            for score in scores:
                new_mastery_score = update_mastery_from_diagnostic_performance(
                    prior_mastery,
                    success=(score >= 70)
                )

            if concept_name in existing_concepts_dict:
                existing_concept = existing_concepts_dict[concept_name]
                existing_concept.mastery_score = new_mastery_score
                existing_concept.last_updated = datetime.now(UTC)
            else:
                new_concept = Concept(
                    concept_name=concept_name,
                    mastery_score= new_mastery_score,
                    last_updated=datetime.now(UTC)
                )
                user_concept_mastery.concepts.append(new_concept)

    await user_concept_mastery.save()






