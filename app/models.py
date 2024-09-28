from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class TaskStatus(enum.Enum):
    """enum values class for TaskStatus."""
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class User(Base):
    """model class for User schema."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)  # Add length
    hashed_password = Column(String(255), nullable=False)  # Add length
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    """model class for Task schema."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)  # Add length
    description = Column(String(255), nullable=True)  # Add length
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO.value)
    priority = Column(String(10), nullable=True)  # Add length
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
