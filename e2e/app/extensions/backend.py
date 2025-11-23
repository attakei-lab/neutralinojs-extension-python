import logging
import os
from pathlib import Path

from neutralinojs_extension import Connection, Extension

app = Extension()


@app.event("calculate")
def calculate(app: Extension, data):
    result = eval(data)
    app.send("app.broadcast", {"event": "app_resultCalculate", "data": result})


@app.event("hello")
def hello(app: Extension, data):
    logging.info("Called 'hello' handler.")
    app.send("debug.log", {"message": "Hello, world"})
    app.send("window.setTitle", {"title": "Hello, world"})
    app.send(
        "app.broadcast", {"event": "app_updateTitle", "data": {"title": "Hello, world"}}
    )


if __name__ == "__main__":
    log_path = Path(os.environ["NL_TMPDIR"])
    logging.basicConfig(level=logging.DEBUG, filename=log_path / "backend.log")
    conn = Connection.from_stdin()
    app.start(conn)
