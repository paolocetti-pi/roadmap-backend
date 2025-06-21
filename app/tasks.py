import requests
from datetime import datetime
from .celery_worker import celery
from . import crud

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

@celery.task(name="app.tasks.fetch_weather_data")
def fetch_weather_data(location: str):
    """
    Fetches weather data for a given location from Open-Meteo API
    and saves it to Redis if the task is enabled.
    """
    if not crud.is_task_enabled('fetch_weather'):
        print("Fetch weather task is disabled.")
        return

    # Example coordinates for New York
    latitude = 40.71
    longitude = -74.01
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
    }
    try:
        response = requests.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        crud.save_weather_data(location, weather_data)
        print(f"Weather data for {location} saved.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")


@celery.task(name="app.tasks.save_message")
def save_message():
    """
    Saves a timestamped message to Redis if the task is enabled.
    """
    if not crud.is_task_enabled('save_message'):
        print("Save message task is disabled.")
        return
        
    message = f"Log message generated at {datetime.utcnow().isoformat()}"
    crud.save_log_message(message)
    print("Log message saved.") 