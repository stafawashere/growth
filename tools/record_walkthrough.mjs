/*
Records a captioned walkthrough of a web page as an MP4. Headless Brave runs the steps of a JSON
script over the Chrome DevTools Protocol, Page.startScreencast frames are saved with their
timestamps, and ffmpeg stitches them at a steady frame rate with the captions burned in.

   node tools/record_walkthrough.mjs --script walk.json --out var/agent/drawing/walkthrough.mp4
   node tools/record_walkthrough.mjs --script walk.json --dry-run
   node tools/record_walkthrough.mjs --script walk.json --out walk.mp4 --keep-frames var/agent/frames

A script is {"viewport": {"width", "height", "deviceScaleFactor", "mobile"}, "fps": 10, "steps": [...]}.
Each step names its kind in "do":

   {"do": "navigate", "url": "http://localhost:5176/"}
   {"do": "cookie", "name": "session", "value": "...", "url": "http://localhost:5176/"}
   {"do": "click", "selector": "#draw"} or {"do": "click", "text": "Show all", "role": "button"}
   {"do": "drag", "selector": ".board-title", "by": [120, 80], "steps": 12, "duration_ms": 600}
   {"do": "type", "selector": "textarea", "text": "sketch y = x^2"}
   {"do": "press", "key": "Meta+/"}
   {"do": "wait_for", "selector": "svg.figure", "timeout_ms": 20000} or {"do": "wait_for", "text": "Figure:"}
   {"do": "wait", "ms": 1500}
   {"do": "viewport", "width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": true}
   {"do": "media", "reduced_motion": "reduce", "color_scheme": "dark"}
   {"do": "eval", "expression": "localStorage.setItem('tour', 'done')"}
   {"do": "screenshot", "path": "var/agent/drawing/phone.png"}
   {"do": "caption", "text": "The figure draws in step by step"}

Any step may carry "caption", which shows from that step until the next caption; an empty caption
clears it. Click by text looks at buttons, links and [role] elements, and wait_for a selector waits
until it is visible. A drag presses the left button at the centre of the selector's first match,
moves it by "by" in "steps" moves spread over "duration_ms" (12 and 600 when left out) and lets go
there, so a component listening for pointer events sees a real drag. Recording starts once the first navigate step has loaded, so setup before it
stays out of the video. The video is the size of the starting viewport in device pixels, and frames
from later viewports are scaled to fit it. Paths are relative to the working directory. Typed text
and cookie values are never printed.

A failed step prints its number and reason, saves <out>.failed-step-N.png beside the video, still
stitches what was recorded and exits 1. --keep-frames DIR keeps the frames, the caption images and
timeline.json in DIR instead of a temp directory.

Chrome only sends a screencast frame when the page changes, so each frame is held until the next
one. The frames are sampled at the script's fps into a numbered image sequence rather than an
ffmpeg concat list with durations, because a size change partway through a concat list makes
ffmpeg rebuild its filter graph and drop the frame just before the change. The Homebrew ffmpeg on
this machine is built without libfreetype, so it has no drawtext filter. Brave draws each caption
into a transparent PNG instead, and ffmpeg lays it over the video.
*/
import { spawn, spawnSync } from "node:child_process";
import { copyFileSync, existsSync, linkSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import { basename, dirname, extname, join, resolve } from "node:path";
import { parseArgs } from "node:util";

const BRAVE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser";
const FFMPEG = "/opt/homebrew/bin/ffmpeg";

const CDP_CALL_TIMEOUT_MS = 30000;
const LAUNCH_TIMEOUT_MS = 20000;
const BROWSER_EXIT_WAIT_MS = 5000;
const DEFAULT_WAIT_TIMEOUT_MS = 15000;
const NAVIGATE_TIMEOUT_MS = 30000;
const POLL_INTERVAL_MS = 100;
const SCREENCAST_SETTLE_MS = 250;
const SILENT_SCREENCAST_WAIT_MS = 400;
const LAST_FRAME_HOLD_SECONDS = 1;
const FFMPEG_TIMEOUT_MS = 600000;
const LETTERBOX_COLOR = "0x101014";

const DEFAULT_VIEWPORT = { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false };
const DEFAULT_FPS = 10;
const MAX_FPS = 60;
const DEFAULT_DRAG_STEPS = 12;
const MAX_DRAG_STEPS = 60;
const DEFAULT_DRAG_DURATION_MS = 600;
const MAX_DRAG_DURATION_MS = 5000;

const SCRIPT_FIELDS = { required: { steps: "object" }, optional: { viewport: "object", fps: "number" } };
const VIEWPORT_FIELDS = { required: { width: "number", height: "number" }, optional: { deviceScaleFactor: "number", mobile: "boolean" } };
const COMMON_STEP_FIELDS = { do: "string", caption: "string" };

const STEP_FIELDS = {
   navigate: { required: { url: "string" }, optional: { timeout_ms: "number" } },
   click: { required: {}, optional: { selector: "string", text: "string", role: "string", timeout_ms: "number" } },
   drag: { required: { selector: "string", by: "object" }, optional: { steps: "number", duration_ms: "number", timeout_ms: "number" } },
   type: { required: { text: "string" }, optional: { selector: "string", timeout_ms: "number" } },
   press: { required: { key: "string" }, optional: {} },
   wait_for: { required: {}, optional: { selector: "string", text: "string", timeout_ms: "number" } },
   wait: { required: { ms: "number" }, optional: {} },
   viewport: VIEWPORT_FIELDS,
   media: { required: {}, optional: { reduced_motion: "string", color_scheme: "string" } },
   eval: { required: { expression: "string" }, optional: {} },
   screenshot: { required: { path: "string" }, optional: {} },
   caption: { required: { text: "string" }, optional: {} },
   cookie: { required: { name: "string", value: "string", url: "string" }, optional: {} }
};

const REDUCED_MOTION_VALUES = ["reduce", "no-preference"];
const COLOR_SCHEME_VALUES = ["light", "dark"];

const MODIFIER_BITS = { Alt: 1, Control: 2, Meta: 4, Shift: 8 };

const NAMED_KEYS = {
   Enter: { code: "Enter", keyCode: 13, text: "\r" },
   Tab: { code: "Tab", keyCode: 9 },
   Escape: { code: "Escape", keyCode: 27 },
   Backspace: { code: "Backspace", keyCode: 8 },
   Delete: { code: "Delete", keyCode: 46 },
   Space: { key: " ", code: "Space", keyCode: 32, text: " " },
   ArrowLeft: { code: "ArrowLeft", keyCode: 37 },
   ArrowUp: { code: "ArrowUp", keyCode: 38 },
   ArrowRight: { code: "ArrowRight", keyCode: 39 },
   ArrowDown: { code: "ArrowDown", keyCode: 40 },
   Home: { code: "Home", keyCode: 36 },
   End: { code: "End", keyCode: 35 },
   PageUp: { code: "PageUp", keyCode: 33 },
   PageDown: { code: "PageDown", keyCode: 34 }
};

const PUNCTUATION_KEYS = {
   "/": { code: "Slash", keyCode: 191 },
   "?": { code: "Slash", keyCode: 191 },
   ".": { code: "Period", keyCode: 190 },
   ",": { code: "Comma", keyCode: 188 },
   ";": { code: "Semicolon", keyCode: 186 },
   "=": { code: "Equal", keyCode: 187 },
   "+": { code: "Equal", keyCode: 187 },
   "-": { code: "Minus", keyCode: 189 },
   "[": { code: "BracketLeft", keyCode: 219 },
   "]": { code: "BracketRight", keyCode: 221 },
   "\\": { code: "Backslash", keyCode: 220 },
   "'": { code: "Quote", keyCode: 222 },
   "`": { code: "Backquote", keyCode: 192 }
};

const PAGE_HELPERS = `
   const normalize = (value) => (value ?? "").replace(/\\s+/g, " ").trim();

   const isVisible = (element) => {
      const box = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      const hasArea = box.width > 0 && box.height > 0;
      const isShown = style.visibility !== "hidden" && style.display !== "none";

      return hasArea && isShown;
   };
`;

const USAGE = "usage: node tools/record_walkthrough.mjs --script walk.json --out walkthrough.mp4 [--dry-run] [--keep-frames DIR]";

function sleep(ms) {
   return new Promise((done) => setTimeout(done, ms));
}

function log(line) {
   console.log(`[${new Date().toISOString().slice(11, 23)}] ${line}`);
}

function shorten(text, limit) {
   const isShort = text.length <= limit;

   return isShort ? text : `${text.slice(0, limit - 3)}...`;
}

function withDeadline(promise, ms, label) {
   let timer;
   const expiry = new Promise((_, fail) => {
      timer = setTimeout(() => fail(new Error(`${label} took longer than ${ms} ms`)), ms);
   });

   return Promise.race([promise, expiry]).finally(() => clearTimeout(timer));
}

function isPlainObject(value) {
   const isObject = typeof value === "object" && value !== null;

   return isObject && !Array.isArray(value);
}

function checkFieldTypes(object, required, optional, where, problems) {
   const known = { ...required, ...optional };

   for (const field of Object.keys(required)) {
      if (object[field] === undefined) {
         problems.push(`${where}: missing "${field}"`);
      }
   }

   for (const [field, value] of Object.entries(object)) {
      const expected = known[field];

      if (expected === undefined) {
         problems.push(`${where}: unknown field "${field}"`);
         continue;
      }

      const hasExpectedType = typeof value === expected && value !== null;
      const article = expected === "object" ? "an" : "a";

      if (!hasExpectedType) {
         problems.push(`${where}: "${field}" must be ${article} ${expected}`);
      }
   }
}

function checkViewportValues(viewport, where, problems) {
   for (const field of ["width", "height"]) {
      const value = viewport[field];
      const isPositiveInteger = Number.isInteger(value) && value > 0;

      if (typeof value === "number" && !isPositiveInteger) {
         problems.push(`${where}: "${field}" must be a positive whole number of CSS pixels`);
      }
   }

   const scale = viewport.deviceScaleFactor;
   const scaleIsInvalid = typeof scale === "number" && !(scale > 0 && scale <= 4);

   if (scaleIsInvalid) {
      problems.push(`${where}: "deviceScaleFactor" must be above 0 and at most 4`);
   }
}

function checkUrl(value, where, field, problems) {
   try {
      new URL(value);
   } catch {
      problems.push(`${where}: "${field}" is not a URL`);
   }
}

function checkTimeout(step, where, problems) {
   const timeout = step.timeout_ms;
   const timeoutIsInvalid = typeof timeout === "number" && !(timeout > 0);

   if (timeoutIsInvalid) {
      problems.push(`${where}: "timeout_ms" must be above 0`);
   }
}

function checkOneTarget(step, where, problems) {
   const hasSelector = step.selector !== undefined;
   const hasText = step.text !== undefined;
   const hasExactlyOne = hasSelector !== hasText;

   if (!hasExactlyOne) {
      problems.push(`${where}: give either "selector" or "text", not both and not neither`);
   }

   const emptySelector = step.selector === "";
   const emptyText = step.text === "";

   if (emptySelector || emptyText) {
      problems.push(`${where}: the selector or text is empty`);
   }
}

function checkStepMeaning(step, where, problems) {
   switch (step.do) {
      case "navigate":
         checkUrl(step.url, where, "url", problems);
         break;
      case "click": {
         checkOneTarget(step, where, problems);

         const roleWithoutText = step.role !== undefined && step.text === undefined;

         if (roleWithoutText) {
            problems.push(`${where}: "role" only narrows a click by text`);
         }
         break;
      }
      case "drag": {
         const emptySelector = step.selector === "";
         const byIsList = Array.isArray(step.by);
         const byIsPair = byIsList && step.by.length === 2 && step.by.every(Number.isFinite);
         const stepsIsValid = Number.isInteger(step.steps) && step.steps >= 1 && step.steps <= MAX_DRAG_STEPS;
         const badSteps = step.steps !== undefined && !stepsIsValid;
         const durationIsValid = step.duration_ms > 0 && step.duration_ms <= MAX_DRAG_DURATION_MS;
         const badDuration = step.duration_ms !== undefined && !durationIsValid;

         if (emptySelector) {
            problems.push(`${where}: "selector" is empty`);
         }

         if (!byIsPair) {
            problems.push(`${where}: "by" must be a pair of finite numbers, as in [120, 80]`);
         }

         if (badSteps) {
            problems.push(`${where}: "steps" must be a whole number from 1 to ${MAX_DRAG_STEPS}`);
         }

         if (badDuration) {
            problems.push(`${where}: "duration_ms" must be above 0 and at most ${MAX_DRAG_DURATION_MS}`);
         }
         break;
      }
      case "type":
         if (step.text === "") {
            problems.push(`${where}: "text" is empty`);
         }
         break;
      case "press":
         if (parseKeyCombo(step.key) === null) {
            problems.push(`${where}: unknown key "${step.key}" (modifiers are Alt, Control, Meta and Shift, as in "Meta+/")`);
         }
         break;
      case "wait_for":
         checkOneTarget(step, where, problems);
         break;
      case "wait": {
         const msIsInvalid = !(step.ms >= 0 && Number.isFinite(step.ms));

         if (msIsInvalid) {
            problems.push(`${where}: "ms" must be 0 or more`);
         }
         break;
      }
      case "viewport":
         checkViewportValues(step, where, problems);
         break;
      case "media": {
         const setsNothing = step.reduced_motion === undefined && step.color_scheme === undefined;
         const badMotion = step.reduced_motion !== undefined && !REDUCED_MOTION_VALUES.includes(step.reduced_motion);
         const badScheme = step.color_scheme !== undefined && !COLOR_SCHEME_VALUES.includes(step.color_scheme);

         if (setsNothing) {
            problems.push(`${where}: set "reduced_motion", "color_scheme" or both`);
         }

         if (badMotion) {
            problems.push(`${where}: "reduced_motion" must be one of ${REDUCED_MOTION_VALUES.join(", ")}`);
         }

         if (badScheme) {
            problems.push(`${where}: "color_scheme" must be one of ${COLOR_SCHEME_VALUES.join(", ")}`);
         }
         break;
      }
      case "screenshot":
         if (!step.path.toLowerCase().endsWith(".png")) {
            problems.push(`${where}: "path" must end in .png`);
         }
         break;
      case "cookie": {
         checkUrl(step.url, where, "url", problems);

         const isWebUrl = /^https?:\/\//.test(step.url);

         if (!isWebUrl) {
            problems.push(`${where}: a cookie "url" must start with http:// or https://`);
         }
         break;
      }
   }

   checkTimeout(step, where, problems);
}

function validateScript(script) {
   const problems = [];

   if (!isPlainObject(script)) {
      return ["the script must be a JSON object"];
   }

   checkFieldTypes(script, SCRIPT_FIELDS.required, SCRIPT_FIELDS.optional, "script", problems);

   const hasViewport = script.viewport !== undefined;

   if (hasViewport && !isPlainObject(script.viewport)) {
      problems.push("viewport: must be an object");
   } else if (hasViewport) {
      checkFieldTypes(script.viewport, VIEWPORT_FIELDS.required, VIEWPORT_FIELDS.optional, "viewport", problems);
      checkViewportValues(script.viewport, "viewport", problems);
   }

   const fps = script.fps;
   const fpsIsInvalid = fps !== undefined && !(Number.isInteger(fps) && fps >= 1 && fps <= MAX_FPS);

   if (fpsIsInvalid) {
      problems.push(`fps: must be a whole number from 1 to ${MAX_FPS}`);
   }

   const hasStepList = Array.isArray(script.steps) && script.steps.length > 0;

   if (!hasStepList) {
      problems.push("steps: must be a non-empty list");

      return problems;
   }

   script.steps.forEach((step, index) => {
      const where = `step ${index + 1}`;

      if (!isPlainObject(step)) {
         problems.push(`${where}: must be an object`);

         return;
      }

      const isKnownKind = typeof step.do === "string" && Object.hasOwn(STEP_FIELDS, step.do);

      if (!isKnownKind) {
         problems.push(`${where}: unknown "do" ${JSON.stringify(step.do)} (known: ${Object.keys(STEP_FIELDS).join(", ")})`);

         return;
      }

      const fields = STEP_FIELDS[step.do];
      const kindWhere = `${where} (${step.do})`;
      const typeProblems = [];

      checkFieldTypes(step, fields.required, { ...COMMON_STEP_FIELDS, ...fields.optional }, kindWhere, typeProblems);
      problems.push(...typeProblems);

      if (typeProblems.length === 0) {
         checkStepMeaning(step, kindWhere, problems);
      }
   });

   return problems;
}

function parseKeyCombo(combo) {
   const match = /^((?:(?:Alt|Control|Meta|Shift)\+)*)(.+)$/.exec(combo);

   if (match === null) {
      return null;
   }

   const modifierNames = match[1].split("+").filter((name) => name !== "");
   const keyName = match[2];
   const modifiers = modifierNames.reduce((bits, name) => bits | MODIFIER_BITS[name], 0);
   const shiftHeld = (modifiers & MODIFIER_BITS.Shift) !== 0;
   if (Object.hasOwn(NAMED_KEYS, keyName)) {
      const named = NAMED_KEYS[keyName];

      return { key: named.key ?? keyName, code: named.code, keyCode: named.keyCode, text: named.text, modifiers };
   }

   const isLetter = /^[a-zA-Z]$/.test(keyName);

   if (isLetter) {
      const upper = keyName.toUpperCase();
      const key = shiftHeld ? upper : keyName;

      return { key, code: `Key${upper}`, keyCode: upper.charCodeAt(0), text: key, modifiers };
   }

   const isDigit = /^[0-9]$/.test(keyName);

   if (isDigit) {
      return { key: keyName, code: `Digit${keyName}`, keyCode: keyName.charCodeAt(0), text: keyName, modifiers };
   }

   if (Object.hasOwn(PUNCTUATION_KEYS, keyName)) {
      const punctuation = PUNCTUATION_KEYS[keyName];

      return { key: keyName, code: punctuation.code, keyCode: punctuation.keyCode, text: keyName, modifiers };
   }

   return null;
}

function describeTarget(step) {
   if (step.selector !== undefined) {
      return step.selector;
   }

   const roleNote = step.role === undefined ? "" : ` (role ${step.role})`;

   return `text ${JSON.stringify(step.text)}${roleNote}`;
}

function describeStep(step) {
   let description;

   switch (step.do) {
      case "navigate":
         description = `navigate ${step.url}`;
         break;
      case "click":
         description = `click ${describeTarget(step)}`;
         break;
      case "drag": {
         const [dx, dy] = step.by;
         const moveCount = step.steps ?? DEFAULT_DRAG_STEPS;
         const durationMs = step.duration_ms ?? DEFAULT_DRAG_DURATION_MS;

         description = `drag ${step.selector} by (${dx}, ${dy}) in ${moveCount} moves over ${durationMs} ms`;
         break;
      }
      case "type":
         description = `type into ${step.selector ?? "the focused element"} (value hidden)`;
         break;
      case "press":
         description = `press ${step.key}`;
         break;
      case "wait_for":
         description = `wait_for ${describeTarget(step)}, up to ${step.timeout_ms ?? DEFAULT_WAIT_TIMEOUT_MS} ms`;
         break;
      case "wait":
         description = `wait ${step.ms} ms`;
         break;
      case "viewport": {
         const mobileNote = step.mobile ? " mobile" : "";

         description = `viewport ${step.width}x${step.height} at ${step.deviceScaleFactor ?? 1}x${mobileNote}`;
         break;
      }
      case "media": {
         const settings = [];

         if (step.reduced_motion !== undefined) {
            settings.push(`reduced_motion ${step.reduced_motion}`);
         }

         if (step.color_scheme !== undefined) {
            settings.push(`color_scheme ${step.color_scheme}`);
         }

         description = `media ${settings.join(", ")}`;
         break;
      }
      case "eval":
         description = `eval ${shorten(step.expression.replace(/\s+/g, " "), 100)}`;
         break;
      case "screenshot":
         description = `screenshot ${resolve(step.path)}`;
         break;
      case "caption":
         description = `caption ${JSON.stringify(step.text)}`;
         break;
      case "cookie":
         description = `cookie ${step.name} for ${step.url} (value hidden)`;
         break;
   }

   const hasCaption = step.caption !== undefined && step.do !== "caption";

   return hasCaption ? `${description} [caption ${JSON.stringify(step.caption)}]` : description;
}

function startingViewport(script) {
   return { ...DEFAULT_VIEWPORT, ...(script.viewport ?? {}) };
}

function videoCanvas(viewport) {
   const width = Math.round(viewport.width * viewport.deviceScaleFactor);
   const height = Math.round(viewport.height * viewport.deviceScaleFactor);

   return { width: width + (width % 2), height: height + (height % 2) };
}

function captionTexts(steps) {
   const texts = new Set();

   for (const step of steps) {
      const stepCaption = step.do === "caption" ? step.text : step.caption;
      const showsText = typeof stepCaption === "string" && stepCaption !== "";

      if (showsText) {
         texts.add(stepCaption);
      }
   }

   return [...texts];
}

function freePort() {
   return new Promise((done, fail) => {
      const server = createServer();

      server.once("error", fail);
      server.listen(0, "127.0.0.1", () => {
         const { port } = server.address();

         server.close(() => done(port));
      });
   });
}

function killBrowserGroup(browser) {
   try {
      process.kill(-browser.pid, "SIGKILL");
   } catch {
      return false;
   }

   return true;
}

function waitForExit(child, timeoutMs) {
   const alreadyExited = child.exitCode !== null || child.signalCode !== null;

   if (alreadyExited) {
      return Promise.resolve(true);
   }

   return new Promise((done) => {
      const timer = setTimeout(() => done(false), timeoutMs);

      child.once("exit", () => {
         clearTimeout(timer);
         done(true);
      });
   });
}

async function launchBrave() {
   const profileDir = mkdtempSync(join(tmpdir(), "record-walkthrough-profile-"));
   const port = await freePort();
   const args = [
      "--headless=new",
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profileDir}`,
      "--no-first-run",
      "--no-default-browser-check",
      "--hide-scrollbars",
      "--disable-gpu",
      "about:blank"
   ];

   const browser = spawn(BRAVE, args, { detached: true, stdio: ["ignore", "ignore", "pipe"] });
   const launched = { browser, profileDir, closed: false };
   let launchOutput = "";

   browser.stderr.on("data", (chunk) => {
      launchOutput = (launchOutput + chunk).slice(-4000);
   });

   const stopOnSignal = (signal) => {
      killBrowserGroup(browser);

      try {
         rmSync(profileDir, { recursive: true, force: true, maxRetries: 3, retryDelay: 200 });
      } catch {
         console.error(`left the Brave profile at ${profileDir}`);
      }

      process.exit(signal === "SIGINT" ? 130 : 143);
   };

   process.once("SIGINT", stopOnSignal);
   process.once("SIGTERM", stopOnSignal);
   process.once("exit", () => {
      if (!launched.closed) {
         killBrowserGroup(browser);
      }
   });

   const deadline = Date.now() + LAUNCH_TIMEOUT_MS;

   while (Date.now() < deadline) {
      const browserExited = browser.exitCode !== null || browser.signalCode !== null;

      if (browserExited) {
         rmSync(profileDir, { recursive: true, force: true });
         throw new Error(`Brave exited with ${browser.exitCode ?? browser.signalCode}:\n${launchOutput}`);
      }

      try {
         const response = await fetch(`http://127.0.0.1:${port}/json/version`, { signal: AbortSignal.timeout(1000) });
         const version = await response.json();

         return Object.assign(launched, { socketUrl: version.webSocketDebuggerUrl, product: version.Browser });
      } catch {
         await sleep(250);
      }
   }

   killBrowserGroup(browser);
   rmSync(profileDir, { recursive: true, force: true, maxRetries: 3, retryDelay: 200 });
   throw new Error(`Brave did not open its debugging port within ${LAUNCH_TIMEOUT_MS / 1000} s:\n${launchOutput}`);
}

