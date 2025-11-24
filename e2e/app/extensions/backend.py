import logging
import os
from pathlib import Path

from neutralinojs_extension import Connection, Extension
from neutralinojs_extension.native_api.app import Broadcast
from neutralinojs_extension.native_api.debug import Log
from neutralinojs_extension.native_api.window import SetTitle

app = Extension()


@app.event("calculate")
def calculate(app: Extension, data):
    result = eval(data)
    app.send("app.broadcast", Broadcast("app_resultCalculate", result))


@app.event("hello")
def hello(app: Extension, data):
    logging.info("Called 'hello' handler.")
    app.send(Log("Hello, world"))
    app.send(SetTitle("Hello, world"))
    app.send(Broadcast("app_updateTitle", {"title": "Hello, world"}))


if __name__ == "__main__":
    log_path = Path(os.environ["NL_TMPDIR"])
    logging.basicConfig(level=logging.DEBUG, filename=log_path / "backend.log")
    conn = Connection.from_stdin()
    app.start(conn)
