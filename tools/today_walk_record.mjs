import { spawn, spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { createServer } from "node:net";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const BRAVE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser";
const FFMPEG = "/opt/homebrew/bin/ffmpeg";
const SCRATCH = "/private/tmp/claude-502/-Users-mahfujm-dev-growth/db01190c-9ae9-4388-976f-508d87d8e8ee/scratchpad";
const REPO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const OUTPUT_DIR = join(REPO, "var", "today-redesign");
const VIDEO_PATH = join(OUTPUT_DIR, "today-redesign-walk.mp4");

const CANVAS = { width: 1280, height: 900 };
const DESKTOP = { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false };
const PHONE = { width: 390, height: 844, deviceScaleFactor: 2, mobile: true };

const LONG_WAIT_MS = 90000;
const HOME_WAIT_MS = 180000;
const SHORT_WAIT_MS = 15000;
const DRAIN_BUDGET_MS = 480000;
const DRAIN_ITEM_CAP = 40;
const PHONE_SEARCH_BUDGET_MS = 300000;
const PHONE_SEARCH_ITEM_CAP = 10;
const LAST_FRAME_SECONDS = 0.1;

const FRESH = {
   web: "http://localhost:5176",
   username: process.env.WALK_FRESH_USER ?? "walk_fresh",
   password: process.env.WALK_FRESH_PASSWORD
};

const HISTORY = {
   web: "http://localhost:5175",
   username: process.env.WALK_HISTORY_USER ?? "walk_history",
   password: process.env.WALK_HISTORY_PASSWORD
};

const report = { parts: {}, notes: [], consoleErrors: [], failedRequests: [] };

function sleep(ms) {
   return new Promise((done) => setTimeout(done, ms));
}

function log(line) {
   console.log(`[${new Date().toISOString().slice(11, 19)}] ${line}`);
}

function note(line) {
   report.notes.push(line);
   log(`note: ${line}`);
}

function withDeadline(promise, ms, label) {
   let timer;
   const expiry = new Promise((_, fail) => {
      timer = setTimeout(() => fail(new Error(`${label} took longer than ${ms} ms`)), ms);
   });

   return Promise.race([promise, expiry]).finally(() => clearTimeout(timer));
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
      await withDeadline(new Promise((done, fail) => {
         this.socket.addEventListener("open", done, { once: true });
         this.socket.addEventListener("error", fail, { once: true });
      }), 20000, "opening the DevTools socket");

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

         if (!waiter) {
            return;
         }

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
      const reply = new Promise((done, fail) => {
         if (this.isClosed) {
            fail(new Error(`${method}: the DevTools socket closed`));

            return;
         }

         this.pending.set(id, { done, fail, method });
         this.socket.send(JSON.stringify({ id, method, params, sessionId }));
      });

      return withDeadline(reply, LONG_WAIT_MS, method).finally(() => this.pending.delete(id));
   }

   onEvent(listener) {
      this.listeners.push(listener);
   }

   close() {
      this.socket.close();
   }
}

class Recorder {
   constructor(framesDir) {
      this.framesDir = framesDir;
      this.frames = [];
      this.segments = [];
      this.tab = null;
      this.frameCount = 0;
   }

   attach(tab) {
      tab.cdp.onEvent((message) => {
         const isFrame = message.method === "Page.screencastFrame" && message.sessionId === tab.sessionId;

         if (!isFrame) {
            return;
         }

         const isRecordingThisTab = this.tab === tab;

         tab.send("Page.screencastFrameAck", { sessionId: message.params.sessionId }).catch(() => undefined);

         if (!isRecordingThisTab) {
            return;
         }

         this.frameCount += 1;

         const fileName = `frame-${String(this.frameCount).padStart(6, "0")}.jpg`;

         writeFileSync(join(this.framesDir, fileName), Buffer.from(message.params.data, "base64"));
         this.frames.push({ file: fileName, at: Date.now() });
      });
   }

   async start(tab) {
      const alreadyRecording = this.tab !== null;

      if (alreadyRecording) {
         await this.stop();
      }

      this.tab = tab;
      this.frames = [];
      await tab.send("Page.bringToFront");
      await tab.send("Page.startScreencast", { format: "jpeg", quality: 80, maxWidth: CANVAS.width, maxHeight: CANVAS.height, everyNthFrame: 1 });
      await tab.forceRepaint();
   }

