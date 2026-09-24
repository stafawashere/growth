import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
import { describe, expect, it, vi, beforeEach } from "vitest";

import {
   ApiError,
   openSession,
   readSession,
   readNextItem,
   openDiagnostic,
   readDiagnostic,
   submitAttempt,
   readFeedback,
   submitConfidence,
   submitErrorNote,
   submitSelfExplanation,
   closeSession,
   readMe,
   requestPurge,
   readProgress,
   readCalibration,
   readMasteryMap,
   readReview,
   readSettings,
   updateSettings,
   readProviders,
   readBudgets,
   updateBudget,
   requestExport,
   readExport,
   beginReauth,
   finishReauth,
   reauthenticate,
   readMetrics,
   readRepresentations,
   readExperiments,
   setExperimentState,
   readCheckpoints,
   startCheckpoint,
   readCheckpoint,
   scoreCheckpointPart,
   finishCheckpoint,
   readProbe,
   startProbe,
   readNextProbeItem,
   answerProbeItem,
   readFrqUnits,
   openUnitCheck,
   readUnitCheck,
   startFrqAttempt,
   uploadPhoto,
   requestReadBack,
   readReadBack,
   confirmReadBack,
   submitTypedAnswer,
   readGradings,
   askForReread
} from "./client";

const here = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.join(here, "..", "..", "..");
const routesDir = path.join(appDir, "api", "routes");

function pythonSource(relativePath: string) {
   return fs.readFileSync(path.join(appDir, relativePath), "utf8");
}

function depthByIndex(text: string) {
   const depths = new Array<number>(text.length).fill(0);
   let depth = 0;
   let index = 0;

   while (index < text.length) {
      const character = text[index];
      const isQuote = character === "\"";

      if (isQuote) {
         const closingQuote = text.indexOf("\"", index + 1);
         const stop = closingQuote === -1 ? text.length - 1 : closingQuote;

         for (let position = index; position <= stop; position += 1) {
            depths[position] = depth;
         }

         index = stop + 1;
         continue;
      }

      const opens = "{[(".includes(character);
      const closes = "}])".includes(character);

      if (opens) {
         depth += 1;
      }

      depths[index] = depth;

      if (closes) {
         depth -= 1;
      }

      index += 1;
   }

   return depths;
}

function balancedSlice(text: string, openIndex: number) {
   const depths = depthByIndex(`${text.slice(openIndex)}\n`);
   let index = 1;

   while (index < depths.length) {
      const hasClosed = depths[index] === 0;

      if (hasClosed) {
         return text.slice(openIndex, openIndex + index + 1);
      }

      index += 1;
   }

   throw new Error(`the literal at offset ${openIndex} never closes`);
}

function topLevelQuotedKeys(slice: string) {
   const depths = depthByIndex(slice);
   const pattern = /"([^"]+)"\s*:/g;
   const keys: string[] = [];
   let match = pattern.exec(slice);

   while (match !== null) {
      const isTopLevel = depths[match.index] === 1;

      if (isTopLevel) {
         keys.push(match[1]);
      }

      match = pattern.exec(slice);
   }

   return keys;
}

function topLevelKeywordNames(slice: string) {
   const depths = depthByIndex(slice);
   const pattern = /([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)/g;
   const names: string[] = [];
   let match = pattern.exec(slice);

   while (match !== null) {
      const isTopLevel = depths[match.index] === 1;

      if (isTopLevel) {
         names.push(match[1]);
      }

      match = pattern.exec(slice);
   }

   return names;
}

function returnedFields(relativePath: string, functionName: string) {
   const source = pythonSource(relativePath);
   const defIndex = source.indexOf(`def ${functionName}(`);
   const hasFunction = defIndex >= 0;

   if (!hasFunction) {
      throw new Error(`${relativePath} declares no ${functionName}`);
   }

   const returnIndex = source.indexOf("return {", defIndex);
   const nextTopLevelDef = source.indexOf("\ndef ", defIndex + 1);
   const hasDictReturn = returnIndex >= 0;
   const escapesTheFunction = nextTopLevelDef >= 0 && returnIndex > nextTopLevelDef;

   if (!hasDictReturn || escapesTheFunction) {
      throw new Error(`${functionName} in ${relativePath} returns no dict literal`);
   }

   return topLevelQuotedKeys(balancedSlice(source, source.indexOf("{", returnIndex)));
}

function nestedDictFields(relativePath: string, anchor: string) {
   const source = pythonSource(relativePath);
   const anchorIndex = source.indexOf(anchor);
   const hasAnchor = anchorIndex >= 0;

   if (!hasAnchor) {
      throw new Error(`${relativePath} carries no ${anchor}`);
   }

   return topLevelQuotedKeys(balancedSlice(source, source.indexOf("{", anchorIndex)));
}

function callKeywordFields(relativePath: string, anchor: string) {
   const source = pythonSource(relativePath);
   const anchorIndex = source.indexOf(anchor);
   const hasAnchor = anchorIndex >= 0;

   if (!hasAnchor) {
      throw new Error(`${relativePath} carries no ${anchor}`);
   }

   return topLevelKeywordNames(balancedSlice(source, source.indexOf("(", anchorIndex)));
}

function tupleConstantFields(relativePath: string, constantName: string) {
   const source = pythonSource(relativePath);
   const anchorIndex = source.indexOf(`${constantName} = (`);
   const hasConstant = anchorIndex >= 0;

   if (!hasConstant) {
      throw new Error(`${relativePath} declares no ${constantName}`);
   }

   const slice = balancedSlice(source, source.indexOf("(", anchorIndex));

   return [...slice.matchAll(/"([^"]+)"/g)].map((match) => match[1]);
}

function dressedItemFields() {
   const source = pythonSource("engine/select.py");

   return [...source.matchAll(/served\["([A-Za-z_]+)"\]\s*=/g)].map((match) => match[1]);
}

function declaredTypeFields(moduleFile: string, typeName: string): string[] {
   const source = fs.readFileSync(path.join(here, moduleFile), "utf8");
   const header = new RegExp(`export interface ${typeName}(?: extends ([A-Za-z_]+))? \\{`).exec(source);
   const hasType = header !== null;

   if (!hasType) {
      throw new Error(`${moduleFile} declares no ${typeName}`);
   }

   const parentName = header[1];
   const inherited = parentName === undefined ? [] : declaredTypeFields(moduleFile, parentName);
   const slice = balancedSlice(source, header.index + header[0].length - 1);
   const depths = depthByIndex(slice);
   const pattern = /\n\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:/g;
   const fields: string[] = [...inherited];
   let match = pattern.exec(slice);

   while (match !== null) {
      const nameOffset = match.index + match[0].indexOf(match[1]);
      const isTopLevel = depths[nameOffset] === 1;

      if (isTopLevel) {
         fields.push(match[1]);
      }

      match = pattern.exec(slice);
   }

   return fields;
}

function functionSource(relativePath: string, functionName: string) {
   const source = pythonSource(relativePath);
   const defIndex = source.indexOf(`def ${functionName}(`);
   const hasFunction = defIndex >= 0;

   if (!hasFunction) {
      throw new Error(`${relativePath} declares no ${functionName}`);
   }

   const rest = source.slice(defIndex + 1);
   const nextTopLevel = rest.search(/\n(?:@|def |class |[A-Z_]+ = )/);
   const end = nextTopLevel === -1 ? source.length : defIndex + 1 + nextTopLevel;

   return source.slice(defIndex, end);
}

function routeFunctionName(relativePath: string, method: string, routePath: string) {
   const source = pythonSource(relativePath);
   const prefixMatch = source.match(/APIRouter\(\s*prefix="([^"]*)"/);
   const prefix = prefixMatch ? prefixMatch[1] : "";
   const pattern = /@router\.(get|post|put|delete)\(\s*"([^"]*)"[^)]*\)\s*\ndef ([A-Za-z_][A-Za-z0-9_]*)\(/g;

   for (const match of source.matchAll(pattern)) {
      const declaredPath = (prefix + match[2]).replace(/\{[^}]+\}/g, "{}");
      const isRoute = match[1].toUpperCase() === method && declaredPath === routePath;

      if (isRoute) {
         return match[3];
      }
   }

   throw new Error(`${relativePath} declares no ${method} ${routePath}`);
}

