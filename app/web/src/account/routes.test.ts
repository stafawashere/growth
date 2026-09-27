import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
   changePassword,
   readAuthStatus,
   reauthenticate,
   resetWithRecoveryCode,
   signIn,
   signOut,
   signUp
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

describe("password auth paths", () => {
   const declared = declaredAuthRoutes();

   const calls = [
      { name: "signUp", invoke: () => signUp({ username: "student", password: "p" }) },
      { name: "signIn", invoke: () => signIn({ username: "student", password: "p" }) },
      { name: "signOut", invoke: () => signOut() },
      { name: "readAuthStatus", invoke: () => readAuthStatus() },
      { name: "reauthenticate", invoke: () => reauthenticate({ password: "p" }) },
      {
         name: "changePassword",
         invoke: () => changePassword({ current_password: "p", new_password: "q", reauth_token: "t" })
      },
      {
         name: "resetWithRecoveryCode",
         invoke: () => resetWithRecoveryCode({ recovery_code: "r", new_password: "q", username: "student" })
      }
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

describe("password auth payload vocabulary", () => {
   const shapes = [
      {
         typeName: "SignUpFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "signup")
      },
      {
         typeName: "SignUpResult",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "signup"))
      },
      {
         typeName: "RegisteredUser",
         server: () => topLevelKeys(nestedLiteral(returnedLiteral("api/routes/auth.py", "signup"), "user"))
      },
      {
         typeName: "SignInFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "login")
      },
      {
         typeName: "SignInResult",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "login"))
      },
      {
         typeName: "SignOutResult",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "logout"))
      },
      {
         typeName: "AuthStatus",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "status"))
      },
      {
         typeName: "ReauthFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "reauth")
      },
      {
         typeName: "ReauthResult",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "reauth"))
      },
      {
         typeName: "ChangePasswordFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "change_password")
      },
      {
         typeName: "ChangePasswordResult",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "change_password"))
      },
      {
         typeName: "RecoveryResetFields",
         server: () => bodyFieldsRead("api/routes/auth.py", "recovery_reset")
      },
      {
         typeName: "RecoveryResetResult",
         server: () => topLevelKeys(returnedLiteral("api/routes/auth.py", "recovery_reset"))
      }
   ];

   it.each(shapes)("$typeName carries the field names the server module uses", (shape) => {
      const served = shape.server();

      expect(served.length).toBeGreaterThan(0);
      expect(sorted(clientInterfaceFields(shape.typeName))).toEqual(sorted(served));
   });
});