async function closeBrave(launched, connection) {
   if (connection !== null) {
      await connection.send("Browser.close", {}, undefined, 3000).catch(() => undefined);
      connection.close();
   }

   const exitedCleanly = await waitForExit(launched.browser, BROWSER_EXIT_WAIT_MS);

   killBrowserGroup(launched.browser);
   await waitForExit(launched.browser, BROWSER_EXIT_WAIT_MS);
   launched.closed = true;
   rmSync(launched.profileDir, { recursive: true, force: true, maxRetries: 3, retryDelay: 200 });

   return exitedCleanly;
}

class DevToolsConnection {
   constructor(socketUrl) {
      this.socket = new WebSocket(socketUrl);
      this.nextId = 1;
      this.pending = new Map();
      this.listeners = [];
      this.isClosed = false;
   }

   async open() {
      await withDeadline(new Promise((done, fail) => {
         this.socket.addEventListener("open", done, { once: true });
         this.socket.addEventListener("error", () => fail(new Error("the DevTools socket did not open")), { once: true });
      }), CDP_CALL_TIMEOUT_MS, "opening the DevTools socket");

      this.socket.addEventListener("message", (event) => this.receive(JSON.parse(event.data)));
      this.socket.addEventListener("close", () => this.closed());
   }

   closed() {
      this.isClosed = true;

      for (const waiter of this.pending.values()) {
         waiter.fail(new Error(`${waiter.method}: the DevTools socket closed`));
      }

      this.pending.clear();
   }

