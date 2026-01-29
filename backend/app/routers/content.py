"""
Content API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID

from ..database import get_db
from ..models.content import Content, ContentLike, ContentView
from ..models.user import User
from ..schemas.content import ContentCreate, ContentUpdate, ContentResponse, ContentListResponse
from .users import get_current_user, require_auth

router = APIRouter(prefix="/api/content", tags=["Content"])


@router.get("", response_model=ContentListResponse)
async def list_content(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    user_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    """List content with optional filters"""
    query = select(Content).where(Content.is_public == True)
    
    if type:
        query = query.where(Content.type == type)
    if user_id:
        query = query.where(Content.user_id == user_id)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated results
    query = query.order_by(Content.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    content = result.scalars().all()
    
    return ContentListResponse(
        items=content,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/trending", response_model=ContentListResponse)
async def trending_content(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get trending content"""
    query = select(Content).where(Content.is_public == True)
    query = query.order_by(Content.view_count.desc(), Content.like_count.desc())
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated results
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    content = result.scalars().all()
    
    return ContentListResponse(
        items=content,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    content_data: ContentCreate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Create new content"""
    new_content = Content(
        user_id=current_user.id,
        **content_data.model_dump()
    )
    
    db.add(new_content)
    await db.commit()
    await db.refresh(new_content)
    
    return new_content


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get specific content"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: UUID,
    content_data: ContentUpdate,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Update content"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    if content.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this content"
        )
    
    for field, value in content_data.model_dump(exclude_unset=True).items():
        setattr(content, field, value)
    
    await db.commit()
    await db.refresh(content)
    
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: UUID,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Delete content"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    if content.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this content"
        )
    
    await db.delete(content)
    await db.commit()


@router.post("/{content_id}/like", status_code=status.HTTP_201_CREATED)
async def like_content(
    content_id: UUID,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """Like content"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Check if already liked
    result = await db.execute(
        select(ContentLike).where(
            ContentLike.user_id == current_user.id,
            ContentLike.content_id == content_id
        )
    )
    
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked"
        )
    
    like = ContentLike(user_id=current_user.id, content_id=content_id)
    db.add(like)
    
    content.like_count += 1
    await db.commit()
    
    return {"message": "Liked successfully"}


@router.post("/{content_id}/view", status_code=status.HTTP_201_CREATED)
async def record_view(
    content_id: UUID,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Record a content view"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    view = ContentView(
        content_id=content_id,
        user_id=current_user.id if current_user else None
    )
    db.add(view)
    
    content.view_count += 1
    await db.commit()
    
    return {"message": "View recorded"}
