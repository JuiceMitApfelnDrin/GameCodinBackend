from GameCodin.Submission.submission import Submission
from .game_room_config import GameRoomConfig
from puzzle.puzzle import Puzzle
from bson.objectid import ObjectId
from ..user.user import User
from dataclasses import dataclass, asdict, field


@dataclass
class GameRoom:
    puzzle_id: ObjectId
    creator_id: ObjectId
    start_time: int
    gameroom_config: GameRoomConfig

    results: dict[ObjectId, Submission] = field(
        default_factory=dict[ObjectId, Submission])
    players: dict[ObjectId, User] = field(default_factory=dict[ObjectId, User])

    @property
    def asdict(self):
        gameroom_dict = asdict(self)
        gameroom_dict["gameroom_config"] = self.gameroom_config.dict

    def start_game(self):
        # websocket stuff
        pass

    def end_game(self):
        # websocket stuff
        pass

    def add_player(self, player: User):
        self.players[player.user_id] = player

    def remove_player(self, user_id: ObjectId):
        del self.players[user_id]

    def execute(self, code: str, language: str, user_id: str):
        # TODO:
        # => fetch puzzle code (validators)
        # => execute it in pistonapi
        # => remove users previous result from result list
        # => add result to result list
        # => return result
        return

    @property
    def end_time(self):
        # duration is a value representing the minutes
        # probably needs to be transformed and then added to start_time
        return self.start_time+self.gameroom_config.duration
