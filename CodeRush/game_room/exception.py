from __future__ import annotations

__all__ = ("GameRoomException", "GameLaunchException")

from ..exceptions import CodeRushException

class GameRoomException(CodeRushException):
    pass

class GameLaunchException(CodeRushException):
    pass