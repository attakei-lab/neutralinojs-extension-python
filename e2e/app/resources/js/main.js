// Initialize Neutralino
Neutralino.init();

// Register event listeners
Neutralino.events.on("windowClose", () => {
  Neutralino.app.exit();
});
Neutralino.events.on("app_updateTitle", (e) => {
  document.querySelector("title").textContent = e.detail.title;
});

(async () => {
  const tmpDir = await Neutralino.filesystem.getNormalizedPath(
    await Neutralino.os.getEnv("NL_TMPDIR"),
  );
  // Process control for tests.
  const sharedDir = await Neutralino.filesystem.getJoinedPath(tmpDir, "shared");
  await Neutralino.filesystem.writeFile(
    await Neutralino.filesystem.getJoinedPath(sharedDir, "proc"),
    NL_APPID,
  );
  const watcherId = await Neutralino.filesystem.createWatcher(sharedDir);
  Neutralino.events.on("watchFile", async (event) => {
    console.debug("File changed:", event.detail);
    if (watcherId !== event.detail.id) return;
    const { dir, filename, action } = event.detail;
    if (dir === sharedDir && filename === "proc" && action === "delete") {
      Neutralino.app.exit();
    }
    if (dir === sharedDir && filename.endsWith(".js") && action === "add") {
      await eval(
        await Neutralino.filesystem.readFile(
          await Neutralino.filesystem.getJoinedPath(dir, filename),
        ),
      );
      await Neutralino.filesystem.move(
        await Neutralino.filesystem.getJoinedPath(dir, filename),
        await Neutralino.filesystem.getJoinedPath(dir, `${filename}_done`),
      );
    }
  });
})();
// Start the application
Neutralino.extensions.dispatch(
  "dev.attakei.neutralinojs.pythonext.e2e.backend",
  "hello",
);