   async stop() {
      const tab = this.tab;

      if (tab === null) {
         return;
      }

      await sleep(150);
      await tab.send("Page.stopScreencast").catch(() => undefined);
      this.tab = null;

      const stoppedAt = Date.now();

      if (this.frames.length > 0) {
         this.segments.push({ frames: this.frames, stoppedAt });
      }

      this.frames = [];
   }

   concatList() {
      const lines = [];
      let lastFile = null;
      let totalSeconds = 0;

      for (const segment of this.segments) {
         segment.frames.forEach((frame, index) => {
            const following = segment.frames[index + 1];
            const endsAt = following ? following.at : segment.stoppedAt;
            const seconds = Math.max((endsAt - frame.at) / 1000, 1 / 60);
            const isSegmentEnd = following === undefined;
            const shown = isSegmentEnd ? Math.max(seconds, LAST_FRAME_SECONDS) : seconds;

            lines.push(`file '${join(this.framesDir, frame.file)}'`);
            lines.push(`duration ${shown.toFixed(4)}`);
            lastFile = frame.file;
            totalSeconds += shown;
         });
      }

      if (lastFile !== null) {
         lines.push(`file '${join(this.framesDir, lastFile)}'`);
      }

      return { text: lines.join("\n") + "\n", totalSeconds };
   }
}

class Tab {
   constructor(cdp, sessionId, label, targetId) {
      this.cdp = cdp;
      this.targetId = targetId;
      this.sessionId = sessionId;
      this.label = label;
      this.postCount = 0;
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

   async caption(text) {
      await this.evaluate(`(() => {
         let bar = document.getElementById("walk-caption");

         if (bar === null) {
            bar = document.createElement("div");
            bar.id = "walk-caption";
            Object.assign(bar.style, {
               position: "fixed",
               top: "0",
               left: "0",
               right: "0",
               zIndex: "2147483647",
               background: "rgba(16, 16, 20, 0.9)",
               color: "#ffffff",
               font: "600 16px/1.4 -apple-system, system-ui, sans-serif",
               padding: "10px 16px",
               pointerEvents: "none",
               boxShadow: "0 2px 8px rgba(0, 0, 0, 0.3)"
            });
            document.documentElement.appendChild(bar);
         }

         bar.textContent = ${JSON.stringify(text)};
      })()`);
   }

   async forceRepaint() {
      await this.evaluate(`new Promise((done) => {
         const bar = document.getElementById("walk-caption") ?? document.body;

         bar.style.opacity = "0.98";
         requestAnimationFrame(() => requestAnimationFrame(() => {
            bar.style.opacity = "1";
            done();
         }));
      })`).catch(() => undefined);
   }

   async pageBackground() {
      return this.evaluate("getComputedStyle(document.body).backgroundColor + ' ' + getComputedStyle(document.documentElement).backgroundColor");
   }

   async scrollPageSlowly(durationMs) {
      await this.evaluate(`new Promise((done) => {
         const scroller = document.scrollingElement;
         const distance = scroller.scrollHeight - scroller.clientHeight;
         const startedAt = performance.now();
         const halfMs = ${durationMs} / 2;

         if (distance <= 0) {
            setTimeout(done, ${durationMs});

            return;
         }

         const step = (now) => {
            const elapsed = now - startedAt;
            const goingDown = elapsed < halfMs;
            const progress = goingDown ? elapsed / halfMs : Math.max(0, 2 - elapsed / halfMs);

            scroller.scrollTop = distance * progress;

            if (elapsed >= halfMs * 2) {
               scroller.scrollTop = 0;
               done();

               return;
            }

            requestAnimationFrame(step);
         };

         requestAnimationFrame(step);
      })`);
   }

   async pageOverflow() {
      return this.evaluate(`({
         scrollWidth: document.documentElement.scrollWidth,
         clientWidth: document.documentElement.clientWidth
      })`);
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

async function openTab(cdp, recorder, label, viewport, scheme) {
   const { browserContextId } = await cdp.send("Target.createBrowserContext", { disposeOnDetach: true });
   const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank", browserContextId });
   const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
   const tab = new Tab(cdp, sessionId, label, targetId);

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

               report.consoleErrors.push({ tab: label, source: "console", text: text.slice(0, 300) });
            }
            break;
         case "Runtime.exceptionThrown":
            report.consoleErrors.push({ tab: label, source: "exception", text: (params.exceptionDetails.exception?.description ?? params.exceptionDetails.text).slice(0, 300) });
            break;
         case "Log.entryAdded":
            if (params.entry.level === "error") {
               report.consoleErrors.push({ tab: label, source: `log:${params.entry.source}`, text: params.entry.text.slice(0, 300), url: params.entry.url });
            }
            break;
         case "Network.requestWillBeSent": {
            const isApiPost = params.request.method === "POST";

            if (isApiPost) {
               tab.postCount += 1;
            }
            break;
         }
         case "Network.responseReceived":
            if (params.response.status >= 400) {
               report.failedRequests.push({ tab: label, url: params.response.url, status: params.response.status });
            }
            break;
      }
   });

   recorder.attach(tab);

   await tab.send("Page.enable");
   await tab.send("Runtime.enable");
   await tab.send("Log.enable");
   await tab.send("Network.enable");
   await tab.send("Emulation.setDeviceMetricsOverride", viewport);
   await tab.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: scheme }] });

   return tab;
}

