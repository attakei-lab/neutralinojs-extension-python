import time


def test_extension_communication(neutralino_app):
    time.sleep(2)  # Wait sending event by extension

    assert "Hello, world" in neutralino_app.log_path.read_text()
