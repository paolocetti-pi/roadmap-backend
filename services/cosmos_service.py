import os
from azure.cosmos import CosmosClient
from azure.cosmos.partition_key import PartitionKey
from azure.core.exceptions import AzureError
from dotenv import load_dotenv
import logging

load_dotenv()

class CosmosDBService:
    """Service class for managing CosmosDB connections and operations"""

    def __init__(self):
        self.endpoint = os.getenv("COSMOS_ENDPOINT")
        self.key = os.getenv("COSMOS_KEY")
        self.database_name = os.getenv("COSMOS_DATABASE", "roadmap-backend")
        self.container_name = os.getenv("COSMOS_CONTAINER", "characters")
        
        if not self.endpoint or not self.key:
            logging.error("COSMOS_ENDPOINT and COSMOS_KEY must be set in environment variables.")
            raise ValueError("COSMOS_ENDPOINT and COSMOS_KEY must be set.")

        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )
        logging.info(f"CosmosDB service initialized for database '{self.database_name}' and container '{self.container_name}'")

    def get_container(self):
        """Returns the Cosmos DB container client."""
        return self.container

# Global CosmosDB service instance
cosmos_db_service = CosmosDBService()

def get_cosmos_container():
    """Dependency injection function for FastAPI to get CosmosDB container."""
    return cosmos_db_service.get_container() 