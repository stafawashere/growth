"""The unauthenticated-reachable route list docs/plan/09-security-and-privacy.md's "Per IP"
paragraph names, checked against the live route table so the doc cannot drift from the code.

A route is unauthenticated-reachable when its dependency tree carries neither current_session nor
current_user (app/api/deps.py); current_user itself depends on current_session, so walking the
dependant tree for either name catches both. GET /healthz carries neither dependency either, but
refuses any non-loopback caller inside the handler itself rather than through a session dependency,
so it is unauthenticated-reachable by this test's definition and named in the doc's set below.

The application under test is built with build_application, app.main's composition root, rather
than create_app alone, because app.main.mount_client adds three more unauthenticated routes after
create_app returns: GET /growth-tokens.css and GET / (each a plain APIRoute the client mount adds
directly to the application) and the /assets StaticFiles mount, which carries no dependant tree at
all and so is checked separately below. A test built only from create_app's routers would miss all
three and go on missing any future unauthenticated route mount_client adds.
"""
from fastapi.routing import APIRoute
from starlette.routing import Mount

from app.api.deps import current_session, current_user
from app.main import build_application

DOC_UNAUTHENTICATED_ROUTES = {
   ("POST", "/auth/passkey/register/begin"),
   ("POST", "/auth/passkey/register/finish"),
   ("GET", "/auth/status"),
   ("POST", "/auth/recovery/register/begin"),
   ("POST", "/auth/recovery/register/finish"),
   ("POST", "/auth/passkey/login/begin"),
   ("POST", "/auth/passkey/login/finish"),
   ("GET", "/healthz"),
   ("GET", "/growth-tokens.css"),
   ("GET", "/"),
}

DOC_UNAUTHENTICATED_STATIC_MOUNTS = {
   "/assets",
}


def _dependant_names_an_auth_check(dependant):
   is_auth_dependency = dependant.call in (current_session, current_user)

   if is_auth_dependency:
      return True

   return any(_dependant_names_an_auth_check(sub) for sub in dependant.dependencies)


def _api_routes(routes):
   """FastAPI wraps an included APIRouter as an internal _IncludedRouter rather than flattening
   its routes onto app.routes, so a plain app.routes scan misses every route this application
   defines; walk into original_router to reach the real APIRoute objects."""
   found = []

   for route in routes:
      if isinstance(route, APIRoute):
         found.append(route)
      elif hasattr(route, "original_router"):
         found.extend(_api_routes(route.original_router.routes))

   return found


def _unauthenticated_routes(app):
   found = set()

   for route in _api_routes(app.routes):
      requires_auth = _dependant_names_an_auth_check(route.dependant)

      if requires_auth:
         continue

      for method in route.methods - {"HEAD", "OPTIONS"}:
         found.add((method, route.path))

   return found


def _unauthenticated_static_mounts(app):
   """A Mount carries no dependant tree at all, so it cannot be walked for an auth dependency the
   way an APIRoute can; StaticFiles serves whatever file matches regardless of any cookie, so
   every Mount app.main adds is unauthenticated-reachable by construction."""
   found = set()

   for route in app.routes:
      if isinstance(route, Mount):
         found.add(route.path)

   return found


def test_unauthenticated_reachable_routes_match_the_documented_list(tmp_path):
   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db")}
   application = build_application(env)

   assert _unauthenticated_routes(application) == DOC_UNAUTHENTICATED_ROUTES
   assert _unauthenticated_static_mounts(application) == DOC_UNAUTHENTICATED_STATIC_MOUNTS
