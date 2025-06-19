from pydantic import BaseModel, Field
from typing import Optional


class CharacterBase(BaseModel):
    name: str
    height: int
    mass: int
    hair_color: str
    skin_color: str
    eye_color_id: int


class CharacterCreate(CharacterBase):
    pass


class CharacterResponse(CharacterBase):
    id: int
    eye_color: str

    class Config:
        from_attributes = True


class CharacterDeleteResponse(BaseModel):
    message: str 