   receive(message) {
      const isReply = message.id !== undefined;

      if (!isReply) {
         for (const listener of this.listeners) {
            listener(message);
         }

         return;
      }

      const waiter = this.pending.get(message.id);

      this.pending.delete(message.id);

      if (waiter === undefined) {
         return;
      }

      if (message.error) {
         waiter.fail(new Error(`${waiter.method}: ${message.error.message}`));
      } else {
         waiter.done(message.result);
      }
   }

   send(method, params = {}, sessionId = undefined, timeoutMs = CDP_CALL_TIMEOUT_MS) {
      const id = this.nextId++;
      const reply = new Promise((done, fail) => {
         if (this.isClosed) {
            fail(new Error(`${method}: the DevTools socket closed`));

            return;
         }

         this.pending.set(id, { done, fail, method });
         this.socket.send(JSON.stringify({ id, method, params, sessionId }));
      });

      return withDeadline(reply, timeoutMs, method).finally(() => this.pending.delete(id));
   }

   onEvent(listener) {
      this.listeners.push(listener);
   }

   close() {
      this.socket.close();
   }
}

class Page {
   constructor(connection, sessionId, targetId) {
      this.connection = connection;
      this.sessionId = sessionId;
      this.targetId = targetId;
   }

   send(method, params = {}, timeoutMs = CDP_CALL_TIMEOUT_MS) {
      return this.connection.send(method, params, this.sessionId, timeoutMs);
   }

