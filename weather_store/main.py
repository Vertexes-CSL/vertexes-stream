import os
from app.container import KafkaContainer
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Retrieve configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS')
TOPIC_CONSUMER = os.getenv('TOPIC_CONSUMER')
MONGO_URI = os.getenv('MONGO_URI_3')  # Ensure your Mongo URI is in the .env

if __name__ == "__main__":
    # Initialize KafkaContainer
    container = KafkaContainer()

    # Set up configuration for the Kafka container
    container.config.from_dict(
        {
            'bootstrap_servers': BOOTSTRAP_SERVERS,
            'kafka_config': {
                'bootstrap.servers': BOOTSTRAP_SERVERS,
                'group.id': 'queue',
                'auto.offset.reset': 'latest',
            }
        }, True)

    # Initialize MongoDB client
    mongo_client = MongoClient(MONGO_URI)

    # Register the MongoDB client with the container if it's part of the container's dependencies
    container.mongo_client = mongo_client

    # Instantiate data_processor with mongo_client dependency
    data_processor = container.data_processor(mongo_client=mongo_client)

    print("=" * 20 + f"Consuming Data From {TOPIC_CONSUMER} Topic" + "=" * 20)
    data_processor.consume(TOPIC_CONSUMER)
