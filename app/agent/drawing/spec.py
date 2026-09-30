"""The figure reader (docs/agent/drawing-design.md, The figure language and The compiler).

read_figure takes the text between a figure fence and its closing fence and returns the figure as
a mapping, or raises FigureRefused with the reason the design names: oversized for anything over a
cap (the 2,000 characters, a count, a length, a window span, a parameter span, an expression's
characters, tokens or depth) and malformed for everything else. The JSON is read with json.loads
under the character cap, with NaN and Infinity refused and a RecursionError caught with the
ValueError, then validated against schemas/agent/figure.schema.json, then checked for what a
schema cannot state: ids unique, references to earlier elements of the right shape, fade and
erase naming elements of earlier steps, windows ordered, every expression readable in its
variables, and the 16-element cap. No reason quotes the block.
"""
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

from app.agent.drawing import expression

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
FIGURE_SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "agent" / "figure.schema.json"

MALFORMED = "malformed"
OVERSIZED = "oversized"

MAX_BLOCK_CHARACTERS = 2000
MAX_ELEMENTS = 16
MAX_SIGN_ROWS = 3
MAX_SEQUENCE_TERMS = 30
MAX_WINDOW_SPAN = 200
MAX_PARAMETER_SPAN = 8 * math.pi
SIZE_VALIDATORS = ("maxItems", "maxLength")
COUNT_FIELDS = ("n",)

GRAPH = "graph"
DIAGRAM = "diagram"
NUMBER_LINE = "number_line"
TABLE = "table"

CURVE_VARIABLES = ("x",)
PARAMETRIC_VARIABLES = ("t",)
POLAR_VARIABLES = ("theta",)
SEQUENCE_VARIABLES = ("n",)
FIELD_VARIABLES = ("x", "y")

SHAPE_KEYS = (
   "curve",
   "parametric",
   "polar",
   "point",
   "line",
   "segment",
   "secant",
   "tangent",
   "vline",
   "hline",
   "area",
   "riemann",
   "slope_field",
   "solution",
   "euler",
   "sequence",
   "vector",
   "circle",
   "arc",
   "angle",
   "right_angle",
   "box",
   "triangle",
   "polygon",
   "brace",
   "text",
   "callout",
   "ring",
   "interval",
   "signs",
   "highlight",
)

_VALIDATOR = Draft202012Validator(json.loads(FIGURE_SCHEMA_PATH.read_text()))


class FigureRefused(ValueError):
   """A figure the server will not draw. reason is one of the figure_refused reasons."""

   def __init__(self, reason):
      super().__init__(reason)
      self.reason = reason


def shape_of(element):
   return next(key for key in SHAPE_KEYS if key in element)


def elements_in_order(figure):
   """Every element with the id of the step that adds it, in the order the figure writes them."""
   ordered = []

   for step in figure["steps"]:
      for element in step.get("add") or ():
         ordered.append((step["id"], element))

   return ordered


def _refuse_constant(_name):
   raise ValueError("not a finite number")


def _parsed(text):
   try:
      return json.loads(text, parse_constant=_refuse_constant)
   except (ValueError, RecursionError):
      raise FigureRefused(MALFORMED) from None


def _every_error(errors):
   for error in errors:
      yield error
      yield from _every_error(error.context)


def _is_cap(error):
   """A length or count past its cap. The common fields (id, role, label, stroke) sit in every
   branch of an element's oneOf, so a cap is found wherever it fails and not only in the branch the
   element was meant for."""
   is_size_cap = error.validator in SIZE_VALIDATORS
   path = list(error.absolute_path)
   is_count_cap = error.validator == "maximum" and len(path) > 0 and path[-1] in COUNT_FIELDS

   return is_size_cap or is_count_cap


def _schema_reason(errors):
   is_over_a_cap = any(_is_cap(error) for error in _every_error(errors))

   return OVERSIZED if is_over_a_cap else MALFORMED


def _validated(figure):
   errors = list(_VALIDATOR.iter_errors(figure))
   has_errors = len(errors) > 0

   if has_errors:
      raise FigureRefused(_schema_reason(errors))


def _check_range(pair, maximum_span):
   low, high = pair
   is_ordered = low < high

   if not is_ordered:
      raise FigureRefused(MALFORMED)

   is_too_wide = high - low > maximum_span

   if is_too_wide:
      raise FigureRefused(OVERSIZED)


