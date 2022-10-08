from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, cast, ClassVar
from bson.objectid import ObjectId

from ..submission.submission import Submission
from ..puzzle.puzzle import Puzzle

from . import GameRoomState, GameRoomVisibility,GameRoomConfig

from ..message.message import Message
from ..message.message_type import MessageType

from ..user import Session, User
from ..user.session_expections import SessionException

from ..database import db_client
from ..database.collection import Collection

# TODO: for version 0.2.0:
# submitted_at: int => allow users to submit one last time after round ends?

@dataclass(eq=False, kw_only=True)
class GameRoom:
    class SubmissionException(Exception):
        """Exception that gets raised when adding a submission fails"""

    __active_gamerooms: ClassVar[dict[ObjectId, GameRoom]]

    _id: ObjectId
    creator: User
    config: GameRoomConfig
    puzzle: Puzzle

    start_time: datetime
    state: GameRoomState

    players: dict[ObjectId, User]
    submissions: dict[ObjectId, Submission]

    sessions: dict[User, list[Session]] = field(default_factory=dict)

    @classmethod
    def create(cls, *, creator: User, puzzle: Puzzle, config: GameRoomConfig, start_time: datetime) -> GameRoom:
        """
        Creates a new gameroom and store it in db. 
        """
        result = db_client[Collection.GAME.value].insert_one(
            {
                "creator_id": creator.id,
                "puzzle_id": puzzle.puzzle_id,
                "config": config.as_dict(),
                "start_time": start_time.isoformat(),
                "game_state": GameRoomState.WAITING_FOR_PLAYERS.name,
                "players_ids": [],
                "submissions_ids": []
            }
        )
        game_room = cls.get_from_db_by_id(result.inserted_id)
        assert game_room is not None
        return game_room

    @classmethod
    def get_by_id(cls, gameroom_id: ObjectId) -> Optional[GameRoom]:
        """
        Tries to find a GameRoom object with the given id from memory and db.
        Returns None if no active GameRoom with that id exists.
        """
        game_room = cls.get_active_gameroom(gameroom_id)
        if game_room is not None:
            return game_room

        return cls.get_from_db_by_id(gameroom_id)

    @classmethod
    def get_from_db_by_id(cls, gameroom_id: ObjectId) -> Optional[GameRoom]:
        """
        Tries to find a GameRoom object with the given id from memory.
        Returns None if no active GameRoom with that id exists.
        """
        info = cast(dict, db_client[Collection.GAME.value].find_one({"_id": gameroom_id}))

        creator = User.get_by_id(info["creator_id"])
        puzzle = Puzzle.get_by_id(info["puzzle_id"])
        assert creator is not None
        assert puzzle is not None

        players = {}
        for player_id in info["players_ids"]:
            player = User.get_by_id(player_id)
            assert player is not None
            players[player_id] = player

        submissions = {}
        for submission_id in info["submissions_ids"]:
            submission = User.get_by_id(submission_id)
            assert submission is not None
            submissions[submission_id] = submissions
        
        return cls(
            _id = info["_id"],
            config = GameRoomConfig.from_dict(info["config"]),
            creator = creator,
            puzzle = puzzle,
            start_time = datetime.fromisoformat(info["start_time"]),
            state = GameRoomState[info["state"]],
            players = players,
            submissions = submissions
        )

    @classmethod
    def get_active_gameroom(cls, gameroom_id: ObjectId) -> Optional[GameRoom]:
        """
        Tries to find a GameRoom object with the given id from memory.
        Returns None if no active GameRoom with that id exists
        (it may still exist in the database).
        """
        return cls.__active_gamerooms[gameroom_id]

    @property
    def id(self):
        return self._id

    @property
    def end_time(self) -> datetime:
        """Returns the end time """
        return self.start_time + timedelta(minutes=self.config.duration_minutes)

    def as_dict(self) -> dict:
        """
        Return a representation of the game room that can be inserted
        into a MongoDB collection using .insert_one() method.
        """
        return {
            "_id": self.id,
            "creator_id": self.creator.id,
            "config": self.config.as_dict(),
            "puzzle": self.puzzle.puzzle_id,
            "start_time": self.start_time.isoformat(),
            "submissions_ids": list(self.submissions.keys()),
            "players_ids": list(self.submissions.keys())
        }

    def add_session(self, session: Session):
        """
        Add session to gameroom
        """
        state = self.state
        visibility = self.config.visibility

        if not (state is GameRoomState.WAITING_FOR_PLAYERS or
                state is GameRoomState.IN_PROGRESS and
                visibility is GameRoomVisibility.PRIVATE):
            raise SessionException("Can't join, game already started!")

        user = session.user
        self.players[user.id] = user
        if user not in self.sessions:
            self.sessions[user] = []

        self.sessions[user].append(session)

    def remove_session(self, session: Session):
        """
        Remove session from gameroom
        """
        user = session.user
        if user.id not in self.players:
            raise SessionException("Can't remove session from Game: User is not in gameroom!")

        sessions = self.sessions[user]
        if session not in sessions:
            raise SessionException("Can't remove session from Game: Session is not in gameroom!")

        sessions.remove(session)

        if not sessions and self.state is GameRoomState.WAITING_FOR_PLAYERS:
            self.players[user.id] = user

    def remove_player(self, user: User):
        if user.id not in self.players:
            raise SessionException("Can't remove player from Game: User is not in gameroom!")

        if not self.state is GameRoomState.WAITING_FOR_PLAYERS:
            raise SessionException("Can't remove player from Game: Game has already started!")
        
        del self.players[user.id]
        del self.sessions[user]

    def add_submission(self, submission: Submission):
        """
        Adds a new submission to the game room. The submission should
        be validated and scored before adding it to the game room.
        Raises an exception when trying to add a submission while the
        game is not in progress.
        """
        state = self.state
        if state == GameRoomState.WAITING_FOR_PLAYERS:
            raise GameRoom.SubmissionException(
                "Can't add submission: Game hasn't started yet!")
        if state == GameRoomState.FINISHED:
            raise GameRoom.SubmissionException(
                "Can't add submission: Game is already finalized!")
        self.submissions[submission.id] = submission

    def launch_game(self, start_time: datetime | None = None):
        """
        Sets the start time for the game to current datetime.
        After calling the game room starts accepting submissions.
        Called when the host decides the game has enough players to start.
        """
        if start_time is None:
            self.start_time = datetime.now()
        else:
            self.start_time = start_time