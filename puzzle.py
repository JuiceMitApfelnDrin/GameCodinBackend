from dataclasses import dataclass, asdict


@dataclass
class Puzzle:
    title: str
    json: str

    @property
    def dict(self):
        return asdict(self)