async function signIn(tab, account) {
   await tab.send("Page.navigate", { url: account.web });
   await tab.waitFor("document.querySelector('#account-username') !== null || document.querySelector(\"[data-testid='home']\") !== null", LONG_WAIT_MS, "the sign-in form");

   const needsSignIn = await tab.has("#account-username");

   if (!needsSignIn) {
      return;
   }

   await tab.typeInto("#account-username", account.username);
   await tab.typeInto("#account-password", account.password);
   await tab.clickSelector("form button[type='submit']");
}

async function waitForHome(tab) {
   const settledOnHome = "document.querySelector(\"[data-testid='home']\") !== null || document.querySelector(\"[data-testid='home-failed']\") !== null";
   const startedAt = Date.now();

   await tab.waitFor(settledOnHome, HOME_WAIT_MS, "home");

   const failed = await tab.has("[data-testid='home-failed']");
   const waitedMs = Date.now() - startedAt;

   log(`${tab.label}: home settled after ${waitedMs} ms${failed ? " (home-failed)" : ""}`);

   return { waitedMs, failed };
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

async function leaveLesson(tab) {
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
      return;
   }

   const lessonSignature = `(document.querySelector("[data-testid='session-lesson']")?.textContent ?? "").slice(0, 300)`;
   const shownLesson = await tab.evaluate(lessonSignature);

   await tab.clickWhere(exitFinder, "a way out of the lesson");
   await tab.waitFor(`${lessonSignature} !== ${JSON.stringify(shownLesson)}`, LONG_WAIT_MS, "the lesson to close");
}

async function nextItemScreen(tab) {
   while (true) {
      const state = await tab.waitFor(SCREEN_STATE + " ?? false", LONG_WAIT_MS, "a session screen");

      if (state !== "session-lesson") {
         return state;
      }

      await leaveLesson(tab);
   }
}

async function answerWrong(tab) {
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
      await sleep(600);

      return "typed 7";
   }

   return "no answer control";
}

async function rateConfidenceIfAsked(tab) {
   const confidenceUnrated = await tab.evaluate(
      "document.querySelector(\"[data-testid='confidence-prompt']\") !== null && document.querySelector(\"[data-testid='confidence-prompt'] input:checked\") === null"
   );

   if (confidenceUnrated) {
      await tab.clickWhere("() => document.querySelector(\"[data-testid='confidence-prompt'] input[value='confident']\").closest('label')", "confident");
      await sleep(300);
   }
}

async function commitAndWaitForFeedback(tab) {
   const deadline = Date.now() + LONG_WAIT_MS;
   let lastCommitAt = 0;

   while (Date.now() < deadline) {
      const state = await tab.evaluate(SCREEN_STATE);
      const reachedOutcome = state === "feedback" || state === "session-end" || state === "session-lesson";

      if (reachedOutcome) {
         return state;
      }

      await rateConfidenceIfAsked(tab);

      const commitVisible = await tab.has("button.motion-instant-submit-answer:not([disabled])");
      const commitIsDue = Date.now() - lastCommitAt > 3000;
      const shouldCommit = commitVisible && commitIsDue;

      if (shouldCommit) {
         await tab.clickSelector("button.motion-instant-submit-answer");
         lastCommitAt = Date.now();
      }

      await sleep(300);
   }

   throw new Error("timed out waiting for feedback after Check");
}

