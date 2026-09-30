"""docs/agent/drawing-design.md, The compiler, and the render spec contract in
docs/agent/drawing-build-plan.md: each shape's geometry against a closed form, the layout FigureView
uses, labels inside the view, fade and erase on every primitive, every output valid against
schemas/agent/figure_render.schema.json, and each cap refusing.
"""
import itertools
import json
import math
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from app.agent.drawing.compile import compile_figure
from app.agent.drawing.spec import FigureRefused, read_figure

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RENDER_SCHEMA = json.loads((REPOSITORY_ROOT / "schemas" / "agent" / "figure_render.schema.json").read_text())
DESIGN_PATH = REPOSITORY_ROOT / "docs" / "agent" / "drawing-design.md"
DESCRIPTION = "A figure built for the test, described in enough words to read."


def _raw(kind, steps, **fields):
   return {"kind": kind, "title": "Test figure", "description": DESCRIPTION, "steps": steps, **fields}


def _figure(kind, steps, **fields):
   return read_figure(json.dumps(_raw(kind, steps, **fields)))


def _steps(*groups):
   return [{"id": f"s{index}", "caption": f"Step {index}", "add": list(group)} for index, group in enumerate(groups)]


def _graph(*elements, window=None):
   return _figure("graph", _steps(elements), window=window or {"x": [-1, 4], "y": [-1, 10]})


def _diagram(*elements):
   return _figure("diagram", _steps(elements), window={"x": [-1, 5], "y": [-1, 5]})


def _compiled(figure):
   return compile_figure(figure)


def _primitives(spec, element_id, primitive_type=None):
   found = []

   for primitive in spec["primitives"]:
      is_of_element = primitive["element"] == element_id
      is_of_type = primitive_type in (None, primitive["type"])

      if is_of_element and is_of_type:
         found.append(primitive)

   return found


def _numbers(facts, channel, element_id):
   return [shown.value for shown in getattr(facts, channel) if shown.element == element_id]


def _slope(points):
   (x1, y1), (x2, y2) = points[0], points[-1]

   return (y2 - y1) / (x2 - x1)


def _to_view(spec, point):
   (x_low, x_high), (y_low, y_high) = spec["window"]["x"], spec["window"]["y"]
   padding = spec["view"]["padding"]
   plot_width = spec["view"]["width"] - 2 * padding
   plot_height = spec["view"]["height"] - 2 * padding

   return (
      padding + (point[0] - x_low) / (x_high - x_low) * plot_width,
      padding + (y_high - point[1]) / (y_high - y_low) * plot_height,
   )


CURVE = {"id": "f", "curve": "x^2", "role": "given"}


def test_the_secant_of_x_squared_on_1_to_3_has_slope_4_and_crosses_the_window():
   spec, facts = _compiled(_graph(CURVE, {"id": "s", "secant": {"on": "f", "x": [1, 3]}}))
   (path,) = _primitives(spec, "s", "path")

   assert _numbers(facts, "lines", "s")[0] == pytest.approx(4, abs=1e-12)
   assert _slope(path["points"]) == pytest.approx(4, abs=1e-4)
   assert path["points"][0][1] == pytest.approx(-1, abs=1e-4)
   assert path["points"][-1][1] == pytest.approx(10, abs=1e-4)


def test_the_tangent_to_x_squared_at_1_has_slope_2():
   spec, facts = _compiled(_graph(CURVE, {"id": "t", "tangent": {"on": "f", "x": 1}}))
   (path,) = _primitives(spec, "t", "path")
   slope, y_intercept, x_intercept = _numbers(facts, "lines", "t")

   assert slope == pytest.approx(2, abs=1e-6)
   assert y_intercept == pytest.approx(-1, abs=1e-6)
   assert x_intercept == pytest.approx(0.5, abs=1e-6)
   assert _slope(path["points"]) == pytest.approx(2, abs=1e-4)


