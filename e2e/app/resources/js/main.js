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
  const tmpDir = await Neutralino.filesystem.getNormalizedPath(
    await Neutralino.os.getEnv("NL_TMPDIR"),
  );
  const pidPath = await Neutralino.filesystem.getJoinedPath(tmpDir, "pid.txt");
  await Neutralino.filesystem.writeFile(pidPath, NL_APPID);
  const watcherId = await Neutralino.filesystem.createWatcher(tmpDir);
  Neutralino.events.on("watchFile", async (event) => {
    console.debug("File changed:", event.detail);
    if (watcherId !== event.detail.id) return;
    const { dir, filename, action } = event.detail;
    if (dir === tmpDir && filename === "pid.txt" && action === "delete") {
      Neutralino.app.exit();
    }
    if (dir === tmpDir && filename === "command.js" && action === "add") {
      eval(
        await Neutralino.filesystem.readFile(
          await Neutralino.filesystem.getJoinedPath(tmpDir, "command.js"),
        ),
      );
      await Neutralino.filesystem.remove(
        await Neutralino.filesystem.getJoinedPath(tmpDir, "command.js"),
      );
    }
  });
})();
// Start the application
Neutralino.extensions.dispatch(
  "dev.attakei.neutralinojs.pythonext.e2e.backend",
  "hello",
);
