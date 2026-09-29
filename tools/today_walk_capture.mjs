import { spawn } from "node:child_process";
import { mkdirSync, mkdtempSync, writeFileSync, existsSync, readFileSync } from "node:fs";
import { createServer } from "node:net";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const BRAVE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser";
const SCRATCH = "/private/tmp/claude-502/-Users-mahfujm-dev-growth/db01190c-9ae9-4388-976f-508d87d8e8ee/scratchpad";
const REPO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SHOTS = join(REPO, "var", "today-redesign", "shots");

const VIEWPORTS = [
   { width: 1280, height: 900, mobile: false, scale: 1 },
   { width: 390, height: 844, mobile: true, scale: 2 }
];

const SCHEMES = ["dark", "light"];
const ITEM_COUNT = 6;
const LONG_WAIT_MS = 90000;
const HOME_WAIT_MS = 180000;
const SHORT_WAIT_MS = 15000;

const { values: options } = parseArgs({
   options: {
      web: { type: "string" },
      username: { type: "string" },
      password: { type: "string" },
      student: { type: "string" },
      viewports: { type: "string", default: "1280,390" },
      schemes: { type: "string", default: "dark,light" }
   }
});

const hasRequiredOptions = options.web && options.username && options.password && options.student;

if (!hasRequiredOptions) {
   console.error("usage: node tools/today_walk_capture.mjs --web <origin> --username <name> --password <pass> --student <label>");
   process.exit(2);
}

function sleep(ms) {
   return new Promise((done) => setTimeout(done, ms));
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

async function launchBrave() {
   mkdirSync(SCRATCH, { recursive: true });

   const profileDir = mkdtempSync(join(SCRATCH, "brave-profile-"));
   const port = await freePort();
   const args = [
      "--headless=new",
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profileDir}`,
      "--no-first-run",
      "--no-default-browser-check",
      "--disable-gpu",
      "--hide-scrollbars",
      "about:blank"
   ];

   const browser = spawn(BRAVE, args, { stdio: ["ignore", "pipe", "pipe"] });
   let launchOutput = "";

   browser.on("exit", (code, signal) => console.log(`Brave exited (code ${code}, signal ${signal})`));

   browser.stdout.on("data", (chunk) => (launchOutput += chunk));
   browser.stderr.on("data", (chunk) => (launchOutput += chunk));

   const deadline = Date.now() + 20000;

   while (Date.now() < deadline) {
      if (browser.exitCode !== null) {
         throw new Error(`Brave exited with code ${browser.exitCode}:\n${launchOutput}`);
      }

      try {
         const response = await fetch(`http://127.0.0.1:${port}/json/version`);
         const version = await response.json();

         return { browser, wsUrl: version.webSocketDebuggerUrl, product: version.Browser };
      } catch {
         await sleep(250);
      }
   }

   browser.kill();
   throw new Error(`Brave did not open its debugging port within 20 s:\n${launchOutput}`);
}

class Cdp {
   constructor(wsUrl) {
      this.socket = new WebSocket(wsUrl);
      this.nextId = 1;
      this.pending = new Map();
      this.listeners = [];
   }

   async open() {
      await new Promise((done, fail) => {
         this.socket.addEventListener("open", done, { once: true });
         this.socket.addEventListener("error", fail, { once: true });
      });

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

      if (isReply) {
         const waiter = this.pending.get(message.id);

         this.pending.delete(message.id);

         if (message.error) {
            waiter.fail(new Error(`${waiter.method}: ${message.error.message}`));
         } else {
            waiter.done(message.result);
         }

         return;
      }

      for (const listener of this.listeners) {
         listener(message);
      }
   }

   send(method, params = {}, sessionId = undefined) {
      const id = this.nextId++;

      return new Promise((done, fail) => {
         if (this.isClosed) {
            fail(new Error(`${method}: the DevTools socket closed`));

            return;
         }

         this.pending.set(id, { done, fail, method });
         this.socket.send(JSON.stringify({ id, method, params, sessionId }));
      });
   }

