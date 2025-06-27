from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
import os
from services.database import get_db
from services.character_service import character_service
from services.cosmos_character_service import CosmosCharacterService
from services.cosmos_service import get_cosmos_container
from schemas.character import CharacterCreate, CharacterResponse, CharacterDeleteResponse
from .base_router import BaseRouter
from routes.user_routes import get_current_user, require_admin_user
import logging

def get_character_service():
    """Dependency to provide the correct character service based on DB_TYPE env var."""
    db_type = os.getenv("DB_TYPE", "sql")
    if db_type == "cosmos":
        container = get_cosmos_container()
        return CosmosCharacterService(container)
    else:
        return character_service

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
            description="Retrieves a list of all characters with their details including eye color as string",
            dependencies=[Depends(get_current_user)]
        )
        
        self.router.add_api_route(
            "/get/{name}",
            self.get_character_by_name,
            methods=["GET"],
            response_model=List[CharacterResponse],
            summary="Get characters by name",
            description="Retrieves all characters that match the given name",
            dependencies=[Depends(get_current_user)]
        )
        
        self.router.add_api_route(
            "/add",
            self.create_character,
            methods=["POST"],
            response_model=CharacterResponse,
            status_code=201,
            summary="Add a new character",
            description="Creates a new character with the provided details",
            dependencies=[Depends(require_admin_user)]
        )
        
        self.router.add_api_route(
            "/delete/{id}",
            self.delete_character,
            methods=["DELETE"],
            response_model=CharacterDeleteResponse,
            summary="Delete a character",
            description="Deletes a character by their ID",
            dependencies=[Depends(require_admin_user)]
        )
        
        self.router.add_api_route(
            "/update/{id}",
            self.update_character,
            methods=["PUT"],
            response_model=CharacterResponse,
            summary="Update a character",
            description="Updates an existing character with the provided details",
            dependencies=[Depends(require_admin_user)]
        )
        
        self.router.add_api_route(
            "/{id}/phrases",
            self.get_character_with_phrases,
            methods=["GET"],
            summary="Get character with phrases (SQL Only)",
            description="Retrieves a character with all their key phrases. This endpoint only works with the SQL database.",
            dependencies=[Depends(get_current_user)]
        )
    
    async def get_all_characters(self, service = Depends(get_character_service), db: AsyncSession = Depends(get_db)):
        """Get all characters endpoint"""
        logging.info("Getting all characters")
        try:
            if isinstance(service, CosmosCharacterService):
                characters = await service.get_all_characters()
            else:
                characters = await service.get_all_characters(db)
            logging.debug(f"{len(characters)} characters found")
            return characters
        except Exception as e:
            logging.error(f"Error getting all characters: {e}")
            raise self.handle_exception(e)
    
    async def get_character_by_name(self, name: str, service = Depends(get_character_service), db: AsyncSession = Depends(get_db)):
        """Get characters by name endpoint"""
        logging.info(f"Getting characters by name: {name}")
        try:
            if isinstance(service, CosmosCharacterService):
                characters = await service.get_character_by_name(name)
            else:
                characters = await service.get_character_by_name(db, name)

            if not characters:
                logging.warning(f"No characters found with name: {name}")
                raise HTTPException(
                    status_code=404,
                    detail="No characters found with this name"
                )
            logging.debug(f"{len(characters)} characters found with name: {name}")
            return characters
        except Exception as e:
            logging.error(f"Error getting characters by name '{name}': {e}")
            raise self.handle_exception(e)
    
    async def create_character(self, character: CharacterCreate, service = Depends(get_character_service), db: AsyncSession = Depends(get_db)):
        """Create character endpoint"""
        logging.info(f"Creating character: {character.name}")
        try:
            if isinstance(service, CosmosCharacterService):
                new_char = await service.create_character(character.model_dump())
            else:
                new_char = await service.create_character(db, character.model_dump())
            logging.info(f"Character '{character.name}' created successfully.")
            return new_char
        except Exception as e:
            logging.error(f"Error creating character '{character.name}': {e}")
            raise self.handle_exception(e)
    
    async def delete_character(self, id: Union[int, str], service = Depends(get_character_service), db: AsyncSession = Depends(get_db)):
        """Delete character endpoint"""
        logging.info(f"Deleting character with id: {id}")
        try:
            if isinstance(service, CosmosCharacterService):
                if not isinstance(id, str):
                    raise HTTPException(status_code=400, detail="For CosmosDB, character ID must be a string.")
                await service.delete_character(id)
            else:
                if not isinstance(id, int):
                    raise HTTPException(status_code=400, detail="For SQL, character ID must be an integer.")
                await service.delete_character(db, id)
            
            logging.info(f"Character with id {id} successfully deleted")
            return {"message": f"Character with id {id} successfully deleted"}
        except Exception as e:
            logging.error(f"Error deleting character with id {id}: {e}")
            raise self.handle_exception(e)
    
    async def update_character(self, id: Union[int, str], character: CharacterCreate, service = Depends(get_character_service), db: AsyncSession = Depends(get_db)):
        """Update character endpoint"""
        logging.info(f"Updating character with id: {id}")
        try:
            if isinstance(service, CosmosCharacterService):
                if not isinstance(id, str):
                    raise HTTPException(status_code=400, detail="For CosmosDB, character ID must be a string.")
                updated_char = await service.update_character(id, character.model_dump())
            else:
                if not isinstance(id, int):
                    raise HTTPException(status_code=400, detail="For SQL, character ID must be an integer.")
                updated_char = await service.update_character(db, id, character.model_dump())
            
            logging.info(f"Character with id {id} updated successfully")
            return updated_char
        except Exception as e:
            logging.error(f"Error updating character with id {id}: {e}")
            raise self.handle_exception(e)
    
    async def get_character_with_phrases(self, id: int, db: AsyncSession = Depends(get_db)):
        """Get character with phrases endpoint"""
        db_type = os.getenv("DB_TYPE", "sql")
        if db_type == "cosmos":
            raise HTTPException(status_code=400, detail="Phrases are not supported for CosmosDB.")

        logging.info(f"Getting character with phrases for id: {id}")
        try:
            char_with_phrases = await character_service.get_character_with_phrases(db, id)
            logging.debug(f"Character with id {id} and their phrases retrieved")
            return char_with_phrases
        except Exception as e:
            logging.error(f"Error getting character with phrases for id {id}: {e}")
            raise self.handle_exception(e)


# Global character router instance
character_router = CharacterRouter()
router = character_router.get_router() 