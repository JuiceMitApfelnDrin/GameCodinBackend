from __future__ import annotations
from enum import Enum

from typing import cast


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    IMPOSSIBLE = 4

    @classmethod
    def members(cls) -> tuple[Difficulty, ...]:
        return cast(tuple[Difficulty, ...], cls._member_map_.values())
