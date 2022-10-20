from __future__ import annotations
from ..game_room.game_room import GameRoom
from dataclasses import dataclass, field
from requests import request

from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
from sanic.request import Request

import asyncio
from typing import Final, ClassVar, Optional

import json

from . import Session, SessionException, SendPacket, RecvPacket
from ..user import User
from ..game_room import GameRoom

class SessionManager(Session):
    gameroom: Optional[GameRoom]
    async def ws_handler(self):
        # TODO: make each packet handling a seperate function because it's pretty messy!
        await self.__auth()
        try:
            while True:
                packet_id, *message = await self.recv()
                try:
                    if packet_id == RecvPacket.join:
                        if self.gameroom:
                            self.gameroom.remove_session(self)
                            self.gameroom = None
                        gameroom_id, = message
                        gameroom = GameRoom.get_active_gameroom(gameroom_id)
                        if gameroom is None:
                            raise SessionException(
                                "Can't join game: There is no active gameroom with such id!")
                        gameroom.add_session(self)
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
            except SessionException:
                pass

