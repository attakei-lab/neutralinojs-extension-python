// Initialize Neutralino
Neutralino.init();

// Register event listeners
Neutralino.events.on("windowClose", () => {
  Neutralino.app.exit();
});
Neutralino.events.on("app_updateTitle", (e) => {
  document.querySelector("title").textContent = e.detail.title;
});

// Process control for tests.
(async () => {
  const tmpDir = await Neutralino.filesystem.getJoinedPath(NL_PATH, ".tmp");
  const pidPath = await Neutralino.filesystem.getJoinedPath(tmpDir, "pid.txt");
  await Neutralino.filesystem.writeFile(pidPath, NL_APPID);
  const watcherId = await Neutralino.filesystem.createWatcher(tmpDir);
  Neutralino.events.on("watchFile", (event) => {
    console.debug("File changed:", event.detail);
    if (watcherId !== event.detail.id) return;
    const { dir, filename, action } = event.detail;
    if (dir === tmpDir && filename === "pid.txt" && action === "delete") {
      Neutralino.app.exit();
    }
  });
})();

// Start the application
Neutralino.extensions.dispatch(
  "dev.attakei.neutralinojs.pythonext.e2e.backend",
  "hello",
);
