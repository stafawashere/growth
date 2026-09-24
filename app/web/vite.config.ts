import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const FONT_FILE = /\.(woff2?|ttf|otf)$/;

export default defineConfig({
   plugins: [react()],
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
