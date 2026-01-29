"""
User-related SQLAlchemy models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    """User account model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    bio = Column(Text)
    avatar_url = Column(String(500))
    cover_image_url = Column(String(500))
    website_url = Column(String(255))
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    credits_balance = Column(Integer, default=50)
    role = Column(String(20), default="user")
    email_verified_at = Column(DateTime)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prompts = relationship("Prompt", back_populates="user")
    content = relationship("Content", back_populates="user")
    collections = relationship("Collection", back_populates="user")
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    

class UserFollower(Base):
    """User follower relationship"""
    __tablename__ = "user_followers"
    
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSettings(Base):
    """User settings model"""
    __tablename__ = "user_settings"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    weekly_digest = Column(Boolean, default=True)
    show_activity_status = Column(Boolean, default=True)
    private_profile = Column(Boolean, default=False)
    theme = Column(String(20), default="dark")
    language = Column(String(10), default="en")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="settings")
