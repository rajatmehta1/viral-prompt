"""
User Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    website_url: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for creating a user"""
    email: EmailStr
    username: str
    password: str
    display_name: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    website_url: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: UUID
    email: EmailStr
    username: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    website_url: Optional[str] = None
    is_verified: bool = False
    is_premium: bool = False
    credits_balance: int = 50
    role: str = "user"
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""
    user_id: Optional[str] = None
