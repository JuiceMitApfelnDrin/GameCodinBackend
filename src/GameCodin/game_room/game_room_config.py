from dataclasses import dataclass

from attr import asdict
from .game_mode import GameMode
from .game_language import Language
from puzzle.puzzle_difficulty import Difficulty
from .game_room_visibility import Visibility


@dataclass
class GameRoomConfig:
    game_mode: GameMode
    languages: list[Language]

    duration: int = 15
    max_players: int = 50
    visibility: Visibility = Visibility.PUBLIC
    difficulty: Difficulty = Difficulty.RANDOM

    @property
    def dict(self):
        return asdict(self)