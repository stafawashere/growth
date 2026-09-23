import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { HomeScreen, type HomeScreenProps, type QueueLine } from "./HomeScreen";

const queueLines: QueueLine[] = [
   { id: "due", label: "skills due for review", count: 12 },
   { id: "frontier", label: "skills at your current frontier", count: 4 },
   { id: "corrected", label: "corrected items coming back", count: 2 }
];

function baseProps(): HomeScreenProps {
   return {
      status: "ready",
      examDate: "2027-05-10",
      daysToExam: 596,
      queueMinutes: 23,
      queueLines,
      onStartSession: vi.fn(),
      onAddPracticeSet: vi.fn(),
      onResumeSession: vi.fn()
   };
}

afterEach(() => {
   cleanup();
});

describe("HomeScreen, queue ready", () => {
   it("states the commitment in minutes and presents exactly one primary action", () => {
      render(<HomeScreen {...baseProps()} />);

      expect(screen.getByText(/23 minutes/)).toBeTruthy();

      const buttons = screen.getAllByRole("button");

      expect(buttons.length).toBe(1);
      expect(buttons[0].textContent).toContain("Start today's set");
   });

   it("renders the queue lines from its props, ranging over the props rather than a typed-out list", () => {
      const arbitraryLines: QueueLine[] = [
         { id: "a", label: "alpha skills", count: 7 },
         { id: "b", label: "beta skills", count: 1 },
         { id: "c", label: "gamma skills", count: 9 },
         { id: "d", label: "delta skills", count: 3 },
         { id: "e", label: "epsilon skills", count: 5 }
      ];

      render(<HomeScreen {...baseProps()} queueMinutes={40} queueLines={arbitraryLines} />);

      const rendered = screen.getAllByTestId("queue-line");

      expect(rendered.length).toBe(arbitraryLines.length);

      arbitraryLines.forEach((line) => {
         const matcher = new RegExp(`${line.count}\\s+${line.label}`);

         expect(screen.getByText(matcher)).toBeTruthy();
      });
   });

   it("the primary action is a real button that calls the handler when activated", () => {
      const onStartSession = vi.fn();

      render(<HomeScreen {...baseProps()} onStartSession={onStartSession} />);

      const startButton = screen.getByRole("button", { name: "Start today's set" });

      fireEvent.click(startButton);

      expect(onStartSession).toHaveBeenCalledTimes(1);
   });
});

describe("HomeScreen, queue empty", () => {
   it("offers the optional extra set as the one next action, in the plan's own copy", () => {
      const onAddPracticeSet = vi.fn();

      render(
         <HomeScreen
            {...baseProps()}
            status="empty"
            queueMinutes={0}
            queueLines={[]}
            onAddPracticeSet={onAddPracticeSet}
         />
      );

      expect(
         screen.getByText("Nothing is due today. You can add a 15 minute practice set if you want one.")
      ).toBeTruthy();

      const buttons = screen.getAllByRole("button");

      expect(buttons.length).toBe(1);
      expect(buttons[0].textContent).toContain("Add a 15 minute practice set");

      fireEvent.click(buttons[0]);
      expect(onAddPracticeSet).toHaveBeenCalledTimes(1);
   });

   it("does not offer to start today's set when there is nothing due", () => {
      render(<HomeScreen {...baseProps()} status="empty" queueMinutes={0} queueLines={[]} />);

      expect(screen.queryByText("Start today's set")).toBeNull();
   });
});

describe("HomeScreen, session in progress", () => {
   it("offers resume as the one next action", () => {
      const onResumeSession = vi.fn();

      render(<HomeScreen {...baseProps()} status="inProgress" onResumeSession={onResumeSession} />);

      const buttons = screen.getAllByRole("button");

      expect(buttons.length).toBe(1);
      expect(buttons[0].textContent).toContain("Resume");

      fireEvent.click(buttons[0]);
      expect(onResumeSession).toHaveBeenCalledTimes(1);
   });

   it("does not offer to start today's set while a session is already in progress", () => {
      render(<HomeScreen {...baseProps()} status="inProgress" />);

      expect(screen.queryByText("Start today's set")).toBeNull();
   });
});

/* The named-colour vocabulary is not hand-typed here. Any value the DOM's own CSS parser keeps
   when it is assigned to the color property is a colour, which covers every named colour, every
   hex form and the rgb, rgba, hsl and hsla function forms without this file listing one. The
   only values the parser keeps that name no colour are the CSS-wide keywords and the two
   context keywords, so those are subtracted by name. */
const CSS_WIDE_KEYWORDS = ["inherit", "initial", "unset", "revert", "revert-layer"];

const CONTEXT_COLOUR_KEYWORDS = ["currentcolor", "transparent"];

const HEX_COLOUR = /#[0-9a-fA-F]{3,8}\b/;

const STRING_LITERAL = /"([^"\n]*)"|'([^'\n]*)'|`([^`]*)`/g;

