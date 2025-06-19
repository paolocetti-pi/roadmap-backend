from sqlalchemy.orm import Session
from models.eye_color import EyeColor
from fastapi import HTTPException
from typing import List, Dict, Any
from .base_service import BaseService


class EyeColorService(BaseService):
    """Service class for managing eye color operations"""
    
    def __init__(self):
        super().__init__(EyeColor)
    
    def validate_data(self, data: dict) -> bool:
        """Validate eye color data before creating or updating"""
        if "color" not in data or not data["color"]:
            raise HTTPException(status_code=400, detail="Color field is required")
        
        if not isinstance(data["color"], str):
            raise HTTPException(status_code=400, detail="Color must be a string")
        
        if len(data["color"]) > 50:
            raise HTTPException(status_code=400, detail="Color must be 50 characters or less")
        
        return True
    
    def get_all_eye_colors(self, db: Session) -> List[Dict[str, Any]]:
        """Get all eye colors"""
        return self.get_all(db)
    
    def get_eye_color_by_id(self, db: Session, eye_color_id: int) -> Dict[str, Any]:
        """Get eye color by ID"""
        return self.get_by_id(db, eye_color_id)
    
    def create_eye_color(self, db: Session, eye_color_data: dict) -> Dict[str, Any]:
        """Create a new eye color with validation"""
        self.validate_data(eye_color_data)
        return self.create(db, eye_color_data)
    
    def update_eye_color(self, db: Session, eye_color_id: int, eye_color_data: dict) -> Dict[str, Any]:
        """Update an eye color with validation"""
        self.validate_data(eye_color_data)
        return self.update(db, eye_color_id, eye_color_data)
    
    def delete_eye_color(self, db: Session, eye_color_id: int) -> bool:
        """Delete an eye color by ID"""
        return self.delete(db, eye_color_id)
    
    def get_eye_color_by_color(self, db: Session, color: str) -> Dict[str, Any]:
        """Get eye color by color name"""
        try:
            eye_color = db.query(EyeColor).filter(EyeColor.color == color).first()
            if not eye_color:
                raise HTTPException(status_code=404, detail="Eye color not found")
            return eye_color.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving eye color: {str(e)}")

# Global eye color service instance
eye_color_service = EyeColorService() 