from ..exceptions import GameCodinException

__all__ = ("UserException", "UserCreationException", "UserFindException", "UserAuthException")

class UserException(GameCodinException):
    pass

class UserCreationException(UserException):
    pass

class UserFindException(UserException):
    pass

class UserAuthException(UserException):
    pass