from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.eye_color import EyeColor
from fastapi import HTTPException
from typing import List, Dict, Any
from .base_service import BaseService
import logging


class EyeColorService(BaseService):
    """Service class for managing eye color operations"""
    
    def __init__(self):
        super().__init__(EyeColor)
    
    def validate_data(self, data: dict) -> bool:
        """Validate eye color data before creating or updating"""
        logging.debug(f"Validating data for eye color: {data.get('color')}")
        if "color" not in data or not data["color"]:
            logging.error("Validation failed: Missing color field")
            raise HTTPException(status_code=400, detail="Color field is required")
        
        if not isinstance(data["color"], str):
            logging.error("Validation failed: Color is not a string")
            raise HTTPException(status_code=400, detail="Color must be a string")
        
        if len(data["color"]) > 50:
            logging.error("Validation failed: Color is too long")
            raise HTTPException(status_code=400, detail="Color must be 50 characters or less")
        
        logging.debug(f"Data validation successful for eye color: {data.get('color')}")
        return True
    
    async def get_all_eye_colors(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """Get all eye colors"""
        logging.info("Getting all eye colors")
        return await self.get_all(db)
    
    async def get_eye_color_by_id(self, db: AsyncSession, eye_color_id: int) -> Dict[str, Any]:
        """Get eye color by ID"""
        logging.info(f"Getting eye color by id: {eye_color_id}")
        return await self.get_by_id(db, eye_color_id)
    
    async def create_eye_color(self, db: AsyncSession, eye_color_data: dict) -> Dict[str, Any]:
        """Create a new eye color with validation"""
        self.validate_data(eye_color_data)
        logging.info(f"Creating eye color: {eye_color_data.get('color')}")
        return await self.create(db, eye_color_data)
    
    async def update_eye_color(self, db: AsyncSession, eye_color_id: int, eye_color_data: dict) -> Dict[str, Any]:
        """Update an eye color with validation"""
        self.validate_data(eye_color_data)
        logging.info(f"Updating eye color with id: {eye_color_id}")
        return await self.update(db, eye_color_id, eye_color_data)
    
    async def delete_eye_color(self, db: AsyncSession, eye_color_id: int) -> bool:
        """Delete an eye color by ID"""
        logging.info(f"Deleting eye color with id: {eye_color_id}")
        return await self.delete(db, eye_color_id)
    
    async def get_eye_color_by_color(self, db: AsyncSession, color: str) -> Dict[str, Any]:
        """Get eye color by color name"""
        logging.info(f"Getting eye color by color: {color}")
        try:
            result = await db.execute(select(EyeColor).where(EyeColor.color == color))
            eye_color = result.scalars().first()
            if not eye_color:
                logging.warning(f"Eye color not found with color: {color}")
                raise HTTPException(status_code=404, detail="Eye color not found")
            return eye_color.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error retrieving eye color by color '{color}': {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving eye color: {str(e)}")

# Global eye color service instance
eye_color_service = EyeColorService() 