import os
import subprocess
import time
from pathlib import Path

import pytest

here = Path(__file__).parent


class NeutralinoAppTester:
    def __init__(self, app_dir: Path, work_dir: Path, timeout=10):
        self.app_dir = app_dir
        self.work_dir = work_dir
        self.timeout = timeout

    @property
    def app_log_path(self) -> Path:
        return self.app_dir / "neutralinojs.log"

    @property
    def backend_log_path(self) -> Path:
        return self.work_dir / "backend.log"

    @property
    def pid_path(self) -> Path:
        return self.work_dir / "pid.txt"

    def start(self):
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
def neutralino_app(tmp_path):
    tester = NeutralinoAppTester(Path(__file__).parent / "app", tmp_path)
    tester.start()

    yield tester

    tester.stop()
