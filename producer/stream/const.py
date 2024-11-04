from enum import Enum

class StrEnum(str, Enum):
    pass

class StreamMode(StrEnum):
    LIVE = 'live'
    PLAYBACK = 'playback'
    IDLE = 'idle'
    FILE = 'file'
