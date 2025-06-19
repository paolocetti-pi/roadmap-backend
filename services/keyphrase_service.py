import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from sqlalchemy.orm import Session
from models.key_phrase import KeyPhrase
from models.character import Character
from fastapi import HTTPException
from typing import List, Dict, Any
from .base_service import BaseService

load_dotenv()

AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")


class KeyphraseService(BaseService):
    """Service class for managing key phrase operations"""
    
    def __init__(self):
        super().__init__(KeyPhrase)
        self._azure_client = None
    
    @property
    def azure_client(self):
        """Lazy initialization of Azure client"""
        if self._azure_client is None and AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY:
            self._azure_client = TextAnalyticsClient(
                endpoint=AZURE_LANGUAGE_ENDPOINT,
                credential=AzureKeyCredential(AZURE_LANGUAGE_KEY)
            )
        return self._azure_client
    
    def extract_key_phrases_azure(self, text: str, language: str = "es") -> List[str]:
        """Extract key phrases from text using Azure Cognitive Services"""
        if not self.azure_client:
            raise HTTPException(status_code=500, detail="Azure Cognitive Services not configured")
        
        try:
            response = self.azure_client.extract_key_phrases([
                {"id": "1", "language": language, "text": text}
            ])
            result = response[0]
            if result.is_error:
                raise RuntimeError(
                    f"Azure error: {result.error.code} - {result.error.message}"
                )
            return result.key_phrases
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling Azure: {str(e)}")
    
    def get_keyphrases_by_character(self, db: Session, character_id: int) -> List[Dict[str, Any]]:
        """Get all key phrases for a specific character"""
        try:
            # Check if character exists
            character = db.query(Character).filter(Character.id == character_id).first()
            if not character:
                raise HTTPException(status_code=400, detail="Character not found")
            
            keyphrases = db.query(KeyPhrase).filter(KeyPhrase.character_id == character_id).all()
            return [keyphrase.to_dict() for keyphrase in keyphrases]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving key phrases: {str(e)}")
    
    def save_key_phrases_for_character(self, db: Session, character_id: int, phrases: List[str]) -> List[Dict[str, Any]]:
        """Save multiple key phrases for a character"""
        try:
            # Check if character exists
            character = db.query(Character).filter(Character.id == character_id).first()
            if not character:
                raise HTTPException(status_code=400, detail="Character not found")
            
            saved_phrases = []
            for phrase in phrases:
                keyphrase_data = {"character_id": character_id, "phrase": phrase}
                saved_phrase = self.create(db, keyphrase_data)
                saved_phrases.append(saved_phrase)
            
            return saved_phrases
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving key phrases: {str(e)}")

# Global keyphrase service instance
keyphrase_service = KeyphraseService()
