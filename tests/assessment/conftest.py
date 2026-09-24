"""An application built by app/main.py over a temporary database, with the generated item banks
written straight into the items table as published rows. Those banks were checked, re-solved and
signed off in stage 5 (docs/operator/p4-generation.md), so running every SymPy check again here
would only slow the suite; the ingestion path has its own tests."""
import glob
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.items.ingest import item_row
from tools import frq_scenarios

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATED_BANKS = str(REPO_ROOT / "content" / "items_gen_unit*" / "*.json")


def publish_generated_items(application):
   written_at = datetime.now(timezone.utc).isoformat()
   snapshot_id = application.state.settings.session_context.snapshot_id

   with OrmSession(application.state.engine) as db:
      for path in sorted(glob.glob(GENERATED_BANKS)):
         record = json.loads(Path(path).read_text())
         db.add(item_row(record, record["id"], snapshot_id, "verified", written_at))

      db.commit()


def skills_state_rows(application, user_id):
   """Every column of every skills_state row, so any change to any row shows."""
   with OrmSession(application.state.engine) as db:
      rows = db.scalars(select(models.SkillState).where(models.SkillState.user_id == user_id)).all()
      columns = [column.name for column in models.SkillState.__table__.columns]

      return {row.skill_id: tuple(getattr(row, column) for column in columns) for row in rows}


@pytest.fixture
def assessment_app(tmp_path):
   application = frq_scenarios.build(tmp_path / "growth.db", None)
   publish_generated_items(application)
   client = frq_scenarios.client_for(application)
   user_id = frq_scenarios.register(client)

   return application, client, user_id


def key_option_id(application, item_id):
   with OrmSession(application.state.engine) as db:
      row = db.get(models.Item, item_id)

      return next(option["id"] for option in row.options if option.get("is_key"))


def wrong_option_id(application, item_id):
   with OrmSession(application.state.engine) as db:
      row = db.get(models.Item, item_id)

      return next(option["id"] for option in row.options if not option.get("is_key"))


def answer_multiple_choice(application, client, kind, session_id, position, part, correct_every=2, visit_ms=45000):
   """Answers every question of an open multiple-choice part: every correct_every-th one right,
   the rest wrong."""
   for index, question in enumerate(part["questions"]):
      is_right = index % correct_every == 0
      item_id = question["item"]["id"]
      option_id = key_option_id(application, item_id) if is_right else wrong_option_id(application, item_id)
      saved = client.put(
         f"/{kind}/{session_id}/sections/{position}/questions/{question['number']}",
         json={"answer": {"option_id": option_id}, "visit_ms": visit_ms},
      )
      assert saved.status_code == 200, saved.text


def worked_read_back(record):
   """The question's own worked solution as the student's confirmed work, so the deterministic
   points have something correct to decide."""
   return {
      "parts": [
         {
            "part_id": part["id"],
            "lines": [
               {"kind": "math", "content": step["latex"], "crossed_out": False, "outside_box": False}
               for step in part["worked_solution"]
            ],
            "answer": part["answer_latex"],
         }
         for part in record["parts"]
      ],
      "unreadable": [],
   }


def session_part(payload, position):
   return next(part for part in payload["parts"] if part["position"] == position)