   onEvent(method, handler) {
      this.connection.onEvent((message) => {
         const isForThisPage = message.sessionId === this.sessionId && message.method === method;

         if (isForThisPage) {
            handler(message.params);
         }
      });
   }

   async evaluate(expression, timeoutMs = CDP_CALL_TIMEOUT_MS) {
      const reply = await this.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true }, timeoutMs);

      if (reply.exceptionDetails) {
         throw new Error(`the page threw: ${reply.exceptionDetails.exception?.description ?? reply.exceptionDetails.text}`);
      }

      return reply.result.value;
   }

   async waitUntil(expression, timeoutMs, label) {
      const deadline = Date.now() + timeoutMs;
      let lastError = null;

      while (Date.now() < deadline) {
         const remainingMs = Math.max(deadline - Date.now(), 1000);

         try {
            const value = await this.evaluate(expression, remainingMs);

            if (value) {
               return value;
            }

            lastError = null;
         } catch (error) {
            lastError = error;
         }

         await sleep(POLL_INTERVAL_MS);
      }

      const detail = lastError === null ? "" : ` (last error: ${lastError.message})`;

      throw new Error(`timed out after ${timeoutMs} ms waiting for ${label}${detail}`);
   }
}

async function openPage(connection) {
   const { targetId } = await connection.send("Target.createTarget", { url: "about:blank" });
   const { sessionId } = await connection.send("Target.attachToTarget", { targetId, flatten: true });
   const page = new Page(connection, sessionId, targetId);

   await page.send("Page.enable");

   return page;
}

