from puzzle import Puzzle
from user import User
from dataclasses import dataclass, asdict


@dataclass
class GameRoom:
    puzzle: Puzzle
    creator: User
    players: User
    end_time: int

    @property
    def dict(self):
        return asdict(self)

    def add_player(self, player: User):
        self.players = [*self.players, player]

    def end_room(self):
        
