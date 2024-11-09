from produce.client import StreamClient
from produce.producer import KafkaProducer
from obspy.clients.seedlink import EasySeedLinkClient
from obspy import Trace
import json
from datetime import datetime
from obspy.clients.seedlink.slpacket import SLPacket
from produce.class_mode import StreamMode


class SeedlinkClient(StreamClient, EasySeedLinkClient):
    def __init__(self, producer: KafkaProducer, server_url: str):
        self.server_url = server_url
        StreamClient.__init__(self, mode=StreamMode.LIVE, producer=producer)
        EasySeedLinkClient.__init__(self, server_url=self.server_url)
        self.__streaming_started = False
        print("Starting new seedlink client")
        for station in self.stations:
            self.select_stream(net="GE", station=station, selector="BH?")
        print("Starting connection to seedlink server ", self.server_hostname)

    def run(self):
        if not len(self.conn.streams):
            raise Exception(
                "No streams specified. Use select_stream() to select a stream"
            )
        self.__streaming_started = True
        print("Starting collection on:", datetime.utcnow())
        while True:
            arrive_time = datetime.utcnow()
            data = self.conn.collect()
            if data == SLPacket.SLTERMINATE:
                self.on_terminate()
                break
            elif data == SLPacket.SLERROR:
                self.on_seedlink_error()
                continue

            assert isinstance(data, SLPacket)
            packet_type = data.get_type()
            if packet_type not in (SLPacket.TYPE_SLINF, SLPacket.TYPE_SLINFT):
                trace = data.get_trace()
                self.on_data(trace, arrive_time=arrive_time)

    def startStreaming(self):
        self.producer.startTrace()
        print("-" * 20, "Streaming miniseed from seedlink server", "-" * 20)
        if not self.__streaming_started:
            self.run()

    def stopStreaming(self):
        self.producer.stopTrace()
        self.close()
        print("-" * 20, "Stopping miniseed", "-" * 20)

    def on_data(self, trace: Trace, arrive_time):
        try:
            arrive_time = datetime.utcnow()
            msg = self._extract_values(trace, arrive_time)
            self.producer.produce_message(
                json.dumps(msg), msg["station"], StreamMode.LIVE
            )
        except Exception as e:
            print(f"Error processing data for station {msg['station']}: {e}")

# from produce.client import StreamClient, StreamMode
# from produce.producer import KafkaProducer
# from obspy.clients.seedlink import EasySeedLinkClient
# from obspy import Trace
# import json
# from datetime import datetime
# from obspy.clients.seedlink.slpacket import SLPacket
# from produce.class_mode import StreamMode
# from produce.redis_client import RedisSingleton


# class SeedlinkClient(StreamClient, EasySeedLinkClient):
#     def __init__(self, producer: KafkaProducer, server_url: str):
#         self.server_url = server_url
#         StreamClient.__init__(self, mode=StreamMode.IDLE, producer=producer)  # Default to IDLE mode
#         EasySeedLinkClient.__init__(self, server_url=self.server_url)
#         self.__streaming_started = False
#         print("Starting new Seedlink client")
#         self.select_streams()
#         print(f"Starting connection to Seedlink server {self.server_hostname}")

#     def select_streams(self):
#         """Select the streams to listen to based on the enabled station codes."""
#         for station in self.stations:
#             self.select_stream(net="GE", station=station, selector="BH?")
#         print("Streams selected:", self.stations)

#     def run(self):
#         """Start streaming and handle incoming data."""
#         if not len(self.conn.streams):
#             raise Exception("No streams specified. Use select_stream() to select a stream")

#         self.__streaming_started = True
#         print("Starting data collection at:", datetime.utcnow())

#         while self.current_mode == StreamMode.LIVE:
#             arrive_time = datetime.utcnow()
#             data = self.conn.collect()

#             if data == SLPacket.SLTERMINATE:
#                 self.on_terminate()
#                 break
#             elif data == SLPacket.SLERROR:
#                 self.on_seedlink_error()
#                 continue

#             if isinstance(data, SLPacket):
#                 packet_type = data.get_type()
#                 if packet_type not in (SLPacket.TYPE_SLINF, SLPacket.TYPE_SLINFT):
#                     trace = data.get_trace()
#                     self.on_data(trace, arrive_time)

#     def startStreaming(self):
#         """Start streaming from Seedlink server."""
#         if self.current_mode == StreamMode.IDLE:
#             self.producer.startTrace()
#             self.current_mode = StreamMode.LIVE
#             print("-" * 20, "Starting Seedlink streaming", "-" * 20)
#             if not self.__streaming_started:
#                 self.run()

#     def stopStreaming(self):
#         """Stop streaming and clean up."""
#         if self.current_mode == StreamMode.LIVE:
#             self.producer.stopTrace()
#             self.current_mode = StreamMode.IDLE
#             self.close()
#             print("-" * 20, "Stopping Seedlink streaming", "-" * 20)

#     def on_data(self, trace: Trace, arrive_time: datetime):
#         """Handle incoming data and send it to Kafka."""
#         try:
#             msg = self._extract_values(trace, arrive_time)
#             self.producer.produce_message(
#                 json.dumps(msg), msg["station"], StreamMode.LIVE
#             )
#         except Exception as e:
#             print(f"Error processing data for station {msg['station']}: {e}")

#     def on_terminate(self):
#         """Handle termination signal from Seedlink server."""
#         print("Received termination signal. Stopping streaming.")
#         self.stopStreaming()

#     def on_seedlink_error(self):
#         """Handle error from Seedlink server."""
#         print("Error received from Seedlink server.")

