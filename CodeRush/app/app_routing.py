from sanic import text, json
from sanic.request import Request

from ..game_room import GameRoom
from ..message import Message, MessageType
from ..puzzle import Puzzle
from ..exceptions import CodeRushException

from .user.user import User

from bson.objectid import ObjectId
from bson.errors import InvalidId

from . import app

from . import exception_handler
from . import user
from . import game_room
from . import ide


@app.get('/puzzles')
async def puzzle(request: Request):
    args = request.args

    if "id" in args:
        try:
            puzzle_id = ObjectId(args["id"][0])
        except InvalidId:
            raise CodeRushException("Invalid puzzle id")

        puzzle = Puzzle.get_by_id(puzzle_id)
        return json(puzzle.as_dict())

    if "author_id" in args:
        try:
            author_id = ObjectId(args["author_id"][0])
        except InvalidId:
            raise CodeRushException("Invalid user id")
        
        puzzles = Puzzle.get_by_author(author_id)
        return json([puzzle.as_dict() for puzzle in puzzles])
        
    raise CodeRushException("No puzzle_id/author_id was provided")
