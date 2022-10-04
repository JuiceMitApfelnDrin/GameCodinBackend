from __future__ import annotations

from bson.objectid import ObjectId

from ..message.message import Message
from GameCodin.message.message_type import MessageType


class GameRoomManager:
    _connections: set

    # active gamerooms => a list of users
    __active_gamerooms: dict[ObjectId, list[ObjectId]]

    @classmethod
    def join_game(cls, ws, game_room_id, user_id):
        """

        """
        user_ids = cls.__active_gamerooms.get(game_room_id)
        if (user_ids is None):
            return ws.send(Message(MessageType.GAME_NOT_FOUND, game_room_id))
        user_ids.append(user_id)
