import logging
from pathlib import Path

from neutralinojs_extension import Connection, Extension
from neutralinojs_extension.native_api.os import ShowNotification

app = Extension()
app_dir = Path(__file__).parent.parent


@app.event("hello")
def hello(app, data: str):
    """When host call 'Hello' event."""
    app.send(ShowNotification("Hi!", f"Hello {data}, I am neutralino-extension!!"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    conn = Connection.from_stdin()
    app.start(conn)
