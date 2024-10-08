from fastapi import APIRouter, HTTPException
from ..models.content import Content

router = APIRouter(prefix="/content", tags=['content'])

@router.post("/", response_model=Content)
async def create_content(content: Content):
    await content.insert()
    return content

@router.get("/{content_id}",response_model=Content)
async def get_content(content_id: str):
    content = await Content.get(content_id)
    if content is None:
        raise HTTPException(status_code=404,detail="Content not found")
    return content

@router.put("/{content_id}",response_model=Content)
async def update_content(content_id: str, updated_data: dict):
    content = await Content.get(content_id)
    if content is None:
        raise HTTPException(status_code=404,detail="Content not found")
    await content.set(updated_data)
    return content

@router.delete("/{content_id}",response_model=Content)
async def delete_content(content_id: str):
    content = await Content.get(content_id)
    if content is None:
        raise HTTPException(status_code=404,detail="Content not found")
    await content.delete()
    return content