"""docs/agent/drawing-design.md, The figure language and The compiler: the reader takes every example
the design gives, and refuses a block over a cap as oversized and any other bad block as malformed.
"""
import json
import re
from pathlib import Path

import pytest

from app.agent.drawing.spec import FigureRefused, read_figure

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DESIGN_PATH = REPOSITORY_ROOT / "docs" / "agent" / "drawing-design.md"
FIGURE_BLOCK = re.compile(r"```figure\n(.*?)```", re.DOTALL)


def _graph(*steps, window=None):
   return {
      "kind": "graph",
      "title": "A curve and its secant",
      "description": "The curve y equals x squared with a secant through two of its points.",
      "window": window or {"x": [-1, 4], "y": [-1, 9]},
      "steps": list(steps),
   }


def _step(step_id, *elements, fade=None, erase=None):
   step = {"id": step_id, "caption": f"Step {step_id}", "add": list(elements)}

   if fade is not None:
      step["fade"] = fade

   if erase is not None:
      step["erase"] = erase

   return step


def _base():
   return _graph(
      _step("curve", {"id": "f", "curve": "x^2", "role": "given"}),
      _step("secant", {"id": "P", "point": {"on": "f", "x": 1}}, {"id": "s", "secant": {"on": "f", "x": [1, 3]}}),
   )


def _number_line(*elements):
   return {
      "kind": "number_line",
      "title": "Where f prime changes sign",
      "description": "A number line with the critical values of f and the sign of f prime between them.",
      "window": {"x": [-3, 3]},
      "steps": [_step("line", *elements)],
   }


def _table(*elements, rows=None):
   return {
      "kind": "table",
      "title": "Values of f",
      "description": "A table of x and f of x at four points, with one row picked out.",
      "columns": ["\\(x\\)", "\\(f(x)\\)"],
      "rows": rows or [["0", "1"], ["1", "3"], ["2", "7"], ["3", "13"]],
      "steps": [_step("row", *elements)],
   }


def _read(figure):
   return read_figure(json.dumps(figure))


def _reason(figure_or_text):
   text = figure_or_text if isinstance(figure_or_text, str) else json.dumps(figure_or_text)

   with pytest.raises(FigureRefused) as refusal:
      read_figure(text)

   return refusal.value.reason


def test_every_figure_block_in_the_design_reads():
   blocks = FIGURE_BLOCK.findall(DESIGN_PATH.read_text())

   assert len(blocks) >= 1

   for block in blocks:
      figure = read_figure(block)

      assert figure["kind"] in ("graph", "diagram", "number_line", "table")


def test_the_base_figures_of_these_tests_read():
   _read(_base())
   _read(_number_line({"id": "c", "point": 1}, {"id": "s", "signs": {"name": "f'(x)", "at": [-1, 1], "signs": ["+", "-", "+"]}}))
   _read(_table({"id": "h", "highlight": {"row": 2}}))