@pytest.mark.parametrize(
   "rule, total, dots",
   [("left", 1.75, 4), ("right", 3.75, 4), ("midpoint", 2.625, 4), ("trapezoid", 2.75, 5)],
)
def test_the_riemann_and_trapezoid_totals_of_x_squared_on_0_to_2_with_4_pieces(rule, total, dots):
   riemann = {"id": "R", "riemann": {"on": "f", "from": 0, "to": 2, "n": 4, "rule": rule}}
   spec, facts = _compiled(_graph(CURVE, riemann))
   pieces = [path for path in _primitives(spec, "R", "path") if path["closed"]]

   assert _numbers(facts, "approximations", "R") == [pytest.approx(total, abs=1e-12)]
   assert len(pieces) == 4
   assert len(_primitives(spec, "R", "dot")) == dots


def test_the_area_under_x_squared_on_0_to_3_is_9():
   spec, facts = _compiled(_graph(CURVE, {"id": "A", "area": {"under": "f", "from": 0, "to": 3}}))
   (region,) = _primitives(spec, "A", "path")

   assert _numbers(facts, "areas", "A") == [pytest.approx(9, abs=1e-6), pytest.approx(9, abs=1e-6)]
   assert region["closed"] is True
   assert region["fill"] == "region"


def test_an_area_that_crosses_the_axis_is_split_with_its_signed_and_absolute_values():
   line = {"id": "g", "curve": "x"}
   spec, facts = _compiled(_graph(line, {"id": "A", "area": {"under": "g", "from": -1, "to": 2}}))
   fills = [path["fill"] for path in _primitives(spec, "A", "path")]
   signs = [label["text"] for label in _primitives(spec, "A", "label")]

   assert _numbers(facts, "areas", "A") == [pytest.approx(1.5, abs=1e-6), pytest.approx(2.5, abs=1e-6)]
   assert fills == ["region_below", "region"]
   assert signs == ["\\(-\\)", "\\(+\\)"]


def test_the_area_between_two_curves_is_their_difference():
   line = {"id": "g", "curve": "x"}
   _spec, facts = _compiled(_graph(line, CURVE, {"id": "A", "area": {"between": ["g", "f"], "from": 0, "to": 1}}))

   assert _numbers(facts, "areas", "A") == [pytest.approx(1 / 6, abs=1e-6), pytest.approx(1 / 6, abs=1e-6)]


def test_a_curve_is_broken_at_its_asymptote_and_not_joined_across_it():
   spec, _facts = _compiled(_graph({"id": "h", "curve": "1/x"}, window={"x": [-2, 2.9], "y": [-50, 50]}))
   segments = [path["points"] for path in _primitives(spec, "h", "path")]

   assert len(segments) == 2
   assert all(point[0] < 0 for point in segments[0])
   assert all(point[0] > 0 for point in segments[1])


def test_a_right_triangle_has_its_vertices_and_a_right_angle_mark_at_the_corner():
   triangle = {"id": "T", "triangle": {"kind": "right", "at": [0, 0], "base": 3, "height": 4}}
   spec, facts = _compiled(_diagram(triangle))
   outline, mark = _primitives(spec, "T", "path")
   corner = _to_view(spec, (0, 0))
   mark_in_view = [_to_view(spec, point) for point in mark["points"]]

   assert outline["points"] == [[0, 0], [3, 0], [0, 4]]
   assert outline["closed"] is True
   assert mark["weight"] == "thin"
   assert math.dist(corner, mark_in_view[0]) == pytest.approx(10, abs=1e-3)
   assert math.dist(corner, mark_in_view[1]) == pytest.approx(10 * math.sqrt(2), abs=1e-3)
   assert math.dist(corner, mark_in_view[2]) == pytest.approx(10, abs=1e-3)
   assert {3.0, 4.0} <= set(_numbers(facts, "coordinates", "T"))


def _midpoint(points):
   return [(points[0][0] + points[-1][0]) / 2, (points[0][1] + points[-1][1]) / 2]


