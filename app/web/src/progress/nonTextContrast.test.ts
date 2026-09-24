import { readFileSync } from "node:fs";
import { join } from "node:path";

import { describe, expect, it } from "vitest";

/* WCAG 2.2 SC 1.4.11 on the two progress graphics: every colour the mastery map and the
   calibration curve draw a mark with is one of app/design/tokens.py's GRAPHIC_TOKENS and holds
   3:1 against every surface in both themes of app/design/growth-tokens.json. The ratio arithmetic
   is WCAG's relative luminance, the same definition app/design/contrast.py implements. */

const SOURCE_ROOT = __dirname;

const DESIGN_ROOT = join(SOURCE_ROOT, "..", "..", "..", "design");

const TOKEN_FILE = JSON.parse(readFileSync(join(DESIGN_ROOT, "growth-tokens.json"), "utf8")) as Record<
   string,
   Record<string, string>
>;

const CONTRAST_SOURCE = readFileSync(join(DESIGN_ROOT, "contrast.py"), "utf8");

const TOKENS_SOURCE = readFileSync(join(DESIGN_ROOT, "tokens.py"), "utf8");

const SURFACES = ["surface-page", "surface-raised", "surface-sunken"];

function pythonFloor() {
   const match = /^NON_TEXT_CONTRAST_FLOOR = ([\d.]+)$/m.exec(CONTRAST_SOURCE);

   expect(match, "contrast.py declares no NON_TEXT_CONTRAST_FLOOR").not.toBeNull();

   return Number(match![1]);
}

function graphicTokens() {
   const match = /^GRAPHIC_TOKENS = \(([^)]*)\)$/m.exec(TOKENS_SOURCE);

   expect(match, "tokens.py declares no GRAPHIC_TOKENS").not.toBeNull();

   return [...match![1].matchAll(/"([a-z0-9-]+)"/g)].map((name) => name[1]);
}

function linear(channel: number) {
   const scaled = channel / 255;

   return scaled <= 0.04045 ? scaled / 12.92 : ((scaled + 0.055) / 1.055) ** 2.4;
}

function luminance(hex: string) {
   const body = hex.slice(1);
   const red = parseInt(body.slice(0, 2), 16);
   const green = parseInt(body.slice(2, 4), 16);
   const blue = parseInt(body.slice(4, 6), 16);

   return 0.2126 * linear(red) + 0.7152 * linear(green) + 0.0722 * linear(blue);
}

function ratio(first: string, second: string) {
   const lighter = Math.max(luminance(first), luminance(second));
   const darker = Math.min(luminance(first), luminance(second));

   return (lighter + 0.05) / (darker + 0.05);
}

/* A mark's colour reaches the SVG either as a fill or stroke attribute or through a constant that
   holds the reference; a style object's fill is text and belongs to the 4.5:1 gate. */
function markColours(relativePath: string) {
   const source = readFileSync(join(SOURCE_ROOT, relativePath), "utf8");
   const attributes = [...source.matchAll(/(?:fill|stroke)="var\(--growth-([a-z0-9-]+)\)"/g)];
   const constants = [...source.matchAll(/^const [A-Z_]+ = "var\(--growth-([a-z0-9-]+)\)";$/gm)];

   return [...new Set([...attributes, ...constants].map((match) => match[1]))];
}

describe("non-text contrast on the progress graphics", () => {
   const drawnBy = {
      "mastery map": markColours("MasteryMap.tsx"),
      "calibration curve": markColours("CalibrationCurve.tsx")
   };

   it.each(Object.entries(drawnBy))("the %s draws only with the graphic tokens the gate checks", (_name, colours) => {
      expect(colours.length).toBeGreaterThan(0);
      expect(colours.filter((colour) => !graphicTokens().includes(colour))).toEqual([]);
   });

   it.each(Object.entries(drawnBy))("every %s colour holds 3:1 on every surface in both themes", (_name, colours) => {
      const floor = pythonFloor();
      const below: string[] = [];

      for (const theme of ["light", "dark"]) {
         for (const colour of colours) {
            for (const surface of SURFACES) {
               const measured = ratio(TOKEN_FILE[theme][colour], TOKEN_FILE[theme][surface]);

               if (measured < floor) {
                  below.push(`${theme}: ${colour} on ${surface} is ${measured.toFixed(2)}:1`);
               }
            }
         }
      }

      expect(floor).toBe(3);
      expect(below).toEqual([]);
   });
});