class Recorder {
   constructor(page, framesDir) {
      this.page = page;
      this.framesDir = framesDir;
      this.frames = [];
      this.isRecording = false;
      this.stoppedAt = null;

      page.onEvent("Page.screencastFrame", (params) => this.receive(params));
   }

   receive(params) {
      const arrivedAt = Date.now() / 1000;

      this.page.send("Page.screencastFrameAck", { sessionId: params.sessionId }).catch(() => undefined);

      if (!this.isRecording) {
         return;
      }

      const fileName = `frame-${String(this.frames.length + 1).padStart(6, "0")}.jpg`;

      writeFileSync(join(this.framesDir, fileName), Buffer.from(params.data, "base64"));
      this.frames.push({ fileName, timestamp: params.metadata?.timestamp ?? arrivedAt, arrivedAt });
   }

   async start(canvas) {
      this.isRecording = true;
      await this.page.send("Page.startScreencast", { format: "jpeg", quality: 80, maxWidth: canvas.width, maxHeight: canvas.height, everyNthFrame: 1 });
   }

   // Brave sometimes sends no screencast frame after an emulation change until something else
   // repaints, and a throwaway screenshot makes it paint one.
   async nudgeIfSilent(sinceSeconds) {
      if (!this.isRecording) {
         return;
      }

      const deadline = Date.now() + SILENT_SCREENCAST_WAIT_MS;

      while (Date.now() < deadline) {
         const latest = this.frames.at(-1);
         const sawNewFrame = latest !== undefined && latest.arrivedAt >= sinceSeconds;

         if (sawNewFrame) {
            return;
         }

         await sleep(25);
      }

      await this.page.send("Page.captureScreenshot", { format: "jpeg", quality: 10 }).catch(() => undefined);
   }

   async stop() {
      if (!this.isRecording) {
         return;
      }

      await sleep(SCREENCAST_SETTLE_MS);
      this.stoppedAt = Date.now() / 1000;
      this.isRecording = false;
      await this.page.send("Page.stopScreencast", {}, 5000).catch(() => undefined);
   }
}

function captionPageExpression(text, canvas) {
   const fontPx = Math.max(18, Math.round(canvas.width / 42));
   const gapPx = Math.round(fontPx * 1.1);
   const css = [
      "html, body { margin: 0; background: transparent; }",
      `#strip { position: fixed; left: 0; right: 0; bottom: 0; display: flex; justify-content: center; padding-bottom: ${gapPx}px; }`,
      `#box { max-width: 88%; box-sizing: border-box; padding: ${Math.round(fontPx * 0.45)}px ${Math.round(fontPx * 0.9)}px;`,
      `border-radius: ${Math.round(fontPx * 0.35)}px; background: rgba(12, 12, 16, 0.84); color: #ffffff;`,
      `font: 600 ${fontPx}px/1.35 -apple-system, "Helvetica Neue", Arial, sans-serif; text-align: center; white-space: pre-wrap; }`
   ].join("\n");

   return `(async () => {
      document.head.innerHTML = "<style>" + ${JSON.stringify(css)} + "</style>";
      document.body.innerHTML = "<div id='strip'><div id='box'></div></div>";
      document.getElementById("box").textContent = ${JSON.stringify(text)};
      await document.fonts.ready;
      await new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));

      return document.getElementById("strip").getBoundingClientRect().top;
   })()`;
}

async function renderCaptionImages(connection, texts, canvas, captionsDir) {
   const images = new Map();

   if (texts.length === 0) {
      return images;
   }

   mkdirSync(captionsDir, { recursive: true });

   const page = await openPage(connection);

   await page.send("Emulation.setDeviceMetricsOverride", { width: canvas.width, height: canvas.height, deviceScaleFactor: 1, mobile: false });
   await page.send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });

   for (const [index, text] of texts.entries()) {
      const stripTop = await page.evaluate(captionPageExpression(text, canvas));
      const rawHeight = Math.min(canvas.height - Math.floor(stripTop), canvas.height);
      const stripHeight = rawHeight + (rawHeight % 2);
      const clip = { x: 0, y: canvas.height - stripHeight, width: canvas.width, height: stripHeight, scale: 1 };
      const shot = await page.send("Page.captureScreenshot", { format: "png", clip });
      const imagePath = join(captionsDir, `caption-${String(index + 1).padStart(3, "0")}.png`);

      writeFileSync(imagePath, Buffer.from(shot.data, "base64"));
      images.set(text, imagePath);
   }

   await connection.send("Target.closeTarget", { targetId: page.targetId }).catch(() => undefined);

   return images;
}

