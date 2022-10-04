from dataclasses import asdict, dataclass

from .message_type import MessageType


@dataclass
class Message:
    type: MessageType
    content: dict

    @property
    def dict(self) -> dict:
        return asdict(self)
