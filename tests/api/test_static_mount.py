"""Module F: the ASGI entrypoint serves the built React client and the operator's token
stylesheet from the same origin as the API, per docs/plan/06-architecture.md's system diagram
(the client speaks REST to one process) and BUILD-LEDGER.md's own line for this module:
`GET /growth-tokens.css` serves `stylesheet_from_token_file(GROWTH_TOKENS_PATH)` as `text/css`,
defaulting to the repository's own `app/design/growth-tokens.json` when GROWTH_TOKENS_PATH is
unset (ruled 2026-09-23), 404 when an explicitly configured path is unreadable, and the built
client under `app/web/dist` is served at `/`.

The client mount claims exactly two shapes of path, a real file under dist/assets and GET / for
index.html, so a path that only looks like an API path (GET /export, GET /purge) or is simply
unclaimed falls straight through to Starlette's own 404 or 405, never to a 200 of index.html.
app/web/src/App.tsx routes screens with useState, never a URL path, so nothing in the client
needed a broader fallback.

The mount is exercised two ways. `build_application` proves the real wiring: the live
`app/web/dist` and the live API routers, so the precedence and method tests run against the
actual application rather than a stand-in. `app.main.mount_client` is exercised directly against
a bare FastAPI app and a tmp_path tree for the missing-dist, path-traversal and token-path-at-
request-time cases, so those tests never touch the repository's own `app/web/dist` or var/.
"""
import json
import os
import subprocess
import sys

from fastapi import FastAPI
from starlette.testclient import TestClient

from app.design.tokens import COLOUR_TOKENS, THEMES, TYPE_TOKENS
from app.main import REPO_ROOT, build_application, mount_client


def env_for(tmp_path, **overrides):
   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db")}
   env.update(overrides)
   return env


def full_token_file(tmp_path, name="tokens.json"):
   theme_tokens = {}

   for index, colour_name in enumerate(COLOUR_TOKENS):
      theme_tokens[colour_name] = "#{0:06x}".format(index * 111111 % 0xFFFFFF)

   for type_name in TYPE_TOKENS:
      theme_tokens[type_name] = "1rem"

   tokens = {theme: dict(theme_tokens) for theme in THEMES}
   path = tmp_path / name
   path.write_text(json.dumps(tokens))

   return path


def test_growth_tokens_css_defaults_to_the_repository_token_file_when_the_path_is_unset(tmp_path):
   application = build_application(env_for(tmp_path))
   client = TestClient(application)

   response = client.get("/growth-tokens.css")

   assert response.status_code == 200
   assert response.headers["content-type"].startswith("text/css")
   assert "--growth-surface-page" in response.text


def test_growth_tokens_css_is_404_when_the_file_is_unreadable(tmp_path):
   application = build_application(
      env_for(tmp_path, GROWTH_TOKENS_PATH=str(tmp_path / "missing-tokens.json"))
   )
   client = TestClient(application)

   response = client.get("/growth-tokens.css")

   assert response.status_code == 404
   assert response.content == b""


def test_growth_tokens_css_serves_the_stylesheet_when_configured(tmp_path):
   token_path = full_token_file(tmp_path)
   application = build_application(
      env_for(tmp_path, GROWTH_TOKENS_PATH=str(token_path))
   )
   client = TestClient(application)

   response = client.get("/growth-tokens.css")

   assert response.status_code == 200
   assert response.headers["content-type"].startswith("text/css")
   assert "--growth-surface-page" in response.text


def test_growth_tokens_css_reads_the_path_at_request_time(tmp_path):
   """Checklist 7: configuration read once at build time is frozen configuration. GROWTH_TOKENS_PATH
   is unset when the application is built, and the same env mapping only gains the key afterward,
   so a handler that captured the env value (or a copy of it) at build time would still serve the
   default repository stylesheet here, never the overriding one."""
   env = env_for(tmp_path)
   application = build_application(env)
   client = TestClient(application)

   before = client.get("/growth-tokens.css")

   assert before.status_code == 200
   default_stylesheet = before.text

   token_path = full_token_file(tmp_path, name="tokens.json")
   env["GROWTH_TOKENS_PATH"] = str(token_path)
   after = client.get("/growth-tokens.css")

   assert after.status_code == 200
   assert "--growth-surface-page" in after.text
   assert after.text != default_stylesheet


def _registered_api_paths(routes):
   """Walks application.routes for every GET path an included router (auth, me, sessions,
   purge, content, review, progress, settings, export, health) actually registered, paired
   with the position of its containing router in the top-level list. This FastAPI version
   groups each include_router call into one `_IncludedRouter` entry rather than flattening its
   routes, so a plain `route.path` scan over the top level sees only the client mount's own
   routes and misses the API entirely; walking into `original_router.routes` is what makes the
   enumeration real rather than a scan that would pass by finding nothing."""
   found = []

   for index, route in enumerate(routes):
      is_included_router = type(route).__name__ == "_IncludedRouter"

      if not is_included_router:
         continue

      for sub_route in route.original_router.routes:
         methods = getattr(sub_route, "methods", None) or set()

         if "GET" in methods:
            found.append((index, sub_route.path))

   return found


