"""docs/agent/architecture.md, Streaming end to end: the output screen and its checks.

Each check is shown failing on a sentence crafted to break it, sentences split only outside math
delimiters, and the first failing sentence is replaced by the fixed decline, after which nothing
more is released.
"""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.agent.context import compose_packet, question_key_forms
from app.agent.screen import SentenceScreen, decline_text, sentence_end
from app.content.loader import load_snapshot
from app.evals import agent_checks, golden
from app.runtime.context import DEFAULT_CONTENT_ROOT

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DESIGN_PATH = REPOSITORY_ROOT / "docs" / "agent" / "design.md"
ITEM_PATH = REPOSITORY_ROOT / "content" / "items_unit06_agent" / "ITM-AGT-06002-00.json"
EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)


@pytest.fixture(scope="module")
def item():
   return json.loads(ITEM_PATH.read_text())


@pytest.fixture(scope="module")
def practice_packet(item):
   context = golden.agent_context(load_snapshot(DEFAULT_CONTENT_ROOT))
   screen = {
      "kind": "session_item",
      "session_id": "SES-" + "0c" * 16,
      "attempt_id": "ATT-" + "0d" * 16,
      "item_id": item["id"],
      "format": "mcq",
      "served_stage": "unsupported",
      "submitted": False,
   }
   attempt = SimpleNamespace(submitted_at=None, served_stage="unsupported", format="mcq", correct=None)
   packet, _move = compose_packet(context, screen, item=item, attempt=attempt, lesson=golden.agent_lesson("LSN-CON-06003"))

   return packet


def screened(packet, item, text):
   screen = SentenceScreen(packet, agent_checks.key_forms(item))
   released = screen.feed(text) + screen.flush()

   return screen, released


@pytest.mark.parametrize(
   "sentence, check",
   [
      ("The sum comes to 72.5 liters.", "no_answer_before_submission"),
      ("It is \\( \\frac{290}{4} \\), once simplified.", "no_answer_before_submission"),
      ("That makes it option A.", "no_answer_before_submission"),
      ("Great work on the widths.", "no_praise"),
      ("You have the widths now!", "no_praise"),
      ("Review this tonight before the exam.", "no_study_advice"),
      ("This kind of sum shows up every year.", "no_prediction_talk"),
      ("The widths come first " + EM_DASH + " then the heights.", "no_dash"),
      ("The widths come first " + EN_DASH + " then the heights.", "no_dash"),
      ("Section LSN-CON-06003#s99 covers widths.", "cites_real_id"),
      ("BC-PT-99999 is the form point.", "cites_real_id"),
   ],
)
def test_each_check_withholds_a_sentence_crafted_to_break_it(practice_packet, item, sentence, check):
   screen, released = screened(practice_packet, item, sentence)

   assert screen.withheld is not None
   assert screen.withheld.check == check
   assert released == [screen.decline]


def test_a_clean_practice_sentence_is_released_unchanged(practice_packet, item):
   text = "What width does the first subinterval have, and where in the table do you read it? Section LSN-CON-06003#s6 names the cue."
   screen, released = screened(practice_packet, item, text)

   assert screen.withheld is None
   assert "".join(released) == text


def test_sentences_split_only_outside_math_delimiters(practice_packet, item):
   text = (
      "Compare \\( 3.5 \\cdot 2 \\) with \\( n! \\) here. "
      "Then \\[ f(x) = 1. \\] Is that the form? "
      "A blank line ends one too\n\nand this is the last"
   )
   screen = SentenceScreen(practice_packet, agent_checks.key_forms(item))
   released = []

   for character in text:
      released.extend(screen.feed(character))

   released.extend(screen.flush())

   assert released == [
      "Compare \\( 3.5 \\cdot 2 \\) with \\( n! \\) here.",
      " Then \\[ f(x) = 1. \\] Is that the form?",
      " A blank line ends one too\n\n",
      "and this is the last",
   ]
   assert sentence_end("Unclosed \\( x. y") is None


def test_a_withheld_sentence_yields_the_decline_and_stops(practice_packet, item):
   screen = SentenceScreen(practice_packet, agent_checks.key_forms(item))
   first = screen.feed("What did you try? The key is \\( \\frac{145}{2} \\). ")
   later = screen.feed("Anything after this is dropped. ")
   end = screen.flush()

   assert first == ["What did you try?", screen.decline]
   assert later == []
   assert end == []
   assert screen.withheld.check == "no_answer_before_submission"


def test_the_decline_is_the_design_copy_and_passes_every_check(practice_packet, item):
   design = DESIGN_PATH.read_text()
   row = next(line for line in design.splitlines() if line.startswith("| A reply the screen withheld |"))
   copy = row.split("|")[2].strip()
   decline = decline_text()
   facts = agent_checks.facts_from_packet(practice_packet)
   verdicts = agent_checks.run_checks(decline, facts, agent_checks.key_forms(item), agent_checks.SENTENCE_CHECKS)

   assert decline == copy
   assert all(verdict.passed for verdict in verdicts)


@pytest.fixture(scope="module")
def prediction_lesson():
   return golden.agent_lesson("LSN-CON-01006")


@pytest.fixture(scope="module")
def prediction_packet(prediction_lesson):
   context = golden.agent_context(load_snapshot(DEFAULT_CONTENT_ROOT))
   section = prediction_lesson.body["sections"][0]
   screen = {
      "kind": "lesson",
      "lesson_id": prediction_lesson.id,
      "version": prediction_lesson.version,
      "section_id": section["id"],
      "section_index": 0,
      "section_count": len(prediction_lesson.body["sections"]),
      "return_to": "/lessons",
   }
   packet, _move = compose_packet(context, screen, lesson=prediction_lesson)

   return packet


@pytest.mark.parametrize(
   "sentence",
   [
      "The limit is that height, 2.",
      "So the answer is B.",
   ],
)
def test_a_sentence_stating_the_prediction_key_is_withheld(prediction_packet, prediction_lesson, sentence):
   """The live walk's leak on LSN-CON-01006's prediction, whose keyed option B is labelled 2."""
   forms = question_key_forms(prediction_lesson.body["sections"][0])
   screen = SentenceScreen(prediction_packet, forms)
   released = screen.feed("Which height do both sides approach? " + sentence) + screen.flush()

   assert screen.withheld is not None
   assert screen.withheld.check == "no_answer_before_submission"
   assert released == ["Which height do both sides approach?", screen.decline]
