from pydantic import BaseModel, Field
from typing import Optional


class EyeColorBase(BaseModel):
    color: str = Field(..., min_length=1, max_length=50, description="Eye color name")


class EyeColorCreate(EyeColorBase):
    pass


class EyeColorUpdate(BaseModel):
    color: Optional[str] = Field(None, min_length=1, max_length=50, description="Eye color name")


class EyeColorResponse(EyeColorBase):
    id: int

    class Config:
        from_attributes = True


class EyeColorDeleteResponse(BaseModel):
    message: str 