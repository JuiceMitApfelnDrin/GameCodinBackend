from __future__ import annotations
from enum import Enum


class MessageType(Enum):
    # user
    USER_SUBMITTED  = "USER_SUBMITTED"

    # clash
    CLASH_STARTED = "GAME_STARTED"
    CLASH_FINISHED = "GAME_FINISHED"
    GAME_NOT_FOUND = "GAME_NOT_FOUND"
