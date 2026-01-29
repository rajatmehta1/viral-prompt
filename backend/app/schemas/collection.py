"""
Collection Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CollectionBase(BaseModel):
    """Base collection schema"""
    name: str
    description: Optional[str] = None
    is_public: bool = True


class CollectionCreate(CollectionBase):
    """Schema for creating a collection"""
    cover_image_url: Optional[str] = None


class CollectionUpdate(BaseModel):
    """Schema for updating a collection"""
    name: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: Optional[bool] = None


class CollectionResponse(BaseModel):
    """Schema for collection response"""
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: bool = True
    is_featured: bool = False
    item_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CollectionItemCreate(BaseModel):
    """Schema for adding item to collection"""
    content_id: Optional[UUID] = None
    prompt_id: Optional[UUID] = None


class CollectionListResponse(BaseModel):
    """Schema for paginated collection list"""
    items: List[CollectionResponse]
    total: int
    page: int
    page_size: int
