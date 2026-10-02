"""Marks on the page (docs/agent/drawing-design.md, Marks on the page; the marks contract in
docs/agent/drawing-build-plan.md).

The model cannot see the page, so every mark names an anchor the turn's packet lists: the stem, the
item's graph or table, the feedback and the worked solution steps once checked and shown, a lesson
section and its figure. The options are never listed. read_marks takes a marks block and the turn's anchors, each a
mapping with id and kind, the text for a text anchor, the window for a graph and the row and
column counts for a table, and returns the marks or raises FigureRefused: oversized past 1,500
characters, 12 marks or a length cap, malformed for anything else. A quote must occur in its
anchor's text once whitespace is collapsed; a point, a segment's ends and a line's points sit
inside the item graph's window; a row, a column or a cell is inside the table. An anchor the turn
did not list refuses the block, except an option anchor while the options are hidden, before an
item is checked: that block is read so that the screen withholds the reply, since ringing an option
names an answer.

compile_marks gives the render marks the client places over the anchored elements and a MarksFacts
record for the screen: the coordinates and the slopes, intercepts and guide levels drawn on the
item's graph, every note, caption and the description, and every anchor named. Quoted phrases are
the screen's own text and are not facts.
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator

from app.agent.drawing.compile import Layout, ShownNumber, ShownText, clip_line, line_numbers
from app.agent.drawing.spec import MALFORMED, OVERSIZED, FigureRefused, schema_reason

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MARKS_SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "agent" / "marks.schema.json"

MAX_BLOCK_CHARACTERS = 1500
MAX_MARKS = 12

TEXT_ANCHOR = "text"
GRAPH_ANCHOR = "graph"
TABLE_ANCHOR = "table"
ELEMENT_ANCHOR = "element"
ITEM_FIGURE = "item_figure"
OPTION_ANCHOR_PATTERN = r"option_[A-E]"

SHAPE_KEYS = (
   "ring",
   "underline",
   "highlight",
   "strike",
   "bracket",
   "note",
   "arrow",
   "point",
   "segment",
   "line",
   "vline",
   "hline",
)
GRAPH_SHAPES = ("point", "segment", "line", "vline", "hline")
ADDRESS_FIELDS = ("quote", "at", "row", "column", "cell")

GIVEN = "given"
CONSTRUCTED = "constructed"
HIGHLIGHT = "highlight"
ERROR = "error"
ROLE_WEIGHTS = {GIVEN: "regular", CONSTRUCTED: "bold", HIGHLIGHT: "bold", ERROR: "regular"}
DEFAULT_ROLES = {"strike": ERROR, "highlight": HIGHLIGHT}
DASHED_SHAPES = ("vline", "hline")
ARROW_SHAPES = ("arrow",)
DEFAULT_SIDE = "right"
COORDINATE_DIGITS = 5

_VALIDATOR = Draft202012Validator(json.loads(MARKS_SCHEMA_PATH.read_text()))


@dataclass(frozen=True)
class ShownAnchor:
   element: str
   anchor: str


@dataclass(frozen=True)
class MarksFacts:
   """Every number, text and anchor a compiled marks block shows, by the channel the screen reads."""

   coordinates: tuple = ()
   lines: tuple = ()
   texts: tuple = ()
   anchors: tuple = ()


def is_option_anchor(anchor_id):
   return re.fullmatch(OPTION_ANCHOR_PATTERN, anchor_id) is not None


def normalised(text):
   return " ".join(str(text).split())


def shape_of(mark):
   return next(key for key in SHAPE_KEYS if key in mark)


def marks_in_order(marks):
   ordered = []

   for step in marks["steps"]:
      for mark in step.get("add") or ():
         ordered.append((step["id"], mark))

   return ordered


def _refuse_constant(_name):
   raise ValueError("not a finite number")


def _parsed(text):
   try:
      return json.loads(text, parse_constant=_refuse_constant)
   except (ValueError, RecursionError):
      raise FigureRefused(MALFORMED) from None


class _Anchors:
   def __init__(self, anchors, options_hidden):
      self.by_id = {anchor["id"]: anchor for anchor in anchors}
      self.options_hidden = options_hidden

   def get(self, anchor_id):
      anchor = self.by_id.get(anchor_id)

      if anchor is not None:
         return anchor

      reaches_the_screen = self.options_hidden and is_option_anchor(anchor_id)

      if reaches_the_screen:
         return {"id": anchor_id, "kind": ELEMENT_ANCHOR}

      raise FigureRefused(MALFORMED)

   def graph(self):
      anchor = self.get(ITEM_FIGURE)
      has_window = anchor.get("kind") == GRAPH_ANCHOR and anchor.get("window") is not None

      if not has_window:
         raise FigureRefused(MALFORMED)

      return anchor["window"]


def _inside(window, point):
   x, y = point
   is_across = window["x"][0] <= x <= window["x"][1]
   is_up = window["y"][0] <= y <= window["y"][1]

   return is_across and is_up


def _check_point(anchors, point):
   if not _inside(anchors.graph(), point):
      raise FigureRefused(MALFORMED)


def _check_quote(anchor, quote):
   is_text = anchor.get("kind") == TEXT_ANCHOR
   is_found = is_text and normalised(quote) in normalised(anchor.get("text") or "")

   if not is_found:
      raise FigureRefused(MALFORMED)


def _check_table_address(anchor, row=None, column=None):
   is_table = anchor.get("kind") == TABLE_ANCHOR
   is_row_outside = row is not None and row >= anchor.get("rows", 0)
   is_column_outside = column is not None and column >= anchor.get("columns", 0)
   is_addressable = is_table and not is_row_outside and not is_column_outside

   if not is_addressable:
      raise FigureRefused(MALFORMED)


def _check_target(anchors, target):
   anchor = anchors.get(target["anchor"])

   if "quote" in target:
      _check_quote(anchor, target["quote"])

   if "at" in target:
      is_the_graph = target["anchor"] == ITEM_FIGURE

      if not is_the_graph:
         raise FigureRefused(MALFORMED)

      _check_point(anchors, target["at"])

   if "row" in target:
      _check_table_address(anchor, row=target["row"])

   if "column" in target:
      _check_table_address(anchor, column=target["column"])

   if "cell" in target:
      row, column = target["cell"]
      _check_table_address(anchor, row=row, column=column)


def _check_line(anchors, value):
   if "point" in value:
      _check_point(anchors, value["point"])
      return

   first, second = value["through"]
   is_one_point = first == second

   if is_one_point:
      raise FigureRefused(MALFORMED)

   _check_point(anchors, first)
   _check_point(anchors, second)


def _check_graph_mark(anchors, shape, value):
   window = anchors.graph()

   if shape == "point":
      _check_point(anchors, value["at"])
   elif shape == "segment":
      _check_point(anchors, value["from"])
      _check_point(anchors, value["to"])
   elif shape == "line":
      _check_line(anchors, value)
   elif shape == "vline":
      is_inside = window["x"][0] <= value["x"] <= window["x"][1]

      if not is_inside:
         raise FigureRefused(MALFORMED)
   else:
      is_inside = window["y"][0] <= value["y"] <= window["y"][1]

      if not is_inside:
         raise FigureRefused(MALFORMED)


def _check_mark(anchors, shape, value):
   if shape in GRAPH_SHAPES:
      _check_graph_mark(anchors, shape, value)
   elif shape == "arrow":
      _check_target(anchors, value["from"])
      _check_target(anchors, value["to"])
   elif shape == "note":
      _check_target(anchors, {key: value[key] for key in ("anchor",) + ADDRESS_FIELDS if key in value})
   else:
      _check_target(anchors, value)


def _check_steps(marks):
   step_ids = set()
   added_at = {}
   erased = set()

   for index, step in enumerate(marks["steps"]):
      is_repeated_step = step["id"] in step_ids

      if is_repeated_step:
         raise FigureRefused(MALFORMED)

      step_ids.add(step["id"])
      added = step.get("add") or []
      faded = step.get("fade") or []
      removed = step.get("erase") or []
      changes_nothing = not added and not faded and not removed
      only_adds = bool(added) and not faded and not removed
      breaks_first_step_rule = index == 0 and not only_adds
      named = list(faded) + list(removed)
      names_twice = len(set(named)) != len(named)
      is_malformed_step = changes_nothing or breaks_first_step_rule or names_twice

      if is_malformed_step:
         raise FigureRefused(MALFORMED)

      for mark_id in named:
         is_from_earlier_step = mark_id in added_at and added_at[mark_id] < index
         is_still_drawn = mark_id not in erased
         can_change = is_from_earlier_step and is_still_drawn

         if not can_change:
            raise FigureRefused(MALFORMED)

      erased.update(removed)

      for mark in added:
         added_at[mark["id"]] = index


def check_marks(marks, anchors, options_hidden=False):
   """The rules a schema cannot state, on a marks block that already validates."""
   _check_steps(marks)
   listed = _Anchors(anchors, options_hidden)
   seen = set()

   for _step_id, mark in marks_in_order(marks):
      is_repeated = mark["id"] in seen

      if is_repeated:
         raise FigureRefused(MALFORMED)

      seen.add(mark["id"])
      shape = shape_of(mark)
      _check_mark(listed, shape, mark[shape])

   has_too_many_marks = len(seen) > MAX_MARKS

   if has_too_many_marks:
      raise FigureRefused(OVERSIZED)


def read_marks(text, anchors, options_hidden=False):
   """The marks a block holds, or FigureRefused(reason). options_hidden is true before an item is
   checked, when an option anchor is read so that the screen can withhold the reply."""
   is_text = isinstance(text, str)

   if not is_text:
      raise FigureRefused(MALFORMED)

   if len(text) > MAX_BLOCK_CHARACTERS:
      raise FigureRefused(OVERSIZED)

   marks = _parsed(text)
   is_object = isinstance(marks, dict)

   if not is_object:
      raise FigureRefused(MALFORMED)

   errors = list(_VALIDATOR.iter_errors(marks))

   if errors:
      raise FigureRefused(schema_reason(errors))

   check_marks(marks, anchors, options_hidden)

   return marks


def _rounded(point):
   return [round(float(point[0]), COORDINATE_DIGITS) + 0.0, round(float(point[1]), COORDINATE_DIGITS) + 0.0]


def _render_target(target):
   rendered = {"anchor": target["anchor"], "quote": None, "at": None, "row": None, "column": None, "cell": None}

   if "quote" in target:
      rendered["quote"] = normalised(target["quote"])

   if "at" in target:
      rendered["at"] = _rounded(target["at"])

   for field in ("row", "column"):
      if field in target:
         rendered[field] = target[field]

   if "cell" in target:
      rendered["cell"] = list(target["cell"])

   return rendered


def _role_of(mark, shape):
   return mark.get("role") or DEFAULT_ROLES.get(shape, CONSTRUCTED)


def _stroke_of(mark, shape, role):
   chosen = mark.get("stroke") or {}
   is_dashed = role == ERROR or shape in DASHED_SHAPES
   is_highlighter = role == HIGHLIGHT or shape == "highlight"

   return {
      "style": chosen.get("style", "dashed" if is_dashed else "solid"),
      "weight": chosen.get("weight", ROLE_WEIGHTS[role]),
      "arrow": chosen.get("arrow", "end" if shape in ARROW_SHAPES else "none"),
      "highlighter": chosen.get("highlighter", is_highlighter),
   }


class _Facts:
   def __init__(self):
      self.coordinates = []
      self.lines = []
      self.texts = []
      self.anchors = []

   def point(self, element_id, point):
      self.coordinates.append(ShownNumber(element_id, float(point[0])))
      self.coordinates.append(ShownNumber(element_id, float(point[1])))

   def target(self, element_id, target):
      self.anchors.append(ShownAnchor(element_id, target["anchor"]))

      if "at" in target:
         self.point(element_id, target["at"])

   def frozen(self):
      return MarksFacts(
         coordinates=tuple(self.coordinates),
         lines=tuple(self.lines),
         texts=tuple(self.texts),
         anchors=tuple(self.anchors),
      )


def _layout_of(window):
   return Layout(window["x"][0], window["x"][1], window["y"][0], window["y"][1], 1.0)


def _clipped(window, origin, direction):
   clipped = clip_line(_layout_of(window), origin, direction)

   if clipped is None:
      raise FigureRefused(MALFORMED)

   return [_rounded(point) for point in clipped]


def _graph_fields(shape, value, window, element_id, facts):
   """The points a construction on the item's graph draws, and its facts."""
   facts.anchors.append(ShownAnchor(element_id, ITEM_FIGURE))

   if shape == "point":
      facts.point(element_id, value["at"])

      return {"at": _rounded(value["at"]), "open": value.get("open", False)}

   if shape == "segment":
      facts.point(element_id, value["from"])
      facts.point(element_id, value["to"])

      return {"points": [_rounded(value["from"]), _rounded(value["to"])]}

   if shape == "vline":
      facts.lines.append(ShownNumber(element_id, float(value["x"])))

      return {"points": _clipped(window, (value["x"], window["y"][0]), (0.0, 1.0))}

   if shape == "hline":
      facts.lines.append(ShownNumber(element_id, float(value["y"])))

      return {"points": _clipped(window, (window["x"][0], value["y"]), (1.0, 0.0))}

   if "through" in value:
      first, second = value["through"]
      origin = (float(first[0]), float(first[1]))
      direction = (second[0] - first[0], second[1] - first[1])
      facts.point(element_id, first)
      facts.point(element_id, second)
   else:
      origin = (float(value["point"][0]), float(value["point"][1]))
      direction = (1.0, float(value["slope"]))
      facts.point(element_id, value["point"])

   for number in line_numbers(origin, direction):
      facts.lines.append(ShownNumber(element_id, number))

   return {"points": _clipped(window, origin, direction)}


