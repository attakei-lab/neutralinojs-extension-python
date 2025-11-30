import asyncio
import logging
import os
from pathlib import Path

from neutralinojs_extension import Connection, Extension
from neutralinojs_extension.native_api import Debug_Log
from neutralinojs_extension.native_api.app import Broadcast
from neutralinojs_extension.native_api.window import SetTitle

app = Extension()


@app.event("calculate")
async def calculate(app: Extension, data):
    result = eval(data)
    await app.send("app.broadcast", {"event": "app_resultCalculate", "data": result})


@app.event("hello")
async def hello(app: Extension, data):
    logging.info("Called 'hello' handler.")
    await app.send(Debug_Log(message="Hello, world"))
    await app.send(SetTitle(title="Hello, world"))
    await app.send(Broadcast(event="app_updateTitle", data={"title": "Hello, world"}))


if __name__ == "__main__":
    log_path = Path(os.environ["NL_TMPDIR"])
    logging.basicConfig(level=logging.DEBUG, filename=log_path / "backend.log")
    conn = Connection.from_stdin()
    asyncio.run(app.start(conn))
