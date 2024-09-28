from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def get_tasks_for_user(db: Session, user_id: int):
    """Get Tasks list.
    """
    return db.query(Task).filter(Task.owner_id == user_id).all()

def create_task_db(db: Session, user_id: int, task: TaskCreate):
    """Crete new task"""
    db_task = Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_by_id(db: Session, task_id: int):
    """Get task by id"""
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_db(db: Session, task: Task, task_update: TaskUpdate):
    """Update the task by id"""
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task_db(db: Session, task_id: int):
    """Delete the task by id"""
    task = get_task_by_id(db, task_id)
    db.delete(task)
    db.commit()
    return task
