from dataclasses import dataclass, asdict
from .puzzle_difficulty import Difficulty
from .validator import Validator

@dataclass
class Puzzle:
    title: str
    statement: str
    constraints: str
    author_id: int
    validators: tuple[Validator]
    difficulty: Difficulty = Difficulty.MEDIUM

    @property
    def dict(self):
        return asdict(self)
