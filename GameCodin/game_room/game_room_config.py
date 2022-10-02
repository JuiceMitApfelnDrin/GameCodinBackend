from dataclasses import asdict, dataclass

from ..puzzle.puzzle_type import PuzzleType
from .game_language import Language
# from puzzle.puzzle_difficulty import Difficulty
from .game_room_visibility import Visibility
from .game_room_state import State

# TODO: for version 0.2.0:
# difficulty: Difficulty = Difficulty.RANDOM
# max_players: int = 50


@dataclass
class GameRoomConfig:
    game_mode: PuzzleType
    languages: list[Language]

    duration: int = 15
    visibility: Visibility = Visibility.PUBLIC
    state: State = State.STARTING

    @property
    def dict(self) -> dict:
        return asdict(self)
