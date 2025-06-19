from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services.database import get_db
from services import character_service
from schemas.character import CharacterCreate, CharacterResponse, CharacterDeleteResponse

router = APIRouter(tags=["characters"])

@router.get(
    "/character/getAll",
    response_model=List[CharacterResponse],
    summary="Get all characters",
    description=(
        "Retrieves a list of all characters with their details including "
        "eye color as string"
    )
)
def get_all_characters(db: Session = Depends(get_db)):
    characters = character_service.get_all_characters(db)
    return characters

@router.get(
    "/character/get/{name}",
    response_model=List[CharacterResponse],
    summary="Get characters by name",
    description="Retrieves all characters that match the given name"
)
def get_character_by_name(name: str, db: Session = Depends(get_db)):
    characters = character_service.get_character_by_name(db, name)
    if not characters:
        raise HTTPException(
            status_code=404,
            detail="No characters found with this name"
        )
    return characters

@router.post(
    "/character/add",
    response_model=CharacterResponse,
    summary="Add a new character",
    description="Creates a new character with the provided details"
)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    try:
        return character_service.create_character(db, character.model_dump())
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/character/delete/{id}",
    response_model=CharacterDeleteResponse,
    summary="Delete a character",
    description="Deletes a character by their ID"
)
def delete_character(id: int, db: Session = Depends(get_db)):
    try:
        character_service.delete_character(db, id)
        return {"message": f"Character with id {id} successfully deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 