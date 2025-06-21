import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))

def save_weather_data(location: str, data: dict):
    """Saves weather data for a location in Redis."""
    redis_client.set(f"weather:{location}", json.dumps(data))

def get_weather_data(location: str):
    """Gets weather data for a location from Redis."""
    data = redis_client.get(f"weather:{location}")
    if data:
        return json.loads(data)
    return None

def save_log_message(message: str):
    """Saves a log message in a Redis list."""
    redis_client.rpush("log_messages", message)

def get_log_messages():
    """Gets all log messages from Redis."""
    messages = redis_client.lrange("log_messages", 0, -1)
    return [msg.decode('utf-8') for msg in messages]

def set_task_state(task_name: str, enabled: bool):
    """Sets the state of a task (enabled/disabled) in Redis."""
    redis_client.set(f"task_state:{task_name}", "enabled" if enabled else "disabled")

def is_task_enabled(task_name: str) -> bool:
    """Checks if a task is enabled in Redis. Defaults to enabled if not set."""
    state = redis_client.get(f"task_state:{task_name}")
    if state is None:
        return True # Enabled by default
    return state.decode('utf-8') == "enabled" 