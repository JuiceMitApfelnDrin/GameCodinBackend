from __future__ import annotations
import collections
from typing import ClassVar
from bson.objectid import ObjectId
from dataclasses import dataclass, asdict, field
from GameCodinBackend.src.GameCodin.game_room.game_language import Language

from GameCodinBackend.src.GameCodin.game_room.game_room_visibility import Visibility

from ..Submission.submission import Submission
from ..app.app_routing import puzzle
from ..database import db_client
from ..database.collection import Collection
from ..puzzle.puzzle import Puzzle
from ..puzzle.validator_type import ValidatorType
from ..user.user import User
from ..user.session import Session
from ..user.session_expections import SessionException

from .game_room_config import GameRoomConfig
from .game_room_state import State
from . import piston

@dataclass
class GameRoom:
    __active_gamerooms: ClassVar[dict[ObjectId,GameRoom]]
    puzzle: Puzzle
    creator_id: ObjectId
    start_time: int
    gameroom_config: GameRoomConfig

    results: list[Submission] = field(default_factory=list)
    players: dict[ObjectId, User] = field(default_factory=dict)
    sessions: dict[User, list[Session]] = field(default_factory=dict)

    @classmethod
    def get_active_gameroom(cls, gameroom_id: ObjectId):
        return cls.__active_gamerooms[gameroom_id]

    @property
    def asdict(self):
        # actually asdict applies recursively to dataclass fields
        return asdict(self)

    def start_game(self):
        # websocket stuff
        pass

    def end_game(self):
        # websocket stuff
        pass

    def add_sesssion(self, session: Session):
        state = self.gameroom_config
        visibility = self.gameroom_config.visibility

        if not (state is State.STARTING or
                state is State.STARTED and
                visibility is Visibility.PRIVATE):
            raise SessionException("Can't join, game already started!")
        
        user = session.user
        if user not in self.sessions:
            self.sessions[user] = []
        self.sessions[user].append(session)
        self.add_player(user)

    def remove_session(self, session: Session):
        player = session.user
        if player not in self.sessions:
            raise SessionException("User is not in gameroom!")

        sessions = self.sessions[player]
        if session not in sessions:
            raise SessionException("Session is not in gameroom!")

        sessions.remove(session)

        if not sessions and self.gameroom_config.state is State.STARTING:
            self.remove_player(player)

    def add_player(self, player: User):
        self.players[player.user_id] = player

    def remove_player(self, player: User):
        del self.players[player.user_id]

    def execute(self, code: str, language: Language, user_id: str, validator_type: ValidatorType = ValidatorType.TESTCASE) -> Submission:
        results = []
        lang = language.name
        version = language.version
        for validator in self.puzzle.validators:
            if validator.validator_type == validator_type:
                result = piston.execute(language, version, code, validator.stdin, timeout=100)
                # TODO: deal with special cases

        # TODO:
        # => fetch puzzle code (validators)
        # => execute it in pistonapi
        # => remove users previous result from result list
        # => add result to result list
        # => return result
        raise NotImplementedError

    @property
    def end_time(self):
        # duration is a value representing the minutes
        # probably needs to be transformed and then added to start_time
        return self.start_time+self.gameroom_config.duration
