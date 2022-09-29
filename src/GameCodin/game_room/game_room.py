from .game_room_config import GameRoomConfig
from puzzle.puzzle import Puzzle
from ..user.user import User
from dataclasses import dataclass, asdict, field


@dataclass
class GameRoom:
    puzzle_id: str
    puzzle: Puzzle
    creator: User
    start_time: int
    gameroom_config: GameRoomConfig

    players: list[User] = field(default_factory=list)

    @property
    def asdict(self):
        """
        Note to juice
        We want to store this in database so it doesn't make sense
        to create a dict with objects in them. Those objects needs
        to also to be convereted to dict, and it doesn't make sense
        to store all players infos in each gameroom. Because first 
        of all they can change and also that's using extra space.
        So we store only the player id instead.
        """
        gameroom_dict = asdict(self)
        gameroom_dict["players"] = [player.user_id for player in self.players]
        gameroom_dict["gameroom_config"] = self.gameroom_config.dict

    def add_player(self, player: User):
        self.players.append(player)
    
    @property
    def end_time(self):
        # duration is a value representing the minutes
        # probably needs to be transformed and then added to start_time
        return self.start_time+self.gameroom_config.duration
