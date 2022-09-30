from sanic.server.websockets.impl import WebsocketImplProtocol
from sanic.request import Request
from typing import Final
from sanic import Sanic
from sanic.response import text
from . import app
from ..user.user import User
from ..user.session import Session

app.config.WEBSOCKET_MAX_SIZE = 64
app.config.WEBSOCKET_PING_INTERVAL = None  # type: ignore
app.config.WEBSOCKET_PING_TIMEOUT = None  # type: ignore


@app.websocket("/", name='ws')
async def ws_handler(request: Request, ws: WebsocketImplProtocol):
    session = Session(request, ws)
    await session.ws_handler()