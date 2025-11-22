import time


def test_extension_communication(neutralino_app):
    time.sleep(2)  # Wait sending event by extension

    assert "Hello, world" in neutralino_app.app_log_path.read_text()


def test_receive_button_action(neutralino_app):
    time.sleep(2)  # Wait sending event by extension

    command = """
    document.querySelector("#app").innerHTML = '<button id="button-1">Click me</button>';
    document.querySelector("#button-1").addEventListener("click", () => {
        Neutralino.extensions.dispatch(
            "dev.attakei.neutralinojs.pythonext.e2e.backend",
            "buttonClicked",
        );
    });
    document.querySelector("#button-1").click();
    """
    command_path = neutralino_app.work_dir / "command.js"
    command_path.write_text(command)
    while not command_path.exists():
        time.sleep(0.1)
    assert (
        "Event 'buttonClicked' is unknown. Skip it."
        in neutralino_app.backend_log_path.read_text()
    )
