from kafka import KafkaProducer
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kafka connection parameters
bootstrap_servers = getenv("BOOTSTRAP_SERVERS")
topic_name = getenv("TOPIC_NAME")

try:
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    # Send a test message
    producer.send(topic_name, b'Test message')
    producer.flush()
    print("Message sent successfully to Kafka topic.")
except Exception as e:
    print(f"Failed to send message to Kafka: {e}")