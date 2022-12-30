__all__ = ("PuzzleException", )

from ..exceptions import GameCodinException

class PuzzleException(GameCodinException):
    pass

class PuzzleFindException(PuzzleException):
    pass