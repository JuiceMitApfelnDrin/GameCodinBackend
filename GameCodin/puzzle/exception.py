__all__ = ("PuzzleException", )

from ..exceptions import GameCodinException

class PuzzleException(GameCodinException):
    pass

class PuzzleCreationException(PuzzleException):
    pass

class PuzzleFindException(PuzzleException):
    pass