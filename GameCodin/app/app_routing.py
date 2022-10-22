from sanic import text, json
from sanic.request import Request

from ..game_room import GameRoom
from ..message import Message, MessageType
from ..puzzle import Puzzle
from ..user import User

from bson.objectid import ObjectId
from bson.errors import InvalidId

from . import app
from . import user

@app.get('/game')
async def game(request: Request):
    args = request.args
    if "id" not in args:
        return text("No game_id was provided", status=400)

    try:
        game = GameRoom.get_by_id(ObjectId(args["id"][0]))
    except InvalidId:
        game = None
        
    if game is None:
        return text("Can't find user", status=400)

    return json(game.as_dict())
# XXX: maybe we should seperate this to differnt modules
# And put them in their respective folders for exemple users/user_routing.py etc..
# Or just put them here, and import all of them to here

# TODO: add errors system similar to that of session_execeptions
# Or generalize session_exeception to work here too


@app.get('/puzzles')
async def puzzle(request: Request):
    args = request.args
    if "id" in args:
        try:
            puzzle = Puzzle.get_by_id(ObjectId(args["id"][0]))
        except InvalidId:
            puzzle = None
        if puzzle is None:
            return text("Can't find puzzle", status=400)
        # TODO: check if we should send the solution/validators
        return json(puzzle.as_dict())

    elif "author_id" in args:
        try:
            # XXX: we might want to check if author_id is valid here
            # and return error if not
            puzzles = Puzzle.get_by_author(ObjectId(args["author_id"][0]))
        except InvalidId:
            return text("Invalid author_id", status=400)
        return json([puzzle.as_dict() for puzzle in puzzles])
        
    else:
        return text("No puzzle_id/author_id was provided",status=400)
