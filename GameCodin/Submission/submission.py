from dataclasses import asdict, dataclass
from bson.objectid import ObjectId


@dataclass
class Submission:
    game_room_id: ObjectId
    puzzle_id: ObjectId
    user_id: ObjectId
    validators_success: list[bool]
    code: str
    execution_finished: bool

    # TODO: for version 2.0:
    # submitted_at: int => allow users to submit one last time after round ended?

    @property
    def dict(self):
        return asdict(self)