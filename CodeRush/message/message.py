from dataclasses import asdict, dataclass, field
from .message_type import MessageType
import json

@dataclass
class Message:
    type: MessageType
    content: object
    value: str = ""

    def __post_init__(self):
        if self.value:
            return

        self.value = json.dumps({
            "type": self.type.value,
            "content": self.content
        })

    def from_str(self, value: str):
        message_dict = json.loads(value)
        
        if not isinstance(message_dict,dict) or\
            message_dict.keys() != {"type","content"}:
            raise ValueError

        return Message(
            message_dict["type"],
            message_dict["content"],
            value
        )