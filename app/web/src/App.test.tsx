import { readFileSync } from "node:fs";
import { join } from "node:path";

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";

import * as client from "./api/client";
import type { BudgetsPayload, ProgressPayload, ServedItem, SessionPayload, SettingsPayload } from "./api/types";
import { App, DESTINATIONS, UNSUPPLIED_INPUTS, type Destination } from "./App";
import { daysToExam, formatPlanDate } from "./home/dates";

vi.mock("./api/client");

const mocked = vi.mocked(client);

const SOURCE_ROOT = join(__dirname);

const DESIGN_BRIEF = readFileSync(join(SOURCE_ROOT, "..", "..", "..", "docs", "plan", "08-design-brief.md"), "utf8");

const PROPS_INTERFACE_BY_DESTINATION: Record<Destination, { file: string; name: string }> = {
   home: { file: "home/HomeScreen.tsx", name: "HomeScreenProps" },
   session: { file: "session/SessionScreen.tsx", name: "SessionScreenProps" },
   settings: { file: "settings/SettingsScreen.tsx", name: "SettingsScreenProps" },
   progress: { file: "progress/ProgressRoute.tsx", name: "ProgressRouteProps" }
};

/* P2 scope item 6 brings the progress screen into phase with its calibration curve only; the
   mastery map, the representation matrix and checkpoint history stay out, as do onboarding,
   review and mock (11-phased-delivery.md P2 scope and out of scope). */
const OUT_OF_PHASE_SCREENS = ["onboarding", "review", "mock", "mastery", "matrix", "checkpoint"];

const BAR_DESTINATIONS = ["home", "settings"];

/* A local wall-clock moment, so the calendar date the renderer counts from is the same in every
   time zone the suite runs in. */
const PINNED_NOW = new Date(2027, 0, 5, 9, 30);

const me: client.MePayload = {
   id: "USR-1",
   display_name: null,
   exam_date: "2027-05-10",
   purge_after: "2027-06-09"
};

const readyProgress: ProgressPayload = {
   skills_due_for_review: 12,
   frontier_skills: 4,
   corrected_items_returning: 7,
   forecast_minutes: 23,
   due_today_skills: 12,
   due_today_minutes: 15,
   session_in_progress: null
};

const settingsPayload: SettingsPayload = {
   exam_date: "2027-05-10",
   purge_after: "2027-06-09",
   desired_retention: 0.9
};

const budgetsPayload: BudgetsPayload = {
   day: "2027-01-05",
   roles: [
      {
         role: "tutor",
         cap_usd: 6,
         cap_tokens: 70000,
         cost_usd: 1.25,
         tokens_in: 800,
         tokens_out: 90,
         tokens_cached_read: 31,
         tokens_cached_write: 17,
         hard_stopped: false
      }
   ],
   month_to_date_usd: 3.5
};

const providersPayload = {
   roles: [{ role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true }]
};

const servedItem: ServedItem = {
   id: "ITM-7",
   archetype_id: "BC-ARCH-0301",
   variant_id: null,
   snapshot_id: null,
   parameter_draw: null,
   stem: "Differentiate f(x) = x^2 sin(x)",
   figure_spec: null,
   options: null,
   calculator_status: null,
   representation: null,
   difficulty_settings: null,
   skills: ["BC-SKL-0301"],
   status: "verified",
   stage: "completion",
   format: "short_answer",
   is_probe: false,
   served_steps: [
      { index: 1, text: "Name the factors: u = x^2, v = sin(x)" },
      { index: 2, text: "u' = 2x, v' = cos(x)" }
   ],
   self_explanation_prompt: null
};

const sessionPayload: SessionPayload = {
   id: "SES-9",
   mode: "learning",
   sub_mode: null,
   started_at: "2027-01-05T09:30:00",
   ended_at: null,
   updates_mastery: true,
   snapshot_id: null,
   queue: {
      block1: [],
      block2: [],
      block3: [],
      block4: [],
      forecasts: {},
      coverage_gaps: [],
      interleaving_satisfied: true
   },
   remaining: []
};