function returnedDictCallKeywords(relativePath: string, functionName: string) {
   const body = functionSource(relativePath, functionName);
   const returnedCalls = [...body.matchAll(/return [^\n]*?dict\(/g)];
   const hasCall = returnedCalls.length > 0;

   if (!hasCall) {
      throw new Error(`${functionName} in ${relativePath} returns no dict(...) call`);
   }

   const lastCall = returnedCalls[returnedCalls.length - 1];
   const openIndex = (lastCall.index ?? 0) + lastCall[0].length - 1;

   return topLevelKeywordNames(balancedSlice(body, openIndex));
}

function returnedListItemFields(relativePath: string, functionName: string) {
   const body = functionSource(relativePath, functionName);
   const listIndex = body.indexOf("return [");
   const hasList = listIndex >= 0;

   if (!hasList) {
      throw new Error(`${functionName} in ${relativePath} returns no list`);
   }

   return topLevelQuotedKeys(balancedSlice(body, body.indexOf("{", listIndex)));
}

function returnsCallOf(relativePath: string, functionName: string, callee: string) {
   const body = functionSource(relativePath, functionName);

   return new RegExp(`return ${callee.replace(".", "\\.")}\\(`).test(body);
}

/* The body fields a route reads, whether through fields.get("x") or fields["x"]. */
function readRequestFields(relativePath: string, functionName: string) {
   const body = functionSource(relativePath, functionName);
   const reads = [...body.matchAll(/fields(?:\.get\(|\[)"([A-Za-z_]+)"/g)].map((match) => match[1]);

   return [...new Set(reads)];
}

/* change_budget hands its whole body to budgets.requested_units, which reads one field per name in
   CAP_UNITS, so those names count as read only when the route really makes that call. */
function unitsReadThrough(routeFile: string, route: string, callee: string, constantName: string) {
   const handsOverBody = functionSource(routeFile, route).includes(`${callee}(role, fields)`);
   const readsEachUnit = /fields\[unit\]/.test(functionSource("settings/budgets.py", "requested_units"));

   if (!handsOverBody || !readsEachUnit) {
      return [];
   }

   return tupleConstantFields("settings/budgets.py", constantName);
}

/* budgets.role_view spreads two dicts between its quoted keys, so each spread is resolved to the
   source it names, and a spread this table does not know fails rather than being skipped. */
function roleBudgetFields() {
   const source = functionSource("settings/budgets.py", "role_view");
   const literal = balancedSlice(source, source.indexOf("{", source.indexOf("return {")));
   const spreads = [...literal.matchAll(/\*\*([A-Za-z_]+)/g)].map((match) => match[1]);
   const spreadSources: Record<string, () => string[]> = {
      caps: () => returnedFields("settings/budgets.py", "caps_as_dict"),
      usage: () => tupleConstantFields("settings/budgets.py", "USAGE_FIELDS")
   };
   const unknownSpreads = spreads.filter((name) => !(name in spreadSources));

   if (unknownSpreads.length > 0) {
      throw new Error(`role_view spreads ${unknownSpreads.join(", ")}, which this scan cannot resolve`);
   }

   return [...topLevelQuotedKeys(literal), ...spreads.flatMap((name) => spreadSources[name]())];
}

function queueSlotFields() {
   return [...returnedFields("runtime/bank.py", "_as_item_dict"), ...dressedItemFields()];
}

function servedItemFields() {
   return [
      ...queueSlotFields(),
      ...returnedDictCallKeywords("session/service.py", "served_item"),
      ...returnedDictCallKeywords("api/routes/sessions.py", "read_next_item")
   ];
}

/* A diagnostic item is a queue slot that app/session/diagnostic_session.py advance dresses further,
   with the two fields app/api/routes/sessions.py next_diagnostic_item sets to null. */
function diagnosticItemFields() {
   const advanced = [...functionSource("session/diagnostic_session.py", "advance").matchAll(/served\["([A-Za-z_]+)"\]\s*=/g)];

   return [
      ...new Set([
         ...queueSlotFields(),
         ...advanced.map((match) => match[1]),
         ...returnedDictCallKeywords("api/routes/sessions.py", "next_diagnostic_item")
      ])
   ];
}

function sorted(names: string[]) {
   return [...names].sort();
}

function bodyOf(fields: string[]) {
   return Object.fromEntries(fields.map((field) => [field, `served ${field}`]));
}

const serverShapes = {
   SessionPayload: () => returnedFields("api/routes/sessions.py", "session_payload"),
   NextItemResponse: () => returnedFields("api/routes/sessions.py", "read_next_item"),
   DiagnosticNextItemResponse: () => returnedFields("api/routes/sessions.py", "next_diagnostic_item"),
   DiagnosticServedItem: () => diagnosticItemFields(),
   DiagnosticResult: () => returnedFields("session/diagnostic_session.py", "result_payload"),
   DiagnosticUnit: () => nestedDictFields("session/diagnostic_session.py", "\"units\": ["),
   AttemptResult: () => returnedFields("api/routes/sessions.py", "submit_attempt"),
   ConfidenceResult: () => returnedFields("api/routes/sessions.py", "submit_confidence"),
   ErrorNoteResult: () => returnedFields("api/routes/sessions.py", "submit_error_note"),
   CloseResult: () => returnedFields("api/routes/sessions.py", "close_session"),
   MePayload: () => returnedFields("api/routes/me.py", "read_me"),
   PurgeResult: () => returnedFields("api/routes/purge.py", "purge"),
   StepMark: () => nestedDictFields("feedback/render.py", "\"step_marks\": ["),
   ServedOption: () => tupleConstantFields("runtime/bank.py", "STUDENT_OPTION_FIELDS"),
   ElaboratedPayload: () => [
      ...returnedFields("feedback/render.py", "as_prompt_fields"),
      ...callKeywordFields("feedback/render.py", "dict(payload.as_prompt_fields()")
   ],
   FeedbackPayload: () => [
      ...returnedFields("feedback/render.py", "as_dict"),
      ...callKeywordFields("api/routes/sessions.py", "dict(render.as_dict(feedback)")
   ],
   SessionQueue: () => returnedFields("session/service.py", "queue_payload"),
   QueueSlot: () => queueSlotFields(),
   ServedItem: () => servedItemFields(),
   ServedStep: () => returnedListItemFields("runtime/bank.py", "served_steps"),
   SelfExplanationResult: () =>
      returnedFields(
         "api/routes/sessions.py",
         routeFunctionName("api/routes/sessions.py", "POST", "/sessions/{}/attempts/{}/self-explanation")
      ),
   ProgressPayload: () => returnedFields("session/preview.py", "queue_preview"),
   CalibrationPayload: () => returnedFields("progress/calibration.py", "calibration_view"),
   CalibrationBin: () => returnedFields("progress/calibration.py", "bin_view"),
   MasteryMapPayload: () => returnedFields("progress/mastery.py", "mastery_map"),
   MasteryUnit: () => returnedFields("progress/mastery.py", "unit_payload"),
   MasteryNode: () => returnedFields("progress/mastery.py", "node_payload"),
   ReviewPayload: () => returnedFields("review/screen.py", "review_screen"),
   ComingBackEntry: () => returnedFields("review/screen.py", "coming_back_entry"),
   ErrorNoteEntry: () => returnedListItemFields("review/screen.py", "error_notes"),
   ProvisionalPoint: () => tupleConstantFields("review/screen.py", "PROVISIONAL_POINT_KEYS"),
   SettingsPayload: () => returnedFields("settings/preferences.py", "settings_view"),
   ProvidersPayload: () => returnedFields("settings/providers.py", "providers_view"),
   ProviderRole: () => returnedFields("settings/providers.py", "role_entry"),
   BudgetsPayload: () => returnedFields("settings/budgets.py", "budgets_view"),
   RoleBudget: () => roleBudgetFields(),
   ExportJob: () => returnedFields("api/routes/export.py", "create_export"),
   ReauthBegin: () => returnedFields("auth/service.py", "reauth_begin"),
   ReauthFinish: () => returnedFields("auth/service.py", "reauth_finish"),
   FrqUnitsPayload: () => returnedFields("api/routes/frq.py", "list_units"),
   FrqUnit: () => nestedDictFields("api/routes/frq.py", "\"units\": ["),
   UnitCheckPayload: () => returnedFields("api/routes/frq.py", "open_unit_check"),
   FrqPart: () => nestedDictFields("frq/items.py", "\"parts\": ["),
   FrqAttempt: () => returnedFields("api/routes/frq.py", "attempt_payload"),
   CaptureImage: () => returnedFields("api/routes/frq.py", "image_payload"),
   PhotoVerdict: () => returnedFields("api/routes/frq.py", "upload_image"),
   GradingsPayload: () => returnedFields("api/routes/frq.py", "gradings_payload"),
   GradedPoint: () => nestedDictFields("api/routes/frq.py", "entries.append("),
   DisputeResult: () => returnedFields("api/routes/frq.py", "dispute")
};

const requestShapes = {
   SubmitSelfExplanationFields: () =>
      readRequestFields(
         "api/routes/sessions.py",
         routeFunctionName("api/routes/sessions.py", "POST", "/sessions/{}/attempts/{}/self-explanation")
      ),
   UpdateSettingsFields: () => tupleConstantFields("settings/preferences.py", "EDITABLE_DATES"),
   UpdateBudgetFields: () => [
      ...readRequestFields("api/routes/settings.py", "change_budget"),
      ...unitsReadThrough("api/routes/settings.py", "change_budget", "budgets.requested_units", "CAP_UNITS")
   ],
   RequestExportFields: () => readRequestFields("api/routes/export.py", "create_export"),
   FinishReauthFields: () => readRequestFields("api/routes/auth.py", "reauth_finish"),
   RequestPurgeFields: () => readRequestFields("api/routes/purge.py", "purge")
};

function declaredRoutes(fileName: string) {
   const source = fs.readFileSync(path.join(routesDir, fileName), "utf8");
   const prefixMatch = source.match(/APIRouter\(\s*prefix="([^"]*)"/);
   const prefix = prefixMatch ? prefixMatch[1] : "";
   const decoratorPattern = /@router\.(get|post|put|delete)\(\s*"([^"]*)"/g;
   const routes: { method: string; path: string }[] = [];
   let match = decoratorPattern.exec(source);

   while (match !== null) {
      const method = match[1].toUpperCase();
      const fullPath = (prefix + match[2]).replace(/\{[^}]+\}/g, "{}");

      routes.push({ method, path: fullPath });
      match = decoratorPattern.exec(source);
   }

   return routes;
}

function allDeclaredRoutes() {
   return [
      ...declaredRoutes("sessions.py"),
      ...declaredRoutes("me.py"),
      ...declaredRoutes("purge.py"),
      ...declaredRoutes("progress.py"),
      ...declaredRoutes("review_screen.py"),
      ...declaredRoutes("settings.py"),
      ...declaredRoutes("export.py"),
      ...declaredRoutes("auth.py"),
      ...declaredRoutes("frq.py")
   ];
}

function normalizedIssuedPath(url: string, dynamicValues: string[]) {
   let normalized = url;

   for (const value of dynamicValues) {
      normalized = normalized.split(value).join("{}");
   }

   return normalized;
}

function issuedRequest(fetchMock: ReturnType<typeof vi.fn>) {
   const [url, init] = fetchMock.mock.calls[0];

   return { url: String(url), method: (init && init.method) || "GET", init };
}

function jsonResponse(status: number, body: unknown) {
   return {
      ok: status >= 200 && status < 300,
      status,
      json: () => Promise.resolve(body),
      blob: () => Promise.resolve(new Blob([JSON.stringify(body)], { type: "application/json" }))
   };
}

describe("client path vocabulary", () => {
   const declared = allDeclaredRoutes();

   it("declares at least the routes this client depends on", () => {
      expect(declared.length).toBeGreaterThan(0);
   });

   it("every path openSession issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await openSession({ mode: "learning" });

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, []);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path readSession issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await readSession("sess-1");

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path readNextItem issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, { item: null }));

      vi.stubGlobal("fetch", fetchMock);
      await readNextItem("sess-1");

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path submitAttempt issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await submitAttempt("sess-1", { item_id: "item-1" });

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path readFeedback issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await readFeedback("sess-1", "att-1");

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1", "att-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path submitConfidence issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await submitConfidence("sess-1", "att-1", { confidence: "guess" });

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1", "att-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path submitErrorNote issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await submitErrorNote("sess-1", "att-1", "carried a negative sign wrong");

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1", "att-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path closeSession issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await closeSession("sess-1");

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, ["sess-1"]);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path readMe issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await readMe();

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, []);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("every path requestPurge issues matches a declared FastAPI route", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await requestPurge({ confirmation: "DELETE EVERYTHING" });

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, []);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   const wiringCases = [
      {
         name: "submitSelfExplanation",
         dynamic: ["sess-1", "att-1"],
         invoke: () => submitSelfExplanation("sess-1", "att-1", { answer: "the product rule" })
      },
      { name: "openDiagnostic", dynamic: [], invoke: () => openDiagnostic() },
      { name: "readDiagnostic", dynamic: ["sess-1"], invoke: () => readDiagnostic("sess-1") },
      { name: "readProgress", dynamic: [], invoke: () => readProgress() },
      { name: "readCalibration", dynamic: [], invoke: () => readCalibration() },
      { name: "readMasteryMap", dynamic: [], invoke: () => readMasteryMap() },
      { name: "readReview", dynamic: [], invoke: () => readReview() },
      { name: "readSettings", dynamic: [], invoke: () => readSettings() },
      { name: "updateSettings", dynamic: [], invoke: () => updateSettings({ exam_date: "2027-05-10" }) },
      { name: "readProviders", dynamic: [], invoke: () => readProviders() },
      { name: "readBudgets", dynamic: [], invoke: () => readBudgets() },
      {
         name: "updateBudget",
         dynamic: [],
         invoke: () => updateBudget({ role: "tutor", cap_usd: 1, cap_tokens: null, reauth_token: "t" })
      },
      { name: "requestExport", dynamic: [], invoke: () => requestExport({ reauth_token: "t" }) },
      { name: "readExport", dynamic: ["EXP-1"], invoke: () => readExport("EXP-1") },
      { name: "beginReauth", dynamic: [], invoke: () => beginReauth() },
      { name: "finishReauth", dynamic: [], invoke: () => finishReauth({ challenge_id: "c", credential: {} }) },
      { name: "readFrqUnits", dynamic: [], invoke: () => readFrqUnits() },
      { name: "openUnitCheck", dynamic: [], invoke: () => openUnitCheck("BC-UNIT-05") },
      { name: "readUnitCheck", dynamic: ["SES-1"], invoke: () => readUnitCheck("SES-1") },
      { name: "startFrqAttempt", dynamic: ["SES-1", "FRQ-1"], invoke: () => startFrqAttempt("SES-1", "FRQ-1", "photo") },
      { name: "uploadPhoto", dynamic: ["ATT-1"], invoke: () => uploadPhoto("ATT-1", { media_type: "image/jpeg", data_base64: "AA==" }) },
      { name: "requestReadBack", dynamic: ["ATT-1"], invoke: () => requestReadBack("ATT-1") },
      { name: "readReadBack", dynamic: ["ATT-1"], invoke: () => readReadBack("ATT-1") },
      { name: "confirmReadBack", dynamic: ["ATT-1"], invoke: () => confirmReadBack("ATT-1", { confidence: "unsure" }) },
      { name: "submitTypedAnswer", dynamic: ["ATT-1"], invoke: () => submitTypedAnswer("ATT-1", { read_back: { parts: [], unreadable: [] } }) },
      { name: "readGradings", dynamic: ["ATT-1"], invoke: () => readGradings("ATT-1") },
      { name: "askForReread", dynamic: ["GRD-1"], invoke: () => askForReread("GRD-1") }
   ];

   it.each(wiringCases)("every path $name issues matches a declared FastAPI route", async (wiringCase) => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await wiringCase.invoke();

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, wiringCase.dynamic);

      expect(declared).toContainEqual({ method, path: normalized });
   });
});

