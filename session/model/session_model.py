# app/session/models/session_model.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

# --- SQLAlchemy ORM Model ---
class SessionORM(Base):
    """SQLAlchemy ORM model for the Sessions table."""
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    session_name = Column(String, nullable=False) # New field
    login_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    active_status = Column(Integer, default=1, nullable=False) # 1 for active, 0 for inactive

    # Define relationship to User
    user = relationship("UserORM")

    def __repr__(self):
        return f"<Session(session_id='{self.session_id}', session_name='{self.session_name}')>"

# --- Pydantic Schemas ---
class SessionBase(BaseModel):
    """Base schema for Session."""
    user_id: str = Field(..., example="user_123")
    session_name: str = Field(..., example="My First Chat Session") # New field

class SessionCreate(SessionBase):
    """Schema for creating a new Session."""
    session_id: str = Field(..., example="session_abc")
    login_time: datetime = Field(default_factory=datetime.utcnow, alias="created_time") # Map created_time to login_time

class SessionRename(BaseModel):
    """Schema for renaming a session."""
    new_session_name: str = Field(..., example="Renamed Chat Session")

class Session(SessionCreate):
    """Full Session schema, including active status and logout time."""
    logout_time: Optional[datetime] = None
    active_status: int = Field(default=1, description="Session status: 1 for active, 0 for inactive")

    class Config:
        # Enable Pydantic to read data from SQLAlchemy models
        from_attributes = True # Renamed from 'orm_mode' in Pydantic V2
        # Allow population by field name or alias for 'created_time'
        validate_by_name = True # Renamed from 'allow_population_by_field_name' in Pydantic V2