async function feedbackVerdict(tab) {
   return tab.evaluate(`(() => {
      const head = document.querySelector("[data-testid='feedback-verdict']");

      if (!head) {
         return "noverdict";
      }

      return head.querySelector(".text-correct") ? "correct" : "incorrect";
   })()`);
}

async function moveOnFromFeedback(tab) {
   const errorNoteSelector = "[data-testid='error-note-field'] textarea, [data-testid='error-note-field'] input";
   const hasErrorNote = await tab.has(errorNoteSelector);

   if (hasErrorNote) {
      await tab.typeInto(errorNoteSelector, "note from the recorded walk");
      await sleep(300);
   }

   await tab.waitFor("document.querySelector('button.motion-instant-question-move:not([disabled])') !== null", SHORT_WAIT_MS, "Next item to enable");
   await tab.clickSelector("button.motion-instant-question-move");
   await tab.waitFor("document.querySelector(\"[data-testid='feedback']\") === null", LONG_WAIT_MS, "feedback to close");
}

async function showEmptyCheck(tab) {
   await tab.caption("Empty field: Check stays disabled");
   await sleep(1000);

   const checkButton = "button.motion-instant-submit-answer";
   const hasCheck = await tab.has(checkButton);

   if (!hasCheck) {
      note("part 2: no Check button on the first item, empty-field step shown without a click");
      await sleep(2000);

      return { clicked: false };
   }

   const leftoverDraft = await tab.evaluate(`(() => {
      const field = document.querySelector("[data-testid='math-answer'] math-field");

      if (field === null || !field.value) {
         return null;
      }

      const draft = field.value;

      field.focus();
      field.executeCommand("deleteAll");

      return draft;
   })()`);

   if (leftoverDraft !== null) {
      note(`part 2: the math field held a saved draft ${JSON.stringify(leftoverDraft)}, cleared before the empty-field click`);
      await sleep(800);
   }

   const disabledBefore = await tab.evaluate(`document.querySelector(${JSON.stringify(checkButton)}).disabled`);

   if (!disabledBefore) {
      note("part 2: Check was enabled with the field empty, so it was not clicked");
      await sleep(2000);

      return { clicked: false, disabledBefore, leftoverDraft };
   }

   const postsBefore = tab.postCount;

   await tab.clickSelector(checkButton);
   await sleep(2000);

   const stateAfter = await tab.evaluate(SCREEN_STATE);
   const postsDuringClick = tab.postCount - postsBefore;
   const result = { clicked: true, disabledBefore, leftoverDraft, stateAfter, postsDuringClick };

   log(`part 2 empty check: ${JSON.stringify(result)}`);

   return result;
}

