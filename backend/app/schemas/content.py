"""
Content Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


class ContentBase(BaseModel):
    """Base content schema"""
    title: str
    description: Optional[str] = None
    type: str  # image, video, reel, music, ai_art
    media_url: str
    is_public: bool = True


class ContentCreate(ContentBase):
    """Schema for creating content"""
    prompt_id: Optional[UUID] = None
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    is_ai_generated: bool = False
    ai_model: Optional[str] = None
    generation_settings: Optional[dict] = None


class ContentUpdate(BaseModel):
    """Schema for updating content"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    thumbnail_url: Optional[str] = None


class ContentResponse(BaseModel):
    """Schema for content response"""
    id: UUID
    user_id: Optional[UUID] = None
    prompt_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    type: str
    media_url: str
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    is_ai_generated: bool = False
    ai_model: Optional[str] = None
    is_public: bool = True
    is_featured: bool = False
    view_count: int = 0
    like_count: int = 0
    share_count: int = 0
    comment_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    """Schema for paginated content list"""
    items: List[ContentResponse]
    total: int
    page: int
    page_size: int


class CommentCreate(BaseModel):
    """Schema for creating a comment"""
    body: str
    parent_id: Optional[UUID] = None


class CommentResponse(BaseModel):
    """Schema for comment response"""
    id: UUID
    content_id: UUID
    user_id: UUID
    parent_id: Optional[UUID] = None
    body: str
    like_count: int = 0
    is_edited: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True
