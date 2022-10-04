from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from time import time
from typing import Optional, cast
from bson.objectid import ObjectId

from ..database.collection import Collection
from ..database import db_client
from .language import Language

from ..utils import asdict


@dataclass
class Submission:
    _id: ObjectId
    puzzle_id: ObjectId
    user_id: ObjectId
    code: str
    language: Language
    submitted_at: datetime

    validators: list[bool] = field(default_factory=list)
    execution_finished: bool = False
    _max_code_size = 9001

    @property
    def id(self):
        return self._id

    @classmethod
    def create(cls, user_id, puzzle_id, language: Language, code) -> Optional[Submission]:
        timestamp = datetime.now().isoformat()
        result = db_client[Collection.SUBMISSION.value].insert_one(
            {
                "user_id": user_id,
                "puzzle_id": puzzle_id,
                "language": language.name,
                "code": code,
                "submitted_at": timestamp
            }
        )
        submission = Submission.get_by_id(result.inserted_id)
        return submission

    @classmethod
    def get_by_id(cls, submission_id: ObjectId) -> Optional[Submission]:
        submission_info = cls.__get_user_info_from_db(submission_id)
        if submission_info is None:
            return
        return Submission.from_dict(submission_info)

    @classmethod
    def __get_user_info_from_db(cls, submission_id: ObjectId) -> Optional[dict]:
        return cast(dict, db_client[Collection.SUBMISSION.value].find_one({"_id": submission_id}))

    @classmethod
    def from_dict(cls, info: dict) -> Submission:
        return cls(
            ObjectId(info["_id"]),
            ObjectId(info["puzzle_id"]),
            ObjectId(info["user_id"]),
            info["code"],
            Language.get(info["language"]),
            datetime.fromisoformat(info["submitted_at"])
        )

    async def execute_testcases(self, puzzle):
        # execute for each validator the code
        # aka does the code work or not for a given Validator?
        assert puzzle is not None
        for validator in puzzle.validators:
            success, _ = await validator.execute(self.code, self.language)
            self.validators.append(success)

        self.execution_finished = True

    @property
    def score(self) -> Optional[float]:
        if not self.execution_finished:
            return None
        return sum(self.validators)/len(self.validators)

    @property
    def dict(self):
        return asdict(self)

    @property
    def time(self) -> datetime:
        return self.submitted_at

    @property
    def code_size(self) -> int:
        return len(self.code)
