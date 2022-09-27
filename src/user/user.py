from dataclasses import dataclass, asdict, field
from typing import Dict


@dataclass
class User:
    username: str
    email: str

    profile: Dict = field(default_factory=dict)
    rank: Dict = field(default_factory=dict)

    @property
    def dict(self):
        return asdict(self)
