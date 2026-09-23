"""The client's production build, run from the operator's pytest suite.

No numbered gate of docs/plan/11-phased-delivery.md runs the client build, which is how an
app/web/index.html naming an entry module that did not exist survived review. This module runs
`npm run build` and reads the emitted bundle, so a client that cannot be served, or one whose
motion stylesheet no module imports, fails here rather than in a browser.

There is no skip: a client that is not installed is a build that cannot be shown to succeed,
which is a failure, and that is the same stance tests/web/test_reduced_motion.py takes.
"""
import re
import shutil
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent

CLIENT_ROOT = REPOSITORY_ROOT / "app" / "web"

DIST_ROOT = CLIENT_ROOT / "dist"

ENTRY_HTML = CLIENT_ROOT / "index.html"

MOTION_STYLESHEET = CLIENT_ROOT / "src" / "styles" / "motion.css"

# The bundle build, not `npm run build`, which prefixes the same build with a whole-project type
# check. A type error in a module the bundle never loads is a real defect, but it is tsc's
# report to make, and routing it through this module would read as a client that cannot be served.
BUILD_SCRIPT = "build:bundle"

MOTION_CLASS = re.compile(r"^\.(motion-[a-z0-9-]+)", re.MULTILINE)

# No plan document fixes a wall-clock budget for a client build, so this ceiling is an
# operational guard against a hung subprocess and not a specified value.
BUILD_TIMEOUT_SECONDS = 600


def declared_motion_classes():
   """The class selectors motion.css itself declares, read out of the stylesheet rather than
   copied into this module, so a class renamed or removed there is caught here."""
   return sorted({match.group(1) for match in MOTION_CLASS.finditer(MOTION_STYLESHEET.read_text())})


def run_build():
   command = ["npm", "run", BUILD_SCRIPT]

   return subprocess.run(
      command,
      cwd=CLIENT_ROOT,
      capture_output=True,
      text=True,
      timeout=BUILD_TIMEOUT_SECONDS,
   )


def built_stylesheet_text():
   assets = sorted(DIST_ROOT.rglob("*.css"))

   return "\n".join(asset.read_text() for asset in assets)


def test_client_production_build_emits_a_servable_bundle():
   npm_is_installed = shutil.which("npm") is not None
   client_is_installed = (CLIENT_ROOT / "node_modules").is_dir()

   assert npm_is_installed, "npm is not on PATH, so the client build cannot be shown to succeed"
   assert client_is_installed, (
      f"{CLIENT_ROOT}/node_modules is absent, so the client build cannot be shown to succeed"
   )

   expected_classes = declared_motion_classes()

   assert expected_classes, (
      f"{MOTION_STYLESHEET} declares no motion class, so a built stylesheet would prove nothing"
   )

   shutil.rmtree(DIST_ROOT, ignore_errors=True)

   completed = run_build()

   assert completed.returncode == 0, (
      f"npm run {BUILD_SCRIPT} exited {completed.returncode}:\n"
      f"{completed.stdout}\n{completed.stderr}"
   )

   built_page = DIST_ROOT / "index.html"

   assert built_page.is_file(), (
      f"the build wrote no {built_page}:\n{completed.stdout}\n{completed.stderr}"
   )

   page_text = built_page.read_text()
   entry_was_bundled = "/src/main.tsx" not in page_text
   page_loads_a_module = "<script" in page_text and "type=\"module\"" in page_text

   assert entry_was_bundled, (
      "the built page still points at the source entry module, so nothing was bundled:\n"
      f"{page_text}"
   )
   assert page_loads_a_module, f"the built page loads no module script:\n{page_text}"

   stylesheet_text = built_stylesheet_text()

   assert stylesheet_text, (
      "the build emitted no stylesheet, so nothing imports the motion stylesheet:\n"
      f"{completed.stdout}"
   )

   missing_classes = [name for name in expected_classes if name not in stylesheet_text]

   assert missing_classes == [], (
      f"these classes of {MOTION_STYLESHEET.name} are absent from the built stylesheet, so no "
      f"module imports it and no browser would load it: {missing_classes}"
   )
