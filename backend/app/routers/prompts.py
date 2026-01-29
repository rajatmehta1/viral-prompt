"""
Prompts API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID

from ..database import get_db
from ..models.prompt import Prompt, PromptLike, PromptSave
from ..models.user import User
from ..schemas.prompt import PromptCreate, PromptUpdate, PromptResponse, PromptListResponse
from .users import get_current_user, require_auth

router = APIRouter(prefix="/api/prompts", tags=["Prompts"])


@router.get("", response_model=PromptListResponse)
async def list_prompts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List prompts with optional filters"""
    query = select(Prompt).where(Prompt.is_public == True)
    
    if type:
        query = query.where(Prompt.type == type)
    if category_id:
        query = query.where(Prompt.category_id == category_id)
    if search:
        query = query.where(Prompt.title.ilike(f"%{search}%"))
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated results
    query = query.order_by(Prompt.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    prompts = result.scalars().all()
    
    return PromptListResponse(
        items=prompts,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    prompt_data: PromptCreate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Create a new prompt"""
    new_prompt = Prompt(
        user_id=current_user.id,
        **prompt_data.model_dump(exclude={"tags"})
    )
    
    db.add(new_prompt)
    await db.commit()
    await db.refresh(new_prompt)
    
    return new_prompt


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific prompt"""
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    return prompt


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: UUID,
    prompt_data: PromptUpdate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Update a prompt"""
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    if prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this prompt"
        )
    
    for field, value in prompt_data.model_dump(exclude_unset=True).items():
        setattr(prompt, field, value)
    
    await db.commit()
    await db.refresh(prompt)
    
    return prompt


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: UUID,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Delete a prompt"""
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    if prompt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this prompt"
        )
    
    await db.delete(prompt)
    await db.commit()


@router.post("/{prompt_id}/like", status_code=status.HTTP_201_CREATED)
async def like_prompt(
    prompt_id: UUID,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Like a prompt"""
    # Check if prompt exists
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Check if already liked
    result = await db.execute(
        select(PromptLike).where(
            PromptLike.user_id == current_user.id,
            PromptLike.prompt_id == prompt_id
        )
    )
    
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked"
        )
    
    # Add like
    like = PromptLike(user_id=current_user.id, prompt_id=prompt_id)
    db.add(like)
    
    # Update like count
    prompt.like_count += 1
    
    await db.commit()
    
    return {"message": "Liked successfully"}


@router.delete("/{prompt_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_prompt(
    prompt_id: UUID,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Unlike a prompt"""
    result = await db.execute(
        select(PromptLike).where(
            PromptLike.user_id == current_user.id,
            PromptLike.prompt_id == prompt_id
        )
    )
    like = result.scalar_one_or_none()
    
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found"
        )
    
    # Update like count on prompt
    prompt_result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    prompt = prompt_result.scalar_one_or_none()
    if prompt:
        prompt.like_count = max(0, prompt.like_count - 1)
    
    await db.delete(like)
    await db.commit()
