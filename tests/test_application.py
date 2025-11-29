import json
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
