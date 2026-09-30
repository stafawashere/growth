"""docs/agent/drawing-design.md, The screen: before an item is checked, a figure that shows the key in
any channel (a marked coordinate, a line's slope or intercept, an area, a Riemann total, a curve
equal to the key, a table cell, a label naming the key or its letter) is withheld, the verdict names
the channel and the element and never the value; a generic sketch passes; after submission only the
text checks run.
"""
import json
import re
import time
from pathlib import Path

import pytest

from app.agent.drawing.compile import compile_figure
from app.agent.drawing.spec import read_figure
from app.evals import agent_checks, figure_checks

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DESIGN_PATH = REPOSITORY_ROOT / "docs" / "agent" / "drawing-design.md"
AGENT_ITEM_PATH = REPOSITORY_ROOT / "content" / "items_unit06_agent" / "ITM-AGT-06002-00.json"
PRACTICE = {"mode": "practice", "turn_index": 1, "rules": (), "ids": ()}
AFTER_SUBMISSION = {"mode": "after_submission", "turn_index": 1, "rules": (), "ids": ()}
WINDOW = {"x": [-1, 4], "y": [-1, 10]}
CURVE = {"id": "f", "curve": "x^2", "role": "given", "label": "f"}
DESCRIPTION = "A figure built for the screen test, described in enough words to read."


def _figure(*elements, kind="graph", **fields):
   figure = {
      "kind": kind,
      "title": "A figure",
      "description": DESCRIPTION,
      "steps": [{"id": "only", "caption": "Everything at once", "add": list(elements)}],
      **fields,
   }

   if kind != "table":
      figure.setdefault("window", WINDOW)

   return figure


def _facts(figure):
   _spec, facts = compile_figure(read_figure(json.dumps(figure)))

   return facts


def _forms(answer_key=None, options=()):
   return agent_checks.key_forms({"answer_key": answer_key or {}, "options": list(options)})


def _screened(figure, forms, packet_facts=PRACTICE):
   return figure_checks.screen_figure(_facts(figure), packet_facts, forms)


def _design_figure():
   block = re.findall(r"```figure\n(.*?)```", DESIGN_PATH.read_text(), re.DOTALL)[0]

   return read_figure(block)


def _assert_withheld(verdict, check, *reason_parts, value_text=None):
   assert verdict.passed is False
   assert verdict.check == check

   for part in reason_parts:
      assert part in verdict.reason

   if value_text is not None:
      assert value_text not in verdict.reason


@pytest.mark.parametrize(
   "key, point",
   [(3.5, [1, 3.5]), (4, [4, 0]), (-0.25, [-0.25, 2])],
   ids=["decimal", "integer", "negative"],
)
def test_a_point_at_the_key_is_withheld(key, point):
   verdict = _screened(_figure({"id": "P", "point": point, "label": "P"}), _forms({"numeric": key}))

   _assert_withheld(verdict, "no_answer_in_figure", "marked coordinate", "(P)", value_text=str(key))


@pytest.mark.parametrize(
   "element",
   [
      pytest.param({"id": "t", "tangent": {"on": "f", "x": 1.5}}, id="tangent with the key slope"),
      pytest.param({"id": "t", "line": {"point": [2, 4], "slope": 0.5}}, id="line with the key intercept"),
   ],
)
def test_a_line_with_the_key_as_its_slope_or_intercept_is_withheld(element):
   verdict = _screened(_figure(CURVE, element), _forms({"numeric": 3}))

   _assert_withheld(verdict, "no_answer_in_figure", "slope or intercept", "(t)", value_text="3")


def test_a_label_that_states_the_key_is_withheld():
   forms = _forms({"mathjson": ["Rational", 145, 2]})
   verdict = _screened(_figure({"id": "P", "point": [1, 1], "label": "\\(72.5\\)"}), forms)

   _assert_withheld(verdict, "no_answer_before_submission", "label of P", value_text="72.5")


def test_a_shaded_region_whose_area_is_the_key_is_withheld():
   region = {"id": "A", "area": {"under": "f", "from": 0, "to": 3}, "label": "the region"}
   verdict = _screened(_figure(CURVE, region), _forms({"numeric": 9}))

   _assert_withheld(verdict, "no_answer_in_figure", "an area", "(A)", value_text="9")


def test_a_riemann_total_equal_to_the_key_is_withheld():
   riemann = {"id": "R", "riemann": {"on": "f", "from": 0, "to": 2, "n": 4, "rule": "left"}}
   verdict = _screened(_figure(CURVE, riemann), _forms({"numeric": 1.75}))

   _assert_withheld(verdict, "no_answer_in_figure", "approximation total", "(R)", value_text="1.75")


