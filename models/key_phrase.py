# models/key_phrase.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class KeyPhrase(BaseModel):
    """Key phrase model representing memorable phrases for characters"""
    __tablename__ = "key_phrases"
    
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    phrase = Column(String(255), nullable=False)

    character = relationship("Character", back_populates="key_phrases")
    
    def to_dict(self) -> dict:
        """Convert key phrase instance to dictionary"""
        return {
            "id": self.id,
            "character_id": self.character_id,
            "phrase": self.phrase
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create key phrase instance from dictionary"""
        return cls(
            character_id=data.get("character_id"),
            phrase=data.get("phrase")
        )
    
    def __repr__(self):
        return f"<KeyPhrase(id={self.id}, character_id={self.character_id}, phrase='{self.phrase[:20]}...')>"