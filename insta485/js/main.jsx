import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Feed from "./feed";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
root.render(
  <StrictMode>
    <Feed />
  </StrictMode>,
);
