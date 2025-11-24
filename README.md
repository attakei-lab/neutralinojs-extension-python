# Neutralinojs extension toolkit for Python

IMPORTANT: This library is still in development and may not be fully functional. So, this is not published on PyPI yet.

## Overview

This is framework library for Neutralinojs extension that works likely Flask and FastAPI and provides classes and types.

You can develop extension using Python as same as development web applications. 

## Example

Extension implements:

```python
from neutralinojs_extenstion import Extension, Connection
from neutralinojs_extenstion.native_api import Os_ShowNotification

app = Extension()


@app.event("hello")
def handle_hello_extenstion(app, data):
    app.send(Os_ShowNotification(
        "Hi!",
        f"Hello {data['name']}, I am Neutralinojs extension!!",
    )


if __name__ == "__main__":
    host = Connection.from_stdin()
    app.start(host)
```

Desktop implements:

```javascript
Neutralino.init();

Neutralino.events.dispatch("hello", {name: "Kazuya Takei"});
```
