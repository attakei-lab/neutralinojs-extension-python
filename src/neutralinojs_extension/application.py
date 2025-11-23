"""Application core of Neutralinojs extensions."""

from __future__ import annotations

import json
import logging
import threading
from typing import TYPE_CHECKING, overload

from websocket import WebSocketApp

from .native_api import APISchema

if TYPE_CHECKING:
    from typing import Any, Callable

    from .host import Connection

    EventHandler = Callable[["Extension", ...], None]


logger = logging.getLogger(__name__)


class Extension:
    """Main container of extension.

    You need to create instance and bind hendlers.
    """

    _event_handlers: dict[str, EventHandler]
    """Store of event handlers."""
    _conn: Connection | None
    """Using connection."""
    _ws: WebSocketApp | None
    """Connected socket."""
    _logger: logging.Logger

    def __init__(self, name: str = ""):
        self._event_handlers = {}
        self._conn = None
        self._ws = None
        self._logger = logger.getChild(name if name else self.__class__.__name__)

    def event(self, name: str) -> Callable[[EventHandler], None]:
        """Register function as 'Event handler'."""

        def _event(func: EventHandler) -> None:
            if name in self._event_handlers:
                self._logger.warning("Event '%s' is already registered.", name)

            self._event_handlers[name] = func
            self._logger.info("Event '%s' is %s", name, func)

        return _event

    def start(self, conn: Connection):
        """Connect host and start waiting messages."""
        self._conn = conn
        self._ws = WebSocketApp(self._conn.url, on_message=self._on_message)
        self._ws.run_forever()

    @overload
    def send(self, method_or_data: APISchema): ...
    @overload
    def send(self, method_or_data: str, data: APISchema): ...

    def send(
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

        self._ws.send(message.to_json())

    def _on_message(self, ws: WebSocketApp, message: str | bytes):
        """Entrypoint for message from host."""
        self._logger.debug("Recieved: %s", message)
        msg = json.loads(message)

        if "event" not in msg:
            self._logger.debug("Message doesn't have 'event' key.")
            return

        if msg["event"] not in self._event_handlers:
            self._logger.debug("Event '%s' is unknown. Skip it.", msg["event"])
            return

        threading.Thread(
            target=self._event_handlers[msg["event"]],
            args=(self, msg.get("data", None)),
        ).start()