async function partFreshTodayAndSession(cdp, recorder) {
   const tab = await openTab(cdp, recorder, "fresh-1280", DESKTOP, "light");

   await recorder.start(tab);
   await signIn(tab, FRESH);
   await recorder.stop();

   const home = await waitForHome(tab);

   await tab.caption("Today: overview block, full width, no footer");
   await recorder.start(tab);
   await sleep(3000);
   await tab.scrollPageSlowly(12000);
   await sleep(500);
   report.parts.part1 = { captured: true, homeWaitMs: home.waitedMs, homeFailed: home.failed, overflow: await tab.pageOverflow() };

   const started = await startSet(tab);

   if (started === null) {
      note("part 2 and 3: home offered no way into a set");
      await recorder.stop();

      return tab;
   }

   let state = await nextItemScreen(tab);

   await tab.caption("Empty field: Check stays disabled");

   const emptyCheck = state === "session-stage" ? await showEmptyCheck(tab) : { clicked: false, stateAtStart: state };
   let shownWrong = false;
   let itemsAnswered = 0;

   const keepLookingForWrong = () => {
      const onItem = state === "session-stage";
      const underCap = itemsAnswered < 4;

      return !shownWrong && underCap && onItem;
   };

   while (keepLookingForWrong()) {
      const answered = await answerWrong(tab);
      const outcome = await commitAndWaitForFeedback(tab);

      itemsAnswered += 1;

      if (outcome !== "feedback") {
         state = await nextItemScreen(tab);
         continue;
      }

      const verdict = await feedbackVerdict(tab);
      const hasCorrectBlock = await tab.has("[data-testid='correct-answer']");
      const showsWrongAnswer = verdict === "incorrect" && hasCorrectBlock;

      log(`part 2 item ${itemsAnswered}: ${answered}, verdict ${verdict}, correct-answer block ${hasCorrectBlock}`);

      if (showsWrongAnswer) {
         await tab.caption("Wrong answer: step marks and 'The step should give ...'");
         await tab.evaluate("document.querySelector(\"[data-testid='correct-answer']\").scrollIntoView({ block: 'center', behavior: 'smooth' })");
         await sleep(4000);
         shownWrong = true;
         report.parts.part2 = { captured: true, emptyCheck, wrongAnswerItem: itemsAnswered, answered };
      }

      await moveOnFromFeedback(tab);
      state = await nextItemScreen(tab);
   }

   if (!shownWrong) {
      report.parts.part2 = { captured: false, emptyCheck, reason: `no incorrect feedback with a correct-answer block in ${itemsAnswered} items` };
   }

   await recorder.stop();

   const drainStartedAt = Date.now();
   let drained = 0;

   const keepDraining = () => {
      const onItem = state === "session-stage";
      const underCap = drained < DRAIN_ITEM_CAP;
      const withinBudget = Date.now() - drainStartedAt < DRAIN_BUDGET_MS;

      return onItem && underCap && withinBudget;
   };

   while (keepDraining()) {
      await answerWrong(tab);

      const outcome = await commitAndWaitForFeedback(tab);

      drained += 1;

      if (outcome === "feedback") {
         await moveOnFromFeedback(tab);
      }

      state = await nextItemScreen(tab);
      log(`part 3: answered ${drained} more, now ${state}`);
   }

   const endedOnItsOwn = state === "session-end";

   if (!endedOnItsOwn) {
      note(`part 3: set did not end on its own after ${drained} more items (${Math.round((Date.now() - drainStartedAt) / 1000)} s), state ${state}; stopped it with the Stop control`);

      const canStop = await tab.has("button.session-stop");

      if (canStop) {
         await tab.clickSelector("button.session-stop");
         await tab.waitFor("document.querySelector(\"[data-testid='stop-confirmation']\") !== null", SHORT_WAIT_MS, "the stop confirmation");
         await tab.clickButtonText("Stop and close this set");
      }

      await tab.waitFor("document.querySelector(\"[data-testid='session-end']\") !== null", LONG_WAIT_MS, "session end");
   }

   await tab.caption("Session ends when the blocks are empty, no timer, no quota");
   await recorder.start(tab);
   await sleep(3000);
   await recorder.stop();

   report.parts.part3 = { captured: true, endedOnItsOwn, itemsAfterPart2: drained, drainSeconds: Math.round((Date.now() - drainStartedAt) / 1000) };

   return tab;
}

async function partHistory(cdp, recorder) {
   const tab = await openTab(cdp, recorder, "history-1280", DESKTOP, "light");

   await recorder.start(tab);
   await signIn(tab, HISTORY);
   await sleep(1500);
   await recorder.stop();

   const home = await waitForHome(tab);
   const homeStatus = await tab.evaluate("document.querySelector(\"[data-testid='home']\")?.innerText.slice(0, 400) ?? null");
   const dueSentence = await tab.evaluate("[...document.querySelectorAll(\"[data-testid='home'] *\")].map((node) => node.childElementCount === 0 ? node.textContent : '').find((text) => /more skills? (is|are) due today/.test(text)) ?? null");

   await tab.caption("Seeded student: 'N more skills are due today, about M minutes, beyond this set.' and a mixed card without skill names");
   await recorder.start(tab);
   await sleep(4000);
   await tab.scrollPageSlowly(12000);
   await sleep(500);
   report.parts.part4 = { captured: true, homeWaitMsCut: home.waitedMs, homeFailed: home.failed, dueSentence, homeStatus };

   const lightBackground = await tab.pageBackground();

   await recorder.stop();
   await tab.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "dark" }] });
   await tab.caption("Dark mode");
   await sleep(1000);
   await recorder.start(tab);

   const darkBackground = await tab.pageBackground();
   const themeFollowedLive = darkBackground !== lightBackground;
   let darkWaitMs = 0;

   if (!themeFollowedLive) {
      await recorder.stop();
      note(`part 5: the page did not repaint on the media change (${lightBackground}), so it was reloaded under the dark scheme and the wait was cut`);
      await tab.send("Page.reload");
      await sleep(1000);
      darkWaitMs = (await waitForHome(tab)).waitedMs;
      await tab.caption("Dark mode");
      await recorder.start(tab);
   }

   await sleep(3000);
   await recorder.stop();
   report.parts.part5 = { captured: true, themeFollowedLive, lightBackground, darkBackground: await tab.pageBackground(), reloadWaitMsCut: darkWaitMs };

   await tab.send("Emulation.setDeviceMetricsOverride", PHONE);
   await tab.send("Page.reload");
   await sleep(1000);

   const phoneHome = await waitForHome(tab);

   await tab.caption("Phone width: nothing scrolls sideways; wide worked-step math scrolls inside its own box");
   await recorder.start(tab);
   await sleep(3000);
   await tab.scrollPageSlowly(12000);
   await sleep(500);
   await recorder.stop();

   report.parts.part6 = { captured: true, homeWaitMsCut: phoneHome.waitedMs, overflow: await tab.pageOverflow() };

   return tab;
}

