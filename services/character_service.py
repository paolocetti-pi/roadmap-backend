from sqlalchemy.orm import Session
from models.character import Character
from models.eye_color import EyeColor
from fastapi import HTTPException
from typing import List, Dict, Any
from .base_service import BaseService
import logging
from .redis_service import redis_service


class CharacterService(BaseService):
    """Service class for managing character operations"""
    
    def __init__(self):
        super().__init__(Character)
    
    def validate_data(self, data: dict) -> bool:
        """Validate character data before creating or updating"""
        logging.debug(f"Validating data for character: {data.get('name')}")
        required_fields = ["name", "height", "mass", "hair_color", "skin_color", "eye_color_id"]
        
        for field in required_fields:
            if field not in data or data[field] is None:
                logging.error(f"Validation failed: Missing field '{field}' for character {data.get('name')}")
                raise HTTPException(status_code=400, detail=f"Field '{field}' is required")
        
        # Validate numeric fields
        if not isinstance(data.get("height"), int) or data["height"] <= 0:
            logging.error(f"Validation failed: Invalid height for character {data.get('name')}")
            raise HTTPException(status_code=400, detail="Height must be a positive integer")
        
        if not isinstance(data.get("mass"), int) or data["mass"] <= 0:
            logging.error(f"Validation failed: Invalid mass for character {data.get('name')}")
            raise HTTPException(status_code=400, detail="Mass must be a positive integer")
        
        logging.debug(f"Data validation successful for character: {data.get('name')}")
        return True
    
    async def get_all_characters(self, db: Session) -> List[Dict[str, Any]]:
        """Get all characters with their details"""
        cache_key = "items:all"
        cached_characters = await redis_service.get(cache_key)
        if cached_characters is not None:
            return cached_characters

        characters = self.get_all(db)
        characters_dict = [char.to_dict() for char in characters]
        await redis_service.set(cache_key, characters_dict)
        return characters_dict
    
    async def get_character_by_name(self, db: Session, name: str) -> List[Dict[str, Any]]:
        """Get characters by name"""
        cache_key = f"items:name:{name}"
        cached_characters = await redis_service.get(cache_key)
        if cached_characters is not None:
            return cached_characters

        logging.info(f"Querying for characters with name: {name}")
        try:
            characters = db.query(Character).filter(Character.name == name).all()
            logging.info(f"Found {len(characters)} characters with name: {name}")
            characters_dict = [char.to_dict() for char in characters]
            await redis_service.set(cache_key, characters_dict)
            return characters_dict
        except Exception as e:
            logging.error(f"Error retrieving characters by name '{name}': {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving characters: {str(e)}")
    
    async def create_character(self, db: Session, character_data: dict) -> Character:
        """Create a new character with validation"""
        # Validate data
        self.validate_data(character_data)
        
        # Check if eye color exists
        logging.debug(f"Checking for eye color with id: {character_data['eye_color_id']}")
        eye_color = db.query(EyeColor).filter(
            EyeColor.id == character_data["eye_color_id"]
        ).first()
        if not eye_color:
            logging.error(f"Eye color with id {character_data['eye_color_id']} not found")
            raise HTTPException(status_code=400, detail="Eye color not found")
        
        logging.info(f"Creating character: {character_data['name']}")
        new_character = self.create(db, character_data)
        await redis_service.delete("items:all")
        return new_character
    
    async def delete_character(self, db: Session, character_id: int) -> bool:
        """Delete a character by ID"""
        character_to_delete = self.get_by_id(db, character_id)
        if not character_to_delete:
            raise HTTPException(status_code=404, detail="Character not found")

        logging.info(f"Deleting character with id: {character_id}")
        deleted = self.delete(db, character_id)
        if deleted:
            await redis_service.delete("items:all")
            await redis_service.delete(f"items:name:{character_to_delete.name}")
        return deleted
    
    async def update_character(self, db: Session, character_id: int, character_data: dict) -> Dict[str, Any]:
        """Update a character with validation"""
        # Validate data if provided
        if character_data:
            self.validate_data(character_data)
            
            # Check if eye color exists if provided
            if "eye_color_id" in character_data:
                logging.debug(f"Checking for eye color with id: {character_data['eye_color_id']}")
                eye_color = db.query(EyeColor).filter(
                    EyeColor.id == character_data["eye_color_id"]
                ).first()
                if not eye_color:
                    logging.error(f"Eye color with id {character_data['eye_color_id']} not found")
                    raise HTTPException(status_code=400, detail="Eye color not found")
        
        logging.info(f"Updating character with id: {character_id}")
        updated_character = self.update(db, character_id, character_data)
        if updated_character:
            await redis_service.delete("items:all")
            if "name" in updated_character:
                 await redis_service.delete(f"items:name:{updated_character['name']}")
        return updated_character
    
    def get_character_with_phrases(self, db: Session, character_id: int) -> Dict[str, Any]:
        """Get character with their key phrases"""
        logging.info(f"Getting character with phrases for id: {character_id}")
        character = db.query(Character).filter(Character.id == character_id).first()
        if not character:
            logging.warning(f"Character with id {character_id} not found for getting phrases")
            raise HTTPException(status_code=404, detail="Character not found")
        
        character_dict = character.to_dict()
        character_dict["key_phrases"] = character.get_key_phrases()
        logging.debug(f"Retrieved {len(character_dict['key_phrases'])} phrases for character id {character_id}")
        return character_dict
    
    def add_character_phrase(self, db: Session, character_id: int, phrase: str) -> Dict[str, Any]:
        """Add a key phrase to a character"""
        logging.info(f"Adding phrase to character id: {character_id}")
        character = db.query(Character).filter(Character.id == character_id).first()
        if not character:
            logging.warning(f"Character with id {character_id} not found for adding phrase")
            raise HTTPException(status_code=404, detail="Character not found")
        
        from models.key_phrase import KeyPhrase
        key_phrase = KeyPhrase(character_id=character_id, phrase=phrase)
        db.add(key_phrase)
        db.commit()
        db.refresh(key_phrase)
        logging.info(f"Phrase '{phrase}' added to character id {character_id}")
        return key_phrase.to_dict()

# Global character service instance
character_service = CharacterService() 