   onEvent(listener) {
      this.listeners.push(listener);
   }

   close() {
      this.socket.close();
   }
}

class Tab {
   constructor(cdp, sessionId, run) {
      this.cdp = cdp;
      this.sessionId = sessionId;
      this.run = run;
   }

   send(method, params = {}) {
      return this.cdp.send(method, params, this.sessionId);
   }

   async evaluate(expression) {
      const reply = await this.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });

      if (reply.exceptionDetails) {
         throw new Error(`page threw: ${reply.exceptionDetails.exception?.description ?? reply.exceptionDetails.text}`);
      }

      return reply.result.value;
   }

   async waitFor(expression, timeoutMs, label) {
      const deadline = Date.now() + timeoutMs;

      while (Date.now() < deadline) {
         const value = await this.evaluate(expression).catch(() => null);

         if (value) {
            return value;
         }

         await sleep(250);
      }

      throw new Error(`timed out after ${timeoutMs} ms waiting for ${label}`);
   }

   async has(selector) {
      return this.evaluate(`document.querySelector(${JSON.stringify(selector)}) !== null`);
   }

   /* Finds the element in the page, scrolls it into view and returns its centre, so the click is a
      real mouse press rather than a synthetic element.click(). */
   async clickWhere(finderSource, label) {
      const point = await this.evaluate(`(() => {
         const element = (${finderSource})();

         if (!element) {
            return null;
         }

         element.scrollIntoView({ block: "center", inline: "center" });
         const box = element.getBoundingClientRect();

         return { x: box.left + box.width / 2, y: box.top + box.height / 2 };
      })()`);

      if (point === null) {
         throw new Error(`nothing to click for ${label}`);
      }

      for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
         await this.send("Input.dispatchMouseEvent", { type, x: point.x, y: point.y, button: "left", clickCount: 1 });
      }
   }

   clickSelector(selector) {
      return this.clickWhere(`() => document.querySelector(${JSON.stringify(selector)})`, selector);
   }

   clickButtonText(text) {
      const finder = `() => [...document.querySelectorAll("button")].find((button) => button.textContent.trim().startsWith(${JSON.stringify(text)}))`;

      return this.clickWhere(finder, `button "${text}"`);
   }

   async buttonWithText(text) {
      return this.evaluate(`[...document.querySelectorAll("button")].some((button) => button.textContent.trim().startsWith(${JSON.stringify(text)}))`);
   }

   async typeInto(selector, text) {
      await this.evaluate(`(() => {
         const field = document.querySelector(${JSON.stringify(selector)});

         field.focus();

         if ("select" in field && field.tagName !== "MATH-FIELD") {
            field.select();
         }
      })()`);

      await this.send("Input.insertText", { text });
   }

   async capture(name) {
      await sleep(400);

      const overflow = await this.evaluate(`({
         scrollWidth: document.documentElement.scrollWidth,
         clientWidth: document.documentElement.clientWidth
      })`);
      const overflows = overflow.scrollWidth > overflow.clientWidth;
      const shot = await this.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true });
      const fileName = `${this.run.prefix}-${name}.png`;

      writeFileSync(join(SHOTS, fileName), Buffer.from(shot.data, "base64"));

      this.run.screens.push({ name, file: fileName, hash: await this.evaluate("location.hash"), overflows, ...overflow });

      if (overflows) {
         this.run.overflow = true;
      }

      console.log(`   ${fileName}${overflows ? `  (overflow ${overflow.scrollWidth} > ${overflow.clientWidth})` : ""}`);
   }
}

const SCREEN_STATE = `(() => {
   const present = (testId) => document.querySelector("[data-testid='" + testId + "']") !== null;

   for (const testId of ["session-end", "session-lesson", "feedback", "session-stage", "session-failed", "home", "home-failed"]) {
      if (present(testId)) {
         return testId;
      }
   }

   return null;
})()`;

