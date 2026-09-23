import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./App";
import { watchSystemTheme } from "./theme";
import "./styles/motion.css";
import "./styles/app.css";

watchSystemTheme();

const container = document.getElementById("root");

if (container === null) {
   throw new Error("index.html has no element with id root to mount into");
}

createRoot(container).render(
   <StrictMode>
      <App />
   </StrictMode>
);
