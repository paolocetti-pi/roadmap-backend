import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics.aio import TextAnalyticsClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.key_phrase import KeyPhrase
from models.character import Character
from fastapi import HTTPException
from typing import List, Dict, Any
from .base_service import BaseService
import logging

load_dotenv()

AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")


class KeyphraseService(BaseService):
    """Service class for managing key phrase operations"""
    
    def __init__(self):
        super().__init__(KeyPhrase)
        self._azure_client = None
    
    async def get_azure_client(self):
        """Lazy initialization of Azure client"""
        if self._azure_client is None:
            if AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY:
                logging.info("Initializing Azure Text Analytics client")
                self._azure_client = TextAnalyticsClient(
                    endpoint=AZURE_LANGUAGE_ENDPOINT,
                    credential=AzureKeyCredential(AZURE_LANGUAGE_KEY)
                )
            else:
                logging.error("Azure Cognitive Services not configured. Check environment variables.")
                raise HTTPException(status_code=500, detail="Azure Cognitive Services not configured")
        return self._azure_client
    
    async def extract_key_phrases_azure(self, text: str, language: str = "es") -> List[str]:
        """Extract key phrases from text using Azure Cognitive Services"""
        azure_client = await self.get_azure_client()
        if not azure_client:
            raise HTTPException(status_code=500, detail="Azure Cognitive Services not configured")

        try:
            logging.info("Extracting key phrases using Azure Cognitive Services")
            response = await azure_client.extract_key_phrases([
                {"id": "1", "language": language, "text": text}
            ])
            result = response[0]
            if result.is_error:
                logging.error(f"Azure error: {result.error.code} - {result.error.message}")
                raise RuntimeError(
                    f"Azure error: {result.error.code} - {result.error.message}"
                )
            logging.info(f"Extracted {len(result.key_phrases)} key phrases")
            return result.key_phrases
        except Exception as e:
            logging.error(f"Error calling Azure for key phrase extraction: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error calling Azure: {str(e)}")
    
    async def get_keyphrases_by_character(self, db: AsyncSession, character_id: int) -> List[Dict[str, Any]]:
        """Get all key phrases for a specific character"""
        try:
            # Check if character exists
            logging.info(f"Getting keyphrases for character_id: {character_id}")
            result = await db.execute(select(Character).where(Character.id == character_id))
            character = result.scalars().first()
            if not character:
                logging.warning(f"Character not found with id: {character_id}")
                raise HTTPException(status_code=400, detail="Character not found")
            
            result = await db.execute(select(KeyPhrase).where(KeyPhrase.character_id == character_id))
            keyphrases = result.scalars().all()
            logging.info(f"Found {len(keyphrases)} keyphrases for character_id: {character_id}")
            return [keyphrase.to_dict() for keyphrase in keyphrases]
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error retrieving key phrases for character_id {character_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving key phrases: {str(e)}")
    
    async def save_key_phrases_for_character(self, db: AsyncSession, character_id: int, phrases: List[str]) -> List[Dict[str, Any]]:
        """Save multiple key phrases for a character"""
        try:
            # Check if character exists
            logging.info(f"Saving {len(phrases)} key phrases for character_id: {character_id}")
            result = await db.execute(select(Character).where(Character.id == character_id))
            character = result.scalars().first()
            if not character:
                logging.warning(f"Character not found with id: {character_id} when saving phrases")
                raise HTTPException(status_code=400, detail="Character not found")
            
            saved_phrases = []
            for phrase in phrases:
                keyphrase_data = {"character_id": character_id, "phrase": phrase}
                saved_phrase = await self.create(db, keyphrase_data)
                saved_phrases.append(saved_phrase)
            
            logging.info(f"Successfully saved {len(saved_phrases)} key phrases for character_id: {character_id}")
            return saved_phrases
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error saving key phrases for character_id {character_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving key phrases: {str(e)}")

# Global keyphrase service instance
keyphrase_service = KeyphraseService()