async function closeSetQuietly(tab) {
   try {
      const hasFeedback = await tab.has("[data-testid='feedback']");

      if (hasFeedback) {
         await moveOnFromFeedback(tab);
         await nextItemScreen(tab);
      }

      const canStop = await tab.has("button.session-stop");

      if (!canStop) {
         return;
      }

      await tab.clickSelector("button.session-stop");
      await tab.waitFor("document.querySelector(\"[data-testid='stop-confirmation']\") !== null", SHORT_WAIT_MS, "the stop confirmation");
      await tab.clickButtonText("Stop and close this set");
      await tab.waitFor("document.querySelector(\"[data-testid='session-end']\") !== null", LONG_WAIT_MS, "session end");
   } catch (error) {
      note(`closing the phone set failed: ${error.message}`);
   }
}

async function partPhoneMathBox(cdp, recorder) {
   const tab = await openTab(cdp, recorder, "fresh-390", PHONE, "dark");

   await signIn(tab, FRESH);
   await waitForHome(tab);

   const started = await startSet(tab);

   if (started === null) {
      return { shown: false, reason: "home offered no way into a set" };
   }

   const wideBoxFinder = `() => [...document.querySelectorAll("[data-testid='feedback'] .math-overflow")].find((box) => {
      const overflowX = getComputedStyle(box).overflowX;
      const scrollsSideways = overflowX === "auto" || overflowX === "scroll";
      const isWider = box.scrollWidth > box.clientWidth + 4;

      return scrollsSideways && isWider;
   })`;
   const searchStartedAt = Date.now();
   let searched = 0;
   let state = await nextItemScreen(tab);

   const keepSearching = () => {
      const onItem = state === "session-stage";
      const underCap = searched < PHONE_SEARCH_ITEM_CAP;
      const withinBudget = Date.now() - searchStartedAt < PHONE_SEARCH_BUDGET_MS;

      return onItem && underCap && withinBudget;
   };

   while (keepSearching()) {
      await answerWrong(tab);

      const outcome = await commitAndWaitForFeedback(tab);

      searched += 1;

      if (outcome === "feedback") {
         const hasWideBox = await tab.evaluate(`(${wideBoxFinder})() !== undefined`);

         if (hasWideBox) {
            const overflow = await tab.pageOverflow();

            await tab.caption("Phone width: wide worked-step math scrolls inside its own box");
            await tab.evaluate(`(${wideBoxFinder})().scrollIntoView({ block: "center" })`);
            await sleep(500);

            const boxBefore = await tab.evaluate(`(() => {
               const box = (${wideBoxFinder})();
               const rect = box.getBoundingClientRect();

               return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), scrollWidth: box.scrollWidth, clientWidth: box.clientWidth, viewportHeight: innerHeight };
            })()`);

            log(`phone math box: ${JSON.stringify(boxBefore)}`);
            await recorder.start(tab);
            await sleep(1500);
            await tab.evaluate(`new Promise((done) => {
               const box = (${wideBoxFinder})();
               const distance = box.scrollWidth - box.clientWidth;
               const startedAt = performance.now();
               const durationMs = 4000;

               const step = (now) => {
                  const progress = Math.min(1, (now - startedAt) / durationMs);

                  box.scrollLeft = distance * progress;

                  if (progress >= 1) {
                     done();

                     return;
                  }

                  requestAnimationFrame(step);
               };

               requestAnimationFrame(step);
            })`);
            await sleep(2000);
            await recorder.stop();

            const scrolledLeft = await tab.evaluate(`(${wideBoxFinder})().scrollLeft`);

            await closeSetQuietly(tab);

            return { shown: true, itemsSearched: searched, overflow, boxBefore, scrolledLeft };
         }

         await moveOnFromFeedback(tab);
      }

      state = await nextItemScreen(tab);
   }

   return { shown: false, reason: `no feedback panel with a sideways-scrolling math box in ${searched} items (${Math.round((Date.now() - searchStartedAt) / 1000)} s), last state ${state}` };
}

