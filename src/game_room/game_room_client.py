from sanic.server.websockets.impl import WebsocketImplProtocol
from sanic.request import Request
from typing import Final
from sanic import Sanic
from sanic.response import text


app: Final = Sanic("GameCodin", log_config={"version": 1})


app.config.WEBSOCKET_MAX_SIZE = 64
app.config.WEBSOCKET_PING_INTERVAL = None  # type: ignore
app.config.WEBSOCKET_PING_TIMEOUT = None  # type: ignore


@app.websocket("/", name='ws')
async def ws_handler(request: Request, ws: WebsocketImplProtocol):
    await ws.send("pog")


@app.get('/users')
async def handler(request):

    return text("Ok")


app.run(host="0.0.0.0", port=8080, workers=1, debug=False, access_log=False)
