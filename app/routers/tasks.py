from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.dependencies import get_db, get_current_active_user
from app.repo.task_repo import create_task_db, get_tasks_for_user, get_task_by_id, update_task_db, delete_task_db
from app.models import User

router = APIRouter()

@router.post("/api/tasks")
def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
    ):
    """Create task endpoint"""
    return create_task_db(db=db, task=task, user_id=current_user.id)

@router.get("/api/tasks", response_model=List)
def get_tasks(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
    ):
    """Get tasks list endpoint"""
    return get_tasks_for_user(db=db, user_id=current_user.id)

@router.put("/api/tasks/{task_id}")
def update_task(
        task_id: int,
        task: TaskUpdate, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
    ):
    """Update task endpoint"""
    db_task = get_task_by_id(db=db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or you're not authorized to update this task")
    return update_task_db(db=db, task=db_task, task_update=task)

@router.delete("/api/tasks/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
    ):
    """Delete task endpoint"""
    db_task = get_task_by_id(db=db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or you're not authorized to delete this task")
    return delete_task_db(db=db, task_id=task_id)