async function closeTab(cdp, tab) {
   if (tab === null) {
      return;
   }

   await cdp.send("Target.closeTarget", { targetId: tab.targetId }).catch(() => undefined);
}

function assembleVideo(recorder, workDir) {
   const { text, totalSeconds } = recorder.concatList();
   const listPath = join(workDir, "frames.txt");

   writeFileSync(listPath, text);
   log(`assembling ${recorder.segments.length} segments, ${totalSeconds.toFixed(1)} s of frames`);

   const filter = [
      `scale=${CANVAS.width}:${CANVAS.height}:force_original_aspect_ratio=decrease`,
      `pad=${CANVAS.width}:${CANVAS.height}:(ow-iw)/2:(oh-ih)/2:color=0x101014`,
      "fps=30",
      "scale=out_range=tv",
      "format=yuv420p"
   ].join(",");
   const args = ["-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listPath, "-vf", filter, "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-color_range", "tv", "-movflags", "+faststart", VIDEO_PATH];
   const result = spawnSync(FFMPEG, args, { encoding: "utf8", timeout: 400000 });
   const ffmpegFailed = result.status !== 0;

   if (ffmpegFailed) {
      throw new Error(`ffmpeg failed (${result.status ?? result.signal}): ${result.stderr}`);
   }

   log(`wrote ${VIDEO_PATH}`);
}

async function main() {
   const passwordsMissing = !FRESH.password || !HISTORY.password;

   if (passwordsMissing) {
      console.error("set WALK_FRESH_PASSWORD and WALK_HISTORY_PASSWORD");
      process.exit(2);
   }

   mkdirSync(OUTPUT_DIR, { recursive: true });

   const workDir = mkdtempSync(join(SCRATCH, "walk-frames-"));
   const framesDir = join(workDir, "frames");

   mkdirSync(framesDir);

   const { browser, wsUrl, product } = await launchBrave();
   const cdp = new Cdp(wsUrl);
   const recorder = new Recorder(framesDir);

   await cdp.open();
   log(`connected to ${product}, frames in ${framesDir}`);

   try {
      const freshTab = await partFreshTodayAndSession(cdp, recorder).catch(async (error) => {
         await recorder.stop();
         note(`parts 1 to 3 stopped: ${error.message}`);

         return null;
      });

      await closeTab(cdp, freshTab);

      const historyTab = await partHistory(cdp, recorder).catch(async (error) => {
         await recorder.stop();
         note(`parts 4 to 6 stopped: ${error.message}`);

         return null;
      });

      await closeTab(cdp, historyTab);

      const phoneMathBox = await partPhoneMathBox(cdp, recorder).catch(async (error) => {
         await recorder.stop();

         return { shown: false, reason: error.message };
      });

      report.parts.part6MathBox = phoneMathBox;
   } finally {
      await recorder.stop().catch(() => undefined);
      cdp.close();
      browser.kill();
   }

   assembleVideo(recorder, workDir);

   const uniqueErrors = [...new Map(report.consoleErrors.map((entry) => [`${entry.tab} ${entry.text} ${entry.url ?? ""}`, entry])).values()];

   report.consoleErrors = uniqueErrors;
   report.failedRequests = [...new Map(report.failedRequests.map((entry) => [`${entry.tab} ${entry.status} ${entry.url}`, entry])).values()];
   writeFileSync(join(OUTPUT_DIR, "record-report.json"), JSON.stringify(report, null, 3) + "\n");
   log(JSON.stringify(report.parts, null, 3));
   log(`${uniqueErrors.length} distinct console errors, report in var/today-redesign/record-report.json`);
}

main().catch((error) => {
   console.error(error.stack ?? error.message);
   process.exit(1);
});
