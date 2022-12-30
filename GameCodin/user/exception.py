__all__ = ("UserException", "UserCreationException", "UserFindException", "UserAuthException")

from ..exceptions import GameCodinException

class UserException(GameCodinException):
    pass

class UserCreationException(UserException):
    pass

class UserFindException(UserException):
    pass

class UserAuthException(UserException):
    pass