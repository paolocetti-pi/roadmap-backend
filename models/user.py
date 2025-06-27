from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class UserType(BaseModel):
    __tablename__ = "user_types"
    
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="user_type")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    user_type_id = Column(Integer, ForeignKey("user_types.id"), nullable=False)

    user_type = relationship("UserType", back_populates="users")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "user_type_id": self.user_type_id,
            "user_type": self.user_type.name if self.user_type else None
        } 