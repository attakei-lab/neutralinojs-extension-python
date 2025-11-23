import os
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

here = Path(__file__).parent


class NeutralinoAppTester:
    def __init__(self, app_dir: Path, work_dir: Path, timeout=10):
        self.app_dir = app_dir
        self.work_dir = work_dir
        self.timeout = timeout
        self._command_counter = 0
        (self.work_dir / "shared").mkdir()

    @property
    def app_log_path(self) -> Path:
        return self.app_dir / "neutralinojs.log"

    @property
    def backend_log_path(self) -> Path:
        return self.work_dir / "backend.log"

    @property
    def pid_path(self) -> Path:
        return self.work_dir / "shared" / "proc"

    def start(self, html: str | None = None):
        self.app_log_path.unlink(missing_ok=True)
        self.process = subprocess.Popen(
            ["bun", "x", "neu", "run"],
            cwd=self.app_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ.copy() | {"NL_TMPDIR": str(self.work_dir)},
        )
        # Monitor logs
        self._wait_for_ready()
        if html:
            command = f"document.querySelector('#app').innerHTML = `{html}`;"
            self.run_command(command)

    def stop(self):
        self.pid_path.unlink()
        try:
            self.process.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait()

    def run_command(self, command: str, timeout: int = 5, wait: int = 1):
        self._command_counter += 1
        command_path = self.work_dir / "shared" / f"command-{self._command_counter}.js"
        command_path.write_text(command)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not command_path.exists():
                time.sleep(wait)
                return
            time.sleep(0.1)
        raise TimeoutError("Command is not finished in times")

    def wait_for_file(self, target: Path, timeout: int = 5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if target.exists():
                return
            time.sleep(0.1)
        raise TimeoutError(f"File '{target}' is not found in waiting time")

    def _wait_for_ready(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.pid_path.exists():
                return
            time.sleep(0.1)
        raise TimeoutError("Application failed to start")


@pytest.fixture(scope="function")
def make_neutralinojs_app(tmp_path):
    @contextmanager
    def make_app(html: str | None = None, command: str | None = None, timeout: int = 5):
        tester = NeutralinoAppTester(Path(__file__).parent / "app", tmp_path, timeout)
        tester.start(html)

        try:
            yield tester

        finally:
            tester.stop()
            time.sleep(0.5)

    return make_app
