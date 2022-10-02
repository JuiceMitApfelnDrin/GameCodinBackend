from enum import Enum

class RecvPacket(Enum):
    auth = 0
    join = 1

class SendPacket(Enum):
    auth = 0
    join = 1
    error = 2