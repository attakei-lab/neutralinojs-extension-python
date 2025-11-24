# Neutralinojs extension toolkit for Python

## Overview

This is framework library for Neutralinojs extension that works likely Flask and FastAPI and provides classes and types.

You can develop extension using Python as same as development web applications. 

## Example

Extension implements:

```python
from neutralinojs_extenstion import Extension, Connection
from neutralinojs_extenstion.native_api import App_Broadcast

app = Extension()


@app.event("hello")
def handle_hello_extenstion(app: Extension, data):
    app.send(App_Broadcast(
        "showMessageBox",
        {
            "text": f"Hello {data['name']}",
        }
    )


if __name__ == "__main__":
    host = Connection.from_stdin()
    app.start(host)
```

Desktop implements:

```javascript
Neutralino.init();

Neutralino.events.on("showMessageBox", (e) => {
  Neutralino.window.showMessageBox(e.detail.text)
})
Neutralino.events.dispatch("hello", {name: "Kazuya Takei"});
```
