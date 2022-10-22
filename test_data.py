from bson.objectid import ObjectId
from GameCodin.puzzle.validator_type import ValidatorType

from GameCodin.user.user import User
from GameCodin.database import db_client
from GameCodin.puzzle.puzzle import Puzzle
from GameCodin.puzzle.puzzle_type import PuzzleType
from GameCodin.puzzle.validator import Validator

# example users insert stuff, test data
User.create(
    "juicemitapfelndrin",
    "juicemitapfelndrin@dings.com",
    "passw"
)
puzzleAuthor, _ = User.create(
    "Gorn10",
    "Gorn10@dings.com",
    "passw"
)
User.create(
    "Hydrazer",
    "hydrazer@dings.com",
    "passw"
)
User.create(
    "jutyve",
    "jutyve@dings.com",
    "passw"
)
User.create(
    "murat",
    "murat@dings.com",
    "passw"
)
User.create(
    "chief",
    "chief@dings.com",
    "passw"
)
User.create(
    "muumijumala",
    "muumijumala@dings.com",
    "passw"
)
User.create(
    "kanawanagasakiyoko",
    "kanawanagasakiyoko@dings.com",
    "passw"
)

# example puzzle insert stuff, test data
Puzzle.create(
    title="FizzBuzz",
    author_id=ObjectId(puzzleAuthor.id),
    statement="Print numbers from 1 to N, but if the number is divisible by F, print \"Fizz\", and if the number is divisible by B print \"Buzz\". If it is divisible by both print \"FizzBuzz\".",
    constraints="N lines",
    puzzle_types=[PuzzleType.SHORTEST,
                  PuzzleType.FASTEST, PuzzleType.REVERSE],
    validators=[
        Validator(validator_type=ValidatorType.TESTCASE, input="7 2 3",
                  output="1\nFizz\nBuzz\nFizz\n5\nFizzBuzz\n7"),
        Validator(validator_type=ValidatorType.TESTCASE, input="3 1 1",
                  output="FizzBuzz\nFizzBuzz\nFizzBuzz"),
        Validator(validator_type=ValidatorType.TESTCASE, input="10 11 12",
                  output="1\n2\n3\n4\n5\n6\n7\n8\n9\n10"),
    ]
)
