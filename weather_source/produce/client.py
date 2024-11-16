from abc import ABC, abstractmethod
from produce.producer import KafkaProducer
from datetime import datetime
from produce.redis_client import RedisSingleton
import requests


class WeatherClient(ABC):
    def __init__(self, producer: KafkaProducer):
        self.producer = producer
        redis = RedisSingleton()
        # Retrieve city coordinates from Redis
        stats = redis.r.get("CITY_COORDS")
        if stats:
            self.city_coords = dict([tuple(coord.split(":")) for coord in stats.split(",")])
        else:
            self.city_coords = {}

    def _extract_weather_values(self, weather_data, arrive_time):
        # Extract values from the weather data
        msg = {
            "type": "weather",
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "description": weather_data["weather"][0]["description"],
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "rain": weather_data.get("rain", {}).get("1h", 0),
            "clouds": weather_data["clouds"]["all"],
            "wind_speed": weather_data["wind"]["speed"],
            "wind_deg": weather_data["wind"]["deg"],
            "coord_lon": weather_data["coord"]["lon"],
            "coord_lat": weather_data["coord"]["lat"],
            "timestamp": datetime.utcfromtimestamp(weather_data["dt"]).isoformat(),
            "producer_time": [arrive_time.isoformat(), datetime.utcnow().isoformat()],
        }
        return msg
