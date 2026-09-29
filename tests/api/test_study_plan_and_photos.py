"""The settings page's study plan (01's if-then plan) and its "Delete my FRQ photos" (08's settings
wireframe, Data)."""
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tests.api.conftest import world  # noqa: F401

STAMP = "2027-01-05T09:00:00+00:00"


def registered_user_id(world, client):  # noqa: F811
   return world.register(client).json()["user"]["id"]


def add_photo(engine, image_id, user_id, deleted_at=None):
   with OrmSession(engine) as db:
      db.add(
         models.FrqImage(
            id=image_id,
            attempt_id=f"ATT-{image_id}",
            user_id=user_id,
            media_type="image/png",
            data=b"page",
            width=10,
            height=10,
            sha256="0" * 64,
            quality="{}",
            accepted=1,
            deleted_at=deleted_at,
            created_at=STAMP,
            updated_at=STAMP,
         )
      )
      db.commit()


def photo(engine, image_id):
   with OrmSession(engine) as db:
      return db.get(models.FrqImage, image_id)


def test_the_study_plan_starts_empty_and_keeps_what_was_written(world):  # noqa: F811
   client = world.client()
   world.register(client)

   assert client.get("/settings/study-plan").json() == {"study_plan": None}

   written = client.put("/settings/study-plan", json={"study_plan": "  After breakfast, I work at my desk.  "})

   assert written.status_code == 200
   assert written.json() == {"study_plan": "After breakfast, I work at my desk."}
   assert client.get("/settings/study-plan").json() == {"study_plan": "After breakfast, I work at my desk."}


def test_an_empty_plan_clears_it_and_an_overlong_one_is_refused(world):  # noqa: F811
   client = world.client()
   world.register(client)
   client.put("/settings/study-plan", json={"study_plan": "After school, at the kitchen table."})

   overlong = client.put("/settings/study-plan", json={"study_plan": "x" * 281})
   not_text = client.put("/settings/study-plan", json={"study_plan": 3})

   assert (overlong.status_code, not_text.status_code) == (400, 400)
   assert client.get("/settings/study-plan").json() == {"study_plan": "After school, at the kitchen table."}

   cleared = client.put("/settings/study-plan", json={"study_plan": "   "})

   assert cleared.json() == {"study_plan": None}


def test_deleting_every_photo_drops_only_the_students_own_and_audits_each(world):  # noqa: F811
   client = world.client()
   user_id = registered_user_id(world, client)
   add_photo(world.engine, "IMG-1", user_id)
   add_photo(world.engine, "IMG-2", user_id)
   add_photo(world.engine, "IMG-3", user_id, deleted_at=STAMP)
   add_photo(world.engine, "IMG-9", "USER-someone-else")

   deleted = client.delete("/frq/photos")

   assert deleted.status_code == 200
   assert deleted.json() == {"deleted": 2}

   for own in ("IMG-1", "IMG-2"):
      assert photo(world.engine, own).data is None
      assert photo(world.engine, own).deleted_at is not None

   assert photo(world.engine, "IMG-9").data == b"page"

   with OrmSession(world.engine) as db:
      audited = db.query(models.AuditLog).filter(models.AuditLog.action == "frq_image_deleted").count()

   assert audited == 2


def test_the_new_settings_routes_need_a_session(world):  # noqa: F811
   client = world.client()

   assert client.get("/settings/study-plan").status_code == 401
   assert client.put("/settings/study-plan", json={"study_plan": "x"}).status_code == 401
   assert client.delete("/frq/photos").status_code == 401
