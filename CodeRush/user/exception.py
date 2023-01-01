__all__ = ("UserException", "UserCreationException", "UserFindException", "UserAuthException")

from ..exceptions import CodeRushException

class UserException(CodeRushException):
    pass

class UserCreationException(UserException):
    pass

class UserFindException(UserException):
    pass

class UserAuthException(UserException):
    pass