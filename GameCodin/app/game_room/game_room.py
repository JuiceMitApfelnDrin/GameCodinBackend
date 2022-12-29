from __future__ import annotations

from sanic import text, json
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId

from .. import app
from ..user import auth

from ...game_room import GameRoom
from ...message import Message, MessageType
from ...puzzle import Puzzle
from ...exceptions import GameCodinException


@app.get('/game')
async def game(request: Request):
    try:
        args = request.args
        if "id" not in args:
            return text("No game_id was provided", status=400)

        try:
            game = GameRoom.get_by_id(ObjectId(args["id"][0]))
        except InvalidId:
            # TODO remove after updating GameRoom API
            game = None
            
        # TODO remove after updating GameRoom API
        if game is None:
            return GameCodinException("Can't find game room")

        return json(game.as_dict())

    except GameCodinException as exception:
        return text(str(exception), status = 400)

@app.post('/game_join')
async def game_join(request: Request):
    try:
        user = auth(request)

        try:
            game = GameRoom.get_by_id(ObjectId(request.json["game_id"]))
        except InvalidId:
            # TODO remove after updating GameRoom API
            game = None

        # TODO: remove after updating GameRoom API
        if game is None:
            raise GameCodinException("Can't find game room")

        game.add_player(user)
        
        return json(game.as_dict())

    except GameCodinException as exception:
        return text(str(exception), status = 400)
