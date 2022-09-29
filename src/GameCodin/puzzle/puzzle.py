from dataclasses import dataclass, asdict

from GameCodin.puzzle.puzzle_type import PuzzleType
from .puzzle_difficulty import Difficulty
from bson.objectid import ObjectId
from .validator import Validator


@dataclass
class Puzzle:
    puzzle_id: ObjectId
    puzzle_types: list[PuzzleType]
    title: str
    statement: str
    constraints: str
    author_id: ObjectId
    validators: tuple[Validator]

    # default difficulty = medium
    # TODO: for version 2.0:
    # update difficulty based of percentage of people failing/passing in a game
    difficulty: Difficulty = Difficulty.MEDIUM

    @property
    def dict(self):
        return asdict(self)
