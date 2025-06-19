from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from services.auth import get_current_user, verify_admin
from services.tasks import (
    create_task,
    get_task,
    get_tasks,
    get_user_tasks,
    get_pending_tasks,
    get_completed_tasks,
    update_task,
    delete_task,
    update_task_status,
    add_task_comment,
    get_task_comments,
    get_task_status_history
)
from schemas.schemas import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskComment,
    TaskCommentCreate,
    TaskStatusHistory
)
from models.models import User, TaskStatus

router = APIRouter()

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin)
):
    """
    Create a new task. Only admin users can create tasks.
    """
    return create_task(db=db, task=task)

@router.get("/tasks", response_model=List[Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin)
):
    """
    Get all tasks. Only admin users can access this endpoint.
    """
    return get_tasks(db=db, skip=skip, limit=limit)

@router.get("/tasks/completed", response_model=List[Task])
async def read_completed_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin)
):
    """
    Get all completed tasks. Only admin users can access this endpoint.
    """
    return get_completed_tasks(db=db, skip=skip, limit=limit)

@router.get("/tasks/my-tasks", response_model=List[Task])
async def read_my_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks assigned to the current user.
    """
    return get_user_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/tasks/my-tasks/pending", response_model=List[Task])
async def read_my_pending_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all pending tasks assigned to the current user.
    """
    return get_pending_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID. Users can only access tasks assigned to them unless they are admin.
    """
    task = get_task(db=db, task_id=task_id)
    if task.assigned_user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task_info(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin)
):
    """
    Update a task's information. Only admin users can update tasks.
    """
    return update_task(db=db, task_id=task_id, task=task)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_info(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin)
):
    """
    Delete a task. Only admin users can delete tasks.
    """
    delete_task(db=db, task_id=task_id)
    return None

@router.put("/tasks/{task_id}/status/{new_status}", response_model=Task)
async def change_task_status(
    task_id: int,
    new_status: TaskStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change a task's status. Users can only change status of tasks assigned to them.
    """
    task = get_task(db=db, task_id=task_id)
    if task.assigned_user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return update_task_status(db=db, task_id=task_id, new_status=new_status)

@router.post("/tasks/{task_id}/comments", response_model=TaskComment)
async def add_comment_to_task(
    task_id: int,
    comment: TaskCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a comment to a task. Users can only comment on tasks assigned to them.
    """
    task = get_task(db=db, task_id=task_id)
    if task.assigned_user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return add_task_comment(db=db, task_id=task_id, comment=comment, user_id=current_user.id)

@router.get("/tasks/{task_id}/comments", response_model=List[TaskComment])
async def read_task_comments(
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all comments for a task. Users can only access comments of tasks assigned to them.
    """
    task = get_task(db=db, task_id=task_id)
    if task.assigned_user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return get_task_comments(db=db, task_id=task_id, skip=skip, limit=limit)

@router.get("/tasks/{task_id}/status-history", response_model=List[TaskStatusHistory])
async def read_task_status_history(
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin)
):
    """
    Get the status history of a task. Only admin users can access this endpoint.
    """
    return get_task_status_history(db=db, task_id=task_id, skip=skip, limit=limit) 