async function signIn(tab, web) {
   await tab.send("Page.navigate", { url: web });
   await tab.waitFor("document.querySelector('#account-username') !== null || document.querySelector(\"[data-testid='home']\") !== null", LONG_WAIT_MS, "the sign-in form");

   const needsSignIn = await tab.has("#account-username");

   if (!needsSignIn) {
      return;
   }

   await tab.typeInto("#account-username", options.username);
   await tab.typeInto("#account-password", options.password);
   await tab.clickSelector("form button[type='submit']");
}

async function waitForHome(tab) {
   const settledOnHome = "document.querySelector(\"[data-testid='home']\") !== null || document.querySelector(\"[data-testid='home-failed']\") !== null";

   const startedAt = Date.now();

   try {
      await tab.waitFor(settledOnHome, HOME_WAIT_MS, "home");
      tab.run.homeWaitsMs.push(Date.now() - startedAt);

      return true;
   } catch (error) {
      tab.run.notes.push(`home did not settle: ${error.message}; hash ${await tab.evaluate("location.hash")}`);

      return false;
   }
}

async function answerItem(tab) {
   const hasOptions = await tab.has("[data-testid='mcq-answer'] input[type='radio']");
   const hasMathField = await tab.has("[data-testid='math-answer'] math-field");

   if (hasOptions) {
      await tab.clickWhere(`() => {
         const radios = document.querySelectorAll("[data-testid='mcq-answer'] input[type='radio']");
         const second = radios[1] ?? radios[0];

         return second.closest("label") ?? second;
      }`, "the second option");

      return "option 2";
   }

   if (hasMathField) {
      await tab.typeInto("[data-testid='math-answer'] math-field", "7");
      await sleep(1500);

      const inspected = await tab.evaluate("document.querySelector(\"[data-testid='latex-inspector'] code\")?.textContent ?? null");
      const inspectorShowsText = typeof inspected === "string" && inspected.trim().length > 0;

      if (!inspectorShowsText) {
         tab.run.notes.push(`raw LaTeX inspector empty after typing 7 (read ${JSON.stringify(inspected)})`);
      }

      return `typed 7, inspector ${JSON.stringify(inspected)}`;
   }

   return "no answer control";
}

async function commitAndWaitForFeedback(tab) {
   const deadline = Date.now() + LONG_WAIT_MS;
   let lastCommitAt = 0;

   while (Date.now() < deadline) {
      const state = await tab.evaluate(SCREEN_STATE);

      if (state === "feedback" || state === "session-end" || state === "session-lesson") {
         return state;
      }

      const confidenceUnrated = await tab.evaluate(
         "document.querySelector(\"[data-testid='confidence-prompt']\") !== null && document.querySelector(\"[data-testid='confidence-prompt'] input:checked\") === null"
      );

      if (confidenceUnrated) {
         await tab.clickWhere("() => document.querySelector(\"[data-testid='confidence-prompt'] input[value='confident']\").closest('label')", "confident");
         await sleep(300);
      }

      const commitVisible = await tab.has("button.motion-instant-submit-answer:not([disabled])");
      const commitIsDue = Date.now() - lastCommitAt > 3000;

      if (commitVisible && commitIsDue) {
         await tab.clickSelector("button.motion-instant-submit-answer");
         lastCommitAt = Date.now();
      }

      await sleep(300);
   }

   throw new Error("timed out waiting for feedback after Check my answer");
}

