"""
Prompt-related SQLAlchemy models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class PromptCategory(Base):
    """Prompt category model"""
    __tablename__ = "prompt_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    color = Column(String(20))
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prompts = relationship("Prompt", back_populates="category")


class Prompt(Base):
    """Prompt model"""
    __tablename__ = "prompts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    category_id = Column(Integer, ForeignKey("prompt_categories.id", ondelete="SET NULL"))
    title = Column(String(200), nullable=False)
    prompt_text = Column(Text, nullable=False)
    description = Column(Text)
    type = Column(String(20), nullable=False)  # image, video, music, caption, script, text
    preview_image_url = Column(String(500))
    is_featured = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    use_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="prompts")
    category = relationship("PromptCategory", back_populates="prompts")
    tags = relationship("PromptTagRelation", back_populates="prompt")


class PromptTag(Base):
    """Prompt tag model"""
    __tablename__ = "prompt_tags"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    use_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prompts = relationship("PromptTagRelation", back_populates="tag")


class PromptTagRelation(Base):
    """Prompt-tag relationship"""
    __tablename__ = "prompt_tag_relations"
    
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("prompt_tags.id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    prompt = relationship("Prompt", back_populates="tags")
    tag = relationship("PromptTag", back_populates="prompts")


class PromptLike(Base):
    """Prompt like model"""
    __tablename__ = "prompt_likes"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class PromptSave(Base):
    """Prompt save model"""
    __tablename__ = "prompt_saves"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), primary_key=True)
    collection_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.utcnow)