def test_an_isosceles_triangle_has_its_apex_and_a_tick_on_each_equal_side():
   triangle = {"id": "T", "triangle": {"kind": "isosceles", "at": [0, 0], "base": 4, "height": 3}}
   spec, _facts = _compiled(_diagram(triangle))
   outline, *ticks = _primitives(spec, "T", "path")

   assert outline["points"][2] == pytest.approx([2, 3])
   assert [_midpoint(tick["points"]) for tick in ticks] == [pytest.approx([3, 1.5], abs=1e-4), pytest.approx([1, 1.5], abs=1e-4)]


def test_an_equilateral_triangle_has_three_equal_sides_and_three_ticks():
   triangle = {"id": "T", "triangle": {"kind": "equilateral", "at": [0, 0], "side": 2}}
   spec, _facts = _compiled(_diagram(triangle))
   outline, *ticks = _primitives(spec, "T", "path")
   vertices = outline["points"]
   sides = [math.dist(first, second) for first, second in zip(vertices, vertices[1:] + vertices[:1])]

   assert sides == [pytest.approx(2, abs=1e-4)] * 3
   assert len(ticks) == 3


def test_a_polar_curve_keeps_the_window_at_equal_scale():
   polar = {"id": "r", "polar": {"r": "2", "theta": [0, 6.2832]}}
   spec, _facts = _compiled(_graph(polar, window={"x": [-3, 3], "y": [-1, 1]}))
   window = spec["window"]
   plot_height = spec["view"]["height"] - 2 * spec["view"]["padding"]
   plot_width = spec["view"]["width"] - 2 * spec["view"]["padding"]
   window_ratio = (window["y"][1] - window["y"][0]) / (window["x"][1] - window["x"][0])
   points = itertools.chain.from_iterable(path["points"] for path in _primitives(spec, "r", "path"))

   assert spec["equal_scale"] is True
   assert window_ratio == pytest.approx(plot_height / plot_width, abs=1e-6)
   assert all(math.hypot(*point) == pytest.approx(2, abs=1e-4) for point in points)


@pytest.mark.parametrize(
   "window, height",
   [
      ({"x": [-1, 4], "y": [-1, 9]}, 320),
      ({"x": [0, 10], "y": [0, 1]}, 220),
      ({"x": [0, 4], "y": [0, 3]}, 250),
   ],
)
def test_the_view_height_is_the_window_aspect_clamped_as_figure_view_clamps_it(window, height):
   spec, _facts = _compiled(_graph(CURVE, window=window))

   assert spec["view"] == {"width": 320, "height": height, "padding": 20}


def test_the_slope_field_stays_inside_its_15_by_15_cap_with_each_segment_at_its_slope():
   field = {"id": "F", "slope_field": {"dy": "x - y"}}
   spec, _facts = _compiled(_graph(field, window={"x": [-100, 100], "y": [-100, 100]}))
   segments = [path["points"] for path in _primitives(spec, "F", "path")]

   assert 0 < len(segments) <= 15 * 15

   for start, end in segments:
      centre = _midpoint([start, end])

      assert _slope([start, end]) == pytest.approx(centre[0] - centre[1], rel=1e-3, abs=1e-3)


def test_euler_steps_for_dy_equals_x_plus_y():
   euler = {"id": "E", "euler": {"dy": "x + y", "start": [0, 1], "h": 0.1, "n": 2}}
   spec, _facts = _compiled(_graph(euler, window={"x": [-1, 1], "y": [0, 2]}))
   (path,) = _primitives(spec, "E", "path")

   assert path["points"] == [[0, 1], [0.1, 1.1], [0.2, 1.22]]
   assert len(_primitives(spec, "E", "dot")) == 3


def test_the_solution_curve_follows_the_differential_equation():
   solution = {"id": "S", "solution": {"dy": "y", "through": [0, 1]}}
   spec, _facts = _compiled(_graph(solution, window={"x": [-1, 2], "y": [-1, 8]}))
   (path,) = _primitives(spec, "S", "path")

   assert len(path["points"]) == 241
   assert all(y == pytest.approx(math.exp(x), abs=1e-4) for x, y in path["points"])


