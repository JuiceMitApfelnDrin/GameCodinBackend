from __future__ import annotations

__all__ = ("GameRoomException", "GameLaunchException")

from ..exceptions import GameCodinException

class GameRoomException(GameCodinException):
    pass

class GameLaunchException(GameCodinException):
    pass