import subprocess
import time
from pathlib import Path

import pytest

here = Path(__file__).parent


class NeutralinoAppTester:
    def __init__(self, app_dir: Path, timeout=10):
        self.app_dir = here / "app"
        self.timeout = timeout
        self.output_lines = []

    @property
    def log_path(self) -> Path:
        return self.app_dir / "neutralinojs.log"

    @property
    def pid_path(self) -> Path:
        return self.app_dir / ".tmp" / "pid.txt"

    def cleanup(self):
        self.log_path.unlink(missing_ok=True)
        self.pid_path.unlink(missing_ok=True)

    def start(self):
        self.cleanup()
        self.process = subprocess.Popen(
            ["bun", "x", "neu", "run"],
            cwd=self.app_dir,
        )
        # Monitor logs
        self._wait_for_ready()

    def stop(self):
        """アプリを停止"""
        self.pid_path.unlink()
        self.process.communicate()

    def _wait_for_ready(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.pid_path.exists():
                return
            time.sleep(0.1)
        raise TimeoutError("Application failed to start")


@pytest.fixture(scope="function")
def neutralino_app():
    tester = NeutralinoAppTester(Path(__file__) / "app")
    tester.start()

    yield tester

    tester.stop()
