from azure.cosmos.container import ContainerProxy
from azure.cosmos import exceptions
from fastapi import HTTPException
from typing import List, Dict, Any
import logging
import uuid

class CosmosCharacterService:
    """Service class for managing character operations with CosmosDB"""

    def __init__(self, container: ContainerProxy):
        self.container = container
        self.logger = logging.getLogger(__name__)

    def _generate_id(self):
        return str(uuid.uuid4())

    async def get_all_characters(self) -> List[Dict[str, Any]]:
        self.logger.info("Getting all characters from CosmosDB")
        try:
            items = list(self.container.read_all_items())
            return items
        except exceptions.CosmosResourceNotFoundError:
            return []
        except Exception as e:
            self.logger.error(f"Error getting all characters from CosmosDB: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving characters from CosmosDB")

    async def get_character_by_name(self, name: str) -> List[Dict[str, Any]]:
        self.logger.info(f"Querying for characters with name: {name} in CosmosDB")
        try:
            query = "SELECT * FROM c WHERE c.name = @name"
            parameters = [{"name": "@name", "value": name}]
            items = list(self.container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
            return items
        except Exception as e:
            self.logger.error(f"Error retrieving characters by name '{name}' from CosmosDB: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving characters from CosmosDB: {str(e)}")

    async def create_character(self, character_data: dict) -> Dict[str, Any]:
        self.logger.info(f"Creating character in CosmosDB: {character_data.get('name')}")
        try:
            # Cosmos DB needs a unique 'id' for each document.
            character_data['id'] = self._generate_id()
            self.container.upsert_item(body=character_data)
            return character_data
        except Exception as e:
            self.logger.error(f"Error creating character in CosmosDB: {e}")
            raise HTTPException(status_code=400, detail=f"Error creating character in CosmosDB: {str(e)}")

    async def delete_character(self, character_id: str) -> bool:
        self.logger.info(f"Deleting character with id: {character_id} from CosmosDB")
        try:
            self.container.delete_item(item=character_id, partition_key=character_id)
            return True
        except exceptions.CosmosResourceNotFoundError:
            raise HTTPException(status_code=404, detail="Character not found in CosmosDB")
        except Exception as e:
            self.logger.error(f"Error deleting character with id {character_id} from CosmosDB: {e}")
            raise HTTPException(status_code=400, detail=f"Error deleting character from CosmosDB: {str(e)}")

    async def update_character(self, character_id: str, character_data: dict) -> Dict[str, Any]:
        self.logger.info(f"Updating character with id: {character_id} in CosmosDB")
        try:
            # Read the item to make sure it exists and to get the full document
            existing_item = self.container.read_item(item=character_id, partition_key=character_id)
            
            # Update fields
            for key, value in character_data.items():
                existing_item[key] = value

            self.container.upsert_item(body=existing_item)
            return existing_item
        except exceptions.CosmosResourceNotFoundError:
             raise HTTPException(status_code=404, detail="Character not found in CosmosDB")
        except Exception as e:
            self.logger.error(f"Error updating character with id {character_id} in CosmosDB: {e}")
            raise HTTPException(status_code=400, detail=f"Error updating character in CosmosDB: {str(e)}")

    async def get_character_by_id(self, character_id: str) -> Dict[str, Any]:
        """Get a single character by its ID."""
        self.logger.info(f"Getting character with id: {character_id} from CosmosDB")
        try:
            item = self.container.read_item(item=character_id, partition_key=character_id)
            return item
        except exceptions.CosmosResourceNotFoundError:
            raise HTTPException(status_code=404, detail="Character not found in CosmosDB")
        except Exception as e:
            self.logger.error(f"Error retrieving character with id {character_id} from CosmosDB: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving character from CosmosDB") 