def test_the_partial_sums_of_one_over_two_to_the_n():
   sequence = {"id": "Q", "sequence": {"a": "1/2^n", "n": [1, 5], "sums": True}}
   spec, _facts = _compiled(_graph(sequence, window={"x": [0, 6], "y": [0, 1.2]}))
   dots = [dot["at"] for dot in _primitives(spec, "Q", "dot")]

   assert dots == [[1, 0.5], [2, 0.75], [3, 0.875], [4, 0.9375], [5, 0.96875]]


def test_a_point_on_a_curve_where_the_curve_is_undefined_is_malformed():
   figure = _graph({"id": "f", "curve": "sqrt(x)"}, {"id": "P", "point": {"on": "f", "x": -1}})

   with pytest.raises(FigureRefused) as refusal:
      compile_figure(figure)

   assert refusal.value.reason == "malformed"


def test_fade_and_erase_mark_every_primitive_of_their_element():
   figure = _figure(
      "graph",
      [
         {"id": "one", "caption": "Two points", "add": [{"id": "P", "point": [1, 1], "label": "P"}, {"id": "Q", "point": [2, 2]}]},
         {"id": "two", "caption": "P fades", "add": [{"id": "R", "point": [3, 3]}], "fade": ["P"]},
         {"id": "three", "caption": "Q goes", "add": [{"id": "S", "point": [0, 0]}], "erase": ["Q"]},
      ],
      window={"x": [-1, 4], "y": [-1, 4]},
   )
   spec, _facts = _compiled(figure)

   assert {(primitive["faded_at"], primitive["erased_at"]) for primitive in _primitives(spec, "P")} == {("two", None)}
   assert {(primitive["faded_at"], primitive["erased_at"]) for primitive in _primitives(spec, "Q")} == {(None, "three")}
   assert {(primitive["faded_at"], primitive["erased_at"]) for primitive in _primitives(spec, "R")} == {(None, None)}


def _visible_length(text):
   return len(re.sub(r"\\[()]", "", text).strip())


def test_labels_sit_at_their_element_and_inside_the_view():
   figure = _graph(
      {"id": "top", "point": [4, 10], "label": "a long label at the corner"},
      {"id": "low", "point": [-1, -1], "label": "\\(P_0\\)"},
      {"id": "mid", "point": [1.5, 4], "label": "a label too wide for either side"},
      {"id": "edge", "vline": 4, "label": "x = 4"},
   )
   spec, _facts = _compiled(figure)
   labels = [primitive for primitive in spec["primitives"] if primitive["type"] == "label"]

   assert len(labels) == 4
   assert [label["at"] for label in labels[:3]] == [[4, 10], [-1, -1], [1.5, 4]]

   for label in labels:
      view_x, view_y = _to_view(spec, label["at"])
      x = view_x + label["offset"][0]
      baseline = view_y + label["offset"][1]
      width = 8 * _visible_length(label["text"])
      left = {"start": x, "middle": x - width / 2, "end": x - width}[label["align"]]

      assert 0 <= left and left + width <= spec["view"]["width"]
      assert 0 <= baseline - 14 and baseline <= spec["view"]["height"]


