"""The Tutor tab's routes (docs/agent/architecture.md, "The panel and the settings views";
docs/agent/design.md, "Memory in settings").

Every change is checked by reading the database, not the response. Every audit row the routes write
is read back and must carry ids and counts and none of the text it concerns. The installation
holds one account, so another user's rows are written straight into the database, and the signed
in student must neither see nor change them.
"""
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.agent import conversations
from app.auth.service import as_iso
from app.db import models

INTRUDER_ID = "USR-intruder"
MARKER = "MARKERTEXT"
AGENT_AUDIT_ACTIONS = (
   "agent_memory_deleted",
   "agent_memory_edited",
   "agent_memory_cleared",
   "agent_conversation_deleted",
   "agent_memory_paused",
   "agent_memory_resumed",
)


def signed_in(world):
   client = world.client()
   world.register(client)

   with OrmSession(world.engine) as db:
      user_id = db.scalars(select(models.User.id)).one()

   return client, user_id


def add_memory(world, user_id, memory_id, kind, text, **extra):
   stamp = as_iso(datetime.now(timezone.utc))

   with OrmSession(world.engine) as db:
      db.add(
         models.TutorMemory(
            id=memory_id,
            user_id=user_id,
            kind=kind,
            text=text,
            skill_ids=["BC-SKL-0601"],
            source="conversation",
            source_conversation_id="ACV-source",
            evidence_count=1,
            last_confirmed_at=stamp,
            created_at=stamp,
            updated_at=stamp,
            **extra,
         )
      )
      db.commit()


def add_conversation(world, user_id, turn_texts):
   now = datetime.now(timezone.utc)

   with OrmSession(world.engine) as db:
      conversation = conversations.open_conversation(db, user_id, "session_item", now)

      for index, text in enumerate(turn_texts):
         role = "student" if index % 2 == 0 else "agent"
         conversations.append_turn(db, conversation, role, text, now, screen={"kind": "session_item"})

      db.commit()

      return conversation.id


def memory_row(world, memory_id):
   with OrmSession(world.engine) as db:
      return db.get(models.TutorMemory, memory_id)


def audit_rows(world, action):
   with OrmSession(world.engine) as db:
      return db.scalars(select(models.AuditLog).where(models.AuditLog.action == action)).all()


def rows_of(world, model, user_id):
   with OrmSession(world.engine) as db:
      return db.scalars(select(model).where(model.user_id == user_id)).all()


def test_the_routes_need_a_session(world):
   client = world.client()

   assert client.get("/agent/memories").status_code == 401
   assert client.get("/agent/settings").status_code == 401
   assert client.request("DELETE", "/agent/memories", json={"confirmation": "forget everything"}).status_code == 401


def test_memories_are_listed_by_kind_with_the_plain_labels(world):
   client, user_id = signed_in(world)
   add_memory(world, user_id, "MEM-pref", "preference", "Likes a sketch first")
   add_memory(world, user_id, "MEM-conf", "confusion", "Unsure which quantity is changing")
   add_memory(world, user_id, "MEM-epi", "episode", "Talked through a volume setup")
   add_memory(world, user_id, "MEM-gone", "preference", None, deleted_at=as_iso(datetime.now(timezone.utc)))
   add_memory(world, INTRUDER_ID, "MEM-theirs", "preference", "Someone else entirely")

   body = client.get("/agent/memories").json()
   labels = [(group["kind"], group["label"]) for group in body["groups"]]
   listed = {entry["id"]: entry for group in body["groups"] for entry in group["entries"]}

   assert labels == [
      ("preference", "How you like to be helped"),
      ("confusion", "Confusions in your words"),
      ("stated_difficulty", "What you said was hard"),
      ("episode", "Last conversation"),
   ]
   assert set(listed) == {"MEM-pref", "MEM-conf", "MEM-epi"}
   assert listed["MEM-pref"]["editable"] is True
   assert listed["MEM-conf"]["editable"] is True
   assert listed["MEM-epi"]["editable"] is False
   assert listed["MEM-pref"]["source_conversation_id"] == "ACV-source"
   assert body["memory_paused"] is False


