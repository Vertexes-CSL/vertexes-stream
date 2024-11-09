from datetime import datetime
import json
import os
from confluent_kafka import Producer
from dotenv import load_dotenv
import copy

load_dotenv()

TOPIC_PRODUCER = os.getenv("TOPIC_PRODUCER")


class KafkaProducer:
    def __init__(self, bootstrap_servers):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def produce(
        self,
        station,
        channel,
        data,
        start_time,
        end_time,
        producer_time=None,
        arrive_time=datetime.utcnow(),
    ):
        if producer_time is None:
            producer_time = [
                arrive_time.isoformat(),
                datetime.utcnow().isoformat(),
            ]
        data = {
            "station": station,
            "channel": channel,
            "starttime": start_time.isoformat(),
            "endtime": end_time.isoformat(),
            "data": data,
            "len": len(data),
            "producer_time": producer_time,
            "eews_queue_time": [arrive_time.isoformat(), datetime.utcnow().isoformat()],
            "type": "trace",
        }

        print("Producing ", station, channel, len(data))
        self.producer.produce(TOPIC_PRODUCER, key=station, value=json.dumps(data))

    def startTrace(self, partition):
        self.producer.produce(
            topic=TOPIC_PRODUCER,
            key="start",
            value=json.dumps({"type": "start"}),
            partition=int(partition),
        )
        self.producer.flush()
        # print("=" * 20, "Start Trace ", partition, "=" * 20)

    def stopTrace(self, partition):
        self.producer.produce(
            topic=TOPIC_PRODUCER,
            key="stop",
            value=json.dumps({"type": "stop"}),
            partition=int(partition),
        )
        self.producer.flush()
        # print("=" * 20, "Stop Trace ", partition, "=" * 20)
