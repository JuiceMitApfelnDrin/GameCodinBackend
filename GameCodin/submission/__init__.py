__all__ = ["piston", "Submission", "Language", "submissions_collection"]

from pistonapi import PistonAPI
from typing import Final

piston: Final = PistonAPI()

from .collection import submissions_collection
from .language import Language
from .submission import Submission