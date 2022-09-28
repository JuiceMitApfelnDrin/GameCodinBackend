from __future__ import annotations
from dataclasses import dataclass, field
from requests import request

from sanic.server.websockets.impl import WebsocketImplProtocol
from sanic.request import Request

import asyncio
from typing import Final, ClassVar

import json
from .session_packets import RecvPacket, SendPacket
from .session_expections import SessionException
from .user import User

@dataclass
class Session:
    __timeout:  Final = 10 # secs
    __sessions: ClassVar[list[Session]] = []

    request: Request
    ws: WebsocketImplProtocol
    user: User = field(init = False)

    async def __auth(self):
        packet_id, user_id, user_token = asyncio.run(self.recv())
        if packet_id != RecvPacket.auth:
            raise ValueError
        user = User.get_by_id(user_id)
        if user.user_token != user_token:
            return

        user.acquire()
        self.user = user
        self.__sessions.append(self)
        await self.ws_handler()

    async def recv(self) -> list:
        message = await self.ws.recv(self.__timeout)
        # Using an assert is normally not safe because we are dealing with execution exceptions.
        # But json.loads does this already, we need the assert for the type checker.
        assert message is not None
        return json.loads(message)

    async def send(self, message: object):
        await self.send(json.dumps(message))

    async def send_error(self, error: str, message: str = ""):
        # Don't know how to format this :|
        await self.send([
            SendPacket.error,
            {   
                "error": error,
                "message": message 
            }
        ])

    async def ws_handler(self):
        while True:
            packet_id, *message = await self.recv()

            try:
                if packet_id == RecvPacket.join:
                    lobby_id, = message
                    raise NotImplementedError
                else:
                    raise SessionException("Wrong packet id")
            except SessionException as e:
                await self.send_error(e.__class__.__name__, str(e))
    
    def __del__(self):
        self.__sessions.remove(self)
        self.user.release()