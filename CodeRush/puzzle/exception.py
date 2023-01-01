__all__ = ("PuzzleException", )

from ..exceptions import CodeRushException

class PuzzleException(CodeRushException):
    pass

class PuzzleCreationException(PuzzleException):
    pass

class PuzzleFindException(PuzzleException):
    pass