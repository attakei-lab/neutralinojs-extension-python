import asyncio
import logging
from pathlib import Path

from neutralinojs_extension import Connection, Extension
from neutralinojs_extension.native_api.os import ShowNotification

app = Extension()
app_dir = Path(__file__).parent.parent


@app.event("hello")
async def hello(app, data: str):
    """When host call 'Hello' event."""
    await app.send(
        ShowNotification(
            title="Hi!", content=f"Hello {data}, I am neutralino-extension!!"
        )
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    conn = Connection.from_stdin()
    asyncio.run(app.start(conn))
