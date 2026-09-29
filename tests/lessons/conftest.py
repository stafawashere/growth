import json
from pathlib import Path

import pytest

from app.content.loader import load_snapshot
from tools.check_lessons import Context

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "lessons"
HAND_AUTHORED = REPO_ROOT / "content" / "lessons" / "LSN-CON-02013.json"


@pytest.fixture(scope="session")
def snapshot():
   return load_snapshot(REPO_ROOT / "data")


@pytest.fixture(scope="session")
def context(snapshot):
   return Context(snapshot)


@pytest.fixture()
def hand_authored():
   return json.loads(HAND_AUTHORED.read_text())


def load_fixture(name):
   return json.loads((FIXTURE_DIR / name).read_text())
