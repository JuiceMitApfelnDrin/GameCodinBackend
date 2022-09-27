from dataclasses import dataclass, asdict, field


@dataclass
class User:
    username: str
    email: str

    profile: dict = field(default_factory=dict)
    rank: dict = field(default_factory=dict)

    @property
    def dict(self):
        return asdict(self)
