from __future__ import annotations
from dataclasses import asdict, dataclass

from ..puzzle.puzzle_type import PuzzleType
from ..submission.language import Language
# from puzzle.puzzle_difficulty import Difficulty
from .visibility import GameRoomVisibility

# TODO: for version 0.2.0:
# difficulty: Difficulty = Difficulty.RANDOM
# max_players: int = 50


@dataclass
class GameRoomConfig:
    game_mode: PuzzleType
    languages: list[Language]

    duration_minutes: int = 15
    visibility: GameRoomVisibility = GameRoomVisibility.PUBLIC

    def as_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, info: dict) -> GameRoomConfig:
        raise NotImplementedError
