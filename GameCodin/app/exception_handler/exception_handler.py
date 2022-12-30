from __future__ import annotations

from sanic import text, json
from sanic.response import HTTPResponse
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId

from .. import app

from ...exceptions import GameCodinException


@app.exception(GameCodinException)
def gamecoding_error(request: Request, exception: Exception):
    return text(str(exception), status = 400)

@app.exception(Exception)
def internal_error(request: Request, exception: Exception):
    return text("Internal Error", status = 400)

