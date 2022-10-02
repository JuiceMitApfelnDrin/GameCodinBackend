from __future__ import annotations
from enum import Enum

class State(Enum):
    STARTING = 0
    STARTED = 1
    FINISHING = 2
    FINISHED = 3