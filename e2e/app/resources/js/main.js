// Initialize Neutralino
Neutralino.init();

// Register event listeners
Neutralino.events.on("windowClose", () => {
  Neutralino.app.exit();
});
Neutralino.events.on("app_updateTitle", (e) => {
  document.querySelector("title").textContent = e.detail.title;
});
// Monitor quit signal
(async () => {
  const watcherId = await Neutralino.filesystem.createWatcher(window.NL_PATH);
  Neutralino.events.on("watchFile", (event) => {
    console.debug("File changed:", event.detail);
    if (watcherId !== event.detail.id) return;
    if (event.detail.dir === "..tmp" && event.detail.filename === "QUIT") {
      Neutralino.app.exit();
    }
  });
})();

// Start the application
Neutralino.extensions.dispatch(
  "dev.attakei.neutralinojs.pythonext.e2e.backend",
  "hello",
);

Neutralino.debug.log("App is started.", "INFO");
