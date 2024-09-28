from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for User create model post."""
    username: str
    password: str

class UserOut(BaseModel):
    """Schema for User output model"""
    id: int
    username: str
    class Config:
        """configurations."""
        orm_mode = True

class TaskBase(BaseModel):
    """Base Schema model for Tasks"""
    title: str
    description: str
    status: str
    priority: str
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    """Response model for Task information."""
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        """configurations."""
        orm_mode = True
