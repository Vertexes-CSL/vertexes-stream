from celery import Celery
from produce.fetch_weather import fetch_weather_data_srg, fetch_weather_data_jkt, fetch_weather_data_bdg, fetch_weather_data_smr, fetch_weather_data_sby
# from produce.kafka_producer import send_to_kafka
from datetime import datetime
import json
import os


celery_app = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"), include=["produce.celery"])

celery_app.autodiscover_tasks([])

celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.beat_schedule = {
    "fetch-weather-srg-every-30-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_srg",
        "schedule": 15.0,  
    },
    "fetch-weather-jkt-every-30-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_jkt",
        "schedule": 15.0,  
    },
    "fetch-weather-bdg-every-30-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_bdg",
        "schedule": 15.0,  
    },
    "fetch-weather-smr-every-30-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_smr",
        "schedule": 15.0,  
    },
    "fetch-weather-sby-every-30-seconds": {
        "task": "produce.celery.scheduled_fetch_and_save_sby",
        "schedule": 15.0,  
    },
}

@celery_app.task()
def scheduled_fetch_and_save_srg():
    weather_data = fetch_weather_data_srg()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("/app/output", "output_srg", f"weather_data_srg_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
    else:
        print("Failed to fetch Serang weather data")

@celery_app.task()
def scheduled_fetch_and_save_jkt():
    weather_data = fetch_weather_data_jkt()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("/app/output", "output_jkt", f"weather_data_bdg_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
    else:
        print("Failed to fetch Jakarta weather data")

@celery_app.task()
def scheduled_fetch_and_save_bdg():
    weather_data = fetch_weather_data_bdg()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("/app/output", "output_bdg", f"weather_data_bdg_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
    else:
        print("Failed to fetch Bandung weather data")

@celery_app.task()
def scheduled_fetch_and_save_smr():
    weather_data = fetch_weather_data_smr()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("/app/output", "output_smr", f"weather_data_smr_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
    else:
        print("Failed to fetch Semarang weather data")

@celery_app.task()
def scheduled_fetch_and_save_sby():
    weather_data = fetch_weather_data_sby()
    if weather_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("/app/output", "output_sby", f"weather_data_sby_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(weather_data, file)
    else:
        print("Failed to fetch Surabaya weather data")


# @celery_app.task()
# def scheduled_fetch_and_save_srg():
#     weather_data = fetch_weather_data_srg()
#     if weather_data:
#         send_to_kafka(weather_data)
#     else:
#         print("Failed to fetch Serang weather data")

# @celery_app.task()
# def scheduled_fetch_and_save_jkt():
#     weather_data = fetch_weather_data_jkt()
#     if weather_data:
#         send_to_kafka(weather_data)

#     else:
#         print("Failed to fetch Jakarta weather data")

# @celery_app.task()
# def scheduled_fetch_and_save_bdg():
#     weather_data = fetch_weather_data_bdg()
#     if weather_data:
#         send_to_kafka(weather_data)

#     else:
#         print("Failed to fetch Bandung weather data")

# @celery_app.task()
# def scheduled_fetch_and_save_smr():
#     weather_data = fetch_weather_data_smr()
#     if weather_data:
#         send_to_kafka(weather_data)

#     else:
#         print("Failed to fetch Semarang weather data")

# @celery_app.task()
# def scheduled_fetch_and_save_sby():
#     weather_data = fetch_weather_data_sby()
#     if weather_data:
#         send_to_kafka(weather_data)
#     else:
#         print("Failed to fetch Surabaya weather data")

