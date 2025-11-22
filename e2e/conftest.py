import subprocess
import time
from pathlib import Path
from threading import Event, Thread

import pytest

here = Path(__file__).parent


class NeutralinoAppTester:
    def __init__(self, timeout=10):
        self.app_path = here / "app"
        self.log_path = self.app_path / "neutralinojs.log"
        self.timeout = timeout
        self.output_lines = []
        self._log_pos = 0
        self._log_monitor_thread = None
        self._log_monitor_enabled = Event()

    def start(self):
        self.log_path.unlink(missing_ok=True)
        self.log_path.touch()
        self.process = subprocess.Popen(
            ["bun", "x", "neu", "run"],
            cwd=self.app_path,
            shell=True,
            bufsize=1,
        )
        self._log_monitor_enabled.set()
        self._log_monitor_thread = Thread(target=self._monitor_log)
        self._log_monitor_thread.start()
        # Monitor logs
        self._wait_for_ready()

    def _monitor_log(self):
        while self._log_monitor_enabled.is_set():
            try:
                if self.log_path.exists():
                    current_pos = self.log_path.stat().st_size
                    if current_pos > self._log_pos:
                        with self.log_path.open("r", encoding="utf-8") as f:
                            f.seek(self._log_pos)
                            new_lines = f.readlines()
                            self.output_lines += new_lines
                            self._log_pos = f.tell()
            except Exception as e:
                print(f"Error monitoring log: {e}")

    def stop(self):
        """アプリを停止"""
        (self.app_path / ".tmp" / "QUIT").touch()
        self._log_monitor_enabled.clear()
        self._log_monitor_thread.join()
        self.process.communicate()

    def _wait_for_ready(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.verify_log_text("App is started."):
                return True
            time.sleep(0.1)
        raise TimeoutError("Application failed to start")

    def verify_log_text(self, pattern):
        return any(pattern in line for line in self.output_lines)


@pytest.fixture(scope="function")
def neutralino_app():
    tester = NeutralinoAppTester()
    tester.start()

    yield tester

    tester.stop()
