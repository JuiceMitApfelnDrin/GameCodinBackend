from __future__ import annotations

from dataclasses import dataclass, asdict, field
from ..database import db_client
from ..database.collection import Collection

from ..puzzle.puzzle_type import PuzzleType
from .puzzle_difficulty import Difficulty
from bson.objectid import ObjectId
from .validator import Validator


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
    # TODO: for version 2.0:
    # update difficulty based of percentage of people failing/passing in a game
    difficulty: Difficulty = Difficulty.MEDIUM

    @classmethod
    def create(
        cls,
        title,
        statement,
        constraints,
        author_id,
        validators,
        puzzle_types
    ):
        db_client[Collection.PUZZLE.value].insert_one(
            {
                "title": title,
                "statement": statement,
                "constraints": constraints,
                "author_id": author_id,
                "validators": validators,
                "puzzle_types": puzzle_types,
            }
        )

    @property
    def dict(self):
        return asdict(self)

    @classmethod
    def get_by_id(cls, puzzle_id: ObjectId) -> Puzzle:

        raise NotImplementedError

    @classmethod
    def get_by_type(cls, puzzle_type: PuzzleType) -> Puzzle:
        pipeline = [
            {
                "$match":
                    {
                        "$expr": {
                            "$in": ["$puzzle_types", [puzzle_type.value]]
                        }
                    }
            },
            {
                "$sample": {
                    "size": 1
                }
            },
        ]
        db_client[Collection.PUZZLE.value].aggregate(pipeline)
        raise NotImplementedError