def _mark_fields(shape, value, anchors, element_id, facts):
   if shape in GRAPH_SHAPES:
      return _graph_fields(shape, value, anchors.graph(), element_id, facts)

   if shape == "arrow":
      facts.target(element_id, value["from"])
      facts.target(element_id, value["to"])

      return {"from": _render_target(value["from"]), "to": _render_target(value["to"])}

   if shape == "note":
      target = {key: value[key] for key in ("anchor",) + ADDRESS_FIELDS if key in value}
      facts.target(element_id, target)
      facts.texts.append(ShownText(element_id, "note", value["text"]))

      return {"target": _render_target(target), "text": value["text"], "side": value.get("side", DEFAULT_SIDE)}

   facts.target(element_id, value)

   return {"target": _render_target(value)}


def compile_marks(marks, anchors, marks_id="marks", options_hidden=False):
   """(render_marks, facts) for marks read by read_marks against the same anchors."""
   listed = _Anchors(anchors, options_hidden)
   facts = _Facts()
   faded_at = {}
   erased_at = {}
   facts.texts.append(ShownText("marks", "description", marks["description"]))

   for step in marks["steps"]:
      facts.texts.append(ShownText(step["id"], "caption", step["caption"]))

      for mark_id in step.get("fade") or ():
         faded_at[mark_id] = step["id"]

      for mark_id in step.get("erase") or ():
         erased_at[mark_id] = step["id"]

   rendered = []

   for step_id, mark in marks_in_order(marks):
      shape = shape_of(mark)
      role = _role_of(mark, shape)
      entry = {
         "step": step_id,
         "element": mark["id"],
         "role": role,
         "stroke": _stroke_of(mark, shape, role),
         "faded_at": faded_at.get(mark["id"]),
         "erased_at": erased_at.get(mark["id"]),
         "kind": shape,
      }
      entry.update(_mark_fields(shape, mark[shape], listed, mark["id"], facts))
      rendered.append(entry)

   render = {
      "id": marks_id,
      "description": marks["description"],
      "steps": [{"id": step["id"], "caption": step["caption"]} for step in marks["steps"]],
      "marks": rendered,
   }

   return render, facts.frozen()