describe("request semantics", () => {
   beforeEach(() => {
      vi.unstubAllGlobals();
   });

   it("sends credentials and a json content type on a request with a body", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, { id: "sess-1" }));

      vi.stubGlobal("fetch", fetchMock);
      await openSession({ mode: "learning" });

      const [, init] = fetchMock.mock.calls[0];

      expect(init.credentials).toBe("include");
      expect(init.headers["Content-Type"]).toBe("application/json");
      expect(JSON.parse(init.body)).toEqual({ mode: "learning" });
   });

   it("opens a diagnostic by posting the diagnostic mode to /sessions", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, { id: "sess-1" }));

      vi.stubGlobal("fetch", fetchMock);
      await openDiagnostic();

      const [url, init] = fetchMock.mock.calls[0];

      expect(new URL(String(url), "http://x").pathname).toBe("/sessions");
      expect(init.method).toBe("POST");
      expect(JSON.parse(init.body)).toEqual({ mode: "diagnostic" });
   });

   it("names the diagnostic mode the server opens a diagnostic for", () => {
      const declared = pythonSource("session/diagnostic_session.py").match(/^MODE = "([a-z_]+)"$/m);

      expect(declared).not.toBeNull();
      expect(declared![1]).toBe("diagnostic");
   });

   it("raises a typed ApiError carrying the status and detail on a non-2xx response", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(409, { detail: "this attempt is ungraded" }));

      vi.stubGlobal("fetch", fetchMock);

      await expect(readFeedback("sess-1", "att-1")).rejects.toMatchObject({
         status: 409,
         detail: "this attempt is ungraded"
      });
   });

   it("raises an ApiError instance rather than resolving to null on a non-2xx response", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(404, { detail: "no such session" }));

      vi.stubGlobal("fetch", fetchMock);

      let caught: unknown = null;

      try {
         await readSession("missing");
      } catch (error) {
         caught = error;
      }

      expect(caught).toBeInstanceOf(ApiError);
      expect(caught).not.toBeNull();
   });

   it("parses a 2xx response into the declared shape", async () => {
      const body = {
         id: "attempt-1",
         item_id: "item-1",
         correct: true,
         confidence: "confident",
         served_stage: "unsupported",
         format: "mcq",
         p_split: 0.5,
         p_compensatory: null
      };
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, body));

      vi.stubGlobal("fetch", fetchMock);

      const result = await submitAttempt("sess-1", { item_id: "item-1", answer: { option_id: "a" } });

      expect(sorted(Object.keys(body))).toEqual(sorted(returnedFields("api/routes/sessions.py", "submit_attempt")));
      expect(sorted(Object.keys(result as object))).toEqual(sorted(Object.keys(body)));
      expect(result).toEqual(body);
   });
});

