import redis.asyncio as redis
import os
import json
from utils.logger import logger

class RedisService:
    def __init__(self):
        self.redis_client = None
        self.cache_expiration = int(os.getenv("CACHE_EXPIRATION_SECONDS", 60))

    async def initialize(self):
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            await self.redis_client.ping()
            logger.info("Successfully connected to Redis.")
        except redis.ConnectionError as e:
            logger.error(f"Could not connect to Redis: {e}")
            self.redis_client = None

    async def get(self, key):
        if not self.redis_client:
            return None
        try:
            cached_data = await self.redis_client.get(key)
            if cached_data:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(cached_data)
            logger.info(f"Cache miss for key: {key}")
            return None
        except redis.RedisError as e:
            logger.error(f"Redis error on get for key {key}: {e}")
            return None

    async def set(self, key, value):
        if not self.redis_client:
            return
        try:
            # Using a default function to handle non-serializable objects like datetime
            serialized_value = json.dumps(value, default=str)
            await self.redis_client.setex(key, self.cache_expiration, serialized_value)
            logger.info(f"Cache set for key: {key}")
        except redis.RedisError as e:
            logger.error(f"Redis error on set for key {key}: {e}")
            
    async def delete(self, key):
        if not self.redis_client:
            return
        try:
            await self.redis_client.delete(key)
            logger.info(f"Cache deleted for key: {key}")
        except redis.RedisError as e:
            logger.error(f"Redis error on delete for key {key}: {e}")

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed.")

redis_service = RedisService() 