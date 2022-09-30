

from bson.objectid import ObjectId

from src.GameCodin.database import db_client
from src.GameCodin.puzzle.puzzle import Puzzle
from src.GameCodin.puzzle.puzzle_type import PuzzleType

# example users insert stuff, test data
collection_name = db_client["users"]

# item_1 = User(
#     "juicemitapfelndrin",
#     "juicemitapfelndrin@dings.com"
# )
# item_2 = User(
#     "Gorn10",
#     "Gorn10@dings.com"
# )
# item_3 = User(
#     "Hydrazer",
#     "hydrazer@dings.com"
# )
# item_4 = User(
#     "jutyve",
#     "jutyve@dings.com"
# )
# item_5 = User(
#     "murat",
#     "murat@dings.com"
# )
# item_6 = User(
#     "chief",
#     "chief@dings.com"
# )


# collection_name.insert_many(
#     [
#         item_1.dict,
#         item_2.dict,
#         item_3.dict,
#         item_4.dict,
#         item_5.dict,
#         item_6.dict,
#     ]
# )

# example puzzle insert stuff, test data
# collection_name = db_client["puzzle"]

item_1 = Puzzle.create(
    title="FizzBuzz",
    author_id=ObjectId("6333585a0b6e7d94a0c64ce3"),
    statement="Print numbers from 1 to N, but if the number is divisible by F, print \"Fizz\", and if the number is divisible by B print \"Buzz\". If it is divisible by both print \"FizzBuzz\".",
    constraints=["N lines"],
    puzzle_types=[PuzzleType.SHORTEST.value,
                  PuzzleType.FASTEST.value, PuzzleType.REVERSE.value],
    validators=[
        {"input": "7 2 3",
         "output": "1\\nFizz\\nBuzz\\nFizz\\n5\\nFizzBuzz\\n7"},
        {"input": "3 1 1", "output": "FizzBuzz\\nFizzBuzz\\nFizzBuzz"},
        {"input": "10 11 12",
         "output": "1\\n2\\n3\\n4\\n5\\n6\\n7\\n8\\n9\\n10"}
    ]
)

# test query stuff from db
print(Puzzle.get_by_type(PuzzleType.FASTEST))