"""docs/agent/drawing-design.md, Marks on the page, and the marks contract in
docs/agent/drawing-build-plan.md: every mark reads against the turn's anchors and compiles to the
render marks, lines and guides clipped to the item graph's window; a quote not in its anchor, an
unlisted anchor, a point outside the window, a row outside the table and a strike before checking
each refuse; an option anchor before checking is read so the screen can withhold it.
"""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from app.agent.drawing.marks import compile_marks, read_marks
from app.agent.drawing.spec import FigureRefused

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RENDER_SCHEMA = json.loads((REPOSITORY_ROOT / "schemas" / "agent" / "marks_render.schema.json").read_text())
STEM = "The function f is continuous on the closed interval [0, 4], and its graph is shown.\nFind the average rate of change."
PRACTICE_ANCHORS = [
   {"id": "stem", "kind": "text", "text": STEM},
   {"id": "item_figure", "kind": "graph", "window": {"x": [-1, 5], "y": [-2, 6]}},
]
CHECKED_ANCHORS = [
   {"id": "stem", "kind": "text", "text": STEM},
   {"id": "item_table", "kind": "table", "rows": 4, "columns": 2},
   {"id": "option_A", "kind": "element"},
   {"id": "option_B", "kind": "element"},
   {"id": "feedback", "kind": "text", "text": "The response divided by the wrong width. One point is lost."},
   {"id": "solution_step_1", "kind": "text", "text": "The width of the interval is 4 - 0 = 4."},
]


def _marks(*marks, description="Marks that point at the stem and the graph."):
   steps = [{"id": f"s{index}", "caption": f"Mark {index}", "add": [mark]} for index, mark in enumerate(marks)]

   return {"description": description, "steps": steps}


def _read(marks, anchors=PRACTICE_ANCHORS, options_hidden=False):
   return read_marks(json.dumps(marks), anchors, options_hidden)


def _reason(marks, anchors=PRACTICE_ANCHORS, options_hidden=False):
   with pytest.raises(FigureRefused) as refusal:
      _read(marks, anchors, options_hidden)

   return refusal.value.reason


PRACTICE_MARKS = _marks(
   {"id": "u", "underline": {"anchor": "stem", "quote": "closed  interval [0, 4]"}},
   {"id": "r", "ring": {"anchor": "item_figure", "at": [2, 3]}},
   {"id": "n", "note": {"anchor": "item_figure", "at": [2, 3], "text": "\\(f(2)\\)", "side": "above"}},
   {"id": "a", "arrow": {"from": {"anchor": "stem", "quote": "its graph is shown"}, "to": {"anchor": "item_figure"}}},
   {"id": "b", "bracket": {"anchor": "stem"}},
   {"id": "l", "line": {"anchor": "item_figure", "point": [1, 1], "slope": 2}},
)
GRAPH_MARKS = _marks(
   {"id": "t", "line": {"through": [[0, 0], [4, 4]]}},
   {"id": "v", "vline": {"x": 3}},
   {"id": "h", "hline": {"y": 5}},
   {"id": "g", "segment": {"from": [0, 1], "to": [4, 5]}},
   {"id": "p", "point": {"anchor": "item_figure", "at": [4, 5], "open": True}},
)
CHECKED_MARKS = _marks(
   {"id": "k", "strike": {"anchor": "solution_step_1", "quote": "4 - 0"}},
   {"id": "w", "highlight": {"anchor": "item_table", "row": 2}},
   {"id": "c", "highlight": {"anchor": "item_table", "cell": [3, 1]}},
   {"id": "o", "ring": {"anchor": "option_B"}},
   {"id": "e", "note": {"anchor": "feedback", "quote": "wrong width", "text": "each width differs"}},
)


@pytest.mark.parametrize(
   "marks, anchors",
   [(PRACTICE_MARKS, PRACTICE_ANCHORS), (GRAPH_MARKS, PRACTICE_ANCHORS), (CHECKED_MARKS, CHECKED_ANCHORS)],
   ids=["on the stem and the graph", "constructions on the graph", "after checking"],
)
def test_every_shape_reads_and_compiles_to_the_contract(marks, anchors):
   render, _facts = compile_marks(_read(marks, anchors), anchors, marks_id="MRK-1")
   written = [mark["id"] for step in marks["steps"] for mark in step["add"]]

   assert list(Draft202012Validator(RENDER_SCHEMA).iter_errors(json.loads(json.dumps(render, allow_nan=False)))) == []
   assert [mark["element"] for mark in render["marks"]] == written


def _rendered(marks, anchors=PRACTICE_ANCHORS):
   render, facts = compile_marks(_read(marks, anchors), anchors)

   return {mark["element"]: mark for mark in render["marks"]}, facts


def test_lines_and_guides_are_clipped_to_the_item_graphs_window():
   marks, facts = _rendered(GRAPH_MARKS)

   assert marks["t"]["points"] == [[-1, -1], [5, 5]]
   assert marks["v"]["points"] == [[3, -2], [3, 6]]
   assert marks["h"]["points"] == [[-1, 5], [5, 5]]
   assert marks["g"]["points"] == [[0, 1], [4, 5]]
   assert (marks["p"]["at"], marks["p"]["open"]) == ([4, 5], True)
   assert [shown.value for shown in facts.lines if shown.element in ("v", "h")] == [3.0, 5.0]


