import json
import copy
from datetime import datetime, timedelta
from typing import List, Dict, Any
from confluent_kafka import Consumer, Producer
from .missing_data_handler import MissingDataHandler
from .mongo import MongoDBClient  # Assuming MongoDBClient is a class that handles MongoDB operations

class KafkaDataProcessor:
    def __init__(
        self, 
        consumer: Consumer, 
        producer: Producer, 
        data_handler: MissingDataHandler,
        mongo_client: MongoDBClient  # Inject MongoDB client for saving data
    ):
        self.consumer = consumer
        self.data_handler = data_handler
        self.producer = producer
        self.mongo_client = mongo_client  # MongoDB client for saving data
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

    def __process_received_data(self, value: Dict[str, Any], arrive_time: datetime):
        station = value["station"]
        channel = value["channel"]
        producer_time = value["producer_time"]
        data = value["data"]
        start_time = datetime.strptime(value["starttime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strptime(value["endtime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        sampling_rate = value["sampling_rate"]

        self.data_handler.handle_missing_data(
            station, channel, start_time, sampling_rate
        )
        self.__store_data(
            station,
            channel,
            data,
            start_time,
            sampling_rate,
            producer_time=producer_time,
            arrive_time=arrive_time,
        )

    def __store_data(
        self,
        station: str,
        channel: str,
        data: List[int],
        start_time: datetime,
        sampling_rate: float,
        producer_time,
        arrive_time: datetime,
    ):
        current_time = start_time
        if (
            station in self.data_handler.last_processed_time
            and channel in self.data_handler.last_processed_time[station]
        ):
            current_time = self.data_handler.last_processed_time[station][channel]

        self.data_handler.data_pool[station][channel].extend(data)

        while len(self.data_handler.data_pool[station][channel]) >= 128:
            data_to_send = self.data_handler.data_pool[station][channel][:128]
            self.data_handler.data_pool[station][channel] = self.data_handler.data_pool[
                station
            ][channel][128:]
            time_to_add = timedelta(seconds=128 / sampling_rate)
            self.__send_data_to_queue(
                station,
                channel,
                data_to_send,
                current_time,
                current_time + time_to_add,
                producer_time=producer_time,
                arrive_time=arrive_time,
            )
            current_time = current_time + time_to_add

            # Save the data to MongoDB after processing
            self.__save_data_to_mongo(station, channel, data_to_send, current_time, time_to_add, producer_time, arrive_time)

    def __send_data_to_queue(
        self,
        station: str,
        channel: str,
        data: List[int],
        start_time: datetime,
        end_time: datetime,
        producer_time,
        arrive_time: datetime,
    ):
        self.data_handler.update_last_processed_time(station, channel, end_time)
        self.producer.produce(
            station,
            channel,
            data,
            start_time,
            end_time,
            producer_time=producer_time,
            arrive_time=arrive_time,
        )

    def __save_data_to_mongo(
        self,
        station: str,
        channel: str,
        data: List[int],
        start_time: datetime,
        time_to_add: timedelta,
        producer_time,
        arrive_time: datetime
    ):
        # Create a payload to save to MongoDB
        payload = {
            "station": station,
            "channel": channel,
            "data": data,
            "start_time": start_time,
            "end_time": start_time + time_to_add,
            "producer_time": producer_time,
            "arrive_time": arrive_time,
            "type": "data",
        }

        # Save the data to MongoDB
        self.mongo_client.create(payload)
        print(f"Saved to MongoDB: {payload}")

    def _start(self):
        for i in self.partitions:
            self.producer.startTrace(i.partition)
        self.data_handler.reset_state()

    def _flush(self, sampling_rate):
        for station, stationDict in self.data_handler.data_pool.items():
            for channel, data_to_send in stationDict.items():
                end_time = self.data_handler.last_processed_time[station][channel]
                time_to_decrease = timedelta(seconds=len(data_to_send) / sampling_rate)
                start_time = end_time - time_to_decrease
                self.producer.produce(
                    station, channel, data_to_send, start_time, end_time
                )
                # Save the flushed data to MongoDB
                self.__save_data_to_mongo(station, channel, data_to_send, start_time, time_to_decrease, None, None)
        print("=" * 20, "END", "=" * 20)
        for i in self.partitions:
            self.producer.stopTrace(i.partition)
