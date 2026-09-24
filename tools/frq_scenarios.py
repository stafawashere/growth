"""Free-response flows driven through the real application, shared by the tests that replay them
and by tools/record_grading_cassettes.py, which records them once on the operator's subscription.

A flow is recorded and replayed with the same calls in the same order, so the requests match the
cassette book digest for digest. Editing a flow, a prompt template or a question record therefore
means recording again, and a replay that misses the book fails with CassetteMiss rather than
passing on a different answer.

The application is built by app/main.py build_application over a temporary database and the live
data/ registries; the only double is the passkey verifier, because a test process holds no
authenticator. Nothing here reads CLAUDE_CODE_OAUTH_TOKEN.
"""
import base64
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.main import build_application

PAGES_DIR = REPO_ROOT / "tests" / "fixtures" / "frq_pages"
CASSETTE_DIR = REPO_ROOT / "tests" / "fixtures" / "grading_cassettes"
CREDENTIAL_ID = b"frq-credential"
PAPER_TO_GRADE_BOOK = CASSETTE_DIR / "paper_to_grade.json"
PAPER_TO_GRADE_PAGE = PAGES_DIR / "critical_point_sign_change__clean.jpg"
PAPER_TO_GRADE_ITEM = "FRQ-AGT-05007-01"
PAPER_TO_GRADE_UNIT = "BC-UNIT-05"

# The student's own reading of part (b), which the flow types over whatever was read back. The
# page says exactly this, so the correction is the student fixing the read-back to their page.
PAPER_TO_GRADE_PART_B = [
   {"kind": "text", "content": "for \\(x < 3\\), \\(x - 3 < 0\\); for \\(x > 3\\), \\(x - 3 > 0\\)", "crossed_out": False, "outside_box": False},
   {"kind": "text", "content": "so \\(g\\) has a relative minimum at \\(x = 3\\)", "crossed_out": False, "outside_box": False},
]


class PasskeyDouble:
   def __init__(self, rp_id="localhost"):
      self.rp_id = rp_id

   def begin_registration(self, user_id, user_name, exclude_credential_ids=()):
      return {"challenge": "frq-registration", "options": {"rp": {"id": self.rp_id}, "user": {"id": user_id, "name": user_name}}}

   def finish_registration(self, challenge, credential):
      return {"credential_id": CREDENTIAL_ID, "public_key": b"frq-public-key", "sign_count": 1, "transports": None}

   def begin_login(self, credential_ids=None):
      return {"challenge": "frq-login", "options": {"rpId": self.rp_id}}

   def finish_login(self, challenge, credential, public_key, stored_sign_count):
      return {"sign_count": int(credential.get("sign_count", 0))}


def build(database_path, provider, extra_environment=None):
   environment = {
      "GROWTH_DB_PATH": str(database_path),
      "GROWTH_CONTENT_ROOT": str(REPO_ROOT / "data"),
      "GROWTH_AI_BACKEND": "none",
      "GROWTH_ITEMS_DIR": "none",
      "GROWTH_RNG_SEED": "7",
   }
   environment.update(extra_environment or {})
   application = build_application(environment)
   settings = application.state.settings
   settings.verifier = PasskeyDouble(settings.rp_id)
   settings.ai_provider = provider
   settings.grading_sleep = lambda seconds: None

   return application


def client_for(application):
   from starlette.testclient import TestClient

   return TestClient(application, client=("127.0.0.1", 40000), base_url="http://127.0.0.1")


def register(client):
   begun = client.post("/auth/passkey/register/begin", json={"display_name": "Student"})
   finished = client.post(
      "/auth/passkey/register/finish",
      json={"challenge_id": begun.json()["challenge_id"], "credential": {"credential_id": CREDENTIAL_ID.hex(), "sign_count": 1}},
   )

   if finished.status_code != 200:
      raise RuntimeError(f"registration failed: {finished.status_code} {finished.text}")

   return finished.json()["user"]["id"]


def photo_payload(path):
   return {"media_type": "image/jpeg", "data_base64": base64.b64encode(Path(path).read_bytes()).decode("ascii")}


def corrected_read_back(read_back):
   parts = []

   for part in read_back["parts"]:
      is_part_b = part["part_id"] == "b"
      lines = PAPER_TO_GRADE_PART_B if is_part_b else part["lines"]
      parts.append({"part_id": part["part_id"], "lines": lines, "answer": "" if is_part_b else part["answer"]})

   return {"parts": parts, "unreadable": []}


def paper_to_grade(client):
   """Print, photograph a fixture page, correct one part of the read-back, confirm, and read the
   per-point grading. Returns every response the test asserts on."""
   steps = {}
   opened = client.post("/frq/unit-checks", json={"unit_id": PAPER_TO_GRADE_UNIT, "item_id": PAPER_TO_GRADE_ITEM})
   steps["opened"] = opened
   session_id = opened.json()["session_id"]
   started = client.post(f"/sessions/{session_id}/frq/{PAPER_TO_GRADE_ITEM}/attempts", json={"capture_mode": "photo"})
   steps["started"] = started
   attempt_id = started.json()["attempt_id"]
   steps["booklet"] = client.get(f"/attempts/{attempt_id}/booklet.png")
   steps["uploaded"] = client.post(f"/attempts/{attempt_id}/images", json=photo_payload(PAPER_TO_GRADE_PAGE))
   steps["read_back"] = client.post(f"/attempts/{attempt_id}/transcription")
   read_back = steps["read_back"].json()["read_back"]
   corrected = corrected_read_back(read_back)
   steps["confirmed"] = client.post(
      f"/attempts/{attempt_id}/transcription/confirm",
      json={"read_back": corrected, "confidence": "confident"},
   )
   steps["gradings"] = client.get(f"/attempts/{attempt_id}/gradings")
   steps["review"] = client.get("/review", params={"today": date.today().isoformat()})
   steps["attempt_id"] = attempt_id
   steps["corrected"] = corrected

   return steps


def summary(steps):
   gradings = steps["gradings"].json()

   return json.dumps(
      {
         "read_back": steps["read_back"].json()["read_back"],
         "points": [
            {key: point[key] for key in ("point_id", "decided_by", "earned", "provisional", "rationale")}
            for point in gradings["points"]
         ],
         "earned": gradings["earned"],
         "decided": gradings["decided"],
         "provisional": gradings["provisional"],
      },
      indent=1,
   )
