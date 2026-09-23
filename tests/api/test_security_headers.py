"""docs/plan/09-security-and-privacy.md "Transport and hosting": the CORS and CSP paragraphs
(lines 158 and 160). CORS is an empty allowlist with no configuration option to widen it; CSP is
a strict policy with no unsafe-inline or unsafe-eval for scripts, styles restricted to self,
img-src self plus blob:, connect-src self, and frame-ancestors, object-src and base-uri all
locked down.

The expected CSP directives are parsed out of the plan paragraph itself at test time rather than
retyped here, so a hand-typed copy can never drift from the plan and pass anyway (checklist 4).
"""
import json
import re
from pathlib import Path

from starlette.testclient import TestClient

from app.api.app import create_app
from app.design.tokens import COLOUR_TOKENS, THEMES, TYPE_TOKENS
from app.main import build_application, mount_client, settings_from_environment

PLAN_PATH = (
   Path(__file__).resolve().parent.parent.parent
   / "docs" / "plan" / "09-security-and-privacy.md"
)


def csp_paragraph():
   text = PLAN_PATH.read_text()
   match = re.search(r"^\*\*CSP\.\*\*.*$", text, re.MULTILINE)

   assert match, "expected a CSP paragraph in docs/plan/09-security-and-privacy.md"

   return match.group(0)


def cors_paragraph():
   text = PLAN_PATH.read_text()
   match = re.search(r"^\*\*CORS\.\*\*.*$", text, re.MULTILINE)

   assert match, "expected a CORS paragraph in docs/plan/09-security-and-privacy.md"

   return match.group(0)


def directives_named_in_the_plan():
   """Every `directive-name value` backtick token the CSP paragraph names outright."""
   paragraph = csp_paragraph()
   pairs = re.findall(r"`([a-z-]+) ([^`]+)`", paragraph)

   return dict(pairs)


def forbidden_script_tokens_named_in_the_plan():
   paragraph = csp_paragraph()

   return re.findall(r"`(unsafe-[a-z]+)`", paragraph)


def build_application_with_dist(env, dist_dir):
   """The same construction app.main.build_application runs, with the built client's dist_dir
   injected instead of the repository's own app/web/dist, so the test never depends on a real
   client build sitting on disk and never mounts a bare FastAPI in place of the real app."""
   settings = settings_from_environment(env)
   settings.db_path.parent.mkdir(parents=True, exist_ok=True)

   from app.runtime.context import build_session_context

   engine = settings.resolve_engine()
   settings.session_context = build_session_context(engine, settings.content_root)
   application = create_app(settings)
   mount_client(application, env, dist_dir=dist_dir)

   return application


def sample_token_file(path):
   """A token file that satisfies app/design/css.py's own checks, built from the vocabulary
   app/design/tokens.py names rather than a hand-typed subset of it."""
   theme_tokens = {}

   for name in COLOUR_TOKENS:
      theme_tokens[name] = "#336699"

   for name in TYPE_TOKENS:
      theme_tokens[name] = "16px"

   tokens = {theme: dict(theme_tokens) for theme in THEMES}
   path.write_text(json.dumps(tokens))

   return path


def parse_csp(header_value):
   directives = {}

   for clause in header_value.split(";"):
      clause = clause.strip()

      if clause == "":
         continue

      name, _, value = clause.partition(" ")
      directives[name] = value

   return directives


def test_the_plan_names_a_cors_paragraph_with_no_allowlist_configuration():
   paragraph = cors_paragraph()

   assert "empty allowlist" in paragraph
   assert "no configuration option to permit" in paragraph


def test_response_headers_carry_every_csp_directive_the_plan_names(tmp_path):
   expected = directives_named_in_the_plan()

   assert expected, "expected the CSP paragraph to name at least one directive"

   application = build_application({"GROWTH_DB_PATH": str(tmp_path / "growth.db")})
   client = TestClient(application)
   response = client.get("/healthz")
   actual = parse_csp(response.headers["content-security-policy"])

   for name, value in expected.items():
      assert actual[name] == value, "directive {0} was {1!r}, plan names {2!r}".format(
         name, actual.get(name), value
      )

   self_value = expected["default-src"]

   assert actual["script-src"] == self_value
   assert actual["style-src"] == self_value

   for forbidden in forbidden_script_tokens_named_in_the_plan():
      assert forbidden not in actual["script-src"]


def test_csp_header_is_present_on_a_404(tmp_path):
   application = build_application({"GROWTH_DB_PATH": str(tmp_path / "growth.db")})
   client = TestClient(application)
   response = client.get("/this-path-claims-nothing")

   assert response.status_code == 404
   assert "content-security-policy" in response.headers


def test_csp_header_covers_the_mounted_client_index(tmp_path):
   dist_dir = tmp_path / "dist"
   dist_dir.mkdir()
   (dist_dir / "index.html").write_text("<html><body>growth client</body></html>")

   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db")}
   application = build_application_with_dist(env, dist_dir)
   client = TestClient(application)
   response = client.get("/")

   assert response.status_code == 200
   assert "content-security-policy" in response.headers


def test_csp_header_covers_a_mounted_static_asset(tmp_path):
   dist_dir = tmp_path / "dist"
   assets_dir = dist_dir / "assets"
   assets_dir.mkdir(parents=True)
   (dist_dir / "index.html").write_text("<html><body>growth client</body></html>")
   (assets_dir / "app.js").write_text("console.log('growth');")

   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db")}
   application = build_application_with_dist(env, dist_dir)
   client = TestClient(application)

   response = client.get("/assets/app.js")

   assert response.status_code == 200
   assert "content-security-policy" in response.headers


def test_growth_tokens_css_is_served_from_the_configured_path(tmp_path):
   dist_dir = tmp_path / "dist"
   dist_dir.mkdir()
   (dist_dir / "index.html").write_text("<html><body>growth client</body></html>")
   tokens_path = sample_token_file(tmp_path / "design-tokens.json")

   env = {
      "GROWTH_DB_PATH": str(tmp_path / "growth.db"),
      "GROWTH_TOKENS_PATH": str(tokens_path),
   }
   application = build_application_with_dist(env, dist_dir)
   client = TestClient(application)

   response = client.get("/growth-tokens.css")

   assert response.status_code == 200
   assert response.headers["content-type"].startswith("text/css")
   assert "content-security-policy" in response.headers
   assert "--growth-surface-page" in response.text


def test_cross_origin_request_gets_no_access_control_allow_origin_header(world):
   client = world.client()

   response = client.get("/me", headers={"Origin": "https://attacker.example"})

   assert "access-control-allow-origin" not in response.headers


def test_preflight_request_gets_no_access_control_allow_origin_header(world):
   client = world.client()

   response = client.options(
      "/me",
      headers={
         "Origin": "https://attacker.example",
         "Access-Control-Request-Method": "GET",
      },
   )

   assert "access-control-allow-origin" not in response.headers
