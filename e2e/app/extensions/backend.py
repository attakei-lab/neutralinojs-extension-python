import logging

from neutralinojs_extension import Connection, Extension

app = Extension()


@app.event("hello")
def hello(app: Extension, data):
    logging.info("Called 'hello' handler.")
    app.send("window.setTitle", {"title": "Hello, world"})
    app.send(
        "app.broadcast", {"event": "app_updateTitle", "data": {"title": "Hello, world"}}
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    conn = Connection.from_stdin()
    app.start(conn)
