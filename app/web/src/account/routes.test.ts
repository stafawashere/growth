import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
   beginAddPasskey,
   beginLogin,
   beginRecoveryRegistration,
   beginRegistration,
   finishAddPasskey,
   finishLogin,
   finishRecoveryRegistration,
   finishRegistration,
   readAuthStatus
} from "../api/client";

const here = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.join(here, "..", "..", "..");
const clientSource = fs.readFileSync(path.join(here, "..", "api", "client.ts"), "utf8");

function pythonSource(relativePath: string) {
   return fs.readFileSync(path.join(appDir, relativePath), "utf8");
}

function declaredAuthRoutes() {
   const source = pythonSource("api/routes/auth.py");
   const prefix = (source.match(/APIRouter\(\s*prefix="([^"]*)"/) ?? ["", ""])[1];
   const decoratorPattern = /@router\.(get|post|put|delete)\(\s*"([^"]*)"/g;

   return Array.from(source.matchAll(decoratorPattern), (match) => ({
      method: match[1].toUpperCase(),
      path: prefix + match[2]
   }));
}

function functionSource(relativePath: string, name: string) {
   const source = pythonSource(relativePath);
   const start = source.indexOf(`def ${name}(`);

   if (start === -1) {
      throw new Error(`${relativePath} defines no ${name}`);
   }

   const rest = source.slice(start + 1);
   const nextDefinition = rest.search(/\n(@router|def |class )/);

   return nextDefinition === -1 ? rest : rest.slice(0, nextDefinition);
}

function balancedFrom(text: string, openIndex: number) {
   let depth = 0;

   for (let index = openIndex; index < text.length; index += 1) {
      const character = text[index];

      if (character === "{") {
         depth += 1;
      }

      if (character === "}") {
         depth -= 1;
      }

      if (depth === 0) {
         return text.slice(openIndex, index + 1);
      }
   }

   throw new Error("unbalanced dict literal");
}

function returnedLiteral(relativePath: string, name: string) {
   const body = functionSource(relativePath, name);
   const returnAt = body.lastIndexOf("return {");

   if (returnAt === -1) {
      throw new Error(`${name} returns no dict literal`);
   }

   return balancedFrom(body, body.indexOf("{", returnAt));
}

function topLevelKeys(literal: string) {
   const keys: string[] = [];
   let depth = 0;

   for (let index = 0; index < literal.length; index += 1) {
      const character = literal[index];

      if (character === "{") {
         depth += 1;
      }

      if (character === "}") {
         depth -= 1;
      }

      const opensKey = depth === 1 && character === "\"";
      const keyMatch = opensKey ? literal.slice(index).match(/^"(\w+)":/) : null;

      if (keyMatch !== null) {
         keys.push(keyMatch[1]);
         index += keyMatch[0].length - 1;
      }
   }

   return keys;
}

function nestedLiteral(literal: string, key: string) {
   const keyAt = literal.indexOf(`"${key}":`);

   return balancedFrom(literal, literal.indexOf("{", keyAt));
}

function bodyFieldsRead(relativePath: string, name: string) {
   const body = functionSource(relativePath, name);

   return Array.from(body.matchAll(/fields\.get\("(\w+)"\)/g), (match) => match[1]);
}

function clientInterfaceFields(typeName: string) {
   const match = clientSource.match(new RegExp(`export interface ${typeName} \\{([^}]*)\\}`));

   if (match === null) {
      throw new Error(`client.ts declares no interface ${typeName}`);
   }

   return Array.from(match[1].matchAll(/^\s+(\w+)\??:/gm), (field) => field[1]);
}

function sorted(names: string[]) {
   return [...names].sort();
}

afterEach(() => {
   vi.unstubAllGlobals();
});

describe("passkey paths", () => {
   const declared = declaredAuthRoutes();

   const calls = [
      { name: "beginRegistration", invoke: () => beginRegistration() },
      { name: "finishRegistration", invoke: () => finishRegistration({ challenge_id: "c", credential: {} }) },
      { name: "beginLogin", invoke: () => beginLogin() },
      { name: "finishLogin", invoke: () => finishLogin({ challenge_id: "c", credential: {} }) },
      { name: "beginRecoveryRegistration", invoke: () => beginRecoveryRegistration() },
      {
         name: "finishRecoveryRegistration",
         invoke: () => finishRecoveryRegistration({ challenge_id: "c", credential: {}, recovery_code: "r" })
      },
      { name: "readAuthStatus", invoke: () => readAuthStatus() },
      { name: "beginAddPasskey", invoke: () => beginAddPasskey() },
      { name: "finishAddPasskey", invoke: () => finishAddPasskey({ challenge_id: "c", credential: {} }) }
   ];

   it.each(calls)("every path $name issues matches a declared FastAPI route", async (call) => {
      const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 200, json: () => Promise.resolve({}) });

      vi.stubGlobal("fetch", fetchMock);
      await call.invoke();

      const [url, init] = fetchMock.mock.calls[0];
      const issued = { method: init?.method ?? "GET", path: new URL(String(url), "http://x").pathname };

      expect(declared.length).toBeGreaterThan(0);
      expect(declared).toContainEqual(issued);
   });
});

describe("passkey payload vocabulary", () => {
   const shapes = [
      {
         typeName: "CeremonyBegin",
         server: () => topLevelKeys(returnedLiteral("auth/service.py", "register_begin"))
      },
      {
         typeName: "CeremonyBegin",
         server: () => topLevelKeys(returnedLiteral("auth/service.py", "login_begin"))
      },
      {
         typeName: "RegistrationFinish",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "register_finish"))
      },
      {
         typeName: "RegisteredUser",
         server: () => topLevelKeys(nestedLiteral(returnedLiteral("api/routes/auth.py", "register_finish"), "user"))
      },
      {
         typeName: "LoginFinish",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "login_finish"))
      },
      {
         typeName: "FinishRegistrationFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "register_finish")
      },
      {
         typeName: "FinishLoginFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "login_finish")
      },
      {
         typeName: "FinishRecoveryRegistrationFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "recovery_register_finish")
      },
      {
         typeName: "CeremonyBegin",
         server: () => topLevelKeys(returnedLiteral("auth/service.py", "add_passkey_begin"))
      },
      {
         typeName: "AuthStatus",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "status"))
      },
      {
         typeName: "FinishAddPasskeyFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "add_passkey_finish")
      },
      {
         typeName: "AddPasskeyFinish",
         server: () => topLevelKeys(returnedLiteral("auth/service.py", "add_passkey_finish"))
      },
      {
         typeName: "RecoveryRegistrationFinish",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "recovery_register_finish"))
      }
   ];

   it.each(shapes)("$typeName carries the field names the server module uses", (shape) => {
      const served = shape.server();

      expect(served.length).toBeGreaterThan(0);
      expect(sorted(clientInterfaceFields(shape.typeName))).toEqual(sorted(served));
   });
});