async function leaveLesson(tab, readingCount) {
   const exitFinder = `() => {
      const byTestId = document.querySelector("[data-testid='lesson-skip'], [data-testid='lesson-finish']");
      const exitLabels = ["Back to the problem", "Skip to the problem", "Go to the problem"];
      const byLabel = [...document.querySelectorAll("[data-testid='session-lesson'] button")].find((button) => exitLabels.some((label) => button.textContent.trim().startsWith(label)));

      return byTestId ?? byLabel;
   }`;

   const lessonState = `(() => {
      if (document.querySelector("[data-testid='session-lesson']") === null) {
         return "gone";
      }

      return (${exitFinder})() ? "ready" : false;
   })()`;
   const settled = await tab.waitFor(lessonState, SHORT_WAIT_MS, "the lesson to finish rendering");

   if (settled === "gone") {
      return false;
   }

   const lessonSignature = `(() => {
      const shown = document.querySelector("[data-testid='session-lesson']");

      if (shown === null) {
         return null;
      }

      const copy = shown.cloneNode(true);

      copy.querySelectorAll("[data-testid='session-remaining']").forEach((line) => line.remove());

      return copy.textContent.slice(0, 300);
   })()`;
   const shownLesson = await tab.evaluate(lessonSignature);
   const timesShown = (tab.run.lessonsShown.get(shownLesson) ?? 0) + 1;
   const isFirstShowing = timesShown === 1;

   tab.run.lessonsShown.set(shownLesson, timesShown);

   if (isFirstShowing) {
      await tab.capture(readingCount === 0 ? "reading" : `reading-${readingCount + 1}`);
   }

   try {
      await tab.clickWhere(exitFinder, "a way out of the lesson");
   } catch (error) {
      const lessonStillShown = await tab.has("[data-testid='session-lesson']");

      if (lessonStillShown) {
         throw error;
      }

      return isFirstShowing;
   }

   await tab.waitFor(`${lessonSignature} !== ${JSON.stringify(shownLesson)}`, LONG_WAIT_MS, "the lesson to close");

   return isFirstShowing;
}

async function walkSession(tab) {
   let itemNumber = 0;
   let readingCount = 0;

   while (itemNumber < ITEM_COUNT) {
      const state = await tab.waitFor(SCREEN_STATE + " ?? false", LONG_WAIT_MS, "a session screen");

      if (state === "session-end" || state === "session-failed") {
         tab.run.notes.push(`session reached ${state} after ${itemNumber} items`);

         return state;
      }

      if (state === "session-lesson") {
         const captured = await leaveLesson(tab, readingCount);

         readingCount += captured ? 1 : 0;
         continue;
      }

      if (state !== "session-stage") {
         throw new Error(`unexpected screen ${state} while walking the set`);
      }

      itemNumber += 1;

      const stage = (await tab.evaluate("document.querySelector(\"[data-testid='session-stage']\").textContent")).replace("Stage:", "").trim();

      await tab.capture(`item-${itemNumber}-${stage}`);

      const answered = await answerItem(tab);
      const afterCommit = await commitAndWaitForFeedback(tab);

      if (afterCommit !== "feedback") {
         tab.run.items.push({ number: itemNumber, stage, answered, verdict: null, after: afterCommit });
         continue;
      }

      const verdict = await tab.evaluate(`(() => {
         const head = document.querySelector("[data-testid='feedback-verdict']");

         if (!head) {
            return "noverdict";
         }

         return head.querySelector(".text-correct") ? "correct" : "incorrect";
      })()`);

      await tab.capture(`feedback-${itemNumber}-${verdict}`);

      const hasErrorNote = await tab.has("[data-testid='error-note-field'] textarea, [data-testid='error-note-field'] input");

      if (hasErrorNote) {
         await tab.typeInto("[data-testid='error-note-field'] textarea, [data-testid='error-note-field'] input", "note from the capture walk");
         await sleep(300);
      }

      tab.run.items.push({ number: itemNumber, stage, answered, verdict, errorNote: hasErrorNote });

      await tab.waitFor("document.querySelector('button.motion-instant-question-move:not([disabled])') !== null", SHORT_WAIT_MS, "Next item to enable");
      await tab.clickSelector("button.motion-instant-question-move");
      await tab.waitFor("document.querySelector(\"[data-testid='feedback']\") === null", LONG_WAIT_MS, "feedback to close");
   }

   while (true) {
      const state = await tab.waitFor(SCREEN_STATE + " ?? false", LONG_WAIT_MS, "a session screen before stopping");

      if (state !== "session-lesson") {
         return state;
      }

      const captured = await leaveLesson(tab, readingCount);

      readingCount += captured ? 1 : 0;
   }
}

