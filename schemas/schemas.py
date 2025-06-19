from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models.models import UserRole, TaskStatus

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.USER

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    code: str
    title: str
    description: str
    due_date: datetime
    assigned_user_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_user_id: Optional[int] = None
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assigned_user: User

    class Config:
        from_attributes = True

# Task Comment schemas
class TaskCommentBase(BaseModel):
    comment: str

class TaskCommentCreate(TaskCommentBase):
    pass

class TaskComment(TaskCommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime
    user: User

    class Config:
        from_attributes = True

# Task Status History schemas
class TaskStatusHistoryBase(BaseModel):
    from_status: TaskStatus
    to_status: TaskStatus

class TaskStatusHistory(TaskStatusHistoryBase):
    id: int
    task_id: int
    changed_at: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 