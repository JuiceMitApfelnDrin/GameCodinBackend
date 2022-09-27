from dataclasses import dataclass
from game_room.game_mode import GameMode
from game_room.game_language import Language
from puzzle.puzzle_difficulty import Difficulty
from game_room.game_room_visibility import Visibility


@dataclass
class GameRoomConfig:
    game_mode: GameMode
    languages: list[Language]

    duration: int = 15
    max_players: int = 50
    visibility: Visibility = Visibility.PUBLIC
    difficulty: Difficulty = Difficulty.RANDOM