async function stopSet(tab) {
   await tab.clickSelector("button.session-stop");
   await tab.waitFor("document.querySelector(\"[data-testid='stop-confirmation']\") !== null", SHORT_WAIT_MS, "the stop confirmation");
   await tab.capture("stop-confirm");
   await tab.clickButtonText("Stop and close this set");
}

async function startSet(tab) {
   for (const label of ["Start today's set", "Resume today's set", "Add a 15 minute practice set"]) {
      const offered = await tab.buttonWithText(label);

      if (offered) {
         await tab.clickButtonText(label);
         await tab.waitFor("document.querySelector(\"[data-testid='home']\") === null", LONG_WAIT_MS, "home to give way to the set");

         return label;
      }
   }

   return null;
}

async function walkRun(cdp, viewport, scheme) {
   const prefix = `${options.student}-${viewport.width}-${scheme}`;
   const run = { student: options.student, width: viewport.width, scheme, prefix, screens: [], items: [], consoleErrors: [], failedRequests: [], overflow: false, notes: [], lessonsShown: new Map(), homeWaitsMs: [] };

   console.log(`run ${prefix}`);

   const { browserContextId } = await cdp.send("Target.createBrowserContext", { disposeOnDetach: true });
   const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank", browserContextId });
   const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
   const tab = new Tab(cdp, sessionId, run);

   run.phase = "sign-in";
   const requestUrls = new Map();
   const inFlight = new Set();

   cdp.onEvent((message) => {
      const isThisTab = message.sessionId === sessionId;

      if (!isThisTab) {
         return;
      }

      const params = message.params;

      switch (message.method) {
         case "Runtime.consoleAPICalled":
            if (params.type === "error") {
               const text = params.args.map((arg) => arg.value ?? arg.description ?? "").join(" ");

               run.consoleErrors.push({ source: "console", text: text.slice(0, 500), phase: run.phase });
            }
            break;
         case "Runtime.exceptionThrown":
            run.consoleErrors.push({ source: "exception", text: (params.exceptionDetails.exception?.description ?? params.exceptionDetails.text).slice(0, 500), phase: run.phase });
            break;
         case "Log.entryAdded":
            if (params.entry.level === "error") {
               run.consoleErrors.push({ source: `log:${params.entry.source}`, text: params.entry.text.slice(0, 500), url: params.entry.url, phase: run.phase });
            }
            break;
         case "Network.requestWillBeSent":
            requestUrls.set(params.requestId, { url: params.request.url, method: params.request.method, startedAt: Date.now() });
            inFlight.add(params.requestId);
            break;
         case "Network.loadingFinished":
            inFlight.delete(params.requestId);
            break;
         case "Network.responseReceived":
            if (params.response.status >= 400) {
               const request = requestUrls.get(params.requestId);

               run.failedRequests.push({ method: request?.method, url: params.response.url, status: params.response.status, phase: run.phase });
            }
            break;
         case "Network.loadingFailed": {
            inFlight.delete(params.requestId);
            const request = requestUrls.get(params.requestId);

            run.failedRequests.push({ method: request?.method, url: request?.url, error: params.errorText, canceled: params.canceled ?? false, phase: run.phase });
            break;
         }
      }
   });

   await tab.send("Page.enable");
   await tab.send("Runtime.enable");
   await tab.send("Log.enable");
   await tab.send("Network.enable");
   await tab.send("Emulation.setDeviceMetricsOverride", { width: viewport.width, height: viewport.height, deviceScaleFactor: viewport.scale, mobile: viewport.mobile });
   await tab.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: scheme }] });

   try {
      await signIn(tab, options.web);

      const reachedHome = await waitForHome(tab);

      run.phase = "home";
      await tab.capture(reachedHome ? "home" : "not-home");

      if (!reachedHome) {
         run.notes.push("home was not reached, so the set was not walked");
      } else {
         run.phase = "set";
         const started = await startSet(tab);

         run.started = started;

         if (started === null) {
            run.notes.push("home offered no way into a set");
         } else {
            const stateBeforeStop = await walkSession(tab);

            if (stateBeforeStop === "session-stage") {
               await stopSet(tab);
            }

            const ended = await tab.waitFor("document.querySelector(\"[data-testid='session-end']\") !== null", LONG_WAIT_MS, "session end").catch(() => false);

            if (ended) {
               await tab.capture("end");
               await tab.clickButtonText("Back to Today");

               const backHome = await waitForHome(tab);

               await tab.capture(backHome ? "home-after" : "after-end");
            } else {
               await tab.capture("no-session-end");
            }
         }
      }

      run.phase = "review";
      await tab.send("Page.navigate", { url: `${new URL(options.web).origin}/#/review` });
      await sleep(500);
      await tab.waitFor("document.querySelector(\"[data-testid='review-screen']\") !== null || document.querySelector(\"[data-testid='review-waiting']\") === null && location.hash === '#/review' && document.readyState === 'complete'", LONG_WAIT_MS, "review").catch((error) => run.notes.push(error.message));
      await tab.capture("review");
   } catch (error) {
      const unanswered = [...inFlight].map((requestId) => requestUrls.get(requestId)).filter((request) => !request.url.startsWith("data:"));

      run.notes.push(`walk stopped: ${error.message}`);
      run.unansweredRequests = unanswered.map((request) => ({ method: request.method, url: request.url, waitedMs: Date.now() - request.startedAt }));
      console.log(`   stopped: ${error.message}`);
      await tab.capture("stopped-at").catch(() => undefined);
   }

   delete run.phase;

   run.lessonsShown = [...run.lessonsShown].map(([text, times]) => ({ opening: (text ?? "").slice(0, 120), times }));
   await cdp.send("Target.closeTarget", { targetId }).catch(() => undefined);
   await cdp.send("Target.disposeBrowserContext", { browserContextId }).catch(() => undefined);

   return run;
}

