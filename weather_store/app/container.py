from confluent_kafka import Consumer
from .producer import KafkaProducer
from .processor import KafkaDataProcessor
from dependency_injector import containers, providers


class KafkaContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    producer = providers.Singleton(
        KafkaProducer,
        bootstrap_servers=config.bootstrap_servers,
    )
    consumer = providers.Singleton(
        Consumer,
        config.kafka_config
    )
    data_processor = providers.Singleton(
        KafkaDataProcessor,
        consumer=consumer,
        producer=producer,
    )
