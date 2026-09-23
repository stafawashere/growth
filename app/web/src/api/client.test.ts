import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
import { describe, expect, it, vi, beforeEach } from "vitest";

import {
   ApiError,
   openSession,
   readSession,
   readNextItem,
   submitAttempt,
   readFeedback,
   submitConfidence,
   submitErrorNote,
   closeSession,
   readMe,
   requestPurge
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
   const depths = depthByIndex(text.slice(openIndex));
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

function declaredTypeFields(moduleFile: string, typeName: string) {
   const source = fs.readFileSync(path.join(here, moduleFile), "utf8");
   const anchorIndex = source.indexOf(`export interface ${typeName} {`);
   const hasType = anchorIndex >= 0;

   if (!hasType) {
      throw new Error(`${moduleFile} declares no ${typeName}`);
   }

   const slice = balancedSlice(source, source.indexOf("{", anchorIndex));
   const depths = depthByIndex(slice);
   const pattern = /\n\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:/g;
   const fields: string[] = [];
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

function sorted(names: string[]) {
   return [...names].sort();
}

function bodyOf(fields: string[]) {
   return Object.fromEntries(fields.map((field) => [field, `served ${field}`]));
}

const serverShapes = {
   SessionPayload: () => returnedFields("api/routes/sessions.py", "session_payload"),
   NextItemResponse: () => returnedFields("api/routes/sessions.py", "read_next_item"),
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
   ]
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
      ...declaredRoutes("purge.py")
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
      json: () => Promise.resolve(body)
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
      { typeName: "ServedOption", module: "types.ts" },
      { typeName: "AttemptResult", module: "types.ts" },
      { typeName: "StepMark", module: "types.ts" },
      { typeName: "ElaboratedPayload", module: "types.ts" },
      { typeName: "FeedbackPayload", module: "types.ts" },
      { typeName: "NextItemResponse", module: "client.ts" },
      { typeName: "ConfidenceResult", module: "client.ts" },
      { typeName: "ErrorNoteResult", module: "client.ts" },
      { typeName: "CloseResult", module: "client.ts" },
      { typeName: "MePayload", module: "client.ts" },
      { typeName: "PurgeResult", module: "client.ts" }
   ];

   it.each(shapeCases)("$typeName carries the field names its server module returns", (shapeCase) => {
      const declared = declaredTypeFields(shapeCase.module, shapeCase.typeName);
      const returned = serverShapes[shapeCase.typeName as keyof typeof serverShapes]();

      expect(returned.length).toBeGreaterThan(0);
      expect(sorted(declared)).toEqual(sorted(returned));
   });

   it("ServedItem declares no field the served item does not carry", () => {
      const served = [...returnedFields("runtime/bank.py", "_as_item_dict"), ...dressedItemFields()];
      const declared = declaredTypeFields("types.ts", "ServedItem");
      const absentFromTheServer = declared.filter((field) => !served.includes(field));

      expect(served.length).toBeGreaterThan(0);
      expect(absentFromTheServer).toEqual([]);
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
      }
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
