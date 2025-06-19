from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    """Base model class with common functionality for all models"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary - to be overridden by subclasses"""
        return {
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create model instance from dictionary - to be overridden by subclasses"""
        return cls()
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>" 