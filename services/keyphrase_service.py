import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from sqlalchemy.orm import Session
from models.key_phrase import KeyPhrase
from models.character import Character

AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")

def get_azure_client():
    return TextAnalyticsClient(
        endpoint=AZURE_LANGUAGE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_LANGUAGE_KEY)
    )

def extract_key_phrases_azure(text: str, language: str = "es") -> list[str]:
    client = get_azure_client()
    try:
        response = client.extract_key_phrases([{"id": "1", "language": language, "text": text}])
        result = response[0]
        if result.is_error:
            raise RuntimeError(f"Error de Azure: {result.error.code} - {result.error.message}")
        return result.key_phrases
    except Exception as e:
        raise RuntimeError(f"Error al consumir Azure: {str(e)}")

def save_key_phrases(db: Session, character_id: int, phrases: list[str]):
    for phrase in phrases:
        db.add(KeyPhrase(character_id=character_id, phrase=phrase))
    db.commit()

def get_key_phrases_by_character(db: Session, character_id: int):
    return db.query(KeyPhrase).filter(KeyPhrase.character_id == character_id).all()
