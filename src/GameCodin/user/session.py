from __future__ import annotations
from dataclasses import dataclass, field
from requests import request

from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
from sanic.request import Request

import asyncio
from typing import Final, ClassVar, Optional

import json

from .session_packets import RecvPacket, SendPacket
from .session_expections import SessionException
from .user import User

@dataclass
class Session:
    timeout:  ClassVar = 10 # secs
    __sessions: ClassVar[list[Session]] = []

    request: Request
    ws: WebsocketImplProtocol
    user: User = field(init = False)
    gameroom: Optional[GameRoom] = None

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

    async def ws_handler(self):
        # TODO: make each packet handling a seperate function because it's pretty messy!
        try:
            while True:
                packet_id, *message = await self.recv()
                try:
                    if packet_id == RecvPacket.join:
                        if self.gameroom is not None:
                            raise SessionException("Session is already in another gameroom")
                        gameroom_id, = message
                        try:
                            gameroom = GameRoom.get_active_gameroom(gameroom_id)
                        except IndexError:
                            raise SessionException("Gameroom doesn't exist or finished")
                        gameroom.add_sesssion(self)
                        self.gameroom = gameroom
                    else:
                        raise SessionException("Wrong packet id")
                except SessionException as e:
                    await self.send_error(e.__class__.__name__, str(e))
        except (ConnectionClosed, ConnectionClosedError, asyncio.TimeoutError) as e:
            # XXX: LOG ?
            pass
        finally:
            try:
                if self.gameroom is not None:
                    self.gameroom.remove_session(self)
            except SessionException: pass
    
    def __del__(self):
        self.__sessions.remove(self)
        self.user.release()

from ..game_room.game_room import GameRoom