function elementLocator(step) {
   if (step.selector !== undefined) {
      return `() => {
         ${PAGE_HELPERS}
         const element = document.querySelector(${JSON.stringify(step.selector)});
         const isUsable = element !== null && isVisible(element);

         return isUsable ? element : null;
      }`;
   }

   return `() => {
      ${PAGE_HELPERS}
      const wanted = normalize(${JSON.stringify(step.text)});
      const wantedRole = ${JSON.stringify(step.role ?? null)};

      const roleOf = (element) => {
         const explicitRole = element.getAttribute("role");

         if (explicitRole !== null) {
            return explicitRole;
         }

         const implicitRoles = { button: "button", a: "link" };

         return implicitRoles[element.localName] ?? null;
      };

      const labelOf = (element) => normalize(element.innerText);
      const ariaLabelOf = (element) => normalize(element.getAttribute("aria-label"));

      const candidates = [...document.querySelectorAll("button, a, [role]")].filter((element) => {
         const roleMatches = wantedRole === null || roleOf(element) === wantedRole;

         return roleMatches && isVisible(element);
      });

      const exact = candidates.find((element) => {
         const labelMatches = labelOf(element) === wanted;
         const ariaLabelMatches = ariaLabelOf(element) === wanted;

         return labelMatches || ariaLabelMatches;
      });

      if (exact !== undefined) {
         return exact;
      }

      const partial = candidates
         .filter((element) => labelOf(element).includes(wanted))
         .sort((first, second) => labelOf(first).length - labelOf(second).length);

      return partial[0] ?? null;
   }`;
}

async function navigate(page, step) {
   const timeoutMs = step.timeout_ms ?? NAVIGATE_TIMEOUT_MS;
   const reply = await page.send("Page.navigate", { url: step.url }, timeoutMs);

   if (reply.errorText) {
      throw new Error(`navigation failed: ${reply.errorText}`);
   }

   await page.waitUntil("document.readyState === \"complete\"", timeoutMs, "the page to finish loading");
}

function elementCentre(page, step) {
   const pointExpression = `(() => {
      const element = (${elementLocator(step)})();

      if (element === null) {
         return null;
      }

      element.scrollIntoView({ block: "center", inline: "center", behavior: "instant" });

      const box = element.getBoundingClientRect();

      return { x: box.left + box.width / 2, y: box.top + box.height / 2 };
   })()`;

   return page.waitUntil(pointExpression, step.timeout_ms ?? DEFAULT_WAIT_TIMEOUT_MS, describeTarget(step));
}

async function click(page, step) {
   const point = await elementCentre(page, step);

   for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
      const buttons = type === "mousePressed" ? 1 : 0;

      await page.send("Input.dispatchMouseEvent", { type, x: point.x, y: point.y, button: "left", buttons, clickCount: 1 });
   }
}

async function drag(page, step) {
   const start = await elementCentre(page, step);
   const [dx, dy] = step.by;
   const end = { x: start.x + dx, y: start.y + dy };
   const moveCount = step.steps ?? DEFAULT_DRAG_STEPS;
   const pauseMs = (step.duration_ms ?? DEFAULT_DRAG_DURATION_MS) / moveCount;

   await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: start.x, y: start.y, button: "none", buttons: 0 });
   await page.send("Input.dispatchMouseEvent", { type: "mousePressed", x: start.x, y: start.y, button: "left", buttons: 1, clickCount: 1 });

   for (let move = 1; move <= moveCount; move += 1) {
      const progress = move / moveCount;
      const x = start.x + dx * progress;
      const y = start.y + dy * progress;

      await sleep(pauseMs);
      await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x, y, button: "left", buttons: 1 });
   }

   await page.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: end.x, y: end.y, button: "left", buttons: 0, clickCount: 1 });
}

async function typeText(page, step) {
   if (step.selector !== undefined) {
      const focusExpression = `(() => {
         const element = (${elementLocator(step)})();

         if (element === null) {
            return false;
         }

         element.focus();

         return true;
      })()`;

      await page.waitUntil(focusExpression, step.timeout_ms ?? DEFAULT_WAIT_TIMEOUT_MS, step.selector);
   }

   await page.send("Input.insertText", { text: step.text });
}

async function pressKey(page, step) {
   const parsed = parseKeyCombo(step.key);
   const commandBits = MODIFIER_BITS.Alt | MODIFIER_BITS.Control | MODIFIER_BITS.Meta;
   const commandHeld = (parsed.modifiers & commandBits) !== 0;
   const typesText = parsed.text !== undefined && !commandHeld;
   const keyFields = {
      key: parsed.key,
      code: parsed.code,
      windowsVirtualKeyCode: parsed.keyCode,
      modifiers: parsed.modifiers
   };

   await page.send("Input.dispatchKeyEvent", {
      ...keyFields,
      type: typesText ? "keyDown" : "rawKeyDown",
      text: typesText ? parsed.text : undefined,
      unmodifiedText: typesText ? parsed.text : undefined
   });
   await page.send("Input.dispatchKeyEvent", { ...keyFields, type: "keyUp" });
}

async function waitFor(page, step) {
   const timeoutMs = step.timeout_ms ?? DEFAULT_WAIT_TIMEOUT_MS;

   if (step.selector !== undefined) {
      await page.waitUntil(`(${elementLocator(step)})() !== null`, timeoutMs, step.selector);

      return;
   }

   const textExpression = `document.body !== null && document.body.innerText.includes(${JSON.stringify(step.text)})`;

   await page.waitUntil(textExpression, timeoutMs, describeTarget(step));
}

async function emulateMedia(page, step, context) {
   context.media = { ...context.media };

   if (step.reduced_motion !== undefined) {
      context.media.reducedMotion = step.reduced_motion;
   }

   if (step.color_scheme !== undefined) {
      context.media.colorScheme = step.color_scheme;
   }

   const features = [];

   if (context.media.reducedMotion !== undefined) {
      features.push({ name: "prefers-reduced-motion", value: context.media.reducedMotion });
   }

   if (context.media.colorScheme !== undefined) {
      features.push({ name: "prefers-color-scheme", value: context.media.colorScheme });
   }

   await page.send("Emulation.setEmulatedMedia", { media: "", features });
}

function setViewport(page, viewport) {
   return page.send("Emulation.setDeviceMetricsOverride", {
      width: viewport.width,
      height: viewport.height,
      deviceScaleFactor: viewport.deviceScaleFactor ?? 1,
      mobile: viewport.mobile ?? false
   });
}

