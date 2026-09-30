"""docs/agent/architecture.md, "The move": the app escalates, never the model.

Practice opens with a question, offers self-questions while the student keeps answering, and names
a rule or points to a section only after a turn the student did not answer. After submission the
moves follow plan 03's order, and the probe is asked only when a diagnosis wrote one.
"""
import re
from pathlib import Path

import pytest

from app.agent.moves import MOVES, choose_move, drawing_for

DRAWING_DESIGN_PATH = Path(__file__).resolve().parents[2] / "docs" / "agent" / "drawing-design.md"


@pytest.mark.parametrize(
   "turn_index, answered, expected",
   [
      (0, False, "ask_what_tried"),
      (0, True, "restate"),
      (1, True, "next_self_question"),
      (2, True, "next_self_question"),
      (1, False, "name_rule"),
      (2, False, "point_to_section"),
   ],
)
def test_practice_escalates_only_after_an_unanswered_turn(turn_index, answered, expected):
   assert choose_move("practice", turn_index, answered) == expected


def test_no_rule_or_section_before_an_unanswered_turn():
   telling_moves = {"name_rule", "point_to_section"}

   for turn_index in range(3):
      assert choose_move("practice", turn_index, True) not in telling_moves

   assert choose_move("practice", 0, False) not in telling_moves


def test_after_submission_runs_in_order_and_asks_the_probe_only_with_one():
   with_probe = [choose_move("after_submission", index, False, has_probe=True) for index in range(5)]
   without_probe = [choose_move("after_submission", index, False) for index in range(4)]

   assert with_probe == ["discuss_step", "name_point", "self_explanation_question", "probe", "discuss_step"]
   assert without_probe == ["discuss_step", "name_point", "self_explanation_question", "self_explanation_question"]


def test_browsing_explains_a_lesson_and_navigates_elsewhere():
   assert choose_move("browsing", 0, False, screen_kind="lesson") == "explain"
   assert choose_move("browsing", 0, False, screen_kind="session_lesson") == "explain"
   assert choose_move("browsing", 0, False, screen_kind="review") == "navigate"
   assert choose_move("browsing", 2, True, screen_kind="settings") == "navigate"


def test_every_chosen_move_is_in_the_vocabulary_and_an_unknown_mode_is_refused():
   for mode in ("practice", "after_submission", "browsing"):
      for turn_index in range(5):
         for answered in (False, True):
            assert choose_move(mode, turn_index, answered, has_probe=True, screen_kind="lesson") in MOVES

   with pytest.raises(ValueError):
      choose_move("grading", 0, False)


def design_drawing_table():
   """Move to open or closed, read from the table in drawing-design.md, When the tutor draws."""
   table = {}

   for line in DRAWING_DESIGN_PATH.read_text().splitlines():
      cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
      is_drawing_row = len(cells) == 4 and cells[2] in ("open", "closed")

      if is_drawing_row:
         for move in re.split(r",\s*", cells[1]):
            table[move] = cells[2]

   return table


def test_the_design_table_names_every_move():
   assert set(design_drawing_table()) == set(MOVES)


@pytest.mark.parametrize("move", MOVES)
def test_each_move_draws_as_the_design_table_says_and_the_switch_closes_every_move(move):
   assert drawing_for(move, True) == design_drawing_table()[move]
   assert drawing_for(move, False) == "closed"
