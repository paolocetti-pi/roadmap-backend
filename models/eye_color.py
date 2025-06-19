from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class EyeColor(Base):
    __tablename__ = "eye_colors"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(50), unique=True, index=True)
    
    characters = relationship("Character", back_populates="eye_color")
