from kafka import KafkaProducer
import json
import os

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather_data")

producer = KafkaProducer(
    bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def send_to_kafka(data):
    producer.send(KAFKA_TOPIC, value=data)
    producer.flush()
