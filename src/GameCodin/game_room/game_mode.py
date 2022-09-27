from __future__ import annotations
from enum import Enum
from typing import cast


class GameMode(Enum):
    FASTEST = 1
    REVERSED = 2
    SHORTEST = 3

    @classmethod
    # Return all members other than NONE
    def members(cls) -> tuple[GameMode, ...]:
        return cast(tuple[GameMode, ...], cls._member_map_.values())

    @classmethod
    def find_by_value(cls, value: int) -> GameMode:
        for mode in cls._member_map_.values():
            if mode.value == value:
                return cast(GameMode, mode)
        raise ValueError
