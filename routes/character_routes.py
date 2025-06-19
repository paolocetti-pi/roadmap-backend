from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from services.database import get_db
from services.character_service import character_service
from schemas.character import CharacterCreate, CharacterResponse, CharacterDeleteResponse
from .base_router import BaseRouter


class CharacterRouter(BaseRouter):
    """Router class for character-related endpoints"""
    
    def __init__(self):
        super().__init__(prefix="/character", tags=["characters"])
    
    def setup_routes(self):
        """Setup all character routes"""
        self.router.add_api_route(
            "/getAll",
            self.get_all_characters,
            methods=["GET"],
            response_model=List[CharacterResponse],
            summary="Get all characters",
            description="Retrieves a list of all characters with their details including eye color as string"
        )
        
        self.router.add_api_route(
            "/get/{name}",
            self.get_character_by_name,
            methods=["GET"],
            response_model=List[CharacterResponse],
            summary="Get characters by name",
            description="Retrieves all characters that match the given name"
        )
        
        self.router.add_api_route(
            "/add",
            self.create_character,
            methods=["POST"],
            response_model=CharacterResponse,
            summary="Add a new character",
            description="Creates a new character with the provided details"
        )
        
        self.router.add_api_route(
            "/delete/{id}",
            self.delete_character,
            methods=["DELETE"],
            response_model=CharacterDeleteResponse,
            summary="Delete a character",
            description="Deletes a character by their ID"
        )
        
        self.router.add_api_route(
            "/update/{id}",
            self.update_character,
            methods=["PUT"],
            response_model=CharacterResponse,
            summary="Update a character",
            description="Updates an existing character with the provided details"
        )
        
        self.router.add_api_route(
            "/{id}/phrases",
            self.get_character_with_phrases,
            methods=["GET"],
            summary="Get character with phrases",
            description="Retrieves a character with all their key phrases"
        )
    
    def get_all_characters(self, db: Session = Depends(get_db)):
        """Get all characters endpoint"""
        try:
            characters = character_service.get_all_characters(db)
            return characters
        except Exception as e:
            raise self.handle_exception(e)
    
    def get_character_by_name(self, name: str, db: Session = Depends(get_db)):
        """Get characters by name endpoint"""
        try:
            characters = character_service.get_character_by_name(db, name)
            if not characters:
                raise HTTPException(
                    status_code=404,
                    detail="No characters found with this name"
                )
            return characters
        except Exception as e:
            raise self.handle_exception(e)
    
    def create_character(self, character: CharacterCreate, db: Session = Depends(get_db)):
        """Create character endpoint"""
        try:
            return character_service.create_character(db, character.model_dump())
        except Exception as e:
            raise self.handle_exception(e)
    
    def delete_character(self, id: int, db: Session = Depends(get_db)):
        """Delete character endpoint"""
        try:
            character_service.delete_character(db, id)
            return {"message": f"Character with id {id} successfully deleted"}
        except Exception as e:
            raise self.handle_exception(e)
    
    def update_character(self, id: int, character: CharacterCreate, db: Session = Depends(get_db)):
        """Update character endpoint"""
        try:
            return character_service.update_character(db, id, character.model_dump())
        except Exception as e:
            raise self.handle_exception(e)
    
    def get_character_with_phrases(self, id: int, db: Session = Depends(get_db)):
        """Get character with phrases endpoint"""
        try:
            return character_service.get_character_with_phrases(db, id)
        except Exception as e:
            raise self.handle_exception(e)


# Global character router instance
character_router = CharacterRouter()
router = character_router.get_router() 