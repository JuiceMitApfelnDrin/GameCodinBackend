from __future__ import annotations
from enum import Enum

from typing import cast


class Difficulty(Enum):
    RANDOM = 0
    # from easy to hard? doesn't make sense to me :thinking:
    EASY = 1
    MEDIUM = 2
    HARD = 3
    HARDEST = 4

    @classmethod
    def members(cls) -> tuple[Difficulty, ...]:
        return cast(tuple[Difficulty, ...], cls._member_map_.values())