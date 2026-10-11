import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In development the API runs on the host (uvicorn, port 8000); in Docker nginx
// serves the build and forwards /api to the api container (nginx.conf).
export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
});
