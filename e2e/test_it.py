import time


def test_extension_communication(make_neutralinojs_app):
    with make_neutralinojs_app() as neutralino_app:
        time.sleep(2)  # Wait sending event by extension
        assert "Hello, world" in neutralino_app.app_log_path.read_text()


def test_receive_button_action(make_neutralinojs_app):
    with make_neutralinojs_app(
        '<button id="button-1">Click me</button>'
    ) as neutralino_app:
        neutralino_app.run_command("""
        document.querySelector("#button-1").addEventListener("click", async () => {
            await Neutralino.extensions.dispatch(
                "dev.attakei.neutralinojs.pythonext.e2e.backend",
                "buttonClicked",
            );
        });
        """)
        neutralino_app.run_command("""
        document.querySelector("#button-1").click();
        """)
        assert (
            "Event 'buttonClicked' is unknown. Skip it."
            in neutralino_app.backend_log_path.read_text()
        )


def test_receive_calculate(make_neutralinojs_app):
    with make_neutralinojs_app(
        '<button id="button-1">Click me</button><p id="result"></p>'
    ) as neutralino_app:
        neutralino_app.run_command("""
        Neutralino.events.on("app_resultCalculate", async (event) => {
            const outPath = await Neutralino.filesystem.getJoinedPath(
                await Neutralino.os.getEnv("NL_TMPDIR"),
                "output.txt"
            );
            await Neutralino.filesystem.writeFile(outPath, new String(event.detail));
        });
        document.querySelector("#button-1").addEventListener("click", async () => {
            await Neutralino.extensions.dispatch(
                "dev.attakei.neutralinojs.pythonext.e2e.backend",
                "calculate",
                "1 + 2"
            );
        });
        """)
        neutralino_app.run_command("""
        document.querySelector("#button-1").click();
        """)
        neutralino_app.wait_for_file(neutralino_app.work_dir / "output.txt")
        assert (neutralino_app.work_dir / "output.txt").read_text() == "3"
