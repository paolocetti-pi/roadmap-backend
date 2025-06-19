from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class EyeColor(Base):
    __tablename__ = "eye_colors"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(50), unique=True, nullable=False)

    characters = relationship("Character", back_populates="eye_color")