@pytest.mark.parametrize(
   "key, curve",
   [
      (["Add", ["Power", "x", 2], ["Multiply", 3, "x"]], "x(x + 3)"),
      (["Multiply", 3, ["Power", "t", 2]], "3x^2"),
      (["Divide", 1, ["Add", "x", 1]], "1/(x + 1)"),
   ],
   ids=["same polynomial", "key in t", "rational function"],
)
def test_a_curve_equal_to_the_key_expression_is_withheld(key, curve):
   verdict = _screened(_figure({"id": "g", "curve": curve}), _forms({"mathjson": key}))

   _assert_withheld(verdict, "no_answer_in_figure", "a curve", "(g)")


@pytest.mark.parametrize("curve", ["9^9^9^9", "x + 9^9^9^9", "x^(9^9^9)"])
def test_a_curve_with_a_tower_of_powers_is_screened_within_a_second(curve):
   forms = _forms({"mathjson": ["Add", ["Power", "x", 2], 1]})
   facts = _facts(_figure({"id": "g", "curve": curve}))
   started = time.monotonic()
   verdict = figure_checks.no_answer_in_figure(facts, PRACTICE, forms)
   elapsed = time.monotonic() - started

   assert verdict.passed is True
   assert elapsed < 1.0


def test_a_curve_that_differs_from_the_key_expression_passes():
   forms = _forms({"mathjson": ["Add", ["Power", "x", 2], ["Multiply", 3, "x"]]})

   assert _screened(_figure({"id": "g", "curve": "x^2 + 3x + 0.01"}), forms).passed is True


def test_a_table_cell_equal_to_the_key_is_withheld():
   table = _figure(
      {"id": "h", "highlight": {"row": 1}},
      kind="table",
      columns=["\\(x\\)", "\\(f(x)\\)"],
      rows=[["0", "1"], ["1", "3"], ["2", "7"]],
   )
   verdict = _screened(table, _forms({"numeric": 7}))

   _assert_withheld(verdict, "no_answer_in_figure", "a table cell", "(row 2, column 1)", value_text="7")


MCQ_OPTIONS = (
   {"id": "A", "is_key": False, "value": 3},
   {"id": "B", "is_key": False, "value": 5},
   {"id": "C", "is_key": True, "value": ["Rational", 7, 2]},
   {"id": "D", "is_key": False, "value": 6},
)


def test_a_label_naming_the_key_letter_is_withheld_on_a_multiple_choice_item():
   verdict = _screened(_figure({"id": "P", "point": [1, 1], "label": "Choice C"}), _forms(options=MCQ_OPTIONS))

   _assert_withheld(verdict, "no_answer_before_submission", "label of P", "letter")


def test_a_point_at_the_key_options_value_is_withheld_on_a_multiple_choice_item():
   verdict = _screened(_figure({"id": "P", "point": [3.5, 0]}), _forms(options=MCQ_OPTIONS))

   _assert_withheld(verdict, "no_answer_in_figure", "marked coordinate", "(P)", value_text="3.5")


def test_the_generic_secant_sketch_passes_on_an_item_whose_key_is_not_in_it():
   forms = agent_checks.key_forms(json.loads(AGENT_ITEM_PATH.read_text()))
   _spec, facts = compile_figure(_design_figure())

   assert forms.expression is not None
   assert figure_checks.screen_figure(facts, PRACTICE, forms).passed is True


def test_after_submission_only_the_text_checks_run():
   forms = _forms({"numeric": 3.5})
   leaking_point = _figure({"id": "P", "point": [1, 3.5]})
   praising_label = _figure({"id": "P", "point": [1, 3.5], "label": "Great"})

   assert _screened(leaking_point, forms).passed is False
   assert _screened(leaking_point, forms, AFTER_SUBMISSION).passed is True
   _assert_withheld(_screened(praising_label, forms, AFTER_SUBMISSION), "no_praise", "label of P")


def test_the_figure_well_formed_check_reports_the_refusal_reason():
   block = re.findall(r"```figure\n(.*?)```", DESIGN_PATH.read_text(), re.DOTALL)[0]

   assert figure_checks.figure_well_formed(block).passed is True
   assert figure_checks.figure_well_formed(block[:200]) == agent_checks.Verdict(False, "figure_well_formed", "malformed")
   assert figure_checks.figure_well_formed(block + " " * 2000).reason == "oversized"


def test_a_figure_on_a_closed_turn_fails_draws_only_when_open():
   assert figure_checks.draws_only_when_open("closed", True).passed is False
   assert figure_checks.draws_only_when_open("open", True).passed is True
   assert figure_checks.draws_only_when_open("closed", False).passed is True


def test_a_figure_whose_description_only_repeats_its_title_is_not_described():
   figure = _design_figure()

   assert figure_checks.figure_described(figure).passed is True
   assert figure_checks.figure_described({**figure, "description": figure["title"]}).passed is False
   assert figure_checks.figure_described({**figure, "description": "A curve."}).passed is False
