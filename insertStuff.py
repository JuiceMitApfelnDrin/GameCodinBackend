from puzzle import Puzzle
from user import User
from get_databases_client import get_database
dbname = get_database()

# example users insert stuff, test data
collection_name = dbname["users"]

item_1 = User(
    "juicemitapfelndrin",
    "juicemitapfelndrin@dings.com"
)
item_2 = User(
    "Gorn10",
    "Gorn10@dings.com"
)
item_3 = User(
    "Hydrazer",
    "hydrazer@dings.com"
)
item_4 = User(
    "jutyve",
    "jutyve@dings.com"
)

collection_name.insert_many(
    [
        item_1.dict,
        item_2.dict,
        item_4.dict,
        item_3.dict
    ]
)

# example puzzle insert stuff, test data
collection_name = dbname["puzzle"]

item_1 = Puzzle("FizzBuzz", {
    "title": "FizzBuzz",
    "statement": "Print numbers from 1 to N, but if the number is divisible by F, print \"Fizz\", and if the number is divisible by B print \"Buzz\". If it is divisible by both print \"FizzBuzz\".",
    "inputDescription": "Three numbers N, F and B separated by a single space",
    "outputDescription": "N lines",
    "tests": [
        {"input": "7 2 3", "output": "1\\nFizz\\nBuzz\\nFizz\\n5\\nFizzBuzz\\n7"},
        {"input": "3 1 1", "output": "FizzBuzz\\nFizzBuzz\\nFizzBuzz"},
        {"input": "10 11 12", "output": "1\\n2\\n3\\n4\\n5\\n6\\n7\\n8\\n9\\n10"}
    ]
})

collection_name.insert_many(
    [
        item_1.dict
    ]
)
