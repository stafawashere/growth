"""POST /purge beyond gate 24: a refused re-authentication still burns the token, and a real purge
after an export leaves neither the archive file nor its job behind (docs/plan/09-security-and-privacy.md).
"""
import json

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.db import models
from app.export.archive import archive_directory_for


def stored_reauth_hashes(engine, user_id):
   with OrmSession(engine) as db:
      return db.scalars(
         select(models.AuthSession.reauth_token_hash).where(models.AuthSession.user_id == user_id)
      ).all()


def test_a_wrong_purge_token_is_burned(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   token = world.reauth(client).json()["reauth_token"]

   assert any(stored_hash is not None for stored_hash in stored_reauth_hashes(world.engine, user_id))

   wrong = client.post(
      "/purge",
      json={"confirmation": PURGE_CONFIRMATION, "reauth_token": "not-the-token"},
   )

   assert wrong.status_code == 401
   assert stored_reauth_hashes(world.engine, user_id) == [None]

   replayed = client.post(
      "/purge",
      json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token},
   )

   assert replayed.status_code == 401
   assert world.purges.calls == []
   assert len(world.states(user_id)) > 0


def test_export_then_purge_leaves_no_archive_and_no_student_rows(world):
   world.settings.purge_hook = None
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   export_token = world.reauth(client).json()["reauth_token"]
   produced = client.post("/export", json={"reauth_token": export_token})

   assert produced.status_code == 200, produced.text

   with OrmSession(world.engine) as db:
      job = db.get(models.Job, produced.json()["id"])
      archive_path = archive_directory_for(world.engine) / json.loads(job.payload)["archive"]

   assert archive_path.is_file()

   purge_token = world.reauth(client).json()["reauth_token"]
   purged = client.post(
      "/purge",
      json={"confirmation": PURGE_CONFIRMATION, "reauth_token": purge_token},
   )

   assert purged.status_code == 200, purged.text
   assert not archive_path.exists()

   with OrmSession(world.engine) as db:
      assert db.scalars(select(models.Job).where(models.Job.type == "export")).all() == []
      assert db.get(models.User, user_id) is None
      assert db.scalars(select(models.SkillState).where(models.SkillState.user_id == user_id)).all() == []
      assert db.scalars(select(models.AuthSession).where(models.AuthSession.user_id == user_id)).all() == []