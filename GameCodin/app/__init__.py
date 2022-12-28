__all__ = ["app"]

from sanic.server.websockets.impl import WebsocketImplProtocol
from typing import Final
from sanic import Sanic
from sanic.application.constants import ServerStage

from ..app.cors.cors import add_cors_headers
from ..app.cors.options import setup_options

app: Final = Sanic("GameCodin", log_config={"version": 1})

from . import app_ws
from . import app_routing


app.register_listener(setup_options, "before_server_start")
app.register_middleware(add_cors_headers, "response")


def start():
    if app.state.stage is not ServerStage.STOPPED:
        raise Exception("App is already running!")

    print("GameCodin is running on http://localhost:8080/")
    print("----------------------------------------------")

    app.run(host="0.0.0.0", port=8080, workers=1, debug=True, verbosity=1, access_log=False)