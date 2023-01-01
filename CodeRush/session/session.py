from __future__ import annotations
from dataclasses import dataclass, field
from requests import request

from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
from sanic.request import Request

import asyncio
from typing import Final, ClassVar, Optional

import json

from . import SessionException, SendPacket, RecvPacket
from ..user import User


@dataclass
class Session:
    timeout:  ClassVar = 10  # secs
    __sessions: ClassVar[list[Session]] = []

    request: Request
    ws: WebsocketImplProtocol
    user: User = field(init=False)

    # TODO: remove this
    async def __auth(self):
        packet_id, user_id, user_token = asyncio.run(self.recv())

        if packet_id != RecvPacket.auth:
            raise ValueError

        user = User.get_by_id(user_id)

        if user is None or\
                user.token != user_token:
            return

        user.acquire()
        self.user = user
        self.__sessions.append(self)

    async def recv(self) -> list:
        message = await self.ws.recv(self.timeout)
        # Using an assert is normally not safe because we are dealing with execution exceptions.
        # But json.loads does this already, we need the assert for the type checker.
        assert message is not None
        return json.loads(message)

    async def send(self, message: object):
        await self.send(json.dumps(message))

    async def send_error(self, error: str, message: str = ""):
        await self.send([
            SendPacket.error,
            {
                "error": error,
                "message": message
            }
        ])

    def __del__(self):
        self.__sessions.remove(self)
        self.user.release()
