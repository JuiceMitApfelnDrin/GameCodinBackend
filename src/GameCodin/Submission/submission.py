from dataclasses import dataclass
from bson.objectid import ObjectId


@dataclass
class Submission:
    game_room_id: ObjectId
    puzzle_id: ObjectId
    user_id: ObjectId
    failed_validators_ids: set[ObjectId]
    succeeded_validators_ids: set[ObjectId]
    code: str

    # TODO: for version 2.0:
    # submitted_at: int => allow users to submit one last time after round ended?
