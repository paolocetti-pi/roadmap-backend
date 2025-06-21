from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any, Union
from models.eye_color import EyeColor


class CharacterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Character name")
    height: int = Field(..., description="Character height in cm")
    mass: int = Field(..., description="Character mass in kg")
    hair_color: str = Field(..., min_length=1, max_length=50, description="Character hair color")
    skin_color: str = Field(..., min_length=1, max_length=50, description="Character skin color")
    eye_color_id: int = Field(..., gt=0, description="ID of the eye color")


class CharacterCreate(CharacterBase):
    pass


class CharacterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Character name")
    height: Optional[int] = Field(None, description="Character height in cm")
    mass: Optional[int] = Field(None, description="Character mass in kg")
    hair_color: Optional[str] = Field(None, min_length=1, max_length=50, description="Character hair color")
    skin_color: Optional[str] = Field(None, min_length=1, max_length=50, description="Character skin color")
    eye_color_id: Optional[int] = Field(None, gt=0, description="ID of the eye color")


class CharacterResponse(CharacterBase):
    id: Union[int, str]
    eye_color: Optional[str] = None

    @field_validator('eye_color', mode='before')
    @classmethod
    def validate_eye_color(cls, v: Any) -> Optional[str]:
        if isinstance(v, EyeColor):
            return v.color
        return v

    class Config:
        from_attributes = True


class CharacterWithPhrasesResponse(CharacterResponse):
    key_phrases: List[str] = []


class CharacterDeleteResponse(BaseModel):
    message: str 