from abc import ABC, abstractmethod
from produce.producer import KafkaProducer
from obspy import Trace
from produce.redis_client import RedisSingleton
from datetime import datetime
from produce.class_mode import StreamMode


class StreamClient(ABC):
    def __init__(self, mode: StreamMode, producer: KafkaProducer):
        self.mode: StreamMode = mode
        self.producer = producer
        redis = RedisSingleton()
        stats = redis.r.get("ENABLED_STATION_CODES")
        stats = stats.split(",")
        self.stations: set = set(stats)

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
            "producer_time": [arrive_time.isoformat(), datetime.utcnow().isoformat()],
        }
        return msg
