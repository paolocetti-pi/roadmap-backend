from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import BaseModel


class EyeColor(BaseModel):
    """Eye color model representing different eye colors for characters"""
    __tablename__ = "eye_colors"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(50), unique=True, nullable=False)

    characters = relationship("Character", back_populates="eye_color")
    
    def to_dict(self) -> dict:
        """Convert eye color instance to dictionary"""
        return {
            "id": self.id,
            "color": self.color
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create eye color instance from dictionary"""
        return cls(
            color=data.get("color")
        )
    
    def __repr__(self):
        return f"<EyeColor(id={self.id}, color='{self.color}')>"
