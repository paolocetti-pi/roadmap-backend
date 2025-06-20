from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services.database import get_db
from services.eye_color_service import eye_color_service
from schemas.eye_color import EyeColorCreate, EyeColorResponse
from .base_router import BaseRouter
from routes.user_routes import get_current_user, require_admin_user


class EyeColorRouter(BaseRouter):
    """Router class for eye color-related endpoints"""
    
    def __init__(self):
        super().__init__(prefix="/eye-color", tags=["eye-colors"])
    
    def setup_routes(self):
        """Setup all eye color routes"""
        self.router.add_api_route(
            "/getAll",
            self.get_all_eye_colors,
            methods=["GET"],
            response_model=List[EyeColorResponse],
            summary="Get all eye colors",
            description="Retrieves a list of all available eye colors",
            dependencies=[Depends(get_current_user)]
        )
        
        self.router.add_api_route(
            "/get/{id}",
            self.get_eye_color_by_id,
            methods=["GET"],
            response_model=EyeColorResponse,
            summary="Get eye color by ID",
            description="Retrieves a specific eye color by its ID",
            dependencies=[Depends(get_current_user)]
        )
        
        self.router.add_api_route(
            "/add",
            self.create_eye_color,
            methods=["POST"],
            response_model=EyeColorResponse,
            summary="Add a new eye color",
            description="Creates a new eye color with the provided details",
            dependencies=[Depends(require_admin_user)]
        )
        
        self.router.add_api_route(
            "/update/{id}",
            self.update_eye_color,
            methods=["PUT"],
            response_model=EyeColorResponse,
            summary="Update an eye color",
            description="Updates an existing eye color with the provided details",
            dependencies=[Depends(require_admin_user)]
        )
        
        self.router.add_api_route(
            "/delete/{id}",
            self.delete_eye_color,
            methods=["DELETE"],
            summary="Delete an eye color",
            description="Deletes an eye color by its ID",
            dependencies=[Depends(require_admin_user)]
        )
    
    def get_all_eye_colors(self, db: Session = Depends(get_db)):
        """Get all eye colors endpoint"""
        try:
            return eye_color_service.get_all_eye_colors(db)
        except Exception as e:
            raise self.handle_exception(e)
    
    def get_eye_color_by_id(self, id: int, db: Session = Depends(get_db)):
        """Get eye color by ID endpoint"""
        try:
            return eye_color_service.get_eye_color_by_id(db, id)
        except Exception as e:
            raise self.handle_exception(e)
    
    def create_eye_color(self, eye_color: EyeColorCreate, db: Session = Depends(get_db)):
        """Create eye color endpoint"""
        try:
            return eye_color_service.create_eye_color(db, eye_color.model_dump())
        except Exception as e:
            raise self.handle_exception(e)
    
    def update_eye_color(self, id: int, eye_color: EyeColorCreate, db: Session = Depends(get_db)):
        """Update eye color endpoint"""
        try:
            return eye_color_service.update_eye_color(db, id, eye_color.model_dump())
        except Exception as e:
            raise self.handle_exception(e)
    
    def delete_eye_color(self, id: int, db: Session = Depends(get_db)):
        """Delete eye color endpoint"""
        try:
            eye_color_service.delete_eye_color(db, id)
            return {"message": f"Eye color with id {id} successfully deleted"}
        except Exception as e:
            raise self.handle_exception(e)


# Global eye color router instance
eye_color_router = EyeColorRouter()
router = eye_color_router.get_router() 