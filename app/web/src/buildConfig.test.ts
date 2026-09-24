// @vitest-environment node
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { describe, expect, it } from "vitest";

import config from "../vite.config";

/* app/api/security_headers.py sets default-src 'self' with no font-src, so a font the build
   inlines as a data: URL is blocked in the browser. KaTeX_Size3.woff2 is under Vite's 4 KB inline
   limit and was being inlined, which left large delimiters in a fallback font. */

const FONT_DIRECTORY = join(__dirname, "..", "node_modules", "katex", "dist", "fonts");

describe("the production build", () => {
   it("never inlines a KaTeX font the content security policy would block", () => {
      const inlineLimit = config.build?.assetsInlineLimit;

      expect(typeof inlineLimit).toBe("function");

      const decide = inlineLimit as (filePath: string, content: Buffer) => boolean | undefined;
      const fonts = readdirSync(FONT_DIRECTORY);
      const inlined = fonts.filter((name) => {
         const path = join(FONT_DIRECTORY, name);

         return decide(path, readFileSync(path)) !== false;
      });

      expect(fonts.length).toBeGreaterThan(0);
      expect(inlined).toEqual([]);
   });
});