EVERY_SHAPE = [
   _raw(
      "graph",
      _steps(
         [CURVE, {"id": "g", "curve": {"y": "x + 1", "domain": [0, 3]}}, {"id": "p", "parametric": {"x": "cos(t)", "y": "sin(t)", "t": [0, 3]}}, {"id": "P", "point": [1, 1], "open": True, "label": "P"}],
         [{"id": "l1", "line": {"through": ["P", [2, 3]]}}, {"id": "l2", "line": {"point": {"on": "f", "x": 2}, "slope": -1}}, {"id": "sg", "segment": [[0, 0], "P"], "stroke": {"arrow": "both"}}, {"id": "sc", "secant": {"on": "f", "x": [0, 2]}}],
         [{"id": "tg", "tangent": {"on": "f", "x": 1, "length": 2}}, {"id": "v", "vline": 2}, {"id": "h", "hline": 3, "role": "error"}, {"id": "A1", "area": {"under": "f", "from": 0, "to": 1}}],
         [{"id": "A2", "area": {"between": ["g", "f"], "from": 0, "to": 1}}, {"id": "R", "riemann": {"on": "f", "from": 0, "to": 2, "n": 4, "rule": "midpoint"}, "label": "M"}],
      ),
      window={"x": [-1, 4], "y": [-1, 10]},
      axes={"x": "t", "y": "v(t)"},
   ),
   _raw(
      "graph",
      _steps(
         [{"id": "F", "slope_field": {"dy": "x - y"}}, {"id": "S", "solution": {"dy": "x - y", "through": [0, 1]}}],
         [{"id": "E", "euler": {"dy": "x - y", "start": [0, 1], "h": 0.5, "n": 4}}, {"id": "Q", "sequence": {"a": "1/n", "n": [1, 5], "sums": True}}],
         [{"id": "V", "vector": {"from": [0, 0], "components": [2, 1], "legs": True}}, {"id": "W", "vector": {"from": [1, 0], "to": [2, 2]}}, {"id": "C", "circle": {"center": [1, 1], "radius": 1}}, {"id": "K", "arc": {"center": [0, 0], "radius": 1, "from": 300, "to": 30}}],
      ),
      window={"x": [-3, 3], "y": [-3, 3]},
      grid=False,
   ),
   _raw(
      "diagram",
      _steps(
         [{"id": "A", "point": [0, 0]}, {"id": "B", "point": [3, 0]}, {"id": "C", "point": [0, 2]}, {"id": "ang", "angle": {"at": "A", "from": "B", "to": "C"}, "label": "\\(\\theta\\)"}],
         [{"id": "ra", "right_angle": {"at": "A", "from": "B", "to": "C"}}, {"id": "bx", "box": {"at": [3, 3], "width": 1.5, "height": 1, "text": "rate in"}}, {"id": "tr", "triangle": {"kind": "right", "at": [0, 0], "base": 3, "height": 2, "names": ["A", "B", "C"], "sides": ["3", "\\(\\sqrt{13}\\)", "2"]}}, {"id": "sc", "triangle": {"kind": "scalene", "vertices": [[1, 3], [2, 4], [0, 4]], "rotate": 15}}],
         [{"id": "pg", "polygon": [[4, 0], [5, 1], [4, 2], [3.5, 1]]}, {"id": "br", "brace": {"from": [0, 0], "to": [3, 0], "text": "\\(\\Delta x\\)", "side": "right"}}, {"id": "tx", "text": {"at": [2, 4.5], "text": "free text"}}, {"id": "co", "callout": {"target": "B", "at": [4, 3], "text": "look here"}}],
         [{"id": "rg", "ring": {"target": [0, 2]}}, {"id": "eq", "triangle": {"kind": "equilateral", "at": [3, 3.5], "side": 1}}, {"id": "is", "triangle": {"kind": "isosceles", "at": [-0.5, 3], "base": 1, "height": 1}}],
      ),
      window={"x": [-1, 5], "y": [-1, 5]},
   ),
   _raw(
      "graph",
      _steps([{"id": "r", "polar": {"r": "1 + cos(theta)", "theta": [0, 6.2832]}, "label": "\\(r = 1 + \\cos\\theta\\)"}]),
      window={"x": [-1, 3], "y": [-2, 2]},
   ),
   _raw(
      "number_line",
      _steps(
         [{"id": "c", "point": 1, "open": True, "label": "c"}, {"id": "I", "interval": {"from": None, "to": 2, "open": [False, True]}}],
         [{"id": "sg", "signs": {"name": "f'(x)", "at": [-1, 1], "signs": ["+", "-", "+"], "undefined": [1]}}, {"id": "t", "text": {"at": "c", "text": "here"}}, {"id": "b", "brace": {"from": -1, "to": 1, "text": "width 2"}}],
         [{"id": "co", "callout": {"target": -1, "at": 0, "text": "a maximum"}}, {"id": "rg", "ring": {"target": "c"}}, {"id": "seg", "segment": [-2, -1.5]}],
      ),
      window={"x": [-3, 3]},
   ),
   _raw(
      "table",
      _steps(
         [{"id": "r", "highlight": {"row": 1}}, {"id": "k", "highlight": {"column": 0}, "role": "error"}],
         [{"id": "c", "highlight": {"cell": [2, 1]}, "label": "this one"}, {"id": "n", "callout": {"cell": [0, 1], "text": "the start"}}],
      ),
      columns=["\\(x\\)", "\\(f(x)\\)"],
      rows=[["0", "1"], ["1", "3"], ["2", "7"]],
   ),
]


