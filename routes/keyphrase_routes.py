from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from services.database import get_db
from services.keyphrase_service import (
    extract_key_phrases_azure,
    save_key_phrases,
    get_key_phrases_by_character
)
from models.character import Character
from schemas.key_phrase import CharacterKeyPhrasesOut

router = APIRouter(tags=["keyphrases"])


@router.get(
    "/keyphrases",
    response_model=list[str],
    summary="Extract key phrases from text using Azure"
)
def get_key_phrases(text: str = Query(..., description="Text to extract key phrases from")):
    try:
        return extract_key_phrases_azure(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/keyphrases/{character_id}",
    response_model=list[str],
    summary="Extract and save key phrases for a character"
)
def post_key_phrases(
    character_id: int,
    text: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=400, detail="Character not found")
    try:
        phrases = extract_key_phrases_azure(text)
        save_key_phrases(db, character_id, phrases)
        return phrases
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/keyphrases/{character_id}",
    response_model=CharacterKeyPhrasesOut,
    summary="Get key phrases for a character"
)
def get_character_key_phrases(character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=400, detail="Character not found")
    phrases = get_key_phrases_by_character(db, character_id)
    return {
        "id_character": character_id,
        "key_phrases": [p.phrase for p in phrases]
    }