describe("response shape vocabulary", () => {
   const shapeCases = [
      { typeName: "SessionPayload", module: "types.ts" },
      { typeName: "SessionQueue", module: "types.ts" },
      { typeName: "QueueSlot", module: "types.ts" },
      { typeName: "ServedItem", module: "types.ts" },
      { typeName: "ServedStep", module: "types.ts" },
      { typeName: "ProgressPayload", module: "types.ts" },
      { typeName: "CalibrationPayload", module: "types.ts" },
      { typeName: "CalibrationBin", module: "types.ts" },
      { typeName: "MasteryMapPayload", module: "types.ts" },
      { typeName: "MasteryUnit", module: "types.ts" },
      { typeName: "MasteryNode", module: "types.ts" },
      { typeName: "ReviewPayload", module: "types.ts" },
      { typeName: "ComingBackEntry", module: "types.ts" },
      { typeName: "ErrorNoteEntry", module: "types.ts" },
      { typeName: "ProvisionalPoint", module: "types.ts" },
      { typeName: "SettingsPayload", module: "types.ts" },
      { typeName: "ProvidersPayload", module: "types.ts" },
      { typeName: "ProviderRole", module: "types.ts" },
      { typeName: "BudgetsPayload", module: "types.ts" },
      { typeName: "RoleBudget", module: "types.ts" },
      { typeName: "SelfExplanationResult", module: "client.ts" },
      { typeName: "ExportJob", module: "client.ts" },
      { typeName: "ReauthBegin", module: "client.ts" },
      { typeName: "ReauthFinish", module: "client.ts" },
      { typeName: "ServedOption", module: "types.ts" },
      { typeName: "AttemptResult", module: "types.ts" },
      { typeName: "StepMark", module: "types.ts" },
      { typeName: "ElaboratedPayload", module: "types.ts" },
      { typeName: "FeedbackPayload", module: "types.ts" },
      { typeName: "NextItemResponse", module: "client.ts" },
      { typeName: "DiagnosticNextItemResponse", module: "client.ts" },
      { typeName: "DiagnosticServedItem", module: "types.ts" },
      { typeName: "DiagnosticResult", module: "types.ts" },
      { typeName: "DiagnosticUnit", module: "types.ts" },
      { typeName: "ConfidenceResult", module: "client.ts" },
      { typeName: "ErrorNoteResult", module: "client.ts" },
      { typeName: "CloseResult", module: "client.ts" },
      { typeName: "MePayload", module: "client.ts" },
      { typeName: "PurgeResult", module: "client.ts" },
      { typeName: "FrqUnitsPayload", module: "types.ts" },
      { typeName: "FrqUnit", module: "types.ts" },
      { typeName: "UnitCheckPayload", module: "types.ts" },
      { typeName: "FrqPart", module: "types.ts" },
      { typeName: "FrqAttempt", module: "types.ts" },
      { typeName: "CaptureImage", module: "types.ts" },
      { typeName: "PhotoVerdict", module: "types.ts" },
      { typeName: "GradingsPayload", module: "types.ts" },
      { typeName: "GradedPoint", module: "types.ts" },
      { typeName: "DisputeResult", module: "types.ts" }
   ];

   it.each(shapeCases)("$typeName carries the field names its server module returns", (shapeCase) => {
      const declared = declaredTypeFields(shapeCase.module, shapeCase.typeName);
      const returned = serverShapes[shapeCase.typeName as keyof typeof serverShapes]();

      expect(returned.length).toBeGreaterThan(0);
      expect(sorted(declared)).toEqual(sorted(returned));
   });

   it("ProviderRole matches the unwired entry as well as the wired one", () => {
      const declared = declaredTypeFields("types.ts", "ProviderRole");

      expect(sorted(returnedFields("settings/providers.py", "unwired"))).toEqual(sorted(declared));
   });

   const routeHelpers = [
      { file: "api/routes/progress.py", route: "read_progress", callee: "preview.queue_preview" },
      { file: "api/routes/progress.py", route: "read_mastery_map", callee: "mastery.mastery_map" },
      { file: "api/routes/review_screen.py", route: "read_review", callee: "review_screen" },
      { file: "api/routes/settings.py", route: "read_settings", callee: "preferences.settings_view" },
      { file: "api/routes/settings.py", route: "update_settings", callee: "preferences.settings_view" },
      { file: "api/routes/settings.py", route: "read_providers", callee: "providers.providers_view" },
      { file: "api/routes/settings.py", route: "read_budgets", callee: "budgets.budgets_view" },
      { file: "api/routes/settings.py", route: "change_budget", callee: "budgets.budgets_view" },
      { file: "api/routes/auth.py", route: "reauth_begin", callee: "service.reauth_begin" },
      { file: "api/routes/sessions.py", route: "read_diagnostic", callee: "diagnostic_session.result_payload" }
   ];

   it.each(routeHelpers)("$route returns what $callee builds, the function scanned for its shape", (helper) => {
      expect(returnsCallOf(helper.file, helper.route, helper.callee)).toBe(true);
   });
});

