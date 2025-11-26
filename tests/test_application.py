import asyncio
import json

import pytest
from aiohttp import ClientSession, WSMsgType, web

from neutralinojs_extension.application import Extension
from neutralinojs_extension.host import Connection


class Test_Application_send:
    @pytest.mark.asyncio
    async def test_send_message(self, aiohttp_client):
        messages = []

        async def handler(request: web.Request) -> web.WebSocketResponse:
            nonlocal messages
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    messages.append(msg.data)
                elif msg.type == WSMsgType.ERROR:
                    print(f"WebSocket error: {ws.exception()}")
                elif msg.type == WSMsgType.CLOSE:
                    await ws.close()
                    break
            return ws

        host = web.Application()
        host.router.add_route("GET", "/", handler)
        client = await aiohttp_client(host)
        conn = Connection(client.port, "token", "token", "example")

        app = Extension()
        async with ClientSession().ws_connect(conn.url) as ws:
            # await app.start(conn)
            app._conn = conn
            app._ws = ws
            await app.send("app.broadcast", {"event": "hello", "data": None})
            await asyncio.sleep(0.01)
            assert len(messages) == 1
            msg = json.loads(messages[0])
            assert msg["method"] == "app.broadcast"
            assert msg["data"] == {"event": "hello", "data": None}
            assert "id" in msg
            assert "accessToken" in msg
            await app.send("app.getConfig", None)
            await asyncio.sleep(0.01)
            assert len(messages) == 2
            msg = json.loads(messages[1])
            assert msg["method"] == "app.getConfig"
            assert "id" in msg
            assert "accessToken" in msg
            assert "data" not in msg
