"""
Analytics and notification SQLAlchemy models
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from ..database import Base


class GenerationJob(Base):
    """AI generation job model"""
    __tablename__ = "generation_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String(20), nullable=False)  # image, video, music, caption, script
    prompt_text = Column(Text, nullable=False)
    settings = Column(JSONB)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    progress_percent = Column(Integer, default=0)
    result_content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="SET NULL"))
    credits_used = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class CreditTransaction(Base):
    """Credit transaction model"""
    __tablename__ = "credit_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)  # purchase, usage, bonus, refund
    description = Column(String(255))
    job_id = Column(UUID(as_uuid=True), ForeignKey("generation_jobs.id", ondelete="SET NULL"))
    balance_after = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrendingContent(Base):
    """Trending content model"""
    __tablename__ = "trending_content"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"))
    rank_position = Column(Integer, nullable=False)
    period = Column(String(20), nullable=False)  # daily, weekly, monthly, all_time
    score = Column(Numeric(10, 2), nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)


class TrendingHashtag(Base):
    """Trending hashtag model"""
    __tablename__ = "trending_hashtags"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("prompt_tags.id", ondelete="CASCADE"))
    rank_position = Column(Integer, nullable=False)
    period = Column(String(20), nullable=False)  # daily, weekly, monthly
    mention_count = Column(Integer, default=0)
    is_hot = Column(Boolean, default=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)


class UserAnalytics(Base):
    """User analytics model"""
    __tablename__ = "user_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    new_followers = Column(Integer, default=0)
    profile_views = Column(Integer, default=0)


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text)
    data = Column(JSONB)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
