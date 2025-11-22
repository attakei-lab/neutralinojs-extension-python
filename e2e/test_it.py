import time


def test_extension_communication(neutralino_app):
    time.sleep(2)  # Wait sending event by extension

    assert "Hello, world" in neutralino_app.app_log_path.read_text()


def test_receive_button_action(neutralino_app):
    time.sleep(2)  # Wait sending event by extension

    neutralino_app.run_command("""
    document.querySelector("#app").innerHTML = '<button id="button-1">Click me</button>';
    document.querySelector("#button-1").addEventListener("click", () => {
        Neutralino.extensions.dispatch(
            "dev.attakei.neutralinojs.pythonext.e2e.backend",
            "buttonClicked",
        );
    });
    document.querySelector("#button-1").click();
    """)
    assert (
        "Event 'buttonClicked' is unknown. Skip it."
        in neutralino_app.backend_log_path.read_text()
    )
