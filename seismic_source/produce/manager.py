from produce.producer import KafkaProducer, kafkaProducer
from produce.seedlink_client import SeedlinkClient
from produce.class_mode import StreamMode

class StreamManager:
    def __init__(
        self, producer: KafkaProducer, seedlink_server: str
    ):
        self.producer = producer
        self.seedlink_server = seedlink_server
        self.seedlink = SeedlinkClient(self.producer, server_url=self.seedlink_server)

    def start(self, mode: StreamMode, *args, **kwargs):
        if mode == StreamMode.LIVE and self.producer.current_mode == StreamMode.IDLE:
            try:
                self.producer.current_mode = StreamMode.LIVE
                self.seedlink.startStreaming()
            except Exception as err:
                print(err)

        elif mode == StreamMode.IDLE: 
            try:
                self.producer.current_mode = StreamMode.IDLE
                self.seedlink.stopStreaming()
            except Exception as err:
                print(err)
                
streamManager = StreamManager(
    producer=kafkaProducer,
    seedlink_server="geofon.gfz-potsdam.de:18000",
)
