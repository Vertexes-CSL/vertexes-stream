from confluent_kafka import Producer
import json
from os import getenv
from dotenv import load_dotenv

load_dotenv()
TOPIC_NAME = "weather_preprocess"
BOOTSTRAP_SERVERS = getenv("BOOTSTRAP_SERVERS")

producer_config = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
}

class KafkaProducer:
    def __init__(self, topic_name=TOPIC_NAME):
        self.producer = Producer(producer_config)
        self.topic_name = topic_name

    def produce_message(self, data):
        self.producer.produce(self.topic_name, value=json.dumps(data).encode('utf-8'))
        self.producer.flush()

kafka_producer = KafkaProducer()
