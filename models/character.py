from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Character(BaseModel):
    """Character model representing Star Wars characters"""
    __tablename__ = "characters"

    name = Column(String(100), index=True)
    height = Column(Integer)
    mass = Column(Integer)
    hair_color = Column(String(50))
    skin_color = Column(String(50))
    eye_color_id = Column(Integer, ForeignKey("eye_colors.id"))

    key_phrases = relationship("KeyPhrase", back_populates="character")
    eye_color = relationship("EyeColor", back_populates="characters")
    
    def to_dict(self) -> dict:
        """Convert character instance to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color_id": self.eye_color_id,
            "eye_color": self.eye_color.color if self.eye_color else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create character instance from dictionary"""
        return cls(
            name=data.get("name"),
            height=data.get("height"),
            mass=data.get("mass"),
            hair_color=data.get("hair_color"),
            skin_color=data.get("skin_color"),
            eye_color_id=data.get("eye_color_id")
        )
    
    def add_key_phrase(self, phrase: str):
        """Add a key phrase to the character"""
        from models.key_phrase import KeyPhrase
        key_phrase = KeyPhrase(character_id=self.id, phrase=phrase)
        return key_phrase
    
    def get_key_phrases(self):
        """Get all key phrases for the character"""
        return [kp.phrase for kp in self.key_phrases]
    
    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}')>" 