from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List
from services.database import get_db
from services.keyphrase_service import keyphrase_service
from .base_router import BaseRouter


class KeyphraseRouter(BaseRouter):
    """Router class for key phrase-related endpoints"""
    
    def __init__(self):
        super().__init__(prefix="/keyphrases", tags=["keyphrases"])
    
    def setup_routes(self):
        """Setup all key phrase routes"""
        # Extract key phrases from text
        self.router.add_api_route(
            "/",
            self.extract_key_phrases,
            methods=["GET"],
            response_model=List[str],
            summary="Extract key phrases from text",
            description="Extract key phrases from text using Azure Cognitive Services"
        )
        
        # Extract and save key phrases for a character
        self.router.add_api_route(
            "/{character_id}",
            self.extract_and_save_phrases,
            methods=["POST"],
            response_model=List[str],
            summary="Extract and save key phrases for character",
            description="Extract key phrases from text and save them for a character"
        )
        
        # Get key phrases for a character
        self.router.add_api_route(
            "/{character_id}",
            self.get_character_phrases,
            methods=["GET"],
            response_model=List[str],
            summary="Get key phrases for character",
            description="Get all key phrases for a specific character"
        )
    
    def extract_key_phrases(self, text: str = Query(..., description="Text to extract key phrases from")):
        """Extract key phrases from text endpoint"""
        try:
            return keyphrase_service.extract_key_phrases_azure(text)
        except Exception as e:
            raise self.handle_exception(e)
    
    def extract_and_save_phrases(self, character_id: int, text: str = Body(..., embed=True), db: Session = Depends(get_db)):
        """Extract and save key phrases for character endpoint"""
        try:
            phrases = keyphrase_service.extract_key_phrases_azure(text)
            keyphrase_service.save_key_phrases_for_character(db, character_id, phrases)
            return phrases
        except Exception as e:
            raise self.handle_exception(e)
    
    def get_character_phrases(self, character_id: int, db: Session = Depends(get_db)):
        """Get key phrases for character endpoint"""
        try:
            keyphrases = keyphrase_service.get_keyphrases_by_character(db, character_id)
            return [kp["phrase"] for kp in keyphrases]
        except Exception as e:
            raise self.handle_exception(e)


# Global keyphrase router instance
keyphrase_router = KeyphraseRouter()
router = keyphrase_router.get_router()