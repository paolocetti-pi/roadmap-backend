from sqlalchemy.orm import Session
from models.character import Character
from models.eye_color import EyeColor
from fastapi import HTTPException
from typing import List, Dict, Any
from .base_service import BaseService


class CharacterService(BaseService):
    """Service class for managing character operations"""
    
    def __init__(self):
        super().__init__(Character)
    
    def validate_data(self, data: dict) -> bool:
        """Validate character data before creating or updating"""
        required_fields = ["name", "height", "mass", "hair_color", "skin_color", "eye_color_id"]
        
        for field in required_fields:
            if field not in data or data[field] is None:
                raise HTTPException(status_code=400, detail=f"Field '{field}' is required")
        
        # Validate numeric fields
        if not isinstance(data.get("height"), int) or data["height"] <= 0:
            raise HTTPException(status_code=400, detail="Height must be a positive integer")
        
        if not isinstance(data.get("mass"), int) or data["mass"] <= 0:
            raise HTTPException(status_code=400, detail="Mass must be a positive integer")
        
        return True
    
    def get_all_characters(self, db: Session) -> List[Dict[str, Any]]:
        """Get all characters with their details"""
        return self.get_all(db)
    
    def get_character_by_name(self, db: Session, name: str) -> List[Dict[str, Any]]:
        """Get characters by name"""
        try:
            characters = db.query(Character).filter(Character.name == name).all()
            return [character.to_dict() for character in characters]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving characters: {str(e)}")
    
    def create_character(self, db: Session, character_data: dict) -> Dict[str, Any]:
        """Create a new character with validation"""
        # Validate data
        self.validate_data(character_data)
        
        # Check if eye color exists
        eye_color = db.query(EyeColor).filter(
            EyeColor.id == character_data["eye_color_id"]
        ).first()
        if not eye_color:
            raise HTTPException(status_code=400, detail="Eye color not found")
        
        return self.create(db, character_data)
    
    def delete_character(self, db: Session, character_id: int) -> bool:
        """Delete a character by ID"""
        return self.delete(db, character_id)
    
    def update_character(self, db: Session, character_id: int, character_data: dict) -> Dict[str, Any]:
        """Update a character with validation"""
        # Validate data if provided
        if character_data:
            self.validate_data(character_data)
            
            # Check if eye color exists if provided
            if "eye_color_id" in character_data:
                eye_color = db.query(EyeColor).filter(
                    EyeColor.id == character_data["eye_color_id"]
                ).first()
                if not eye_color:
                    raise HTTPException(status_code=400, detail="Eye color not found")
        
        return self.update(db, character_id, character_data)
    
    def get_character_with_phrases(self, db: Session, character_id: int) -> Dict[str, Any]:
        """Get character with their key phrases"""
        character = db.query(Character).filter(Character.id == character_id).first()
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        character_dict = character.to_dict()
        character_dict["key_phrases"] = character.get_key_phrases()
        return character_dict
    
    def add_character_phrase(self, db: Session, character_id: int, phrase: str) -> Dict[str, Any]:
        """Add a key phrase to a character"""
        character = db.query(Character).filter(Character.id == character_id).first()
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        from models.key_phrase import KeyPhrase
        key_phrase = KeyPhrase(character_id=character_id, phrase=phrase)
        db.add(key_phrase)
        db.commit()
        db.refresh(key_phrase)
        
        return key_phrase.to_dict()

# Global character service instance
character_service = CharacterService() 