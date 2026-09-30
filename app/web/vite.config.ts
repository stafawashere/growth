import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const FONT_FILE = /\.(woff2?|ttf|otf)$/;

/* The dev server hands every API path to the backend, so `npm run dev` runs the client against a
   live server on another port. GROWTH_API names it; the default is the port app/serve.sh uses. */
const API_TARGET = process.env.GROWTH_API ?? "http://127.0.0.1:8000";

const API_PATHS = [
   "/auth",
   "/me",
   "/sessions",
   "/progress",
   "/review",
   "/review-queue",
   "/lessons",
   "/frq",
   "/attempts",
   "/gradings",
   "/assessments",
   "/mocks",
   "/drills",
   "/unit-checks",
   "/checkpoints",
   "/probe",
   "/settings",
   "/agent",
   "/export",
   "/purge",
   "/notices",
   "/content",
   "/calculator",
   "/healthz",
   "/growth-tokens.css"
];

export default defineConfig({
   plugins: [react()],
   server: {
      proxy: Object.fromEntries(API_PATHS.map((path) => [path, { target: API_TARGET }]))
   },
   build: {
      /* The CSP in app/api/security_headers.py allows fonts from 'self' only, so a font must ship
         as a file; undefined leaves every other asset to Vite's default limit. */
      assetsInlineLimit: (filePath: string) => (FONT_FILE.test(filePath) ? false : undefined)
   },
   test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./vitest.setup.ts"],
      include: ["src/**/*.test.{ts,tsx}"]
   }
});
