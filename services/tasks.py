from sqlalchemy.orm import Session
from models.models import Task, TaskStatus, TaskComment, TaskStatusHistory
from schemas.schemas import TaskCreate, TaskUpdate, TaskCommentCreate
from fastapi import HTTPException, status
from datetime import datetime

def get_task(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

def get_task_by_code(db: Session, code: str) -> Task:
    task = db.query(Task).filter(Task.code == code).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    return db.query(Task).offset(skip).limit(limit).all()

def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
    return db.query(Task).filter(Task.assigned_user_id == user_id).offset(skip).limit(limit).all()

def get_pending_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
    return db.query(Task).filter(
        Task.assigned_user_id == user_id,
        Task.status == TaskStatus.PENDING
    ).offset(skip).limit(limit).all()

def get_completed_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    return db.query(Task).filter(Task.status == TaskStatus.COMPLETED).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate) -> Task:
    # Check if task code already exists
    if db.query(Task).filter(Task.code == task.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task code already exists"
        )
    
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate) -> Task:
    db_task = get_task(db, task_id)
    
    # Update task fields if provided
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> None:
    db_task = get_task(db, task_id)
    db.delete(db_task)
    db.commit()

def update_task_status(db: Session, task_id: int, new_status: TaskStatus) -> Task:
    db_task = get_task(db, task_id)
    
    # Create status history record
    status_history = TaskStatusHistory(
        task_id=task_id,
        from_status=db_task.status,
        to_status=new_status
    )
    db.add(status_history)
    
    # Update task status
    db_task.status = new_status
    db.commit()
    db.refresh(db_task)
    return db_task

def add_task_comment(db: Session, task_id: int, comment: TaskCommentCreate, user_id: int) -> TaskComment:
    # Verify task exists
    get_task(db, task_id)
    
    db_comment = TaskComment(
        task_id=task_id,
        user_id=user_id,
        comment=comment.comment
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_task_comments(db: Session, task_id: int, skip: int = 0, limit: int = 100) -> list[TaskComment]:
    # Verify task exists
    get_task(db, task_id)
    
    return db.query(TaskComment).filter(
        TaskComment.task_id == task_id
    ).offset(skip).limit(limit).all()

def get_task_status_history(db: Session, task_id: int, skip: int = 0, limit: int = 100) -> list[TaskStatusHistory]:
    # Verify task exists
    get_task(db, task_id)
    
    return db.query(TaskStatusHistory).filter(
        TaskStatusHistory.task_id == task_id
    ).offset(skip).limit(limit).all() 