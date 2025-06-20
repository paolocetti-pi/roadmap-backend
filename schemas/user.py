from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: constr(min_length=6)
    user_type_id: int

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    user_type: UserTypeSchema

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenDataSchema(BaseModel):
    user_id: Optional[int] = None
    user_type: Optional[str] = None 