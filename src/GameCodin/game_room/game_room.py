from game_room.game_room_config import GameRoomConfig
from puzzle.puzzle import Puzzle
from ..user.user import User
from dataclasses import dataclass, asdict, field


@dataclass
class GameRoom:
    puzzle_id: str
    puzzle: Puzzle
    creator: User
    start_time: int
    game_room_config: GameRoomConfig

    players: list[User] = field(default_factory=lambda: [])

    @property
    def dict(self):
        return asdict(self)

    def add_player(self, player: User):
        self.players.append(player)

    @property
    def end_time(self):
        return self.start_time-self.game_room_config.duration

    # def end(self):

    # def start(self):