def _check_window(figure):
   window = figure.get("window")

   if window is None:
      return

   _check_range(window["x"], MAX_WINDOW_SPAN)

   if "y" in window:
      _check_range(window["y"], MAX_WINDOW_SPAN)


def _check_expression(text, variables):
   try:
      expression.parse(text, variables)
   except expression.ExpressionRefused as refused:
      raise FigureRefused(refused.reason) from None


def _expressions(shape, value):
   """Each expression an element carries, with the variables it is written in."""
   if shape == "curve":
      curve_text = value if isinstance(value, str) else value["y"]

      return [(curve_text, CURVE_VARIABLES)]

   if shape == "parametric":
      return [(value["x"], PARAMETRIC_VARIABLES), (value["y"], PARAMETRIC_VARIABLES)]

   if shape == "polar":
      return [(value["r"], POLAR_VARIABLES)]

   if shape in ("slope_field", "solution", "euler"):
      return [(value["dy"], FIELD_VARIABLES)]

   if shape == "sequence":
      return [(value["a"], SEQUENCE_VARIABLES)]

   return []


def _point_values(shape, value):
   """Every value in the element written as a point: [x, y], a point id or a point on a curve."""
   if shape == "point":
      return [value]

   if shape == "line":
      return list(value["through"]) if "through" in value else [value["point"]]

   if shape == "segment":
      return list(value)

   if shape == "polygon":
      return list(value)

   if shape == "solution":
      return [value["through"]]

   if shape == "euler":
      return [value["start"]]

   if shape == "vector":
      return [value["from"], value["to"]] if "to" in value else [value["from"]]

   if shape in ("circle", "arc"):
      return [value["center"]]

   if shape in ("angle", "right_angle"):
      return [value["at"], value["from"], value["to"]]

   if shape == "box":
      return [value["at"]]

   if shape == "triangle":
      return list(value["vertices"]) if "vertices" in value else [value["at"]]

   if shape == "brace":
      return [value["from"], value["to"]]

   if shape == "text":
      return [value["at"]]

   if shape == "callout":
      return [value["at"]]

   return []


def _target_values(shape, value):
   if shape in ("callout", "ring"):
      return [value["target"]]

   return []


def _curve_references(shape, value):
   if shape in ("secant", "tangent", "riemann"):
      return [value["on"]]

   if shape == "area":
      return list(value["between"]) if "between" in value else [value["under"]]

   return []


def _require_earlier(reference, seen, allowed_shapes=None):
   is_known = reference in seen

   if not is_known:
      raise FigureRefused(MALFORMED)

   has_wrong_shape = allowed_shapes is not None and seen[reference] not in allowed_shapes

   if has_wrong_shape:
      raise FigureRefused(MALFORMED)


def _check_point_value(point, seen):
   if isinstance(point, str):
      _require_earlier(point, seen, ("point",))
   elif isinstance(point, dict):
      _require_earlier(point["on"], seen, ("curve",))


def _check_graph_element(shape, value, seen):
   for point in _point_values(shape, value):
      _check_point_value(point, seen)

   for target in _target_values(shape, value):
      if isinstance(target, str):
         _require_earlier(target, seen)
      else:
         _check_point_value(target, seen)

   for curve in _curve_references(shape, value):
      _require_earlier(curve, seen, ("curve",))

   has_domain = shape == "curve" and isinstance(value, dict) and "domain" in value

   if has_domain:
      _check_range(value["domain"], math.inf)

   if shape == "parametric":
      _check_range(value["t"], MAX_PARAMETER_SPAN)

   if shape == "polar":
      _check_range(value["theta"], MAX_PARAMETER_SPAN)

   if shape in ("area", "riemann"):
      _check_range((value["from"], value["to"]), math.inf)

   is_one_point_secant = shape == "secant" and value["x"][0] == value["x"][1]
   is_standing_euler = shape == "euler" and value["h"] == 0

   if is_one_point_secant or is_standing_euler:
      raise FigureRefused(MALFORMED)

   if shape == "sequence":
      first, last = value["n"]

      if last < first:
         raise FigureRefused(MALFORMED)

      has_too_many_terms = last - first + 1 > MAX_SEQUENCE_TERMS

      if has_too_many_terms:
         raise FigureRefused(OVERSIZED)


def _check_signs(value):
   critical_values = value["at"]
   is_increasing = all(low < high for low, high in zip(critical_values, critical_values[1:]))
   has_one_sign_per_interval = len(value["signs"]) == len(critical_values) + 1
   undefined_values = value.get("undefined") or []
   are_undefined_values_critical = all(point in critical_values for point in undefined_values)
   is_well_formed = is_increasing and has_one_sign_per_interval and are_undefined_values_critical

   if not is_well_formed:
      raise FigureRefused(MALFORMED)


