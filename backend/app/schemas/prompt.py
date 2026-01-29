"""
Prompt Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class PromptCategoryResponse(BaseModel):
    """Schema for prompt category response"""
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    
    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    """Base prompt schema"""
    title: str
    prompt_text: str
    description: Optional[str] = None
    type: str  # image, video, music, caption, script, text
    category_id: Optional[int] = None
    is_public: bool = True


class PromptCreate(PromptBase):
    """Schema for creating a prompt"""
    tags: Optional[List[str]] = None


class PromptUpdate(BaseModel):
    """Schema for updating a prompt"""
    title: Optional[str] = None
    prompt_text: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    category_id: Optional[int] = None
    is_public: Optional[bool] = None
    preview_image_url: Optional[str] = None


class PromptResponse(BaseModel):
    """Schema for prompt response"""
    id: UUID
    user_id: Optional[UUID] = None
    category_id: Optional[int] = None
    title: str
    prompt_text: str
    description: Optional[str] = None
    type: str
    preview_image_url: Optional[str] = None
    is_featured: bool = False
    is_public: bool = True
    use_count: int = 0
    like_count: int = 0
    save_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PromptListResponse(BaseModel):
    """Schema for paginated prompt list"""
    items: List[PromptResponse]
    total: int
    page: int
    page_size: int
