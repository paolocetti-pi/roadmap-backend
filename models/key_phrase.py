# models/key_phrase.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class KeyPhrase(Base):
    __tablename__ = "key_phrases"
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    phrase = Column(String(255), nullable=False)

    character = relationship("Character", back_populates="key_phrases")