def _check_number_line_element(shape, value, seen):
   is_text_at_a_point = shape == "text" and isinstance(value["at"], str)

   if is_text_at_a_point:
      _require_earlier(value["at"], seen, ("point",))

   for target in _target_values(shape, value):
      if isinstance(target, str):
         _require_earlier(target, seen)

   if shape == "signs":
      _check_signs(value)

   if shape == "interval":
      low = value["from"]
      high = value["to"]
      is_bounded = low is not None and high is not None
      is_reversed = is_bounded and low >= high

      if is_reversed:
         raise FigureRefused(MALFORMED)

   is_empty_brace = shape == "brace" and value["from"] == value["to"]

   if is_empty_brace:
      raise FigureRefused(MALFORMED)


def _check_table(figure):
   column_count = len(figure["columns"])
   row_count = len(figure["rows"])
   has_ragged_row = any(len(row) != column_count for row in figure["rows"])

   if has_ragged_row:
      raise FigureRefused(MALFORMED)

   for _step_id, element in elements_in_order(figure):
      shape = shape_of(element)
      value = element[shape]
      row = value.get("row")
      column = value.get("column")

      if "cell" in value:
         row, column = value["cell"]

      is_row_outside = row is not None and row >= row_count
      is_column_outside = column is not None and column >= column_count

      if is_row_outside or is_column_outside:
         raise FigureRefused(MALFORMED)


def _check_steps(figure):
   step_ids = set()
   added_at = {}
   erased = set()

   for index, step in enumerate(figure["steps"]):
      step_id = step["id"]
      is_repeated_step = step_id in step_ids

      if is_repeated_step:
         raise FigureRefused(MALFORMED)

      step_ids.add(step_id)
      added = step.get("add") or []
      faded = step.get("fade") or []
      removed = step.get("erase") or []
      changes_nothing = not added and not faded and not removed
      only_adds = bool(added) and not faded and not removed
      breaks_first_step_rule = index == 0 and not only_adds

      if changes_nothing or breaks_first_step_rule:
         raise FigureRefused(MALFORMED)

      named = list(faded) + list(removed)
      names_twice = len(set(named)) != len(named)

      if names_twice:
         raise FigureRefused(MALFORMED)

      for element_id in named:
         is_from_earlier_step = element_id in added_at and added_at[element_id] < index
         is_still_drawn = element_id not in erased
         can_change = is_from_earlier_step and is_still_drawn

         if not can_change:
            raise FigureRefused(MALFORMED)

      erased.update(removed)

      for element in added:
         added_at[element["id"]] = index


def _check_elements(figure):
   kind = figure["kind"]
   seen = {}
   sign_rows = 0

   for _step_id, element in elements_in_order(figure):
      element_id = element["id"]
      is_repeated = element_id in seen

      if is_repeated:
         raise FigureRefused(MALFORMED)

      shape = shape_of(element)
      value = element[shape]

      for text, variables in _expressions(shape, value):
         _check_expression(text, variables)

      if kind in (GRAPH, DIAGRAM):
         _check_graph_element(shape, value, seen)
      elif kind == NUMBER_LINE:
         _check_number_line_element(shape, value, seen)

      sign_rows += 1 if shape == "signs" else 0
      seen[element_id] = shape

   has_too_many_elements = len(seen) > MAX_ELEMENTS
   has_too_many_sign_rows = sign_rows > MAX_SIGN_ROWS

   if has_too_many_elements or has_too_many_sign_rows:
      raise FigureRefused(OVERSIZED)


def check_figure(figure):
   """The rules a schema cannot state, on a figure that already validates."""
   _check_window(figure)

   if figure["kind"] == TABLE:
      _check_table(figure)

   _check_steps(figure)
   _check_elements(figure)


def read_figure(text):
   """The figure a block holds, or FigureRefused(reason)."""
   is_text = isinstance(text, str)

   if not is_text:
      raise FigureRefused(MALFORMED)

   if len(text) > MAX_BLOCK_CHARACTERS:
      raise FigureRefused(OVERSIZED)

   figure = _parsed(text)
   is_object = isinstance(figure, dict)

   if not is_object:
      raise FigureRefused(MALFORMED)

   _validated(figure)
   check_figure(figure)

   return figure