def test_a_target_carries_its_quote_point_or_cell_with_the_rest_null_and_a_strike_is_an_error():
   practice, facts = _rendered(PRACTICE_MARKS)
   checked, _facts = _rendered(CHECKED_MARKS, CHECKED_ANCHORS)

   assert practice["u"]["target"] == {
      "anchor": "stem",
      "quote": "closed interval [0, 4]",
      "at": None,
      "row": None,
      "column": None,
      "cell": None,
   }
   assert practice["r"]["target"]["at"] == [2, 3]
   assert (practice["n"]["text"], practice["n"]["side"]) == ("\\(f(2)\\)", "above")
   assert practice["a"]["to"]["anchor"] == "item_figure"
   assert checked["c"]["target"]["cell"] == [3, 1]
   assert (checked["k"]["role"], checked["k"]["stroke"]["style"]) == ("error", "dashed")
   assert checked["w"]["stroke"]["highlighter"] is True
   assert [shown.value for shown in facts.lines if shown.element == "l"] == [2.0, -1.0, 0.5]


@pytest.mark.parametrize(
   "mark, anchors",
   [
      pytest.param({"id": "u", "underline": {"anchor": "stem", "quote": "open interval"}}, PRACTICE_ANCHORS, id="quote not in the stem"),
      pytest.param({"id": "u", "underline": {"anchor": "section", "quote": "interval"}}, PRACTICE_ANCHORS, id="unlisted anchor"),
      pytest.param({"id": "r", "ring": {"anchor": "item_figure", "at": [6, 3]}}, PRACTICE_ANCHORS, id="point outside the window"),
      pytest.param({"id": "v", "vline": {"x": -3}}, PRACTICE_ANCHORS, id="guide outside the window"),
      pytest.param({"id": "k", "strike": {"anchor": "solution_step_1", "quote": "4 - 0"}}, PRACTICE_ANCHORS, id="strike before checking"),
      pytest.param({"id": "u", "underline": {"anchor": "item_figure", "quote": "graph"}}, PRACTICE_ANCHORS, id="quote on a graph"),
      pytest.param({"id": "w", "highlight": {"anchor": "item_table", "row": 4}}, CHECKED_ANCHORS, id="row outside the table"),
      pytest.param({"id": "r", "ring": {"anchor": "stem", "at": [1, 1]}}, PRACTICE_ANCHORS, id="point on a text anchor"),
      pytest.param({"id": "l", "line": {"through": [[1, 1], [1, 1]]}}, PRACTICE_ANCHORS, id="line through one point"),
      pytest.param({"id": "o", "ring": {"anchor": "option_C"}}, CHECKED_ANCHORS, id="option not listed after checking"),
      pytest.param({"id": "x", "circle": {"anchor": "stem"}}, PRACTICE_ANCHORS, id="unknown shape"),
      pytest.param({"id": "r", "ring": {"anchor": "stem", "quote": "graph", "at": [1, 1]}}, PRACTICE_ANCHORS, id="two addresses"),
   ],
)
def test_each_rule_refuses_the_block_as_malformed(mark, anchors):
   assert _reason(_marks(mark), anchors) == "malformed"


def test_an_option_anchor_before_checking_is_read_so_the_screen_can_withhold_it():
   ringed = _marks({"id": "o", "ring": {"anchor": "option_A"}})
   _render, facts = compile_marks(_read(ringed, options_hidden=True), PRACTICE_ANCHORS, options_hidden=True)

   assert _reason(ringed) == "malformed"
   assert [(shown.element, shown.anchor) for shown in facts.anchors] == [("o", "option_A")]


def test_the_caps_refuse_as_oversized():
   rings = [{"id": f"r{index}", "ring": {"anchor": "stem"}} for index in range(13)]
   thirteen = {
      "description": "Many rings.",
      "steps": [{"id": "first", "caption": "Rings", "add": rings[:7]}, {"id": "then", "caption": "More", "add": rings[7:]}],
   }
   padded = json.dumps(PRACTICE_MARKS) + " " * 1500
   long_quote = _marks({"id": "u", "underline": {"anchor": "stem", "quote": "x" * 81}})

   assert _reason(thirteen) == "oversized"
   assert _reason(json.loads(json.dumps(long_quote))) == "oversized"

   with pytest.raises(FigureRefused) as refusal:
      read_marks(padded, PRACTICE_ANCHORS)

   assert refusal.value.reason == "oversized"


def test_fade_and_erase_name_earlier_marks_only():
   faded = {"description": "A ring that fades.", "steps": [
      {"id": "one", "caption": "Ring", "add": [{"id": "r", "ring": {"anchor": "stem"}}]},
      {"id": "two", "caption": "Fade", "fade": ["r"], "add": [{"id": "b", "bracket": {"anchor": "stem"}}]},
   ]}
   early = {"description": "A fade in its own step.", "steps": [
      {"id": "one", "caption": "Ring", "add": [{"id": "r", "ring": {"anchor": "stem"}}]},
      {"id": "two", "caption": "Fade", "fade": ["b"], "add": [{"id": "b", "bracket": {"anchor": "stem"}}]},
   ]}
   marks, _facts = _rendered(faded)

   assert marks["r"]["faded_at"] == "two"
   assert _reason(early) == "malformed"
