import logging
from bson.objectid import ObjectId
from GameCodin.puzzle.validator_type import ValidatorType

from GameCodin.user.user import User
from GameCodin.database import db_client
from GameCodin.puzzle.puzzle import Puzzle
from GameCodin.puzzle.puzzle_type import PuzzleType
from GameCodin.puzzle.validator import Validator

from pymongo.errors import DuplicateKeyError

# example users insert stuff, test data

def create_user(nickname: str, email: str, password: str) -> tuple[User, str] | None:
    try:
        return User.create(
            nickname,
            email,
            password
        )
    except DuplicateKeyError as duplicate_error:
        details = duplicate_error.details
        if details is None:
            raise TypeError("Can't get duplicate_error details", duplicate_error)

        keys = ', '.join(details["keyPattern"])
        
        if len(details["keyPattern"]) > 1:
            error_message = keys + " are taken"
        else:
            error_message = keys + " is taken"

        logging.log(logging.WARN, error_message)        

def create_puzzle(title: str, statement: str, constraints: str, validators: list[Validator], puzzle_types: list[PuzzleType], author_id: ObjectId) -> Puzzle | None:
    try:
        return Puzzle.create(
            title = title,
            statement = statement,
            constraints = constraints,
            validators = validators,
            puzzle_types = puzzle_types,
            author_id = author_id
        )
    except DuplicateKeyError as duplicate_error:
        details = duplicate_error.details
        if details is None:
            raise TypeError("Can't get duplicate_error details", duplicate_error)

        keys = ', '.join(details["keyPattern"])
        
        if len(details["keyPattern"]) > 1:
            error_message = keys + " are taken"
        else:
            error_message = keys + " is taken"

        logging.log(logging.WARN, error_message)        


create_user(
    "Gorn10",
    "Gorn10@dings.com",
    "passw"
)

puzzle_author = User.get_by_nickname("Gorn10")
assert puzzle_author is not None

create_user(
    "Hydrazer",
    "hydrazer@dings.com",
    "passw"
)

create_user(
    "jutyve",
    "jutyve@dings.com",
    "passw"
)

create_user(
    "murat",
    "murat@dings.com",
    "passw"
)

create_user(
    "chief",
    "chief@dings.com",
    "passw"
)

create_user(
    "muumijumala",
    "muumijumala@dings.com",
    "passw"
)

create_user(
    "kanawanagasakiyoko",
    "kanawanagasakiyoko@dings.com",
    "passw"
)

# example puzzle insert stuff, test data
create_puzzle(
    title="FizzBuzz",
    statement="Print numbers from 1 to N, but if the number is divisible by F, print \"Fizz\", and if the number is divisible by B print \"Buzz\". If it is divisible by both print \"FizzBuzz\".",
    constraints="N lines",
    validators=[
        Validator(validator_type=ValidatorType.TESTCASE, input="7 2 3",
                  output="1\nFizz\nBuzz\nFizz\n5\nFizzBuzz\n7"),
        Validator(validator_type=ValidatorType.TESTCASE, input="3 1 1",
                  output="FizzBuzz\nFizzBuzz\nFizzBuzz"),
        Validator(validator_type=ValidatorType.TESTCASE, input="10 11 12",
                  output="1\n2\n3\n4\n5\n6\n7\n8\n9\n10"),
    ],
    puzzle_types=[PuzzleType.SHORTEST,
                  PuzzleType.FASTEST, PuzzleType.REVERSE],
    author_id=ObjectId(puzzle_author.id)
)