def test_an_edit_marks_the_entry_and_audits_without_the_text(world):
   client, user_id = signed_in(world)
   add_memory(world, user_id, "MEM-pref", "preference", "Likes a sketch first")
   add_memory(world, user_id, "MEM-epi", "episode", "Talked through a volume setup")

   edited = client.put("/agent/memories/MEM-pref", json={"text": f"Wants a sketch then one line {MARKER}"})
   refused_kind = client.put("/agent/memories/MEM-epi", json={"text": "Changed"})
   refused_length = client.put("/agent/memories/MEM-pref", json={"text": "z" * 201})
   row = memory_row(world, "MEM-pref")
   audits = audit_rows(world, "agent_memory_edited")

   assert edited.status_code == 200
   assert refused_kind.status_code == 400
   assert refused_length.status_code == 400
   assert row.text == f"Wants a sketch then one line {MARKER}"
   assert row.edited_by_student == 1
   assert memory_row(world, "MEM-epi").text == "Talked through a volume setup"
   assert len(audits) == 1
   assert MARKER not in audits[0].detail
   assert json.loads(audits[0].detail) == {"memory_id": "MEM-pref"}


def test_forget_this_leaves_a_tombstone_and_audits_without_the_text(world):
   client, user_id = signed_in(world)
   add_memory(world, user_id, "MEM-pref", "preference", f"Likes a sketch first {MARKER}")

   response = client.delete("/agent/memories/MEM-pref")
   row = memory_row(world, "MEM-pref")
   audits = audit_rows(world, "agent_memory_deleted")

   assert response.status_code == 200
   assert row.text is None
   assert row.deleted_at is not None
   assert row.kind == "preference"
   assert row.skill_ids == ["BC-SKL-0601"]
   assert client.delete("/agent/memories/MEM-pref").status_code == 404
   assert len(audits) == 1
   assert MARKER not in audits[0].detail


def test_forget_everything_needs_the_typed_phrase(world):
   client, user_id = signed_in(world)
   add_memory(world, user_id, "MEM-pref", "preference", "Likes a sketch first")
   add_memory(world, user_id, "MEM-gone", "preference", None, deleted_at=as_iso(datetime.now(timezone.utc)))
   add_memory(world, INTRUDER_ID, "MEM-theirs", "preference", "Someone else entirely")
   add_conversation(world, user_id, [f"What is this asking {MARKER}", "What have you tried so far?"])
   add_conversation(world, INTRUDER_ID, ["Their question"])

   missing = client.request("DELETE", "/agent/memories", json={})
   wrong = client.request("DELETE", "/agent/memories", json={"confirmation": "forget"})
   kept_after_refusals = len(rows_of(world, models.TutorMemory, user_id))
   cleared = client.request("DELETE", "/agent/memories", json={"confirmation": "forget everything"})
   audits = audit_rows(world, "agent_memory_cleared")

   assert missing.status_code == 400
   assert wrong.status_code == 400
   assert kept_after_refusals == 2
   assert cleared.status_code == 200
   assert rows_of(world, models.TutorMemory, user_id) == []
   assert rows_of(world, models.AgentTurn, user_id) == []
   assert rows_of(world, models.AgentConversation, user_id) == []
   assert len(rows_of(world, models.TutorMemory, INTRUDER_ID)) == 1
   assert len(rows_of(world, models.AgentConversation, INTRUDER_ID)) == 1
   assert len(audits) == 1
   assert MARKER not in audits[0].detail
   assert json.loads(audits[0].detail)["tutor_memories"] == 2


