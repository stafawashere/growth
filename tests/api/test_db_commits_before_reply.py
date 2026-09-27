"""A write commits before its response is sent, because the client reads straight after it."""
import re
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2] / "app"


def test_every_database_dependency_ends_before_the_response_is_sent():
   declarations = []

   for path in sorted(APP_ROOT.rglob("*.py")):
      for match in re.finditer(r"Depends\(get_db[^)]*\)", path.read_text()):
         declarations.append((path.relative_to(APP_ROOT).as_posix(), match.group(0)))

   late = [entry for entry in declarations if 'scope="function"' not in entry[1]]

   assert len(declarations) > 50
   assert late == []
