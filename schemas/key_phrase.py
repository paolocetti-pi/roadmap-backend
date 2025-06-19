from pydantic import BaseModel
from typing import List

class KeyPhraseBase(BaseModel):
    phrase: str

class KeyPhraseCreate(KeyPhraseBase):
    pass

class KeyPhraseOut(KeyPhraseBase):
    id: int

    class Config:
        orm_mode = True

class CharacterKeyPhrasesOut(BaseModel):
    id_character: int
    key_phrases: List[str]