def test_api_routes_precede_the_client_mount(tmp_path):
   """The client's own routes (GET / and the /assets mount) are registered last, so they never
   shadow an API route, enumerated from application.routes rather than typed out."""
   application = build_application(env_for(tmp_path))
   routes = application.routes
   client_route_indexes = [
      index for index, route in enumerate(routes)
      if getattr(route, "path", None) == "/" or getattr(route, "name", None) == "web-assets"
   ]

   assert client_route_indexes, "expected the client mount to have registered its own routes"

   first_client_index = min(client_route_indexes)
   api_paths = _registered_api_paths(routes)

   assert api_paths, "expected create_app's routers to register at least one GET route"
   assert any(path == "/me" for _, path in api_paths)
   assert any(path == "/settings" for _, path in api_paths)
   assert any(path == "/progress" for _, path in api_paths)

   shadowed = [path for index, path in api_paths if index > first_client_index]

   assert shadowed == []


def test_get_me_is_answered_by_the_api_not_the_client_mount(tmp_path):
   application = build_application(env_for(tmp_path))
   client = TestClient(application)

   response = client.get("/me")

   assert response.headers["content-type"].startswith("application/json")


def test_get_export_is_405_not_the_client_index(tmp_path):
   """/export is POST-only. Before the fallback was narrowed, a catch-all route matched every
   GET unconditionally, which is a full match ahead of the POST route's method-only partial
   match, so GET /export answered 200 with the client's index.html instead of the 405 Starlette
   gives a path whose shape matches a route but whose method does not."""
   application = build_application(env_for(tmp_path))
   client = TestClient(application)

   response = client.get("/export")

   assert response.status_code == 405
   assert "text/html" not in response.headers.get("content-type", "")


def test_get_purge_is_405_not_the_client_index(tmp_path):
   application = build_application(env_for(tmp_path))
   client = TestClient(application)

   response = client.get("/purge")

   assert response.status_code == 405
   assert "text/html" not in response.headers.get("content-type", "")


def test_get_an_unknown_path_is_404_with_no_html_body(tmp_path):
   application = build_application(env_for(tmp_path))
   client = TestClient(application)

   response = client.get("/this-path-claims-nothing")

   assert response.status_code == 404
   assert "text/html" not in response.headers.get("content-type", "")


def test_missing_dist_directory_answers_404_naming_the_build_step(tmp_path):
   application = FastAPI()
   mount_client(application, env={}, dist_dir=tmp_path / "dist")
   client = TestClient(application)

   response = client.get("/")

   assert response.status_code == 404
   assert response.text != ""
   assert "app/web" in response.text


def test_dist_present_serves_index_html_at_root(tmp_path):
   dist_dir = tmp_path / "dist"
   dist_dir.mkdir()
   index_html = dist_dir / "index.html"
   index_html.write_text("<html><body>growth client</body></html>")

   application = FastAPI()
   mount_client(application, env={}, dist_dir=dist_dir)
   client = TestClient(application)

   response = client.get("/")

   assert response.status_code == 200
   assert "growth client" in response.text


def test_dist_present_does_not_fall_back_to_index_html_for_an_unclaimed_path(tmp_path):
   """The narrowed mount answers only / and a real file under assets. A path that is neither,
   such as /settings, must not get a 200 of index.html: nothing in the client is routed by URL
   path, so a browser typing /settings should hit the API's own GET /settings, or Starlette's
   plain 404 in a bare app that registers no such route, never client HTML."""
   dist_dir = tmp_path / "dist"
   dist_dir.mkdir()
   (dist_dir / "index.html").write_text("<html><body>growth client</body></html>")

   application = FastAPI()
   mount_client(application, env={}, dist_dir=dist_dir)
   client = TestClient(application)

   response = client.get("/settings")

   assert response.status_code == 404
   assert "growth client" not in response.text


def test_dist_present_serves_a_real_asset_file_as_itself(tmp_path):
   dist_dir = tmp_path / "dist"
   dist_dir.mkdir()
   (dist_dir / "index.html").write_text("<html><body>growth client</body></html>")
   assets_dir = dist_dir / "assets"
   assets_dir.mkdir()
   (assets_dir / "app.js").write_text("console.log('growth');")

   application = FastAPI()
   mount_client(application, env={}, dist_dir=dist_dir)
   client = TestClient(application)

   response = client.get("/assets/app.js")

   assert response.status_code == 200
   assert "console.log" in response.text


