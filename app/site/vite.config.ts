import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // Relative asset paths: the static build works under any GitHub Pages sub-path.
  base: "./",
  server: {
    host: "127.0.0.1",
  },
});