async function saveScreenshot(page, path) {
   const shot = await page.send("Page.captureScreenshot", { format: "png" });

   mkdirSync(dirname(path), { recursive: true });
   writeFileSync(path, Buffer.from(shot.data, "base64"));
}

async function setCookie(page, step) {
   const reply = await page.send("Network.setCookie", { name: step.name, value: step.value, url: step.url });

   if (reply.success === false) {
      throw new Error(`the browser refused cookie ${step.name}`);
   }
}

function setCaption(context, text) {
   context.captionLog.push({ text, at: Date.now() / 1000 });
}

async function runStep(context, step) {
   const page = context.page;
   const startedAt = Date.now() / 1000;

   if (step.caption !== undefined) {
      setCaption(context, step.caption);
   }

   switch (step.do) {
      case "navigate":
         await navigate(page, step);
         break;
      case "click":
         await click(page, step);
         break;
      case "drag":
         await drag(page, step);
         break;
      case "type":
         await typeText(page, step);
         break;
      case "press":
         await pressKey(page, step);
         break;
      case "wait_for":
         await waitFor(page, step);
         break;
      case "wait":
         await sleep(step.ms);
         break;
      case "viewport":
         await setViewport(page, step);
         await context.recorder.nudgeIfSilent(startedAt);
         break;
      case "media":
         await emulateMedia(page, step, context);
         await context.recorder.nudgeIfSilent(startedAt);
         break;
      case "eval": {
         const value = await page.evaluate(step.expression);
         const shown = value === undefined ? "undefined" : JSON.stringify(value);

         log(`   eval result: ${shorten(shown, 300)}`);
         break;
      }
      case "screenshot": {
         const path = resolve(step.path);

         await saveScreenshot(page, path);
         log(`   saved ${path}`);
         break;
      }
      case "caption":
         setCaption(context, step.text);
         break;
      case "cookie":
         await setCookie(page, step);
         break;
   }
}

function buildTimeline(recorder, captionLog, fps) {
   const frames = [...recorder.frames].sort((first, second) => first.timestamp - second.timestamp);
   const clockOffset = frames.reduce((smallest, frame) => Math.min(smallest, frame.arrivedAt - frame.timestamp), Infinity);
   const origin = frames[0].timestamp;
   const videoTimeOf = (wallSeconds) => wallSeconds - clockOffset - origin;
   const lastFrame = frames.at(-1);
   const lastStartsAt = lastFrame.timestamp - origin;
   const stoppedAt = videoTimeOf(recorder.stoppedAt ?? lastFrame.arrivedAt);
   const capturedSeconds = lastStartsAt + Math.max(stoppedAt - lastStartsAt, LAST_FRAME_HOLD_SECONDS);
   const outputFrameCount = Math.max(1, Math.round(capturedSeconds * fps));
   const totalSeconds = outputFrameCount / fps;

   const startsBy = (index, seconds) => {
      const frame = frames[index];

      return frame !== undefined && frame.timestamp - origin <= seconds;
   };

   const shownFrames = [];
   let showing = 0;

   for (let outputIndex = 0; outputIndex < outputFrameCount; outputIndex += 1) {
      const sampledAt = outputIndex / fps;

      while (startsBy(showing + 1, sampledAt)) {
         showing += 1;
      }

      shownFrames.push(frames[showing].fileName);
   }

   const clampToVideo = (seconds) => Math.min(Math.max(seconds, 0), totalSeconds);
   const captions = [];

   captionLog.forEach((entry, index) => {
      const next = captionLog[index + 1];
      const start = clampToVideo(videoTimeOf(entry.at));
      const end = next === undefined ? totalSeconds : clampToVideo(videoTimeOf(next.at));
      const isShown = entry.text !== "" && end > start;

      if (isShown) {
         captions.push({ text: entry.text, start, end });
      }
   });

   const captured = frames.map((frame) => ({
      fileName: frame.fileName,
      startsAt: frame.timestamp - origin,
      arrivedAt: videoTimeOf(frame.arrivedAt)
   }));

   return { totalSeconds, clockOffset, captions, captured, shownFrames };
}

function runFfmpeg(args) {
   const result = spawnSync(FFMPEG, ["-y", "-hide_banner", "-loglevel", "error", ...args], { encoding: "utf8", timeout: FFMPEG_TIMEOUT_MS });
   const failed = result.status !== 0;

   if (failed) {
      throw new Error(`ffmpeg failed (${result.status ?? result.signal}): ${result.stderr || result.error?.message}`);
   }
}

function linkOrCopy(source, target) {
   try {
      linkSync(source, target);
   } catch {
      copyFileSync(source, target);
   }
}

function stitchVideo({ timeline, framesDir, workDir, captionImages, canvas, fps, outPath }) {
   const sequenceDir = join(workDir, "sequence");
   const sequencePattern = join(sequenceDir.replaceAll("%", "%%"), "%06d.jpg");
   const basePath = join(workDir, "base.mp4");

   rmSync(sequenceDir, { recursive: true, force: true });
   mkdirSync(sequenceDir, { recursive: true });
   writeFileSync(join(workDir, "timeline.json"), JSON.stringify(timeline, null, 3) + "\n");

   timeline.shownFrames.forEach((fileName, index) => {
      linkOrCopy(join(framesDir, fileName), join(sequenceDir, `${String(index + 1).padStart(6, "0")}.jpg`));
   });

   const fitToCanvas = [
      `scale=${canvas.width}:${canvas.height}:force_original_aspect_ratio=decrease`,
      `pad=${canvas.width}:${canvas.height}:(ow-iw)/2:(oh-ih)/2:color=${LETTERBOX_COLOR}`,
      "scale=out_range=tv",
      "format=yuv420p"
   ].join(",");

   runFfmpeg([
      "-framerate", String(fps),
      "-start_number", "1",
      "-i", sequencePattern,
      "-vf", fitToCanvas,
      "-fps_mode", "cfr",
      "-c:v", "libx264",
      "-preset", "veryfast",
      "-crf", "12",
      "-pix_fmt", "yuv420p",
      "-color_range", "tv",
      basePath
   ]);

   const inputs = ["-i", basePath];
   const chains = [];
   let current = "[0:v]";

   timeline.captions.forEach((caption, index) => {
      const label = `[captioned${index + 1}]`;
      const shownWhile = `gte(t,${caption.start.toFixed(3)})*lt(t,${caption.end.toFixed(3)})`;

      inputs.push("-i", captionImages.get(caption.text));
      chains.push(`${current}[${index + 1}:v]overlay=x=0:y=main_h-overlay_h:enable='${shownWhile}'${label}`);
      current = label;
   });

   chains.push(`${current}scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p[video]`);
   runFfmpeg([
      ...inputs,
      "-filter_complex", chains.join(";"),
      "-map", "[video]",
      "-r", String(fps),
      "-fps_mode", "cfr",
      "-c:v", "libx264",
      "-preset", "medium",
      "-crf", "22",
      "-pix_fmt", "yuv420p",
      "-color_range", "tv",
      "-movflags", "+faststart",
      outPath
   ]);
}

