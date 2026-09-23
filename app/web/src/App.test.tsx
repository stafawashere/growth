import { readFileSync } from "node:fs";
import { join } from "node:path";

import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";

import { App, DESTINATIONS, UNSUPPLIED_INPUTS, type Destination } from "./App";

const SOURCE_ROOT = join(__dirname);

const PROPS_INTERFACE_BY_DESTINATION: Record<Destination, { file: string; name: string }> = {
   home: { file: "home/HomeScreen.tsx", name: "HomeScreenProps" },
   session: { file: "session/SessionScreen.tsx", name: "SessionScreenProps" },
   settings: { file: "settings/SettingsScreen.tsx", name: "SettingsScreenProps" }
};

const OUT_OF_P1_SCREENS = ["onboarding", "review", "progress", "mock"];

function sourceOf(relativePath: string): string {
   return readFileSync(join(SOURCE_ROOT, relativePath), "utf8");
}

function declaredPropertyNames(relativePath: string, interfaceName: string): string[] {
   const source = sourceOf(relativePath);
   const block = new RegExp(`export interface ${interfaceName} \\{([^}]*)\\}`).exec(source);

   expect(block, `${relativePath} declares no ${interfaceName}`).not.toBeNull();

   const properties = block![1].matchAll(/^\s{3}(\w+)\??:/gm);

   return [...properties].map((match) => match[1]);
}

function visit(destination: Destination): void {
   const label = DESTINATIONS.find((entry) => entry.id === destination)!.label;

   fireEvent.click(screen.getByRole("button", { name: label }));
}

describe("the client shell", () => {
   afterEach(cleanup);

   it("routes between the three screens P1 builds and offers no other destination", () => {
      render(<App />);

      const labels = screen.getAllByRole("button").map((button) => button.textContent);

      expect(labels).toEqual(DESTINATIONS.map((entry) => entry.label));
      expect(DESTINATIONS.map((entry) => entry.id)).toEqual(["home", "session", "settings"]);

      const shellSource = sourceOf("App.tsx").toLowerCase();
      const named = OUT_OF_P1_SCREENS.filter((screenName) => shellSource.includes(screenName));

      expect(named, "App.tsx names a screen that is out of P1 scope").toEqual([]);
   });

   it("names every input it cannot supply, using the name the screen itself declares", () => {
      for (const destination of DESTINATIONS.map((entry) => entry.id)) {
         const target = PROPS_INTERFACE_BY_DESTINATION[destination];
         const declared = declaredPropertyNames(target.file, target.name);
         const listed = UNSUPPLIED_INPUTS[destination].map((input) => input.name);

         expect(listed.length, `${destination} lists no unsupplied input`).toBeGreaterThan(0);

         const undeclared = listed.filter((name) => !declared.includes(name));

         expect(undeclared, `${target.file} declares no such prop`).toEqual([]);
      }
   });

   it("shows the unsupplied inputs on the screen rather than leaving the gap silent", () => {
      render(<App />);

      for (const destination of DESTINATIONS.map((entry) => entry.id)) {
         visit(destination);

         for (const input of UNSUPPLIED_INPUTS[destination]) {
            expect(screen.getByText(input.name)).toBeTruthy();
         }
      }
   });

   it("puts no figure on any screen, because every figure it could show is unsupplied", () => {
      render(<App />);

      for (const destination of DESTINATIONS.map((entry) => entry.id)) {
         visit(destination);

         const rendered = document.body.textContent ?? "";

         expect(rendered, `${destination} renders a figure no route supplies`).not.toMatch(/\d/);
      }
   });

   it("says so when the generated design-token stylesheet is absent", () => {
      const probe = getComputedStyle(document.documentElement).getPropertyValue("--growth-surface-page");

      expect(probe.trim(), "this case needs a document with no token stylesheet").toEqual("");

      render(<App />);

      expect(screen.getByRole("status").textContent).toContain("design tokens");
   });

   it("mounts the shell from the entry module index.html names and bundles the motion stylesheet", () => {
      const entry = sourceOf("main.tsx");

      expect(entry).toContain("./styles/motion.css");
      expect(entry).toContain("root");
      expect(entry).toContain("App");

      const page = readFileSync(join(SOURCE_ROOT, "..", "index.html"), "utf8");

      expect(page).toContain("/src/main.tsx");
   });
});
