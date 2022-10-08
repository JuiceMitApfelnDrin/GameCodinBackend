from __future__ import annotations
from enum import Enum

from typing import cast

class PuzzleDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    IMPOSSIBLE = 4