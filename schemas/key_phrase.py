from pydantic import BaseModel, Field
from typing import List, Optional


class KeyPhraseBase(BaseModel):
    phrase: str = Field(..., min_length=1, max_length=255, description="Key phrase text")
    character_id: int = Field(..., gt=0, description="ID of the character this phrase belongs to")


class KeyPhraseCreate(KeyPhraseBase):
    pass


class KeyPhraseUpdate(BaseModel):
    phrase: Optional[str] = Field(None, min_length=1, max_length=255, description="Key phrase text")
    character_id: Optional[int] = Field(None, gt=0, description="ID of the character this phrase belongs to")


class KeyPhraseResponse(KeyPhraseBase):
    id: int

    class Config:
        from_attributes = True


class KeyPhraseDeleteResponse(BaseModel):
    message: str


class CharacterKeyPhrasesOut(BaseModel):
    id_character: int
    key_phrases: List[str]