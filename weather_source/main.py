import time
import json
from datetime import datetime
from produce.producer import KafkaProducer
from produce.ow_client import OpenWeatherClient  # Assuming OpenWeatherClient is in a separate file named weather_client.py
import requests
from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI()

# Read PORT environment variable
PORT = os.getenv("PORT")
TOPIC_NAME = os.getenv("TOPIC_NAME")

# Create a producer instance
producer = KafkaProducer(TOPIC_NAME)

# OpenWeatherClient configuration
weather_client = OpenWeatherClient(producer)
scheduler = BackgroundScheduler()

@app.get("/start")
async def start_weather_data_collection(background_tasks: BackgroundTasks):
    """Start the weather data collection using the OpenWeatherClient."""
    print("Received request to start weather data collection")
    background_tasks.add_task(weather_client.start_streaming)
    return {"message": "Weather data collection task triggered in the background"}

@app.post("/stop")
async def stop_weather_data_collection(background_tasks: BackgroundTasks):
    """Stop the weather data collection using the OpenWeatherClient."""
    print("Received request to stop weather data collection")
    background_tasks.add_task(weather_client.stop_streaming)
    return "Weather data collection stopped."

# Run the FastAPI app with Uvicorn server
if __name__ == "__main__":
    import uvicorn
    config = uvicorn.Config("main:app", port=int(PORT), log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