function failureScreenshotPath(outPath, stepNumber) {
   const stem = basename(outPath, extname(outPath));

   return join(dirname(outPath), `${stem}.failed-step-${stepNumber}.png`);
}

function readScript(scriptPath) {
   const text = readFileSync(scriptPath, "utf8");

   try {
      return JSON.parse(text);
   } catch (error) {
      throw new Error(`${scriptPath} is not valid JSON: ${error.message}`);
   }
}

function printPlan(scriptPath, script, canvas, fps, outPath) {
   const viewport = startingViewport(script);
   const mobileNote = viewport.mobile ? " mobile" : "";

   console.log(`script ${scriptPath}: ${script.steps.length} steps, viewport ${viewport.width}x${viewport.height} at ${viewport.deviceScaleFactor}x${mobileNote}, video ${canvas.width}x${canvas.height} at ${fps} fps`);

   script.steps.forEach((step, index) => {
      console.log(`${String(index + 1).padStart(4)}. ${describeStep(step)}`);
   });

   if (outPath !== null) {
      console.log(`output ${outPath}`);
   }
}

async function record({ script, canvas, fps, outPath, workDir }) {
   const framesDir = join(workDir, "frames");
   const launched = await launchBrave();
   const steps = script.steps;
   let connection = null;
   let recorder = null;
   let failure = null;
   let stepsRun = 0;
   let captionImages = new Map();
   const context = { page: null, recorder: null, captionLog: [], media: {} };

   mkdirSync(framesDir, { recursive: true });

   try {
      connection = new DevToolsConnection(launched.socketUrl);
      await connection.open();
      log(`${launched.product}, video ${canvas.width}x${canvas.height} at ${fps} fps, frames in ${framesDir}`);

      captionImages = await renderCaptionImages(connection, captionTexts(steps), canvas, join(workDir, "captions"));
      context.page = await openPage(connection);
      recorder = new Recorder(context.page, framesDir);
      context.recorder = recorder;

      await setViewport(context.page, startingViewport(script));
      await context.page.send("Page.bringToFront");

      const firstNavigateIndex = steps.findIndex((step) => step.do === "navigate");

      if (firstNavigateIndex === -1) {
         await recorder.start(canvas);
      }

      for (const [index, step] of steps.entries()) {
         log(`step ${index + 1}/${steps.length} ${describeStep(step)}`);

         try {
            await runStep(context, step);
            stepsRun += 1;

            if (index === firstNavigateIndex) {
               await recorder.start(canvas);
            }
         } catch (error) {
            failure = { stepNumber: index + 1, kind: step.do, reason: error.message };
            break;
         }
      }

      if (failure !== null) {
         console.error(`step ${failure.stepNumber} (${failure.kind}) failed: ${failure.reason}`);

         const shotPath = failureScreenshotPath(outPath, failure.stepNumber);

         await saveScreenshot(context.page, shotPath)
            .then(() => console.error(`screenshot of the failure: ${shotPath}`))
            .catch((error) => console.error(`no failure screenshot: ${error.message}`));
      }

      await recorder.stop();
   } finally {
      const exitedCleanly = await closeBrave(launched, connection);

      if (!exitedCleanly) {
         log("Brave did not exit on Browser.close, so its process group was killed");
      }
   }

   return { frames: recorder?.frames ?? [], recorder, captionLog: context.captionLog, captionImages, failure, stepsRun, framesDir };
}

async function main() {
   let options;

   try {
      options = parseArgs({
         options: {
            script: { type: "string" },
            out: { type: "string" },
            "dry-run": { type: "boolean", default: false },
            "keep-frames": { type: "string" }
         }
      }).values;
   } catch (error) {
      console.error(`${error.message}\n${USAGE}`);

      return 2;
   }

   const isDryRun = options["dry-run"];
   const missingScript = options.script === undefined;
   const missingOut = options.out === undefined && !isDryRun;

   if (missingScript || missingOut) {
      console.error(USAGE);

      return 2;
   }

   const scriptPath = resolve(options.script);
   const outPath = options.out === undefined ? null : resolve(options.out);
   let script;

   try {
      script = readScript(scriptPath);
   } catch (error) {
      console.error(error.message);

      return 2;
   }

   const problems = validateScript(script);

   if (problems.length > 0) {
      console.error(`${scriptPath}: ${problems.length} problem(s)`);

      for (const problem of problems) {
         console.error(`   ${problem}`);
      }

      return 2;
   }

   const canvas = videoCanvas(startingViewport(script));
   const fps = script.fps ?? DEFAULT_FPS;

   if (isDryRun) {
      printPlan(scriptPath, script, canvas, fps, outPath);
      console.log("dry run: the script is valid, nothing was launched");

      return 0;
   }

   for (const tool of [BRAVE, FFMPEG]) {
      if (!existsSync(tool)) {
         console.error(`not found: ${tool}`);

         return 1;
      }
   }

   const keepFrames = options["keep-frames"] !== undefined;
   const workDir = keepFrames ? resolve(options["keep-frames"]) : mkdtempSync(join(tmpdir(), "record-walkthrough-"));

   mkdirSync(workDir, { recursive: true });
   mkdirSync(dirname(outPath), { recursive: true });

   const recording = await record({ script, canvas, fps, outPath, workDir });
   const totalSteps = script.steps.length;

   if (recording.frames.length === 0) {
      console.log(`${recording.stepsRun} of ${totalSteps} steps run, 0 frames, no video written`);

      return 1;
   }

   const timeline = buildTimeline(recording.recorder, recording.captionLog, fps);

   stitchVideo({ timeline, framesDir: recording.framesDir, workDir, captionImages: recording.captionImages, canvas, fps, outPath });

   if (!keepFrames) {
      rmSync(workDir, { recursive: true, force: true });
   }

   const outcome = recording.failure === null ? "done" : `stopped at step ${recording.failure.stepNumber}`;

   console.log(`${outcome}: ${recording.stepsRun} of ${totalSteps} steps run, ${recording.frames.length} frames, ${timeline.totalSeconds.toFixed(1)} s of video, ${outPath}`);

   return recording.failure === null ? 0 : 1;
}

main()
   .then((code) => process.exit(code))
   .catch((error) => {
      console.error(error.stack ?? error.message);
      process.exit(1);
   });
