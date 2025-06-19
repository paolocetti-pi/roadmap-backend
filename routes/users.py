from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from services.auth import get_current_user, verify_admin
from services.users import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user
)
from schemas.schemas import User, UserCreate, UserUpdate
from models.models import User as UserModel

router = APIRouter()

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Create a new user. Only admin users can create new users.
    """
    return create_user(db=db, user=user)

@router.get("/users", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Get all users. Only admin users can access this endpoint.
    """
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get a specific user by ID. Users can only access their own information unless they are admin.
    """
    if current_user.id != user_id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return get_user(db=db, user_id=user_id)

@router.put("/users/{user_id}", response_model=User)
async def update_user_info(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Update a user's information. Users can only update their own information unless they are admin.
    """
    if current_user.id != user_id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return update_user(db=db, user_id=user_id, user=user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_info(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Delete a user. Only admin users can delete users.
    """
    delete_user(db=db, user_id=user_id)
    return None 