def test_a_truncated_block_is_malformed():
   block = FIGURE_BLOCK.findall(DESIGN_PATH.read_text())[0]

   assert _reason(block[: len(block) // 2]) == "malformed"


def test_a_block_over_2000_characters_is_oversized_before_it_is_parsed():
   padded = json.dumps(_base()) + " " * 2000

   assert _reason(padded) == "oversized"


def test_nan_and_infinity_are_malformed():
   text = json.dumps(_base()).replace('"x": 1}', '"x": NaN}', 1)

   assert "NaN" in text
   assert _reason(text) == "malformed"


def _with(change):
   figure = _base()
   change(figure)

   return figure


def _seven_steps(figure):
   figure["steps"] += [_step(f"more{index}", {"id": f"p{index}", "point": [index, 0]}) for index in range(5)]


def _five_added(figure):
   figure["steps"][1]["add"] += [{"id": f"p{index}", "point": [index, 0]} for index in range(3)]


def _seventeen_elements(figure):
   for step, count in enumerate((4, 4, 4, 2)):
      points = [{"id": f"p{step}_{index}", "point": [index, step]} for index in range(count)]
      figure["steps"].append(_step(f"more{step}", *points))


def _add(element):
   def change(figure):
      figure["steps"][1]["add"].append(element)

   return change


def _set(path, value):
   def change(figure):
      target = figure

      for key in path[:-1]:
         target = target[key]

      target[path[-1]] = value

   return change


@pytest.mark.parametrize(
   "change",
   [
      pytest.param(_seven_steps, id="seven steps"),
      pytest.param(_five_added, id="five added in a step"),
      pytest.param(_seventeen_elements, id="seventeen elements"),
      pytest.param(_add({"id": "R", "riemann": {"on": "f", "from": 0, "to": 2, "n": 13, "rule": "left"}}), id="13 Riemann pieces"),
      pytest.param(_add({"id": "E", "euler": {"dy": "x + y", "start": [0, 1], "h": 0.1, "n": 11}}), id="11 Euler steps"),
      pytest.param(_add({"id": "G", "polygon": [[index, index % 2] for index in range(9)]}), id="9 polygon vertices"),
      pytest.param(_add({"id": "S", "sequence": {"a": "1/n", "n": [1, 31]}}), id="31 sequence terms"),
      pytest.param(_set(("title",), "t" * 61), id="61-character title"),
      pytest.param(_set(("description",), "d" * 401), id="401-character description"),
      pytest.param(_set(("steps", 0, "caption"), "c" * 101), id="101-character caption"),
      pytest.param(_set(("steps", 0, "add", 0, "label"), "l" * 41), id="41-character label"),
      pytest.param(_set(("steps", 0, "add", 0, "curve"), "x" + " " * 80), id="81-character expression"),
      pytest.param(_set(("steps", 0, "add", 0, "curve"), "--" + "+".join(["x"] * 24)), id="49-token expression"),
      pytest.param(_set(("steps", 0, "add", 0, "curve"), "(" * 11 + "x" + ")" * 11), id="depth-11 expression"),
      pytest.param(_set(("window", "x"), [-100, 101]), id="201-wide window"),
      pytest.param(_set(("axes",), {"x": "time in hours"}), id="13-character axis title"),
      pytest.param(_add({"id": "C", "parametric": {"x": "cos(t)", "y": "sin(t)", "t": [0, 26]}}), id="parameter past 8 pi"),
   ],
)
def test_each_cap_refuses_as_oversized(change):
   assert _reason(_with(change)) == "oversized"


def test_more_than_three_sign_rows_is_oversized():
   rows = [{"id": f"s{index}", "signs": {"name": f"g{index}", "at": [0], "signs": ["+", "-"]}} for index in range(4)]
   figure = _number_line(*rows[:3])
   figure["steps"].append(_step("fourth", rows[3]))

   assert _reason(figure) == "oversized"


@pytest.mark.parametrize(
   "change",
   [
      pytest.param(_add({"id": "big", "point": [1001, 0]}), id="number past 1000"),
      pytest.param(_add({"id": "P", "point": [0, 0]}), id="repeated element id"),
      pytest.param(lambda figure: figure["steps"][1].update(id="curve"), id="repeated step id"),
      pytest.param(lambda figure: figure["steps"][0]["add"].insert(0, {"id": "Z", "point": {"on": "f", "x": 0}}), id="reference to a later element"),
      pytest.param(_add({"id": "T", "tangent": {"on": "P", "x": 1}}), id="on names a point"),
      pytest.param(_add({"id": "V", "segment": ["f", [0, 0]]}), id="point id names a curve"),
      pytest.param(_add({"id": "W", "segment": ["nowhere", [0, 0]]}), id="point id names nothing"),
      pytest.param(lambda figure: figure["steps"][1].update(fade=["P"]), id="fade of the same step"),
      pytest.param(lambda figure: figure["steps"][0].update(fade=["f"]), id="fade in the first step"),
      pytest.param(lambda figure: figure["steps"].append(_step("gone", erase=["nothing"])), id="erase of an unknown id"),
      pytest.param(
         lambda figure: figure["steps"].extend([_step("gone", erase=["s"]), _step("again", erase=["s"])]),
         id="erase of an erased element",
      ),
      pytest.param(lambda figure: figure["steps"].append(_step("still")), id="a step that changes nothing"),
      pytest.param(_set(("window", "x"), [4, -1]), id="window reversed"),
      pytest.param(_set(("window", "y"), [2, 2]), id="window with no height"),
      pytest.param(_add({"id": "U", "spiral": "x"}), id="unknown shape"),
      pytest.param(_add({"id": "U", "vline": 1, "hline": 2}), id="two shapes"),
      pytest.param(_add({"id": "U", "curve": "q x"}), id="name outside the grammar"),
      pytest.param(_add({"id": "U", "curve": "t^2"}), id="curve in t"),
      pytest.param(_add({"id": "U", "secant": {"on": "f", "x": [2, 2]}}), id="secant through one point"),
      pytest.param(_add({"id": "U", "euler": {"dy": "x", "start": [0, 0], "h": 0, "n": 3}}), id="Euler step of zero"),
      pytest.param(_add({"id": "U", "sequence": {"a": "1/n", "n": [5, 2]}}), id="sequence running backwards"),
      pytest.param(_add({"id": "U", "area": {"under": "f", "from": 2, "to": 1}}), id="area bounds reversed"),
      pytest.param(lambda figure: figure.update(kind="diagram", axes={"x": "x"}), id="axes on a diagram"),
      pytest.param(lambda figure: figure.update(columns=["x"]), id="columns on a graph"),
      pytest.param(_add({"id": "U", "point": [0, 0], "colour": "red"}), id="a field the language has no word for"),
      pytest.param(_add({"id": "U", "point": [0, 0], "role": "ghost"}), id="a role the model cannot pick"),
   ],
)
def test_each_rule_refuses_as_malformed(change):
   assert _reason(_with(change)) == "malformed"


@pytest.mark.parametrize(
   "figure",
   [
      pytest.param(_number_line({"id": "c", "point": [1, 0]}), id="number-line point as a pair"),
      pytest.param(_number_line({"id": "s", "signs": {"name": "f'", "at": [-1, 1], "signs": ["+", "-"]}}), id="one sign short"),
      pytest.param(_number_line({"id": "s", "signs": {"name": "f'", "at": [1, -1], "signs": ["+", "-", "+"]}}), id="critical values out of order"),
      pytest.param(
         _number_line({"id": "s", "signs": {"name": "f'", "at": [0], "signs": ["+", "-"], "undefined": [2]}}),
         id="undefined value that is not critical",
      ),
      pytest.param(_number_line({"id": "i", "interval": {"from": 2, "to": 1}}), id="interval reversed"),
      pytest.param(_table({"id": "h", "highlight": {"row": 4}}), id="highlight past the last row"),
      pytest.param(_table({"id": "h", "highlight": {"row": 1}}, rows=[["0", "1"], ["1"]]), id="ragged row"),
      pytest.param(_table({"id": "h", "highlight": {"row": 1}, "role": "given"}), id="table highlight role"),
   ],
)
def test_each_number_line_and_table_rule_refuses_as_malformed(figure):
   assert _reason(figure) == "malformed"


@pytest.mark.parametrize(
   "figure",
   [
      pytest.param(_table({"id": "h", "highlight": {"row": 1}}, rows=[["0", "1"]] * 11), id="11 rows"),
      pytest.param(_table({"id": "h", "highlight": {"row": 1}}, rows=[["0", "1" * 25], ["1", "2"]]), id="25-character cell"),
   ],
)
def test_each_table_cap_refuses_as_oversized(figure):
   assert _reason(figure) == "oversized"


def test_a_block_that_is_not_an_object_is_malformed():
   assert _reason(json.dumps([_base()])) == "malformed"
   assert _reason(json.dumps("figure")) == "malformed"