function saveReport(product, runs) {
   const reportPath = join(SHOTS, "report.json");
   const earlier = existsSync(reportPath) ? JSON.parse(readFileSync(reportPath, "utf8")) : { runs: [] };
   const kept = earlier.runs.filter((entry) => !runs.some((run) => run.prefix === entry.prefix));
   const report = { browser: product, updated: new Date().toISOString(), runs: [...kept, ...runs] };

   writeFileSync(reportPath, JSON.stringify(report, null, 3) + "\n");
}

async function main() {
   mkdirSync(SHOTS, { recursive: true });

   const { browser, wsUrl, product } = await launchBrave();
   const cdp = new Cdp(wsUrl);

   await cdp.open();
   console.log(`connected to ${product}`);

   const widths = options.viewports.split(",").map(Number);
   const schemes = options.schemes.split(",");
   const runs = [];

   try {
      for (const viewport of VIEWPORTS.filter((entry) => widths.includes(entry.width))) {
         for (const scheme of SCHEMES.filter((entry) => schemes.includes(entry))) {
            const run = await walkRun(cdp, viewport, scheme);

            runs.push(run);
            saveReport(product, runs);
            console.log(`${run.prefix}: ${run.screens.length} screens, ${run.consoleErrors.length} console errors, ${run.failedRequests.length} failed requests, overflow ${run.overflow}`);
         }
      }
   } finally {
      cdp.close();
      browser.kill();
   }
}

main().catch((error) => {
   console.error(error.message);
   process.exit(1);
});
