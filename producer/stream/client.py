from abc import ABC, abstractmethod
from stream.producer import KafkaProducer
from obspy import Trace
from utils.redis_client import RedisSingleton
from datetime import datetime
from stream.const import StreamMode
# class StreamClient(ABC):
#     def __init__(self, mode: StreamMode, producer: KafkaProducer):
#         self.mode: StreamMode = mode
#         self.producer = producer
#         redis = RedisSingleton()
#         stats: str = redis.r.get("ENABLED_STATION_CODES")
#         print(redis.r.get("ENABLED_STATION_CODES"))
#         stats = stats.split(",")
#         # self.stations: set = set(['BBJI','BKB','BKNI','BNDI','CISI','FAKI','GENI','GSI','JAGI','LHMI','LUWI','MMRI','MNAI','PLAI','PMBI','PMBT','SANI','SAUI','SMRI','TNTI','TOLI','TOLI2','UGM','YOGI'])
#         # self.stations: set = set(['JAGI', 'SMRI', 'BBJI'])
#         self.stations: set = set(stats)

#     @abstractmethod
#     def startStreaming():
#         pass

#     @abstractmethod
#     def stopStreaming():
#         pass

#     def _extract_values(self, trace: Trace, arrive_time):
#         msg = {
#             "type":"trace",
#             "network": trace.stats.network,
#             "station": trace.stats.station,
#             "channel": trace.stats.channel,
#             "location": trace.stats.location,
#             "starttime": str(trace.stats.starttime),
#             "endtime": str(trace.stats.endtime),
#             "delta": trace.stats.delta,
#             "npts": trace.stats.npts,
#             "calib": trace.stats.calib,
#             "data": trace.data.tolist(),
#             "len": len(trace.data.tolist()),
#             "sampling_rate": trace.stats.sampling_rate,
#             "eews_producer_time":[arrive_time.isoformat(), datetime.utcnow().isoformat()]
#         }
#         return msg

class StreamClient(ABC):
    def __init__(self, mode: StreamMode, producer: KafkaProducer):
        self.mode: StreamMode = mode
        self.producer = producer
        redis = RedisSingleton()

        # Retrieve the enabled station codes from Redis
        stats: str = redis.r.get("ENABLED_STATION_CODES")
        
        
        stats = stats.split(",")
        # self.stations: set = set(['BBJI','BKB','BKNI','BNDI','CISI','FAKI','GENI','GSI','JAGI','LHMI','LUWI','MMRI','MNAI','PLAI','PMBI','PMBT','SANI','SAUI','SMRI','TNTI','TOLI','TOLI2','UGM','YOGI'])
        # self.stations: set = set(['JAGI', 'SMRI', 'BBJI'])
        self.stations: set = set(stats)


        if stats is None:
            # Handle the case where there are no enabled station codes
            print("No enabled station codes found in Redis.")
            self.stations: set = set()  # or assign a default set of stations
        else:
            # Check if stats is a bytes object or a list
            if isinstance(stats, bytes):
                print(f"Enabled station codes retrieved: {stats.decode('utf-8')}")
                stats = stats.decode('utf-8').split(",")  # Decode bytes to string before splitting
            elif isinstance(stats, list):
                # Handle the list case (if you expect multiple entries)
                print(f"Enabled station codes retrieved: {', '.join(map(str, stats))}")
                # Assuming the list contains strings or bytes-like objects
                stats = [s.decode('utf-8') if isinstance(s, bytes) else s for s in stats]
            else:
                print("Unexpected data type for enabled station codes.")

            self.stations: set = set(stats)

    @abstractmethod
    def startStreaming(self):
        pass

    @abstractmethod
    def stopStreaming(self):
        pass

    def _extract_values(self, trace: Trace, arrive_time):
        msg = {
            "type": "trace",
            "network": trace.stats.network,
            "station": trace.stats.station,
            "channel": trace.stats.channel,
            "location": trace.stats.location,
            "starttime": str(trace.stats.starttime),
            "endtime": str(trace.stats.endtime),
            "delta": trace.stats.delta,
            "npts": trace.stats.npts,
            "calib": trace.stats.calib,
            "data": trace.data.tolist(),
            "len": len(trace.data.tolist()),
            "sampling_rate": trace.stats.sampling_rate,
            "eews_producer_time": [arrive_time.isoformat(), datetime.utcnow().isoformat()]
        }
        return msg

