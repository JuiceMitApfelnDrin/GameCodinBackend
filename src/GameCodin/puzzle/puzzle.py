from dataclasses import dataclass, asdict
from .puzzle_difficulty import Difficulty


@dataclass
class Puzzle:
    title: str
    statement: str
    constraints: str
    author: str
    testcases: list[testcase]
    difficulty: Difficulty = Difficulty.MEDIUM


    @property
    def dict(self):
        return asdict(self)
