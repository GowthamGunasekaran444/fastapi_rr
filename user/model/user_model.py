# app/user/models/user_model.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime
from core.db import Base

# --- SQLAlchemy ORM Model ---
class UserORM(Base):
    """SQLAlchemy ORM model for the Users table."""
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Integer, default=1, nullable=False) # 1 for active, 0 for deactive

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}')>"

# --- Pydantic Schemas ---
# These are used for request/response validation and serialization

class UserBase(BaseModel):
    """Base schema for User."""
    username: str = Field(..., example="john_doe")
    email: str = Field(..., example="john.doe@example.com")

class UserCreate(UserBase):
    """Schema for creating a new User."""
    user_id: str = Field(..., example="user_123")
    created_time: datetime = Field(default_factory=datetime.utcnow)

class User(UserCreate):
    """Full User schema, including active status."""
    is_active: int = Field(default=1, description="User status: 1 for active, 0 for deactive")

    class Config:
        # Enable Pydantic to read data from SQLAlchemy models
        from_attributes = True # Renamed from 'orm_mode' in Pydantic V2
