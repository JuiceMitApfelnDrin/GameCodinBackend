from dataclasses import asdict, dataclass

from ..puzzle.puzzle_type import PuzzleType
from .game_language import Language
# from puzzle.puzzle_difficulty import Difficulty
from .game_room_visibility import Visibility
from .game_room_state import GameRoomState

@dataclass
class GameRoomConfig:
    game_mode: PuzzleType
    languages: list[Language]

    duration_minutes: int = 15
    visibility: Visibility = Visibility.PUBLIC
    # TODO: for version 2.0:
    # difficulty: Difficulty = Difficulty.RANDOM
    # max_players: int = 50

    def as_dict(self) -> dict:
        return asdict(self)
