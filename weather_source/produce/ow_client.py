from os import getenv
from dotenv import load_dotenv
import time
import json
from datetime import datetime
from produce.producer import KafkaProducer
from produce.client import WeatherClient  # Assuming WeatherClient is in a separate file named weather_client.py
import requests

load_dotenv()

OPENWEATHER_API_KEY = getenv("OPENWEATHER_API_KEY")

class OpenWeatherClient(WeatherClient):
    def __init__(self, producer: KafkaProducer):
        super().__init__(producer)
        self.__streaming_started = False
        self.API_KEY = OPENWEATHER_API_KEY

    def fetch_weather_data(self, lat, lon):
        # Fetching data from the OpenWeather API using coordinates
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return None

    def run(self):
        if not self.city_coords:
            raise Exception("No city coordinates specified. Please use Redis to store city coordinates.")
        self.__streaming_started = True
        print("Starting weather data collection:", datetime.utcnow())

        while self.__streaming_started:
            # Iterate through each city coordinate (latitude, longitude)
            
            for lat, lon in self.city_coords.items():
                weather_data = self.fetch_weather_data(lat, lon)
                
                if weather_data:
                    arrive_time = datetime.utcnow()
                    msg = self._extract_weather_values(weather_data, arrive_time)
                    # Send the message to Kafka with a topic name based on the city
                    print("ok")
                    self.producer.produce_message(
                        json.dumps(msg), msg["city"]
                    )
            
            # Sleep for 5 seconds before fetching the data again
            time.sleep(5)  # 5-second interval for the next iteration

    def start_streaming(self):
        if not self.__streaming_started:
            self.run()

    def stop_streaming(self):
        self.__streaming_started = False
        print("Weather streaming stopped.")