from enum import Enum

from matplotlib.pyplot import disconnect

class RecvPacket(Enum):
    auth = 0
    join = 1

class SendPacket(Enum):
    auth = 0
    join = 1
    error = 2