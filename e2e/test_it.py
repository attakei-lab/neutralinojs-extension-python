import time


def test_extension_communication(neutralino_app):
    time.sleep(2)  # Wait sending event by extension

    assert neutralino_app.verify_log_text("Hello, world")