@pytest.mark.parametrize("raw", EVERY_SHAPE, ids=["graph shapes", "field shapes", "diagram shapes", "polar", "number line", "table"])
def test_every_shape_draws_and_the_spec_validates_against_the_render_schema(raw):
   figure = read_figure(json.dumps(raw))
   spec, _facts = _compiled(figure)
   wire = json.loads(json.dumps(spec, allow_nan=False))
   drawn = {primitive["element"] for primitive in spec["primitives"]}
   written = {element["id"] for step in figure["steps"] for element in step.get("add") or ()}
   point_count = sum(len(primitive.get("points", [])) for primitive in spec["primitives"])

   assert list(Draft202012Validator(RENDER_SCHEMA).iter_errors(wire)) == []
   assert written <= drawn
   assert len(spec["primitives"]) <= 200
   assert point_count <= 4000


def test_the_design_example_validates_against_the_render_schema():
   block = re.findall(r"```figure\n(.*?)```", DESIGN_PATH.read_text(), re.DOTALL)[0]
   spec, _facts = compile_figure(read_figure(block))

   assert list(Draft202012Validator(RENDER_SCHEMA).iter_errors(json.loads(json.dumps(spec, allow_nan=False)))) == []


def test_a_number_line_draws_its_own_line_and_ticks():
   spec, _facts = _compiled(read_figure(json.dumps(EVERY_SHAPE[4])))
   frame = _primitives(spec, "_axis")

   assert frame[0]["type"] == "path"
   assert frame[0]["arrow"] == "both"
   assert [label["text"] for label in frame if label["type"] == "label"] == ["-3", "-2", "-1", "0", "1", "2", "3"]
   assert {primitive["step"] for primitive in frame} == {"s0"}


def _refusal(figure, **options):
   with pytest.raises(FigureRefused) as refusal:
      compile_figure(figure, **options)

   return refusal.value.reason


def test_a_figure_past_4000_points_is_oversized():
   areas = [{"id": f"A{index}", "area": {"between": ["g", "f"], "from": 0, "to": 2}} for index in range(14)]
   curves = [{"id": "f", "curve": "x^2"}, {"id": "g", "curve": "x + 5"}]
   figure = _figure("graph", _steps(curves + areas[:2], areas[2:6], areas[6:10], areas[10:14]), window={"x": [-1, 4], "y": [-1, 10]})
   fewer = _figure("graph", _steps(curves + areas[:2], areas[2:6], areas[6:10]), window={"x": [-1, 4], "y": [-1, 10]})

   compile_figure(fewer)

   assert _refusal(figure) == "oversized"


def test_a_figure_past_200_primitives_is_oversized():
   fields = [{"id": f"F{index}", "slope_field": {"dy": "x"}} for index in range(2)]
   window = {"x": [-5, 5], "y": [-5, 5]}

   compile_figure(_graph(fields[0], window=window))

   assert _refusal(_graph(*fields, window=window)) == "oversized"


def test_a_figure_past_100_ms_is_oversized():
   ticks = itertools.count()
   figure = _graph(CURVE, {"id": "P", "point": [1, 1]}, {"id": "Q", "point": [2, 2]})

   compile_figure(figure)

   assert _refusal(figure, clock=lambda: next(ticks) * 0.06) == "oversized"
