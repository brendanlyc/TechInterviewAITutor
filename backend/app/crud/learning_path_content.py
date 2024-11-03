from fastapi import HTTPException
from ..models.learning_path_content import LearningPathContent
from ..models.learning_path_content import ChatMessage
from datetime import datetime, UTC

async def get_learning_path_content(user_id: int, learning_path_id: int):
    return await LearningPathContent.find_one({"user_id": user_id, "learning_path_id": learning_path_id})

async def mark_level_as_completed(user_id: int, learning_path_id: int, level_index: int):
    learning_path_content = await get_learning_path_content(user_id=user_id,learning_path_id=learning_path_id)
    if learning_path_content:
        if level_index + 1 < len(learning_path_content.levels):
            learning_path_content.current_level_index += 1
            learning_path_content.current_learning_objective_index = 0

        level = learning_path_content.levels[level_index]
        level.is_completed = True
        level.last_updated = datetime.now(UTC)
        await learning_path_content.save()

async def mark_learning_objectives_as_completed(user_id: int, learning_path_id: int, level_index: int, objective_index: int):
    learning_path_content = await get_learning_path_content(user_id=user_id,learning_path_id=learning_path_id)
    if learning_path_content:
        objective = learning_path_content.levels[level_index].learning_objectives[objective_index]
        objective.is_completed = True
    
        all_completed = all(obj.is_completed for obj in learning_path_content.levels[level_index].learning_objectives)

        if all_completed:
            await mark_level_as_completed(user_id=user_id,learning_path_id=learning_path_id,level_index=level_index)
        else:
            learning_path_content.current_learning_objective_index += 1
            await learning_path_content.save()

async def save_chat_history(user_id: int, learning_path_id: int, message: ChatMessage):
    learning_path_content = await get_learning_path_content(user_id=user_id,learning_path_id=learning_path_id)

    current_level_index = learning_path_content.current_level_index
    current_learning_objective_index = learning_path_content.current_learning_objective_index

    if not learning_path_content:
        raise HTTPException(status_code=404, detail="Learning path content not found")

    learning_path_content.chat_history.append(message)
    learning_path_content.levels[current_level_index].learning_objectives[current_learning_objective_index].learning_objective_chat_history.append(message)

    await learning_path_content.save()
    
async def update_learning_objective_chat_summary(user_id: int, learning_path_id: int, summary: str):
    learning_path_content = await get_learning_path_content(user_id=user_id,learning_path_id=learning_path_id)

    current_level_index = learning_path_content.current_level_index
    current_learning_objective_index = learning_path_content.current_learning_objective_index

    if not learning_path_content:
        raise HTTPException(status_code=404, detail="Learning path content not found")

    learning_path_content.levels[current_level_index].learning_objectives[current_learning_objective_index].learning_objective_chat_summary = summary

    await learning_path_content.save()

async def update_level_chat_summary(user_id: int, learning_path_id: int, summary: str):
    learning_path_content = await get_learning_path_content(user_id=user_id,learning_path_id=learning_path_id)

    current_level_index = learning_path_content.current_level_index

    if not learning_path_content:
        raise HTTPException(status_code=404, detail="Learning path content not found")

    learning_path_content.levels[current_level_index].level_chat_summary = summary

    await learning_path_content.save()  

async def update_learning_path_summary(user_id: int, learning_path_id: int, summary: str):
    learning_path_content = await get_learning_path_content(user_id=user_id,learning_path_id=learning_path_id)

    if not learning_path_content:
        raise HTTPException(status_code=404, detail="Learning path content not found")

    learning_path_content.chat_summary = summary

    await learning_path_content.save()    