describe("request body vocabulary", () => {
   const requestCases = Object.keys(requestShapes) as (keyof typeof requestShapes)[];

   it.each(requestCases)("%s names exactly the body fields its route reads", (typeName) => {
      const declared = declaredTypeFields("client.ts", typeName);
      const read = requestShapes[typeName]();

      expect(read.length).toBeGreaterThan(0);
      expect(sorted(declared)).toEqual(sorted(read));
   });
});

describe("response parsing", () => {
   beforeEach(() => {
      vi.unstubAllGlobals();
   });

   const parseCases = [
      { name: "openSession", typeName: "SessionPayload", invoke: () => openSession({ mode: "learning" }) },
      { name: "readSession", typeName: "SessionPayload", invoke: () => readSession("sess-1") },
      { name: "readNextItem", typeName: "NextItemResponse", invoke: () => readNextItem("sess-1") },
      { name: "openDiagnostic", typeName: "SessionPayload", invoke: () => openDiagnostic() },
      { name: "readDiagnostic", typeName: "DiagnosticResult", invoke: () => readDiagnostic("sess-1") },
      {
         name: "submitAttempt",
         typeName: "AttemptResult",
         invoke: () => submitAttempt("sess-1", { item_id: "item-1" })
      },
      { name: "readFeedback", typeName: "FeedbackPayload", invoke: () => readFeedback("sess-1", "att-1") },
      {
         name: "submitConfidence",
         typeName: "ConfidenceResult",
         invoke: () => submitConfidence("sess-1", "att-1", { confidence: "guess" })
      },
      {
         name: "submitErrorNote",
         typeName: "ErrorNoteResult",
         invoke: () => submitErrorNote("sess-1", "att-1", "dropped the chain rule factor")
      },
      { name: "closeSession", typeName: "CloseResult", invoke: () => closeSession("sess-1") },
      { name: "readMe", typeName: "MePayload", invoke: () => readMe() },
      {
         name: "requestPurge",
         typeName: "PurgeResult",
         invoke: () => requestPurge({ confirmation: "DELETE EVERYTHING" })
      },
      {
         name: "submitSelfExplanation",
         typeName: "SelfExplanationResult",
         invoke: () => submitSelfExplanation("sess-1", "att-1", { answer: "the product rule" })
      },
      { name: "readProgress", typeName: "ProgressPayload", invoke: () => readProgress() },
      { name: "readCalibration", typeName: "CalibrationPayload", invoke: () => readCalibration() },
      { name: "readMasteryMap", typeName: "MasteryMapPayload", invoke: () => readMasteryMap() },
      { name: "readReview", typeName: "ReviewPayload", invoke: () => readReview() },
      { name: "readSettings", typeName: "SettingsPayload", invoke: () => readSettings() },
      {
         name: "updateSettings",
         typeName: "SettingsPayload",
         invoke: () => updateSettings({ exam_date: "2027-05-10" })
      },
      { name: "readProviders", typeName: "ProvidersPayload", invoke: () => readProviders() },
      { name: "readBudgets", typeName: "BudgetsPayload", invoke: () => readBudgets() },
      {
         name: "updateBudget",
         typeName: "BudgetsPayload",
         invoke: () => updateBudget({ role: "tutor", cap_usd: 1, cap_tokens: null, reauth_token: "t" })
      },
      { name: "requestExport", typeName: "ExportJob", invoke: () => requestExport({ reauth_token: "t" }) },
      { name: "beginReauth", typeName: "ReauthBegin", invoke: () => beginReauth() },
      {
         name: "finishReauth",
         typeName: "ReauthFinish",
         invoke: () => finishReauth({ challenge_id: "c", credential: {} })
      },
      { name: "readFrqUnits", typeName: "FrqUnitsPayload", invoke: () => readFrqUnits() },
      { name: "openUnitCheck", typeName: "UnitCheckPayload", invoke: () => openUnitCheck("BC-UNIT-05") },
      { name: "startFrqAttempt", typeName: "FrqAttempt", invoke: () => startFrqAttempt("SES-1", "FRQ-1", "typed") },
      { name: "uploadPhoto", typeName: "PhotoVerdict", invoke: () => uploadPhoto("ATT-1", { media_type: "image/jpeg", data_base64: "AA==" }) },
      { name: "requestReadBack", typeName: "FrqAttempt", invoke: () => requestReadBack("ATT-1") },
      { name: "confirmReadBack", typeName: "FrqAttempt", invoke: () => confirmReadBack("ATT-1", {}) },
      { name: "readGradings", typeName: "GradingsPayload", invoke: () => readGradings("ATT-1") },
      { name: "askForReread", typeName: "DisputeResult", invoke: () => askForReread("GRD-1") }
   ];

   it.each(parseCases)("$name hands back every field $typeName names", async (parseCase) => {
      const returned = serverShapes[parseCase.typeName as keyof typeof serverShapes]();
      const body = bodyOf(returned);
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, body));

      vi.stubGlobal("fetch", fetchMock);

      const result = await parseCase.invoke();

      expect(sorted(Object.keys(result as object))).toEqual(sorted(returned));
      expect(result).toEqual(body);
   });
});

