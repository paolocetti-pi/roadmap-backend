from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from services.database import get_db
from services import eye_color_service
from schemas.eye_color import EyeColorResponse

router = APIRouter()

@router.get("/eye-colors", response_model=List[EyeColorResponse],
    summary="Get all eye colors",
    description="Retrieves a list of all available eye colors")
def get_all_eye_colors(db: Session = Depends(get_db)):
    return eye_color_service.get_all_eye_colors(db) 