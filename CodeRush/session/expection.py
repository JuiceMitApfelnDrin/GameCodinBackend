from __future__ import annotations

from ..exceptions import CodeRushException


class SessionException(CodeRushException):
    pass

class InvalidMessageException(SessionException):
    pass