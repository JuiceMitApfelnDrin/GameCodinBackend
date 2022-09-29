from __future__ import annotations
from enum import Enum
from typing import cast


class PuzzleType(Enum):
    FASTEST = 1
    REVERSE = 2
    SHORTEST = 3

    @classmethod
    def members(cls) -> tuple[PuzzleType, ...]:
        return cast(tuple[PuzzleType, ...], cls._member_map_.values())

    @classmethod
    def find_by_value(cls, value: int) -> PuzzleType:
        for mode in cls._member_map_.values():
            if mode.value == value:
                return cast(PuzzleType, mode)
        raise ValueError
