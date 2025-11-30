"""Application core of Neutralinojs extensions."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, overload

from aiohttp import ClientSession, WSMsgType

from .native_api._base import APISchema

if TYPE_CHECKING:
    from typing import Any, Callable, Coroutine

    from aiohttp import ClientWebSocketResponse

    from .host import Connection

    # TODO: Currently, event handlers must be async functions.
    EventHandler = Callable[["Extension", ...], Coroutine[Any, Any, None]]


logger = logging.getLogger(__name__)


class Extension:
    """Main container of extension.

    You need to create instance and bind hendlers.
    """

    _event_handlers: dict[str, EventHandler]
    """Store of event handlers."""
    _conn: Connection | None
    """Using connection."""
    _ws: ClientWebSocketResponse | None
    """Connected WebSocket."""
    _logger: logging.Logger

    def __init__(self, name: str = ""):
        self._event_handlers = {}
        self._conn = None
        self._ws = None
        self._logger = logger.getChild(name if name else self.__class__.__name__)

    # ------
    # Declaring methods
    # ------

    def event(self, name: str) -> Callable[[EventHandler], None]:
        """Register function as 'Event handler'."""

        def _event(func: EventHandler) -> None:
            if name in self._event_handlers:
                self._logger.warning("Event '%s' is already registered.", name)

            self._event_handlers[name] = func
            self._logger.info("Event '%s' is %s", name, func)

        return _event

    # ------
    # Running methods
    # ------

    async def start(self, conn: Connection):
        """Connect host and start waiting messages."""
        self._conn = conn
        async with ClientSession().ws_connect(self._conn.url) as ws:
            self._ws = ws
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    asyncio.create_task(self._on_message(msg.data))
                elif msg.type == WSMsgType.CLOSE:
                    await ws.close()
                    break
                else:
                    self._logger.warning(msg)

    async def _on_message(self, message: str | bytes):
        """Entrypoint for message from host."""
        self._logger.debug("Recieved: %s", message)
        msg = json.loads(message)

        if "event" not in msg:
            self._logger.debug("Message doesn't have 'event' key.")
            return

        if msg["event"] not in self._event_handlers:
            self._logger.debug("Event '%s' is unknown. Skip it.", msg["event"])
            return

        func = self._event_handlers[msg["event"]]
        result = func(self, msg.get("data", None))
        if asyncio.iscoroutine(result):
            return await result
        return result

    # ------
    # Action methods
    # ------

    @overload
    async def send(self, method_or_data: APISchema): ...
    @overload
    async def send(self, method_or_data: str, data: APISchema | Any | None = None): ...

    async def send(
        self,
        method_or_data: str | APISchema,
        data: APISchema | Any | None = None,
    ):
        """Send message to host.

        :param method_or_data: Method name or APIParameters object.
        :param data: Data to send (This is used if ``method_or_data`` is a string).
        """
        if not self._conn or not self._ws:
            self._logger.warning("Sending message, but it doesn't connect anywhere.")
            return

        if isinstance(method_or_data, APISchema):
            message = self._conn.make_message(method_or_data.ID, method_or_data)
        else:
            message = self._conn.make_message(method_or_data, data)

        return await self._ws.send_str(message.to_json())
