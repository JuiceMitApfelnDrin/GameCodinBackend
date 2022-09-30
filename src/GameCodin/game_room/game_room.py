from __future__ import annotations
import collections
from typing import ClassVar
from bson.objectid import ObjectId
from dataclasses import dataclass, asdict, field
from pistonapi.exceptions import PistonError

from .game_language import Language
from .game_room_visibility import Visibility
from ..Submission.submission import Submission
from ..app.app_routing import puzzle
from ..database import db_client
from ..database.collection import Collection
from ..puzzle.puzzle import Puzzle
from ..puzzle.validator_type import ValidatorType
from ..user.user import User
from ..user.session import Session
from ..user.session_expections import SessionException
from ..puzzle.validator import Validator

from .game_room_config import GameRoomConfig
from .game_room_state import State
from . import piston


@dataclass
class GameRoom:
    __active_gamerooms: ClassVar[dict[ObjectId,GameRoom]]

    game_room_id: ObjectId
    puzzle: Puzzle
    creator_id: ObjectId
    start_time: int
    gameroom_config: GameRoomConfig

    # ObjectId here is the player's ObjectId,
    # Submission doesn't ahve objectid for the moment
    # Using player's objectid because we 
    # want to get player's submission easier to check
    # If they submited code or not
    submissions: dict[ObjectId, Submission] = field(default_factory=dict)
    players: dict[ObjectId, User] = field(default_factory=dict)

    # TODO: add spectators to sessions.
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

    async def submit(self, code: str, language: Language, user_id: str):
        if user_id not in self.players:
            # TODO: add error message
            raise SessionException("")

        if self.gameroom_config.state is State.STARTING:
            # TODO: add error message
            raise SessionException("")
        
        # TODO: add a special case: player can submit old code
        if self.gameroom_config.state is State.FINISHING:
            # TODO: add error message
            raise SessionException("")

        if self.gameroom_config.state is State.FINISHED:
            # TODO: add error message
            raise SessionException("")

        if user_id in self.submissions:
            # TODO: add error message
            raise SessionException("")

        # TODO: fix
        # We need this to lock players from submitting mutliple times.
        # that creates a problem because the frontend doesn't now anymore if the player finished the submit me or not.
        # For that we need to add a state to Submission.
        submission = Submission(self.game_room_id, self.puzzle.puzzle_id, user_id, [], code)
        self.submissions[user_id] = submission

        for validator in self.puzzle.validators:
            if validator.validator_type is ValidatorType.VALIDATOR:
                success, _ = await validator.execute(code, language)
                submission.validators_success.append(success)

        # TODO: send to all sessions the results 

    async def execute_testcase(self, code: str, language: Language, validator_id: int) -> tuple[bool, str]:
        validator = self.puzzle.validators[validator_id]

        if validator.validator_type is ValidatorType.VALIDATOR:
            # TODO: add error message
            # Player trying to trick us monkaS
            raise SessionException("")

        return await validator.execute(code, language)

    @property
    def end_time(self):
        # duration is a value representing the minutes
        # probably needs to be transformed and then added to start_time
        return self.start_time+self.gameroom_config.duration
