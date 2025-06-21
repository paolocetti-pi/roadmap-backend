import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

celery.conf.beat_schedule = {
    'fetch-weather-every-30-seconds': {
        'task': 'app.tasks.fetch_weather_data',
        'schedule': 30.0, # seconds
        'args': ("New York",)
    },
    'save-message-every-10-seconds': {
        'task': 'app.tasks.save_message',
        'schedule': 10.0, # seconds
    },
}
celery.conf.timezone = 'UTC'

celery.autodiscover_tasks(['app.tasks']) 