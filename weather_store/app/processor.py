import json
import copy
from datetime import datetime, timedelta
from typing import List, Dict, Any
from confluent_kafka import Consumer, Producer
from .mongo import MongoDBClient


class KafkaDataProcessor:
    def __init__(
        self,
        consumer: Consumer,
        producer: Producer,
        mongo_client: MongoDBClient,
    ):
        self.consumer = consumer
        self.producer = producer
        self.mongo_client = mongo_client
        self.partitions = []

    def consume(self, topic: str):
        self.consumer.subscribe([topic])
        i = 1
        show_nf = True
        while True:
            msg = self.consumer.poll(10)
            self.partitions = self.consumer.assignment()

            if msg is None:
                if show_nf:
                    print("No message received :(")
                show_nf = False
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue

            show_nf = True
            value = msg.value()
            value = json.loads(value)
            logvalue = copy.copy(value)
            logvalue["data"] = None
            if value["type"] == "start":
                print(i)
                self._start()
            if value["type"] == "stop":
                print(i)
                i = 1
                self._flush(sampling_rate=20)
            if value["type"] == "trace":
                i += 1
                self.__process_received_data(value, arrive_time=datetime.utcnow())
            if value["type"] == "weather":
                self.__process_weather_data(value, arrive_time=datetime.utcnow())

    def __process_weather_data(self, value: Dict[str, Any], arrive_time: datetime):
        city = value["city"]
        country = value["country"]
        description = value["description"]
        temperature = value["temperature"]
        humidity = value["humidity"]
        pressure = value["pressure"]
        rain = value["rain"]
        clouds = value["clouds"]
        wind_speed = value["wind_speed"]
        wind_deg = value["wind_deg"]
        coord_lon = value["coord_lon"]
        coord_lat = value["coord_lat"]
        timestamp = value["timestamp"]
        producer_time = value["producer_time"]

        # Store weather data in MongoDB
        self.__store_weather_data(
            city, country, description, temperature, humidity, pressure, rain,
            clouds, wind_speed, wind_deg, coord_lon, coord_lat, timestamp, producer_time,
            arrive_time
        )

    def __store_weather_data(
        self,
        city: str,
        country: str,
        description: str,
        temperature: float,
        humidity: float,
        pressure: float,
        rain: float,
        clouds: int,
        wind_speed: float,
        wind_deg: int,
        coord_lon: float,
        coord_lat: float,
        timestamp: str,
        producer_time: List[str],
        arrive_time: datetime
    ):
        # Create a payload to save to MongoDB
        payload = {
            "city": city,
            "country": country,
            "description": description,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "rain": rain,
            "clouds": clouds,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "coord_lon": coord_lon,
            "coord_lat": coord_lat,
            "timestamp": timestamp,
            "producer_time": producer_time,
            "arrive_time": arrive_time.isoformat(),
            "type": "weather",
        }

        # Access the database and collection
        database = self.mongo_client[
            "weather_data"  # Replace with your actual database name for weather
        ]
        collection = database[
            "weather_info"  # Replace with your actual collection name
        ]

        # Insert the payload into MongoDB
        collection.insert_one(payload)  # Use insert_many if data is a list of documents
        print(f"Saved weather data to MongoDB: {payload}")

    def _start(self):
        """Start tracing partitions."""
        for i in self.partitions:
            self.producer.startTrace(i.partition)

    def _flush(self, sampling_rate):
        """Flush data for each station and channel."""
        # This part is simplified since we're not using data_handler anymore
        print("=" * 20, "END", "=" * 20)
        for i in self.partitions:
            self.producer.stopTrace(i.partition)

