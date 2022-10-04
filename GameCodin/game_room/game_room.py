from __future__ import annotations
from datetime import datetime
from datetime import timedelta
from typing import ClassVar
from dataclasses import dataclass, field

from bson.objectid import ObjectId

from ..submission.submission import Submission
from ..puzzle.puzzle import Puzzle
from .config import GameRoomConfig
from .state import GameRoomState


# TODO: for version 0.2.0:
# submitted_at: int => allow users to submit one last time after round ends?

@dataclass(eq=False, kw_only=True)
class GameRoom:
    class SubmissionException(Exception):
        """Exception that gets raised when adding a submission fails"""

    __active_gamerooms: ClassVar[dict[ObjectId, GameRoom]]

    game_room_id: ObjectId = field(default_factory=ObjectId)
    creator_id: ObjectId
    configuration: GameRoomConfig
    puzzle: Puzzle

    # this should give the host enough time to launch the game
    start_time: datetime = field(default_factory=lambda: datetime(6969, 6, 9))

    submissions: dict[ObjectId, Submission] = field(default_factory=dict)

    finished: bool = field(repr=False, default=False)

    @classmethod
    def create(
            cls,
            *,
            creator_id: ObjectId,
            puzzle: Puzzle,
            config: GameRoomConfig
    ):
        new_room_id = ObjectId()
        new_room = cls(
            game_room_id=new_room_id,
            creator_id=creator_id,
            configuration=config,
            puzzle=puzzle
        )
        cls.__active_gamerooms[new_room_id] = new_room
        return new_room

    @classmethod
    def get_active_gameroom(cls, gameroom_id: ObjectId) -> GameRoom:
        """
        Tries to find a GameRoom object with the given id from memory.
        Raises an exception if a GameRoom with that id does not exist in
        memory (it may still exist in the database).
        """
        return cls.__active_gamerooms[gameroom_id]

    @property
    def dict(self) -> dict:
        """
        Return a representation of the game room that can be inserted
        into a MongoDB collection using .insert_one() method.
        """
        return {
            "_id": self.game_room_id,
            "creator_id": self.creator_id,
            "configuration": self.configuration.as_dict(),
            "puzzle": self.puzzle.puzzle_id,
            "start_time": self.start_time.isoformat(),
            "submissions": list(self.submissions.keys()),
        }

    @property
    def end_time(self) -> datetime:
        """Returns the end time """
        return self.start_time + timedelta(minutes=self.configuration.duration_minutes)

    def add_submission(self, submission: Submission):
        """
        Adds a new submission to the game room. The submission should
        be validated and scored before adding it to the game room.
        Raises an exception when trying to add a submission while the
        game is not in progress.
        """
        state = self.state()
        if state == GameRoomState.WAITING_FOR_PLAYERS:
            raise GameRoom.SubmissionException(
                "Can't add submission: Game hasn't started yet!")
        if state == GameRoomState.FINISHED:
            raise GameRoom.SubmissionException(
                "Can't add submission: Game is already finalized!")
        self.submissions[submission.id] = submission

    def finalize(self):
        """
        This method should be called when all submissions have been processed.
        After finalizing no new submissions can be added
        """
        self.finished = True

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

    def state(self) -> GameRoomState:
        """
        Returns the state of the game room.
        WAITING_FOR_PLAYERS = the game has not started yet
        IN_PROGRESS = the game has started and it is accepting submissions
        PROCESSING_FINAL_SUBMISSIONS = game has ended but there are still submissions in queue
        FINISHED = game has ended and no new submissions are accepted
        """
        now = datetime.now()
        if self.finished:
            return GameRoomState.FINISHED
        if now < self.start_time:
            return GameRoomState.WAITING_FOR_PLAYERS
        if now < self.end_time:
            return GameRoomState.IN_PROGRESS
        return GameRoomState.PROCESSING_FINAL_SUBMISSIONS