const CUSTOM_PROPERTY_REFERENCE = /var\(\s*--[a-z-]+/g;

function sourceFilesUnder(directory: string): string[] {
   const found: string[] = [];

   for (const entry of readdirSync(directory)) {
      const full = join(directory, entry);

      if (statSync(full).isDirectory()) {
         found.push(...sourceFilesUnder(full));
         continue;
      }

      const isSource = entry.endsWith(".tsx") || entry.endsWith(".ts");

      if (isSource) {
         found.push(full);
      }
   }

   return found;
}

function namesAColour(value: string) {
   const withoutTokens = value.replace(/var\(\s*--[^)]*\)/g, " ").trim();
   const hasSomethingToParse = withoutTokens.length > 0;

   if (!hasSomethingToParse) {
      return false;
   }

   const probe = document.createElement("div");

   probe.style.color = "";
   probe.style.color = withoutTokens;

   const parsed = probe.style.color.toLowerCase();
   const parsedAsColour = parsed.length > 0;
   const isKeyword = CSS_WIDE_KEYWORDS.includes(parsed) || CONTEXT_COLOUR_KEYWORDS.includes(parsed);

   return parsedAsColour && !isKeyword;
}

function colourOffendersIn(file: string) {
   const source = readFileSync(file, "utf8");
   const offenders: string[] = [];

   if (HEX_COLOUR.test(source)) {
      offenders.push(`${file}: hex colour`);
   }

   for (const match of source.matchAll(STRING_LITERAL)) {
      const literal = match[1] ?? match[2] ?? match[3] ?? "";

      if (namesAColour(literal)) {
         offenders.push(`${file}: ${literal}`);
      }
   }

   for (const reference of source.match(CUSTOM_PROPERTY_REFERENCE) ?? []) {
      const isGrowthToken = reference.includes("--growth-");

      if (!isGrowthToken) {
         offenders.push(`${file}: ${reference}`);
      }
   }

   return offenders;
}

describe("HomeScreen, design tokens", () => {
   it("authors no colour of its own under src/home or src/settings, in any CSS form", () => {
      const directories = [join(process.cwd(), "src", "home"), join(process.cwd(), "src", "settings")];
      const offenders: string[] = [];
      let scanned = 0;

      for (const directory of directories) {
         const files = sourceFilesUnder(directory);

         expect({ directory, scannable: files.length > 0 }).toEqual({ directory, scannable: true });

         for (const file of files) {
            scanned += 1;
            offenders.push(...colourOffendersIn(file));
         }
      }

      expect(scanned).toBeGreaterThanOrEqual(directories.length);
      expect(offenders).toEqual([]);
   });

   it("gives the primary action the button-primary class and leaves its colour to app.css's own text-on-accent rule", () => {
      const home = join(process.cwd(), "src", "home", "HomeScreen.tsx");
      const contents = readFileSync(home, "utf8");
      const css = readFileSync(join(process.cwd(), "src", "styles", "app.css"), "utf8");

      expect(contents).toMatch(/className="button-primary"/);
      expect(colourOffendersIn(home)).toEqual([]);

      const buttonPrimaryRule = css.match(/\.button-primary\s*\{[^}]*\}/);

      expect(buttonPrimaryRule).not.toBeNull();
      expect(buttonPrimaryRule![0]).toMatch(/color:\s*var\(--growth-text-on-accent\)/);
      expect(buttonPrimaryRule![0]).not.toMatch(/accent-contrast-text/);
   });
});

describe("design tokens, primary button vocabulary across every screen", () => {
   it("never gives a button accent-contrast-text as its own colour, source-wide", () => {
      const files = sourceFilesUnder(join(process.cwd(), "src")).filter(
         (file) => !file.endsWith(".test.tsx") && !file.endsWith(".test.ts")
      );
      const offenders: string[] = [];

      for (const file of files) {
         for (const match of file ? readFileSync(file, "utf8").matchAll(/<button[\s\S]{0,600}?(?:\/>|<\/button>)/g) : []) {
            const buttonMarkup = match[0];
            const namesAccentContrastText = buttonMarkup.includes("accent-contrast-text");

            if (namesAccentContrastText) {
               offenders.push(`${file}: ${buttonMarkup.slice(0, 80)}`);
            }
         }
      }

      expect(offenders).toEqual([]);
   });

   it("renders at most one button-primary per screen state", () => {
      const readyQueue = render(<HomeScreen {...baseProps()} />);

      expect(readyQueue.container.querySelectorAll(".button-primary").length).toBe(1);
      cleanup();

      const emptyQueue = render(<HomeScreen {...baseProps()} status="empty" queueMinutes={0} queueLines={[]} />);

      expect(emptyQueue.container.querySelectorAll(".button-primary").length).toBe(1);
      cleanup();

      const inProgress = render(<HomeScreen {...baseProps()} status="inProgress" />);

      expect(inProgress.container.querySelectorAll(".button-primary").length).toBe(1);
   });
});