import json
import logging
from unittest.mock import AsyncMock

import pytest

from neutralinojs_extension.application import Extension
from neutralinojs_extension.host import Connection


@pytest.fixture
def simple_app() -> Extension:
    app = Extension()
    app._conn = Connection("0", "token", "token", "example")
    app._ws = AsyncMock()
    return app


class Test_Application_send:
    @pytest.mark.asyncio
    async def test_with_data(self, simple_app):
        await simple_app.send("app.broadcast", {"event": "hello", "data": None})
        msg = json.loads(simple_app._ws.send_str.call_args_list[0][0][0])
        assert msg["method"] == "app.broadcast"
        assert msg["data"] == {"event": "hello", "data": None}
        assert "id" in msg
        assert "accessToken" in msg

    @pytest.mark.asyncio
    async def test_none_data(self, simple_app):
        await simple_app.send("app.getConfig", None)
        msg = json.loads(simple_app._ws.send_str.call_args_list[0][0][0])
        assert msg["method"] == "app.getConfig"
        assert "id" in msg
        assert "accessToken" in msg
        assert "data" not in msg


class Test_Application_handle_text_message:
    @pytest.mark.asyncio
    async def test_registered_event(self, simple_app):
        mock = AsyncMock()

        @simple_app.event("hello")
        async def hello_handler(app, data):
            await mock.func(data)

        await simple_app._on_message(json.dumps({"event": "hello"}))
        assert mock.func.called
        assert mock.func.call_args[0][0] is (None)

    @pytest.mark.asyncio
    async def test_unregistered_event(self, simple_app, caplog):
        mock = AsyncMock()

        @simple_app.event("hello")
        async def hello_handler(app, data):
            await mock.func(data)

        with caplog.at_level(logging.DEBUG):
            await simple_app._on_message(json.dumps({"event": "hello2"}))
            assert not mock.func.called
            assert "Event 'hello2' is unknown" in caplog.text

    @pytest.mark.asyncio
    async def test_none_event(self, simple_app, caplog):
        mock = AsyncMock()

        @simple_app.event("hello")
        async def hello_handler(app, data):
            await mock.func(data)

        with caplog.at_level(logging.DEBUG):
            await simple_app._on_message(json.dumps({"dummy": "hello2"}))
            assert not mock.func.called
            assert "Message doesn't have 'event' key." in caplog.text
