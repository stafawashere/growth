"""POST /agent/turns with a figure in the reply (docs/agent/drawing-design.md, From block to screen,
Events and order, Storage, privacy and logs, and The switch; docs/agent/drawing-build-plan.md,
Slice 3).

The fake claude CLI streams a scripted reply in chunks of a few characters (stream_script), so the
figure fence and the step markers arrive split across deltas as a live stream splits them. A
browsing screen is on the navigate move, which draws; the practice item is on ask_what_tried at its
first turn, which does not, and on name_rule at a second turn the student did not answer, which
does. Every stored row is read back from the database, never from the response.
"""
import json
import logging
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from sqlalchemy.orm import Session as OrmSession

from app.agent.screen import decline_text
from app.api.routes.purge import PURGE_CONFIRMATION
from app.db import models
from app.main import agent_drawing_enabled
from tests.api.test_agent_turn import (
   MARKER,
   agent,
   agent_turns,
   cli,
   names_of,
   no_paid_api,
   post_turn,
   practice,
   rows_of,
   signed_in,
   withheld_rows,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
RENDER_SCHEMA = json.loads((REPOSITORY_ROOT / "schemas" / "agent" / "figure_render.schema.json").read_text())
TODAY_SCREEN = {"kind": "today"}
REFUSED_COPY = "The figure for this reply could not be drawn."
FIGURE = {
   "kind": "graph",
   "title": "Secant to tangent",
   "window": {"x": [-1, 4], "y": [-1, 9]},
   "description": "The curve y equals x squared, a secant through two of its points, and the tangent at the first point.",
   "steps": [
      {"id": "curve", "caption": "The curve", "add": [{"id": "f", "curve": "x^2", "role": "given"}]},
      {
         "id": "secant",
         "caption": "A secant through P and Q",
         "add": [{"id": "P", "point": {"on": "f", "x": 1}, "label": "P"}, {"id": "s", "secant": {"on": "f", "x": [1, 3]}}],
      },
      {"id": "tangent", "caption": "The tangent at P", "fade": ["s"], "add": [{"id": "t", "tangent": {"on": "f", "x": 1}}]},
   ],
}


def fenced(figure):
   text = figure if isinstance(figure, str) else json.dumps(figure)

   return f"```figure\n{text}\n```\n"


def scripted(cli, reply, chunk=7):
   cli.mode("stream_script")
   (cli.home / "fake_claude_stream_text.txt").write_text(reply)
   (cli.home / "fake_claude_chunk").write_text(str(chunk))


def events_named(events, name):
   return [data for event_name, data in events if event_name == name]


def texts(events):
   return "".join(data["delta"] for name, data in events if name == "text")


MARKED_REPLY = (
   "Here is a sketch of the idea.\n"
   + fenced(FIGURE)
   + "[[step:curve]] Start with the curve. "
   + "Then join two points. [[step:secant]] That line is a secant. "
   + "The tangent is where such lines end up."
)


@pytest.mark.parametrize("chunk", [1, 7, 60])
def test_the_figure_and_its_steps_arrive_in_order_before_their_sentences(agent, cli, chunk):
   client, _user_id = signed_in(agent)
   scripted(cli, MARKED_REPLY, chunk)
   _response, events = post_turn(client, TODAY_SCREEN, message="Can you sketch a tangent?")
   figure = events_named(events, "figure")[0]
   steps = [(data["figure"], data["step"]) for data in events_named(events, "figure_step")]
   step_positions = {data["step"]: index for index, (name, data) in enumerate(events) if name == "figure_step"}
   text_positions = {data["delta"].strip(): index for index, (name, data) in enumerate(events) if name == "text"}

   assert names_of(events)[:4] == ["start", "text", "text", "figure_pending"]
   assert names_of(events)[4] == "figure"
   assert names_of(events)[-2:] == ["figure_step", "end"]
   assert steps == [(figure["id"], "curve"), (figure["id"], "secant"), (figure["id"], "tangent")]
   assert step_positions["curve"] == text_positions["Start with the curve."] - 1
   assert step_positions["secant"] == text_positions["That line is a secant."] - 1
   assert step_positions["tangent"] > text_positions["The tangent is where such lines end up."]
   assert "[[step" not in texts(events)
   assert list(Draft202012Validator(RENDER_SCHEMA).iter_errors(figure)) == []
   assert events[-1][1]["outcome"] == "complete"


def test_the_shown_figure_is_stored_with_its_spec_and_steps_and_logged_by_outcome_only(agent, cli, caplog):
   caplog.set_level(logging.DEBUG)
   client, _user_id = signed_in(agent)
   scripted(cli, MARKED_REPLY)
   _response, events = post_turn(client, TODAY_SCREEN, message="Can you sketch a tangent?")
   reply = agent_turns(agent, "agent")[0]
   turn_lines = [record.getMessage() for record in caplog.records if record.name == "app.agent.turn"]

   assert reply.figure == {"spec": FIGURE, "outcome": "shown", "revealed": 3}
   assert reply.text == texts(events)
   assert any(reply.id in line and "figure=shown steps=3" in line for line in turn_lines)


def test_a_later_turn_sends_the_shown_figure_to_the_model_as_one_line(agent, cli):
   client, _user_id = signed_in(agent)
   scripted(cli, MARKED_REPLY)
   _response, first = post_turn(client, TODAY_SCREEN, message="Can you sketch a tangent?")
   cli.mode("stream")
   post_turn(client, TODAY_SCREEN, message="And then?", conversation_id=first[0][1]["conversation_id"])
   prompt = cli.record()["stdin"]
   expected_line = f"[Figure shown: {FIGURE['title']}. {FIGURE['description']}]"

   assert json.dumps(expected_line)[1:-1] in prompt
   assert '"steps"' not in prompt.split("Conversation so far:")[1]
   assert "Drawing: open" in prompt


LEAKING_FIGURE = {
   "kind": "graph",
   "title": "The line to look at",
   "window": {"x": [-2, 3], "y": [-3, 7]},
   "description": f"The line through two points of the plane, labelled {MARKER} for the log check.",
   "steps": [
      {
         "id": "line",
         "caption": "The line",
         "add": [
            {"id": "g", "curve": "(4x + 2)/2", "label": MARKER},
            {"id": "h", "curve": "x^3/7.3891"},
         ],
      },
   ],
}


def second_practice_turn(agent, cli, reply):
   """The first turn on the item is ask_what_tried; a question in reply to the tutor's question
   leaves it unanswered, so the second turn is name_rule, which draws."""
   client, user_id, screen = practice(agent)
   cli.mode("stream")
   _response, first = post_turn(client, screen)
   scripted(cli, reply)
   _response, events = post_turn(client, screen, message="What rule is that?", conversation_id=first[0][1]["conversation_id"])

   return user_id, events


def test_a_figure_that_shows_the_key_withholds_the_reply(agent, cli):
   user_id, events = second_practice_turn(agent, cli, "Think about the line.\n" + fenced(LEAKING_FIGURE) + "More words after it.")
   reply = agent_turns(agent, "agent")[-1]
   audit = withheld_rows(agent)

   assert names_of(events) == ["start", "text", "text", "figure_pending", "text", "end"]
   assert events[4][1] == {"delta": f" {decline_text()}"}
   assert events[-1][1]["outcome"] == "withheld"
   assert "More words" not in texts(events)
   assert reply.outcome == "withheld"
   assert reply.figure == {"spec": None, "outcome": "withheld", "revealed": 0}
   assert len(audit) == 1
   assert audit[0].actor == user_id
   assert json.loads(audit[0].detail) == {
      "check": "no_answer_in_figure",
      "turn_id": reply.id,
      "day": json.loads(audit[0].detail)["day"],
      "part": "figure",
   }


def test_a_marked_label_and_expression_reach_no_log_record_and_no_audit_detail(agent, cli, caplog):
   caplog.set_level(logging.DEBUG)
   _user_id, events = second_practice_turn(agent, cli, "Think about the line.\n" + fenced(LEAKING_FIGURE))
   needles = (MARKER, "7.3891", "(4x + 2)/2")

   assert events[-1][1]["outcome"] == "withheld"
   assert len(withheld_rows(agent)) == 1

   for record in caplog.records:
      for needle in needles:
         assert needle not in record.getMessage()
         assert needle not in repr(record.args)

   for row in rows_of(agent, models.AuditLog):
      for needle in needles:
         assert needle not in (row.detail or "")
         assert needle not in (row.subject or "")

   turn_lines = [record.getMessage() for record in caplog.records if record.name == "app.agent.turn"]

   assert any("outcome=withheld" in line and "figure=withheld steps=0" in line for line in turn_lines)


@pytest.mark.parametrize(
   "block, reason",
   [
      ("{not json", "malformed"),
      (json.dumps(dict(FIGURE, description="d" * 401)), "oversized"),
      (json.dumps(FIGURE) + " " * 2000, "oversized"),
   ],
   ids=["malformed", "over a length cap", "over 2000 characters"],
)
def test_a_block_that_cannot_be_drawn_is_refused_and_the_text_goes_on(agent, cli, block, reason):
   client, _user_id = signed_in(agent)
   scripted(cli, "Before it.\n" + fenced(block) + "After the figure.")
   _response, events = post_turn(client, TODAY_SCREEN, message="Draw it?")

   assert events_named(events, "figure_refused") == [{"reason": reason, "copy": REFUSED_COPY}]
   assert events_named(events, "figure") == []
   assert texts(events).endswith("After the figure.")
   assert events[-1][1]["outcome"] == "complete"
   assert agent_turns(agent, "agent")[0].figure == {"spec": None, "outcome": f"refused:{reason}", "revealed": 0}


def test_a_figure_on_a_turn_whose_move_does_not_draw_is_refused_closed(agent, cli):
   client, _user_id, screen = practice(agent)
   scripted(cli, "What did you try?\n" + fenced(FIGURE) + "Tell me first.")
   _response, events = post_turn(client, screen)

   assert names_of(events)[:5] == ["start", "text", "text", "figure_pending", "figure_refused"]
   assert events[4][1] == {"reason": "closed", "copy": REFUSED_COPY}
   assert events_named(events, "figure") == []
   assert texts(events).endswith("Tell me first.")
   assert agent_turns(agent, "agent")[0].figure["outcome"] == "refused:closed"


def test_with_the_switch_off_every_turn_is_closed_and_a_figure_is_refused_off(agent, cli):
   agent.settings.agent_drawing = False
   client, _user_id = signed_in(agent)
   scripted(cli, "Here.\n" + fenced(FIGURE) + "After.")
   _response, events = post_turn(client, TODAY_SCREEN, message="Draw it?")

   assert events_named(events, "figure_refused") == [{"reason": "off", "copy": REFUSED_COPY}]
   assert events_named(events, "figure") == []
   assert "Drawing: closed" in cli.record()["stdin"]


def test_an_unclosed_block_and_a_second_block_are_refused(agent, cli):
   client, _user_id = signed_in(agent)
   scripted(cli, "One.\n" + fenced(FIGURE) + "Two.\n" + fenced(FIGURE) + "Three.\n```figure\n{")
   _response, events = post_turn(client, TODAY_SCREEN, message="Draw it?")

   assert len(events_named(events, "figure")) == 1
   assert [data["reason"] for data in events_named(events, "figure_refused")] == ["extra", "extra"]

   scripted(cli, "One.\n```figure\n" + json.dumps(FIGURE))
   _response, unclosed = post_turn(client, TODAY_SCREEN, message="Again?")

   assert [data["reason"] for data in events_named(unclosed, "figure_refused")] == ["unclosed"]


def test_the_drawing_switch_reads_on_by_default_and_refuses_any_other_value():
   assert agent_drawing_enabled({}) is True
   assert agent_drawing_enabled({"GROWTH_AGENT_DRAWING": "off"}) is False

   with pytest.raises(ValueError):
      agent_drawing_enabled({"GROWTH_AGENT_DRAWING": "maybe"})


def test_a_turn_with_a_figure_is_exported_and_then_purged(agent, cli):
   agent.settings.purge_hook = None
   client, user_id = signed_in(agent)
   scripted(cli, MARKED_REPLY)
   post_turn(client, TODAY_SCREEN, message="Can you sketch a tangent?")
   export_token = agent.reauth(client).json()["reauth_token"]
   produced = client.post("/export", json={"reauth_token": export_token})
   exported = client.get(f"/export/{produced.json()['id']}").json()
   exported_figures = [row["figure"] for row in exported["tables"]["agent_turns"] if row["role"] == "agent"]
   purge_token = agent.reauth(client).json()["reauth_token"]
   purged = client.post("/purge", json={"confirmation": PURGE_CONFIRMATION, "reauth_token": purge_token})

   assert exported_figures == [{"spec": FIGURE, "outcome": "shown", "revealed": 3}]
   assert purged.status_code == 200

   with OrmSession(agent.engine) as db:
      assert db.query(models.AgentTurn).filter(models.AgentTurn.user_id == user_id).count() == 0


def test_the_settings_view_names_a_shown_figure_under_its_turn(agent, cli):
   client, _user_id = signed_in(agent)
   scripted(cli, MARKED_REPLY)
   _response, events = post_turn(client, TODAY_SCREEN, message="Can you sketch a tangent?")
   opened = client.get(f"/agent/conversations/{events[0][1]['conversation_id']}").json()

   assert [(turn["role"], turn["figure_title"]) for turn in opened["turns"]] == [("student", None), ("agent", FIGURE["title"])]
