from sanic import text, json
from sanic.request import Request

from ..puzzle.puzzle import Puzzle
from ..puzzle.puzzle_type import PuzzleType

from ..user.user import User
from bson.objectid import ObjectId
from bson.errors import InvalidId

from . import app

# XXX: maybe we should seperate this to differnt modules
# And put them in their respective folders for exemple users/user_routing.py etc..
# Or just put them here, and import all of them to here

# TODO: add errors system similar to that of session_execpetions
# Or generalize session_execpetion to work here too

@app.get('/users')
async def users(request: Request):
    args = request.args
    if "id" not in args:
        return json({"error":"No user_id was provided"})

    try:
        user = User.get_by_id(ObjectId(args["id"][0]))
    except InvalidId:
        user = None
        
    if user is None:
        return json({"error":"Can't find user"})

    return json(user.dict)


# @app.get('/game')
# async def game(request: Request):
#     args = request.args
#     if "id" not in args:
#         return text("No game_id was provided :(")

#     # game = GameRoom.get_by_id(ObjectId(args["id"][0]))
#     # if game is None:
#     #     return text("Can't find user :(")
    # return json(game.dict)


@app.get('/puzzle')
async def puzzle(request: Request):
    args = request.args
    if "id" in args:
        try:
            puzzle = Puzzle.get_by_id(ObjectId(args["id"][0]))
        except InvalidId:
            puzzle = None
        if puzzle is None:
            return json({"error":"Can't find puzzle"})
        return json(puzzle.dict)
    elif "author_id" in args:
        try:
            # XXX: we might want to check if author_id is valid here
            # and return error if not
            puzzles = Puzzle.get_by_author(ObjectId(args["author_id"][0]))
        except InvalidId:
            return json({"error":"Invalid author_id"})
        return json([puzzle.dict for puzzle in puzzles])
    else:
        return json({"error":"No puzzle_id/author_id was provided"})