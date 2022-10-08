__all__ = ["piston", "Submission", "Language"]

from .submission import Submission
from .language import Language

from pistonapi import PistonAPI
from typing import Final

piston: Final = PistonAPI()
