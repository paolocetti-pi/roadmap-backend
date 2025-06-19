from sqlalchemy.orm import Session
from models.character import Character
from models.eye_color import EyeColor
from fastapi import HTTPException
from typing import List, Dict, Any


def get_all_characters(db: Session) -> List[Dict[str, Any]]:
    characters = db.query(Character).all()
    return [
        {
            "id": char.id,
            "name": char.name,
            "height": char.height,
            "mass": char.mass,
            "hair_color": char.hair_color,
            "skin_color": char.skin_color,
            "eye_color_id": char.eye_color_id,
            "eye_color": char.eye_color.color if char.eye_color else None
        }
        for char in characters
    ]


def get_character_by_name(db: Session, name: str) -> List[Dict[str, Any]]:
    characters = db.query(Character).filter(Character.name == name).all()
    return [
        {
            "id": char.id,
            "name": char.name,
            "height": char.height,
            "mass": char.mass,
            "hair_color": char.hair_color,
            "skin_color": char.skin_color,
            "eye_color_id": char.eye_color_id,
            "eye_color": char.eye_color.color if char.eye_color else None
        }
        for char in characters
    ]


def create_character(db: Session, character_data: dict) -> Dict[str, Any]:
    # Check if eye color exists
    eye_color = db.query(EyeColor).filter(
        EyeColor.id == character_data["eye_color_id"]
    ).first()
    if not eye_color:
        raise HTTPException(status_code=400, detail="Eye color not found")

    db_character = Character(**character_data)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)

    return {
        "id": db_character.id,
        "name": db_character.name,
        "height": db_character.height,
        "mass": db_character.mass,
        "hair_color": db_character.hair_color,
        "skin_color": db_character.skin_color,
        "eye_color_id": db_character.eye_color_id,
        "eye_color": db_character.eye_color.color if db_character.eye_color else None
    }


def delete_character(db: Session, character_id: int) -> bool:
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=400, detail="Character not found")

    db.delete(character)
    db.commit()
    return True 