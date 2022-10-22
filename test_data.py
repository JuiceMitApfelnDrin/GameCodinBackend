# from bson.objectid import ObjectId

# from GameCodin.user.user import User
# from GameCodin.database import db_client
# from GameCodin.database.collection import Collection
# from GameCodin.puzzle.puzzle import Puzzle
# from GameCodin.puzzle.puzzle_type import PuzzleType
# from GameCodin.puzzle import validator

# # example users insert stuff, test data
# collection_name = db_client[Collection.USERS.value]

# User.create(
#     "juicemitapfelndrin",
#     "juicemitapfelndrin@dings.com",
#     "passw"
# )
# User.create(
#     "Gorn10",
#     "Gorn10@dings.com"
# )
# User.create(
#     "Hydrazer",
#     "hydrazer@dings.com"
# )
# User.create(
#     "jutyve",
#     "jutyve@dings.com"
# )
# User.create(
#     "murat",
#     "murat@dings.com"
# )
# User.create(
#     "chief",
#     "chief@dings.com",
# )

# # example puzzle insert stuff, test data
# # collection_name = db_client["puzzle"]


# User.create(
#     "muumijumala",
#     "muumijumala@dings.com",
# )
# User.create(
#     "kanawanagasakiyoko",
#     "kanawanagasakiyoko@dings.com",
# )

# # example puzzle insert stuff, test data
# item_1 = Puzzle.create(
#     title="FizzBuzz",
#     author_id=ObjectId("6333585a0b6e7d94a0c64ce3"),
#     statement="Print numbers from 1 to N, but if the number is divisible by F, print \"Fizz\", and if the number is divisible by B print \"Buzz\". If it is divisible by both print \"FizzBuzz\".",
#     constraints="N lines",
#     puzzle_types=[PuzzleType.SHORTEST,
#                   PuzzleType.FASTEST, PuzzleType.REVERSE],

#     # TODO: change those with validators
#     validators=[
#         {"input": "7 2 3",
#          "output": "1\\nFizz\\nBuzz\\nFizz\\n5\\nFizzBuzz\\n7"},
#         {"input": "3 1 1", "output": "FizzBuzz\\nFizzBuzz\\nFizzBuzz"},
#         {"input": "10 11 12",
#          "output": "1\\n2\\n3\\n4\\n5\\n6\\n7\\n8\\n9\\n10"}
#     ]
# )