function base64Url(bytes: number[]) {
   return btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

describe("the re-authentication ceremony", () => {
   beforeEach(() => {
      vi.unstubAllGlobals();
   });

   it("hands the authenticator the decoded challenge and finishes with the assertion and a hex credential id", async () => {
      const challengeBytes = [251, 255, 7, 0, 64];
      const credentialBytes = [0, 171, 254, 16];
      const assertion = {
         id: base64Url(credentialBytes),
         rawId: new Uint8Array(credentialBytes).buffer,
         type: "public-key",
         response: {
            clientDataJSON: new Uint8Array([1, 2]).buffer,
            authenticatorData: new Uint8Array([3]).buffer,
            signature: new Uint8Array([4, 5]).buffer,
            userHandle: null
         },
         getClientExtensionResults: () => ({})
      };
      const credentialsGet = vi.fn().mockResolvedValue(assertion);
      const fetchMock = vi
         .fn()
         .mockResolvedValueOnce(
            jsonResponse(200, {
               challenge_id: "CH-1",
               options: {
                  challenge: base64Url(challengeBytes),
                  allowCredentials: [{ id: base64Url(credentialBytes), type: "public-key" }],
                  userVerification: "preferred"
               }
            })
         )
         .mockResolvedValueOnce(jsonResponse(200, { reauth_token: "token-1" }));

      vi.stubGlobal("fetch", fetchMock);
      vi.stubGlobal("navigator", { credentials: { get: credentialsGet } });

      const token = await reauthenticate();

      const publicKey = credentialsGet.mock.calls[0][0].publicKey;
      const [finishUrl, finishInit] = fetchMock.mock.calls[1];
      const finishBody = JSON.parse(finishInit.body);

      expect(token).toBe("token-1");
      expect(Array.from(publicKey.challenge)).toEqual(challengeBytes);
      expect(Array.from(publicKey.allowCredentials[0].id)).toEqual(credentialBytes);
      expect(new URL(String(finishUrl), "http://x").pathname).toBe("/auth/reauth/finish");
      expect(finishBody.challenge_id).toBe("CH-1");
      expect(finishBody.credential.credential_id).toBe("00abfe10");
      expect(finishBody.credential.rawId).toBe(base64Url(credentialBytes));
      expect(finishBody.credential.response.signature).toBe(base64Url([4, 5]));
   });

   it("finishes nothing when the authenticator returns no assertion", async () => {
      const fetchMock = vi
         .fn()
         .mockResolvedValue(jsonResponse(200, { challenge_id: "CH-1", options: { challenge: base64Url([1]) } }));

      vi.stubGlobal("fetch", fetchMock);
      vi.stubGlobal("navigator", { credentials: { get: vi.fn().mockResolvedValue(null) } });

      await expect(reauthenticate()).rejects.toThrow(/no assertion/);
      expect(fetchMock).toHaveBeenCalledTimes(1);
   });
});

describe("evaluation path vocabulary", () => {
   const declared = declaredRoutes("evaluation.py");

   const evaluationCases = [
      { name: "readMetrics", dynamic: [], invoke: () => readMetrics() },
      { name: "readRepresentations", dynamic: [], invoke: () => readRepresentations() },
      { name: "readExperiments", dynamic: [], invoke: () => readExperiments() },
      {
         name: "setExperimentState",
         dynamic: ["feedback_elaboration"],
         invoke: () => setExperimentState("feedback_elaboration", { state: "on" })
      },
      { name: "readCheckpoints", dynamic: [], invoke: () => readCheckpoints() },
      { name: "startCheckpoint", dynamic: [], invoke: () => startCheckpoint() },
      { name: "readCheckpoint", dynamic: ["CKP-1"], invoke: () => readCheckpoint("CKP-1") },
      {
         name: "scoreCheckpointPart",
         dynamic: ["CKP-1"],
         invoke: () => scoreCheckpointPart("CKP-1", { record_id: "BC-FRQ-2024-1A", points_earned: 2 })
      },
      { name: "finishCheckpoint", dynamic: ["CKP-1"], invoke: () => finishCheckpoint("CKP-1") },
      { name: "readProbe", dynamic: [], invoke: () => readProbe() },
      { name: "startProbe", dynamic: [], invoke: () => startProbe() },
      { name: "readNextProbeItem", dynamic: ["PRB-1"], invoke: () => readNextProbeItem("PRB-1") },
      {
         name: "answerProbeItem",
         dynamic: ["PRB-1"],
         invoke: () => answerProbeItem("PRB-1", { item_id: "ITM-1", answer: { option_id: "A" } })
      }
   ];

   it.each(evaluationCases)("every path $name issues matches a route app/api/routes/evaluation.py declares", async (wiringCase) => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await wiringCase.invoke();

      const { url, method } = issuedRequest(fetchMock);
      const normalized = normalizedIssuedPath(new URL(url, "http://x").pathname, wiringCase.dynamic);

      expect(declared).toContainEqual({ method, path: normalized });
   });

   it("passes a stated day to the metrics read as the today query the route takes", async () => {
      const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, {}));

      vi.stubGlobal("fetch", fetchMock);
      await readMetrics("2026-09-24");

      const { url } = issuedRequest(fetchMock);

      expect(new URL(url, "http://x").searchParams.get("today")).toBe("2026-09-24");
      expect(functionSource("api/routes/evaluation.py", "read_metrics")).toContain("today: str | None = None");
   });
});

