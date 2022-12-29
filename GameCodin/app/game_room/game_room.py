from __future__ import annotations

from sanic import text, json
from sanic.response import HTTPResponse
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId

from .. import app
from ..user import auth

from ...game_room import GameRoom
from ...message import Message, MessageType
from ...puzzle import Puzzle
from ...exceptions import GameCodinException


@app.get('/game_info')
async def game_info(request: Request) -> HTTPResponse:
    try:
        args = request.args
        if "id" not in args:
            return text("No game_id was provided", status=400)

        game = GameRoom.get_by_id(ObjectId(args["id"][0]))

        return json(game.as_dict())

    except GameCodinException as exception:
        return text(str(exception), status = 400)


@app.post('/game_join')
async def game_join(request: Request) -> HTTPResponse:
    try:
        user = auth(request)

        game = GameRoom.get_by_id(ObjectId(request.json["game_id"]))
        game.add_player(user)
        
        return json(game.as_dict())

    except GameCodinException as exception:
        return text(str(exception), status = 400)


@app.post('/game_leave')
async def game_leave(request: Request) -> HTTPResponse:
    try:
        user = auth(request)

        game = GameRoom.get_by_id(ObjectId(request.json["game_id"]))
        game.remove_player(user)
        
        return HTTPResponse()

    except GameCodinException as exception:
        return text(str(exception), status = 400)