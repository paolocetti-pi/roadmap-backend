from sqlalchemy.orm import Session
from models.eye_color import EyeColor
from typing import List

def init_eye_colors(db: Session):
    # Check if eye colors already exist
    if db.query(EyeColor).first():
        return
    
    eye_colors = [
        {"id": 1, "color": "blue"},
        {"id": 2, "color": "brown"},
        {"id": 3, "color": "green"},
        {"id": 4, "color": "hazel"},
        {"id": 5, "color": "gray"},
        {"id": 6, "color": "amber"},
        {"id": 7, "color": "red"},
        {"id": 8, "color": "violet"}
    ]
    
    for eye_color in eye_colors:
        db_eye_color = EyeColor(**eye_color)
        db.add(db_eye_color)
    
    db.commit()

def get_all_eye_colors(db: Session) -> List[EyeColor]:
    return db.query(EyeColor).all() 