function mockServer(progress: ProgressPayload) {
   mocked.readMe.mockResolvedValue(me);
   mocked.readProgress.mockResolvedValue(progress);
   mocked.readSettings.mockResolvedValue(settingsPayload);
   mocked.readProviders.mockResolvedValue(providersPayload);
   mocked.readBudgets.mockResolvedValue(budgetsPayload);
   mocked.openSession.mockResolvedValue(sessionPayload);
   mocked.readSession.mockResolvedValue(sessionPayload);
   mocked.readNextItem.mockResolvedValue({ item: servedItem });
   mocked.readAuthStatus.mockResolvedValue({ user_exists: true });

   return [me, progress, settingsPayload, providersPayload, budgetsPayload, sessionPayload, servedItem];
}

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

function leafValues(value: unknown, into: unknown[] = []): unknown[] {
   const isObject = typeof value === "object" && value !== null;

   if (!isObject) {
      into.push(value);

      return into;
   }

   for (const nested of Object.values(value as Record<string, unknown>)) {
      leafValues(nested, into);
   }

   return into;
}

function escapedForPattern(text: string) {
   return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

const MASK = "\u0000";

const NUMBER_TOKEN = /\d+(?:\.\d+)?/g;

/* Every element whose own text holds a digit is checked. A string the mocked responses carry is
   masked first, then each number left must equal a number the mocked responses carry, or
   daysToExam computed from them. A number that traces to neither has to sit in a sentence
   docs/plan/08-design-brief.md prints, with the masked values free. */
function untracedFigures(payloads: unknown[], derived: number[]) {
   const leaves = payloads.flatMap((payload) => leafValues(payload));
   const isoDates = leaves.filter((leaf): leaf is string => typeof leaf === "string" && /^\d{4}-\d{2}-\d{2}$/.test(leaf));
   const strings = [
      ...leaves.filter((leaf): leaf is string => typeof leaf === "string" && /\d/.test(leaf)),
      ...isoDates.map(formatPlanDate)
   ].sort((left, right) => right.length - left.length);
   const numbers = [...leaves.filter((leaf): leaf is number => typeof leaf === "number"), ...derived];
   const brief = DESIGN_BRIEF.replace(/\s+/g, " ").toLowerCase();
   const offenders: string[] = [];

   const withOwnDigits = Array.from(document.body.querySelectorAll("*")).filter((element) =>
      Array.from(element.childNodes).some((node) => node.nodeType === Node.TEXT_NODE && /\d/.test(node.textContent ?? ""))
   );

   for (const field of Array.from(document.body.querySelectorAll("input"))) {
      const holdsDigit = /\d/.test(field.value);
      const isTraced = numbers.includes(Number(field.value)) || strings.includes(field.value);

      if (holdsDigit && !isTraced) {
         offenders.push(`input ${field.value}`);
      }
   }

   for (const element of withOwnDigits) {
      let masked = (element.textContent ?? "").replace(/\s+/g, " ").trim();

      for (const value of strings) {
         masked = masked.split(value).join(MASK);
      }

      const tokens = masked.match(NUMBER_TOKEN) ?? [];
      const untraced = tokens.filter((token) => !numbers.includes(Number(token)));
      const hasUntraced = untraced.length > 0;

      if (!hasUntraced) {
         continue;
      }

      const sentence = new RegExp(escapedForPattern(masked.toLowerCase()).split(MASK).join(".+?"));
      const printedInThePlan = sentence.test(brief);

      if (!printedInThePlan) {
         offenders.push(masked);
      }
   }

   return offenders;
}

function buttonsIn(container: HTMLElement) {
   return Array.from(container.querySelectorAll("button"));
}

function neverAnswers() {
   return new Promise<never>(() => undefined);
}

beforeEach(() => {
   vi.clearAllMocks();
   vi.useFakeTimers({ toFake: ["Date"] });
   vi.setSystemTime(PINNED_NOW);
});

afterEach(() => {
   cleanup();
   vi.useRealTimers();
});

describe("the client shell", () => {
   it("offers home and settings from the bar, opens no session from it, and names no out-of-phase screen", () => {
      mockServer(readyProgress);
      render(<App />);

      const labels = buttonsIn(screen.getByRole("navigation")).map((button) => button.textContent);

      expect(labels).toEqual(["Home", "Settings"]);
      expect(DESTINATIONS.map((entry) => entry.id)).toEqual(BAR_DESTINATIONS);

      const shellSource = sourceOf("App.tsx").toLowerCase();
      const named = OUT_OF_PHASE_SCREENS.filter((screenName) => shellSource.includes(screenName));

      expect(named, "App.tsx names a screen that is out of phase").toEqual([]);
      expect(mocked.openSession).not.toHaveBeenCalled();
   });

   it("reaches progress from home and never from the bar or as the landing screen", async () => {
      mockServer(readyProgress);
      mocked.readCalibration.mockResolvedValue({
         available: false,
         rated_attempts: 4,
         minimum_rated_attempts: 30,
         attempts_needed: 26,
         window_days: 30,
         window_start: "2026-12-07",
         window_end: "2027-01-05",
         bins: []
      });
      render(<App />);

      await screen.findByText(/Start today's set/);

      expect(within(screen.getByRole("navigation")).queryByRole("button", { name: "Progress" })).toBeNull();
      expect(screen.queryByTestId("calibration-not-yet")).toBeNull();
      expect(mocked.readCalibration).not.toHaveBeenCalled();

      fireEvent.click(screen.getByRole("button", { name: "Progress" }));

      expect(await screen.findByTestId("calibration-not-yet")).toBeTruthy();
      expect(screen.queryByText(/Start today's set/)).toBeNull();
      expect(mocked.readCalibration).toHaveBeenCalledTimes(1);
   });

   it("names every input it still cannot supply, using the name the screen itself declares", () => {
      for (const destination of ["home", "session", "settings", "progress"] as Destination[]) {
         const target = PROPS_INTERFACE_BY_DESTINATION[destination];
         const declared = declaredPropertyNames(target.file, target.name);
         const listed = UNSUPPLIED_INPUTS[destination].map((input) => input.name);
         const undeclared = listed.filter((name) => !declared.includes(name));

         expect(undeclared, `${target.file} declares no such prop`).toEqual([]);
      }

      expect(UNSUPPLIED_INPUTS.settings.map((input) => input.name)).toEqual([]);
   });

   it("wires the purge confirmation phrase rather than leaving the purge controls withheld", async () => {
      mockServer(readyProgress);
      render(<App />);
      visit("settings");

      expect(screen.queryByText("purgeConfirmationPhrase")).toBeNull();
      expect(screen.queryByText("This screen is not built yet")).toBeNull();
      expect(await screen.findByText(/delete my data/i)).toBeTruthy();
   });

   it("offers a signed-in student a second passkey on settings and nowhere else", async () => {
      mockServer(readyProgress);
      render(<App />);

      await screen.findByText(/Start today's set/);

      expect(screen.queryByRole("button", { name: "Add a passkey" })).toBeNull();

      visit("settings");

      expect(await screen.findByRole("button", { name: "Add a passkey" })).toBeTruthy();
   });

   it("says so when the generated design-token stylesheet is absent", () => {
      const probe = getComputedStyle(document.documentElement).getPropertyValue("--growth-surface-page");

      expect(probe.trim(), "this case needs a document with no token stylesheet").toEqual("");

      mockServer(readyProgress);
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

describe("home over GET /me and GET /progress", () => {
   it("shows the ready queue with the forecast, the three counts and the days to the exam", async () => {
      mockServer(readyProgress);
      render(<App />);

      expect(await screen.findByText(/About 23 minutes/)).toBeTruthy();

      const lines = screen.getAllByTestId("queue-line").map((line) => line.textContent);
      const days = daysToExam(me.exam_date, PINNED_NOW);

      expect(lines).toEqual([
         "12 skills due for review",
         "4 skills at your current frontier",
         "7 corrected items coming back"
      ]);
      expect(screen.getByText(`Exam: 10 May 2027, ${days} days away`)).toBeTruthy();
      expect(screen.getByRole("button", { name: "Start today's set" })).toBeTruthy();
   });

   it("shows the empty queue when the forecast and every count are zero", async () => {
      mockServer({
         skills_due_for_review: 0,
         frontier_skills: 0,
         corrected_items_returning: 0,
         forecast_minutes: 0,
         due_today_skills: 0,
         due_today_minutes: 0,
         session_in_progress: null
      });
      render(<App />);

      expect(await screen.findByRole("button", { name: "Add a 15 minute practice set" })).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Start today's set" })).toBeNull();
   });

   it("keeps the ready queue when every count is zero but the forecast is not", async () => {
      mockServer({
         skills_due_for_review: 0,
         frontier_skills: 0,
         corrected_items_returning: 0,
         forecast_minutes: 5,
         due_today_skills: 0,
         due_today_minutes: 0,
         session_in_progress: null
      });
      render(<App />);

      expect(await screen.findByRole("button", { name: "Start today's set" })).toBeTruthy();
      expect(screen.getByText(/About 5 minutes/)).toBeTruthy();
   });

   it("keeps the ready queue when only the forecast is zero, since a count is still due", async () => {
      mockServer({ ...readyProgress, skills_due_for_review: 0, frontier_skills: 0, forecast_minutes: 0 });
      render(<App />);

      expect(await screen.findByRole("button", { name: "Start today's set" })).toBeTruthy();
   });

   it("offers resume for the open session and resumes that session rather than opening another", async () => {
      mockServer({ ...readyProgress, session_in_progress: "SES-9" });
      render(<App />);

      fireEvent.click(await screen.findByRole("button", { name: "Resume" }));

      await screen.findByText(servedItem.stem);

      expect(mocked.readSession).toHaveBeenCalledWith("SES-9");
      expect(mocked.openSession).not.toHaveBeenCalled();
   });

   it("opens a new session from Start today's set and draws the steps the served item carries", async () => {
      mockServer(readyProgress);
      render(<App />);

      fireEvent.click(await screen.findByRole("button", { name: "Start today's set" }));

      await screen.findByText(servedItem.stem);

      expect(mocked.openSession).toHaveBeenCalledTimes(1);
      expect(screen.getByText("u' = 2x, v' = cos(x)")).toBeTruthy();
      expect(screen.getByTestId("blanked-step").getAttribute("data-step-index")).toBe("3");
   });

   it("renders exactly one main landmark on home", async () => {
      mockServer(readyProgress);
      render(<App />);

      await screen.findByRole("button", { name: "Start today's set" });

      expect(screen.getAllByRole("main")).toHaveLength(1);
   });

   it("renders exactly one main landmark on a session screen", async () => {
      mockServer(readyProgress);
      render(<App />);

      fireEvent.click(await screen.findByRole("button", { name: "Start today's set" }));
      await screen.findByText(servedItem.stem);

      expect(screen.getAllByRole("main")).toHaveLength(1);
   });
});

describe("days to the exam", () => {
   it("counts calendar days from the student's local date, whatever the hour", () => {
      expect(daysToExam("2027-05-10", new Date(2027, 4, 9, 23, 59))).toBe(1);
      expect(daysToExam("2027-05-10", new Date(2027, 4, 10, 0, 1))).toBe(0);
      expect(daysToExam("2027-05-10", new Date(2027, 4, 10, 23, 59))).toBe(0);
   });

   it("is not moved by a daylight saving change between today and the exam", () => {
      expect(daysToExam("2027-05-10", new Date(2027, 2, 1, 0, 30))).toBe(70);
      expect(daysToExam("2027-12-01", new Date(2027, 9, 1, 23, 30))).toBe(61);
   });
});

describe("no fabricated figure", () => {
   it("traces every digit on home, session and settings to a mocked response value", async () => {
      const payloads = mockServer(readyProgress);
      const derived = [daysToExam(me.exam_date, PINNED_NOW)];

      render(<App />);
      await screen.findByText(/About 23 minutes/);

      expect(document.body.textContent).toMatch(/\d/);
      expect(untracedFigures(payloads, derived), "home").toEqual([]);

      fireEvent.click(screen.getByRole("button", { name: "Start today's set" }));
      await screen.findByText(servedItem.stem);

      expect(untracedFigures(payloads, derived), "session").toEqual([]);

      visit("settings");
      fireEvent.click(await screen.findByRole("button", { name: "open" }));
      await screen.findByText(/Default retention/);

      expect(screen.getAllByTestId("per-role-cap-row").length).toBe(budgetsPayload.roles.length);
      expect(untracedFigures(payloads, derived), "settings").toEqual([]);
   });

   it("traces the empty queue's figures to its mocked values and the plan's own sentence", async () => {
      const payloads = mockServer({
         ...readyProgress,
         skills_due_for_review: 0,
         frontier_skills: 0,
         corrected_items_returning: 0,
         forecast_minutes: 0
      });

      render(<App />);
      await screen.findByRole("button", { name: "Add a 15 minute practice set" });

      expect(untracedFigures(payloads, [daysToExam(me.exam_date, PINNED_NOW)])).toEqual([]);
   });

   it("renders no digit on home or settings while every request is still in flight", async () => {
      for (const name of ["readMe", "readProgress", "readSettings", "readProviders", "readBudgets"] as const) {
         mocked[name].mockReturnValue(neverAnswers());
      }

      render(<App />);

      expect(screen.getByTestId("home-waiting")).toBeTruthy();
      expect(document.body.textContent ?? "").not.toMatch(/\d/);

      visit("settings");

      expect(screen.getByRole("heading", { name: "Budgets" })).toBeTruthy();
      expect(document.body.textContent ?? "").not.toMatch(/\d/);
   });

   it("renders no digit on home or settings after every request failed", async () => {
      for (const name of ["readMe", "readProgress", "readSettings", "readProviders", "readBudgets"] as const) {
         mocked[name].mockRejectedValue(new Error("the connection dropped"));
      }

      render(<App />);

      expect(await screen.findByTestId("home-failed")).toBeTruthy();
      expect(document.body.textContent ?? "").not.toMatch(/\d/);

      visit("settings");

      await waitFor(() => expect(mocked.readBudgets).toHaveBeenCalledTimes(1));
      await Promise.resolve();

      expect(screen.getByRole("heading", { name: "Budgets" })).toBeTruthy();
      expect(document.body.textContent ?? "").not.toMatch(/\d/);
   });
});
describe("signed out over GET /me", () => {
   function signedOutFailure() {
      return Object.assign(Object.create(client.ApiError.prototype), {
         status: 401,
         detail: "a passkey session is required"
      });
   }

   function registered() {
      return {
         user: me,
         seeded_skill_states: 0,
         recovery_code: "RC-from-the-finish-response"
      };
   }

   it("shows only registration on the account screen, and neither home nor the bar, when /me answers 401 and no user exists", async () => {
      mockServer(readyProgress);
      mocked.readAuthStatus.mockResolvedValue({ user_exists: false });
      mocked.readMe.mockRejectedValue(signedOutFailure());
      render(<App />);

      expect(await screen.findByRole("button", { name: "Register a passkey" })).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Sign in with a passkey" })).toBeNull();
      expect(screen.queryByRole("navigation")).toBeNull();
      expect(screen.queryByText("Start today's set")).toBeNull();
   });

   it("shows only sign-in on the account screen when /me answers 401 and a user exists", async () => {
      mockServer(readyProgress);
      mocked.readMe.mockRejectedValue(signedOutFailure());
      render(<App />);

      expect(await screen.findByRole("button", { name: "Sign in with a passkey" })).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Register a passkey" })).toBeNull();
      expect(screen.queryByRole("navigation")).toBeNull();
   });

   it("renders exactly one main landmark on the signed-out account screen", async () => {
      mockServer(readyProgress);
      mocked.readAuthStatus.mockResolvedValue({ user_exists: false });
      mocked.readMe.mockRejectedValue(signedOutFailure());
      render(<App />);

      await screen.findByRole("button", { name: "Register a passkey" });

      expect(screen.getAllByRole("main")).toHaveLength(1);
   });

   it("shows home and no account screen when /me answers 200", async () => {
      mockServer(readyProgress);
      render(<App />);

      expect(await screen.findByText(/Start today's set/)).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Register a passkey" })).toBeNull();
   });

   it("keeps the shell when /me fails for a reason other than a missing session", async () => {
      mockServer(readyProgress);
      mocked.readMe.mockRejectedValue(Object.assign(Object.create(client.ApiError.prototype), { status: 500, detail: "" }));
      render(<App />);

      expect(await screen.findByTestId("home-failed")).toBeTruthy();
      expect(screen.getByRole("navigation")).toBeTruthy();
      expect(screen.queryByRole("button", { name: "Register a passkey" })).toBeNull();
   });

   it("re-reads /me after sign-in and lands on home", async () => {
      mockServer(readyProgress);
      mocked.readMe.mockRejectedValueOnce(signedOutFailure()).mockRejectedValueOnce(signedOutFailure());
      mocked.signInWithPasskey.mockResolvedValue({ user_id: me.id });
      render(<App />);

      fireEvent.click(await screen.findByRole("button", { name: "Sign in with a passkey" }));

      expect(await screen.findByText(/Start today's set/)).toBeTruthy();
      expect(screen.getByRole("navigation")).toBeTruthy();
      expect(mocked.signInWithPasskey).toHaveBeenCalledTimes(1);
      expect(mocked.readMe.mock.calls.length).toBeGreaterThanOrEqual(3);
   });

   it("stays on the account screen when the re-read of /me after sign-in still answers 401", async () => {
      mockServer(readyProgress);
      mocked.readMe.mockRejectedValue(signedOutFailure());
      mocked.signInWithPasskey.mockResolvedValue({ user_id: me.id });
      render(<App />);

      fireEvent.click(await screen.findByRole("button", { name: "Sign in with a passkey" }));

      await waitFor(() => expect(mocked.readMe.mock.calls.length).toBeGreaterThanOrEqual(3));

      expect(screen.getByRole("button", { name: "Sign in with a passkey" })).toBeTruthy();
      expect(screen.queryByRole("navigation")).toBeNull();
   });

   it("shows the recovery code after registration and reaches home only through its acknowledgement", async () => {
      mockServer(readyProgress);
      mocked.readAuthStatus.mockResolvedValue({ user_exists: false });
      mocked.readMe.mockRejectedValueOnce(signedOutFailure()).mockRejectedValueOnce(signedOutFailure());
      mocked.registerPasskey.mockResolvedValue(registered());
      render(<App />);

      fireEvent.click(await screen.findByRole("button", { name: "Register a passkey" }));

      expect(await screen.findByText("RC-from-the-finish-response")).toBeTruthy();
      expect(screen.queryByRole("navigation")).toBeNull();

      fireEvent.click(screen.getByRole("button", { name: "I have saved it" }));

      expect(await screen.findByText(/Start today's set/)).toBeTruthy();
      expect(document.body.textContent ?? "").not.toContain("RC-from-the-finish-response");
   });
});