def test_conversations_are_listed_read_and_deleted(world):
   client, user_id = signed_in(world)
   conversation_id = add_conversation(world, user_id, [f"What is this asking {MARKER}", "What have you tried so far?"])
   theirs = add_conversation(world, INTRUDER_ID, ["Their question"])

   listed = client.get("/agent/conversations").json()["conversations"]
   opened = client.get(f"/agent/conversations/{conversation_id}").json()

   assert [entry["id"] for entry in listed] == [conversation_id]
   assert listed[0]["turn_count"] == 2
   assert listed[0]["opened_on_screen"] == "session_item"
   assert [turn["role"] for turn in opened["turns"]] == ["student", "agent"]
   assert client.get(f"/agent/conversations/{theirs}").status_code == 404
   assert client.delete(f"/agent/conversations/{theirs}").status_code == 404

   deleted = client.delete(f"/agent/conversations/{conversation_id}")
   audits = audit_rows(world, "agent_conversation_deleted")

   assert deleted.status_code == 200
   assert rows_of(world, models.AgentTurn, user_id) == []
   assert rows_of(world, models.AgentConversation, user_id) == []
   assert len(rows_of(world, models.AgentTurn, INTRUDER_ID)) == 1
   assert len(audits) == 1
   assert MARKER not in audits[0].detail
   assert json.loads(audits[0].detail) == {"conversation_id": conversation_id, "turns_deleted": 2}


def test_pause_and_resume_are_stored_and_audited(world):
   client, user_id = signed_in(world)

   paused = client.put("/agent/settings", json={"memory_paused": True})

   with OrmSession(world.engine) as db:
      paused_flag = db.get(models.User, user_id).agent_memory_paused

   resumed = client.put("/agent/settings", json={"memory_paused": False})

   with OrmSession(world.engine) as db:
      resumed_flag = db.get(models.User, user_id).agent_memory_paused

   refused = client.put("/agent/settings", json={"memory_paused": "yes"})

   assert paused.json() == {"memory_paused": True}
   assert paused_flag == 1
   assert resumed.json() == {"memory_paused": False}
   assert resumed_flag == 0
   assert refused.status_code == 400
   assert client.get("/agent/settings").json() == {"memory_paused": False}
   assert len(audit_rows(world, "agent_memory_paused")) == 1
   assert len(audit_rows(world, "agent_memory_resumed")) == 1


def test_another_users_entries_cannot_be_edited_or_deleted(world):
   client, _ = signed_in(world)
   add_memory(world, INTRUDER_ID, "MEM-theirs", "preference", "Someone else entirely")

   assert client.put("/agent/memories/MEM-theirs", json={"text": "Mine now"}).status_code == 404
   assert client.delete("/agent/memories/MEM-theirs").status_code == 404

   row = memory_row(world, "MEM-theirs")

   assert row.text == "Someone else entirely"
   assert row.deleted_at is None
   assert row.edited_by_student == 0


def test_the_profile_is_the_highest_version_and_the_switch_is_absent(world):
   client, user_id = signed_in(world)
   empty = client.get("/agent/profile").json()
   stamp = as_iso(datetime.now(timezone.utc))

   with OrmSession(world.engine) as db:
      for version in (1, 2):
         db.add(
            models.TutorProfile(
               user_id=user_id,
               version=version,
               body={"turn_length": f"band_{version}"},
               evidence={},
               created_at=stamp,
               updated_at=stamp,
            )
         )

      db.commit()

   current = client.get("/agent/profile").json()

   assert empty == {"profile": None, "version": None, "experiment": "absent"}
   assert current == {"profile": {"turn_length": "band_2"}, "version": 2, "experiment": "absent"}


def test_no_agent_audit_row_carries_text(world):
   client, user_id = signed_in(world)
   add_memory(world, user_id, "MEM-pref", "preference", f"Likes a sketch first {MARKER}")
   add_memory(world, user_id, "MEM-conf", "confusion", f"Unsure which quantity {MARKER}")
   conversation_id = add_conversation(world, user_id, [f"Question {MARKER}"])

   client.put("/agent/memories/MEM-conf", json={"text": f"Edited {MARKER}"})
   client.delete("/agent/memories/MEM-pref")
   client.delete(f"/agent/conversations/{conversation_id}")
   client.put("/agent/settings", json={"memory_paused": True})
   client.put("/agent/settings", json={"memory_paused": False})
   client.request("DELETE", "/agent/memories", json={"confirmation": "forget everything"})

   written = [row for action in AGENT_AUDIT_ACTIONS for row in audit_rows(world, action)]

   assert {row.action for row in written} == set(AGENT_AUDIT_ACTIONS)
   assert all(MARKER not in (row.detail or "") for row in written)