describe("evaluation response shape vocabulary", () => {
   const evaluationShapes = [
      { typeName: "LearningMetric", fields: () => returnedFields("progress/learning_metrics.py", "metric") },
      {
         typeName: "ExperimentComparison",
         fields: () => nestedDictFields("experiments/analysis.py", "return {\n      \"name\": comparison.name")
      },
      { typeName: "ArmOutcomes", fields: () => nestedDictFields("experiments/analysis.py", "def arm_view(") },
      {
         typeName: "RepresentationMatrixPayload",
         fields: () => returnedFields("progress/representations.py", "representation_matrix")
      },
      {
         typeName: "CheckpointAvailability",
         fields: () => returnedFields("checkpoint/service.py", "availability")
      },
      { typeName: "CheckpointView", fields: () => returnedFields("checkpoint/service.py", "checkpoint_view") },
      { typeName: "ProbeAvailability", fields: () => returnedFields("checkpoint/probe.py", "availability") },
      {
         typeName: "ProbeAdministration",
         fields: () => returnedFields("checkpoint/probe.py", "administration_view")
      },
      { typeName: "MetricsPayload", fields: () => returnedFields("api/routes/evaluation.py", "read_metrics") },
      {
         typeName: "CheckpointsPayload",
         fields: () => returnedFields("api/routes/evaluation.py", "read_checkpoints")
      },
      { typeName: "ProbePayload", fields: () => returnedFields("api/routes/evaluation.py", "read_probe") }
   ];

   it.each(evaluationShapes)("$typeName carries the field names its server module returns", (shapeCase) => {
      const declared = declaredTypeFields("types.ts", shapeCase.typeName);
      const returned = shapeCase.fields();

      expect(returned.length).toBeGreaterThan(0);
      expect(sorted(declared)).toEqual(sorted(returned));
   });

   it("MetricValue carries value's fields and the two external_checkpoint adds", () => {
      const declared = declaredTypeFields("types.ts", "MetricValue");
      const added = [...functionSource("progress/learning_metrics.py", "external_checkpoint").matchAll(/earned\["([a-z_]+)"\]\s*=/g)].map(
         (match) => match[1]
      );

      expect(added.length).toBeGreaterThan(0);
      expect(sorted(declared)).toEqual(sorted([...returnedFields("progress/learning_metrics.py", "value"), ...added]));
   });

   it("ProbeServedItem is the bank's item dict plus the served format", () => {
      const declared = declaredTypeFields("types.ts", "ProbeServedItem");
      const nextItem = functionSource("checkpoint/probe.py", "next_item");

      expect(nextItem).toContain("dict(_as_item_dict(item_row), format=");
      expect(sorted(declared)).toEqual(sorted([...returnedFields("runtime/bank.py", "_as_item_dict"), "format"]));
   });
});
