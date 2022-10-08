from bson.objectid import ObjectId

from GameCodin.puzzle.puzzle import Puzzle
from GameCodin.puzzle.puzzle_type import PuzzleType


# test query stuff from db
print("\nPuzzles by type")
print(Puzzle.get_by_type(PuzzleType.FASTEST))

print("\nPuzzles by author_id")
print(Puzzle.get_by_author(author_id=ObjectId("6333585a0b6e7d94a0c64ce3")))
