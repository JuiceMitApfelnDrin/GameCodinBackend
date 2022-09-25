from dataclasses import dataclass, asdict

from puzzle.puzzle_difficulty import Difficulty


@dataclass
class Puzzle:
    title: str
    json: dict

    puzzle: Difficulty = Difficulty.HARD

    @property
    def dict(self):
        return asdict(self)
