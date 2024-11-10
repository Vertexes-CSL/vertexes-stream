from celery import Celery
from produce.fetch_weather import fetch_weather_data_jkt, fetch_weather_data_sby
from datetime import datetime
import json
import os

celery_app = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"))

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "fetch-weather-sby-every-10-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_sby",
        "schedule": 10.0, 
    },
    "fetch-weather-jkt-every-10-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_jkt",
        "schedule": 10.0,  
    },
}

@celery_app.task
def scheduled_fetch_and_save_sby():
    weather_data = fetch_weather_data_sby()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("output_sby", f"weather_data_sby_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
        print(f"Saved Surabaya data to {filename}")
    else:
        print("Failed to fetch Surabaya weather data")

@celery_app.task
def scheduled_fetch_and_save_jkt():
    weather_data = fetch_weather_data_jkt()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("output_jkt", f"weather_data_jkt_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
        print(f"Saved Jakarta data to {filename}")
    else:
        print("Failed to fetch Jakarta weather data")