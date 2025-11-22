// Initialize Neutralino
Neutralino.init();

// Register event listeners
Neutralino.events.on("windowClose", () => {
  Neutralino.app.exit();
});
Neutralino.events.on("app_updateTitle", (e) => {
  document.querySelector("title").textContent = e.detail.title;
});

// Start the application
Neutralino.extensions.dispatch(
  "dev.attakei.neutralinojs.pythonext.e2e.backend",
  "hello",
);
