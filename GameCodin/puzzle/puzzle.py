from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, cast
from ..database import db_client
from ..database.collection import Collection

from ..puzzle.puzzle_type import PuzzleType
from .puzzle_difficulty import Difficulty
from bson.objectid import ObjectId
from .validator import Validator

from ..utils import asdict


@dataclass
class Puzzle:
    puzzle_id: ObjectId
    title: str
    statement: str
    constraints: str
    author_id: ObjectId
    validators: tuple[Validator]
    puzzle_types: list[PuzzleType]

    # default difficulty = medium
    # TODO: for version 0.2.0:
    # update difficulty based of percentage of people failing/passing in a game
    difficulty: Difficulty = Difficulty.MEDIUM

    @classmethod
    def create(cls, title, statement, constraints,
               author_id, validators, puzzle_types) -> Optional[Puzzle]:

        result = db_client[Collection.PUZZLE.value].insert_one(
            {
                "title": title,
                "statement": statement,
                "constraints": constraints,
                "author_id": author_id,
                "validators": validators,
                "puzzle_types": puzzle_types,
            }
        )

        return cls.get_by_id(result.inserted_id)

    @classmethod
    def from_dict(cls, info: dict) -> Puzzle:
        return cls(ObjectId(info.get("_id") or info["puzzle_id"]),
                   info["title"],
                   info["statement"],
                   info["constraints"],
                   info["author_id"],
                   info["validators"],
                   info["puzzle_types"])

    @property
    def dict(self) -> dict:
        return asdict(self)

    @classmethod
    def get_by_id(cls, user_id: ObjectId) -> Optional[Puzzle]:
        user_info = cls.__get_puzzle_info_from_db(user_id)
        if user_info is None:
            return
        return Puzzle.from_dict(user_info)

    @classmethod
    def __get_puzzle_info_from_db(cls, puzzle_id: ObjectId) -> Optional[dict]:
        return cast(dict, db_client[Collection.PUZZLE.value].find_one({"_id": puzzle_id}))

    @classmethod
    def get_by_author(cls, author_id: ObjectId) -> tuple[Puzzle]:
        cursor = db_client[Collection.PUZZLE.value].find(
            {"author_id": author_id})
        return tuple(map(Puzzle.from_dict, cursor))

    @classmethod
    def get_by_type(cls, puzzle_type: PuzzleType) -> Puzzle:
        """
        raises an error if there is no puzzles of that type
        """
        pipeline = [
            {
                "$match":
                    {
                        "puzzle_types": {
                            "$in": [puzzle_type.value]
                        }
                    }
            },
            {
                "$sample": {
                    "size": 1
                }
            },
        ]
        cursor = db_client[Collection.PUZZLE.value].aggregate(pipeline)
        return Puzzle.from_dict(cursor.next())