def _planted_secret_tree(tmp_path):
   """A dist/assets directory two levels under a secret file, mirroring the real repository's
   shape: app/web/dist sits three levels under the repo root, so app/web/dist/assets sits four
   levels under it, and var/growth.db and .env are siblings of app/ at the root."""
   root = tmp_path / "repo"
   secret = root / "var" / "growth.db"
   secret.parent.mkdir(parents=True)
   secret.write_text("TOPSECRET")

   dist_dir = root / "app" / "web" / "dist"
   assets_dir = dist_dir / "assets"
   assets_dir.mkdir(parents=True)
   (dist_dir / "index.html").write_text("<html><body>growth client</body></html>")
   (assets_dir / "app.js").write_text("console.log('growth');")

   return dist_dir, secret


def _traversal_client(dist_dir):
   application = FastAPI()
   mount_client(application, env={}, dist_dir=dist_dir)

   return TestClient(application, raise_server_exceptions=False)


def test_asset_traversal_via_dotdot_is_blocked(tmp_path):
   """assets_dir sits four directories under the planted secret's parent (assets, dist, web,
   app), so four ../ segments are what actually reaches var/growth.db; fewer just 404 on a
   nonexistent path without proving anything about the guard."""
   dist_dir, secret = _planted_secret_tree(tmp_path)
   client = _traversal_client(dist_dir)

   response = client.get("/assets/..%2F..%2F..%2F..%2Fvar%2Fgrowth.db")

   assert response.status_code != 200
   assert secret.read_text() not in response.text


def test_asset_traversal_via_encoded_dot_segments_is_blocked(tmp_path):
   dist_dir, secret = _planted_secret_tree(tmp_path)
   client = _traversal_client(dist_dir)

   response = client.get("/assets/%2e%2e/%2e%2e/%2e%2e/%2e%2e/var/growth.db")

   assert response.status_code != 200
   assert secret.read_text() not in response.text


def test_asset_traversal_via_leading_slash_is_blocked(tmp_path):
   """A path segment that starts with a slash after decoding is StaticFiles' other rejected
   shape (lookup_path refuses anything starting with "/" or "\\"), distinct from a relative
   ../ climb, so it is worth its own case rather than folding into the ../ variants above."""
   dist_dir, secret = _planted_secret_tree(tmp_path)
   client = _traversal_client(dist_dir)

   response = client.get("/assets/..%2F..%2F..%2F..%2F%2Fvar%2Fgrowth.db")

   assert response.status_code != 200
   assert secret.read_text() not in response.text


def test_importing_app_main_opens_no_database(tmp_path):
   """A bare `import app.main` must never build the application: build_application (and the
   var/growth.db it opens) runs only when something reads the `application` attribute. GROWTH_DB_PATH
   is pointed at a tmp path in the subprocess's own environment so a regression would create a
   file we can see, rather than silently touching the repository's real var/growth.db."""
   db_path = tmp_path / "growth.db"
   env = dict(os.environ)
   env["GROWTH_DB_PATH"] = str(db_path)

   result = subprocess.run(
      [sys.executable, "-c", "import app.main"],
      cwd=str(REPO_ROOT),
      env=env,
      capture_output=True,
      text=True,
   )

   assert result.returncode == 0, result.stderr
   assert not db_path.exists()


def test_importing_app_main_leaves_the_repository_database_untouched():
   """The same guarantee against the actual default path: importing this module with no
   GROWTH_DB_PATH override must not create or modify the repository's own var/growth.db."""
   db_path = REPO_ROOT / "var" / "growth.db"
   existed_before = db_path.exists()
   mtime_before = db_path.stat().st_mtime if existed_before else None

   result = subprocess.run(
      [sys.executable, "-c", "import app.main"],
      cwd=str(REPO_ROOT),
      capture_output=True,
      text=True,
   )

   assert result.returncode == 0, result.stderr

   if existed_before:
      assert db_path.stat().st_mtime == mtime_before
   else:
      assert not db_path.exists()


def test_application_attribute_still_builds_the_real_app(tmp_path, monkeypatch):
   """`uvicorn app.main:application` resolves the module then reads this attribute, so the
   lazy __getattr__ must still hand back a working FastAPI application on that access. Run in a
   subprocess with GROWTH_DB_PATH pointed at tmp_path so this proof never opens the repository's
   own var/growth.db, and the module-level cache from an earlier in-process access (if any)
   never masks a regression here."""
   db_path = tmp_path / "growth.db"
   env = dict(os.environ)
   env["GROWTH_DB_PATH"] = str(db_path)
   script = (
      "import app.main as m\n"
      "from starlette.testclient import TestClient\n"
      "application = m.application\n"
      "assert application is m.application\n"
      "client = TestClient(application)\n"
      "response = client.get('/growth-tokens.css')\n"
      "assert response.status_code == 200, response.status_code\n"
      "assert '--growth-surface-page' in response.text\n"
      "print('ok')\n"
   )

   result = subprocess.run(
      [sys.executable, "-c", script],
      cwd=str(REPO_ROOT),
      env=env,
      capture_output=True,
      text=True,
   )

   assert result.returncode == 0, result.stderr
   assert "ok" in result.stdout
   assert db_path.exists()
