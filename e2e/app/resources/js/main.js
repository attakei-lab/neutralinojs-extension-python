// Initialize Neutralino
Neutralino.init();

// Register event listeners
Neutralino.events.on("windowClose", () => {
  Neutralino.app.exit();
});

// Start the application
Neutralino.extensions.dispatch(
  "dev.attakei.neutralinojs.pythonext.e2e.backend",
  "hello",
);
