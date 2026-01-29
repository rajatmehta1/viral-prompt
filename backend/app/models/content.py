"""
Content-related SQLAlchemy models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship

from ..database import Base


class Content(Base):
    """Content model for videos, images, music, etc."""
    __tablename__ = "content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="SET NULL"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(20), nullable=False)  # image, video, reel, music, ai_art
    media_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    duration_seconds = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    file_size_bytes = Column(BigInteger)
    is_ai_generated = Column(Boolean, default=False)
    ai_model = Column(String(100))
    generation_settings = Column(JSONB)
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="content")
    comments = relationship("Comment", back_populates="content")
    views = relationship("ContentView", back_populates="content")


class ContentTag(Base):
    """Content-tag relationship"""
    __tablename__ = "content_tags"
    
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("prompt_tags.id", ondelete="CASCADE"), primary_key=True)


class ContentLike(Base):
    """Content like model"""
    __tablename__ = "content_likes"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentView(Base):
    """Content view tracking"""
    __tablename__ = "content_views"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    ip_address = Column(INET)
    user_agent = Column(Text)
    watch_duration_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="views")


class Comment(Base):
    """Comment model"""
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"))
    body = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    is_edited = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])
