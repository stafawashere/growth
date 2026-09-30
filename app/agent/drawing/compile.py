"""The figure compiler (docs/agent/drawing-design.md, The compiler and The render spec; the render
spec contract in docs/agent/drawing-build-plan.md).

compile_figure turns a figure that app/agent/drawing/spec.py has read into the render spec the
client draws and a FigureFacts record for the screen. The server computes every point: curves at
161 samples, broken where undefined or beyond ten window heights, paths at 241, points on curves,
tangent slopes by a central difference, lines clipped to the window, regions split where they
cross, Riemann and trapezoid pieces, the slope-field lattice, the solution curve by fourth-order
Runge-Kutta, Euler steps, sequences, and the marks of angles, triangles, braces, callouts and rings.
Marks that must look right on screen (a right-angle square, an equal-side tick, a ring, a brace)
are built in view units and mapped back into the world.

The layout is FigureView's (app/web/src/figures/FigureView.tsx) at a view width of 320: a padding of
20, a plot height of the window's aspect clamped between 180 and the plot width, or equal scale for
a diagram or a polar curve, where the window is widened around its centre to keep one unit the same
length on both axes. A label sits beside its element, its offset in view units, and is moved back
inside the view when its estimated box would leave it.

FigureFacts groups every number the figure shows by the channel the screen compares
(app/evals/figure_checks.py) and every text it shows. Tick positions, window bounds and expression
literals are not facts. The compiler refuses a figure as oversized past 4,000 points, 200 primitives
or 100 ms, the clock read between elements, and as malformed where a value it needs is undefined.
"""
import math
import re
import time
from dataclasses import dataclass

from app.agent.drawing import expression
from app.agent.drawing.spec import (
   CURVE_VARIABLES,
   DIAGRAM,
   FIELD_VARIABLES,
   GRAPH,
   MALFORMED,
   NUMBER_LINE,
   OVERSIZED,
   PARAMETRIC_VARIABLES,
   POLAR_VARIABLES,
   SEQUENCE_VARIABLES,
   TABLE,
   FigureRefused,
   elements_in_order,
   shape_of,
)

VIEW_WIDTH = 320
PLOT_PADDING = 20
PLOT_WIDTH = VIEW_WIDTH - 2 * PLOT_PADDING
MINIMUM_PLOT_HEIGHT = 180
MAXIMUM_PLOT_HEIGHT = PLOT_WIDTH

CURVE_SAMPLES = 161
PATH_SAMPLES = 241
MAX_POINTS = 4000
MAX_PRIMITIVES = 200
COMPILE_BUDGET_SECONDS = 0.1
ESCAPE_HEIGHTS = 10
AREA_INTERVALS = 64
ROOT_BISECTIONS = 60
DERIVATIVE_STEP = 1e-5
SLOPE_FIELD_PER_AXIS = 11
LATTICE_STEPS = tuple(mantissa * 10.0 ** power for power in range(-3, 4) for mantissa in (1, 2, 5))
GRID_STEPS = (0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)
MAXIMUM_GRIDLINES_PER_AXIS = 16
COORDINATE_DIGITS = 5
OFFSET_DIGITS = 2

LABEL_GAP = 6
CHARACTER_WIDTH = 8
LINE_HEIGHT = 14
CENTRE_DROP = 5
OUTWARD_LABEL = 12
RIGHT_ANGLE_SIDE = 10
EQUAL_SIDE_TICK = 5
ANGLE_RADIUS = 16
ANGLE_LABEL_RADIUS = 28
RING_RADIUS = 10
RING_SAMPLES = 33
ANGLE_SAMPLES = 25
BRACE_START = 2
BRACE_DEPTH = 8
BRACE_TIP = 6
LEADER_GAP = 10
LEADER_END_GAP = 4
SLOPE_SEGMENT_SHARE = 0.7
NUMBER_LINE_TICK = 5
TICK_LABEL_DROP = 16
SIGN_ROW_NAME_RISE = 8
CALLOUT_RISE = 40

GIVEN = "given"
CONSTRUCTED = "constructed"
HIGHLIGHT = "highlight"
ERROR = "error"
ROLE_WEIGHTS = {GIVEN: "regular", CONSTRUCTED: "bold", HIGHLIGHT: "bold", ERROR: "regular"}
DASHED_SHAPES = ("vline", "hline")
ARROW_SHAPES = ("vector", "callout", "parametric")
FILL_SHAPES = ("area", "riemann")

MAIN = "main"
MARK = "mark"
GUIDE = "guide"
MARK_STROKE = {"style": "solid", "weight": "thin", "arrow": "none", "highlighter": False}
GUIDE_STROKE = {"style": "dashed", "weight": "thin", "arrow": "none", "highlighter": False}
AXIS_STROKE = {"style": "solid", "weight": "regular", "arrow": "both", "highlighter": False}
FRAME_ELEMENT = "_axis"

MATH_DELIMITER = r"\\[()\[\]]"
LATEX_COMMAND = r"\\[A-Za-z]+"
LATEX_MARKUP = r"[{}^_]"


@dataclass(frozen=True)
class ShownNumber:
   element: str
   value: float


@dataclass(frozen=True)
class ShownCurve:
   element: str
   tree: tuple
   variable: str
   low: float
   high: float


@dataclass(frozen=True)
class ShownText:
   element: str
   part: str
   text: str


@dataclass(frozen=True)
class FigureFacts:
   """Every number and text a compiled figure shows, grouped by the channel the screen compares."""

   coordinates: tuple = ()
   lines: tuple = ()
   areas: tuple = ()
   approximations: tuple = ()
   constants: tuple = ()
   cells: tuple = ()
   curves: tuple = ()
   texts: tuple = ()


NUMBER_CHANNELS = ("coordinates", "lines", "areas", "approximations", "constants", "cells")


@dataclass(frozen=True)
class Layout:
   x_low: float
   x_high: float
   y_low: float
   y_high: float
   plot_height: float

   @property
   def view_height(self):
      return self.plot_height + 2 * PLOT_PADDING

   @property
   def x_span(self):
      return self.x_high - self.x_low

   @property
   def y_span(self):
      return self.y_high - self.y_low

   def view(self, point):
      x, y = point
      view_x = PLOT_PADDING + (x - self.x_low) / self.x_span * PLOT_WIDTH
      view_y = PLOT_PADDING + (self.y_high - y) / self.y_span * self.plot_height

      return (view_x, view_y)

   def world(self, view_point):
      view_x, view_y = view_point
      x = self.x_low + (view_x - PLOT_PADDING) / PLOT_WIDTH * self.x_span
      y = self.y_high - (view_y - PLOT_PADDING) / self.plot_height * self.y_span

      return (x, y)

   def clamped(self, point):
      x, y = point

      return (min(max(x, self.x_low), self.x_high), min(max(y, self.y_low), self.y_high))


@dataclass(frozen=True)
class _Curve:
   tree: tuple
   low: float
   high: float


def _plot_height(x_span, y_span):
   return min(MAXIMUM_PLOT_HEIGHT, max(MINIMUM_PLOT_HEIGHT, PLOT_WIDTH * y_span / x_span))


def _widened(low, high, span):
   centre = (low + high) / 2

   return (centre - span / 2, centre + span / 2)


def layout_for(x_range, y_range, equal_scale):
   """FigureView's layout; at equal scale the window grows about its centre on the short axis until
   one unit is as long across as up."""
   x_low, x_high = x_range
   y_low, y_high = y_range
   x_span = x_high - x_low
   y_span = y_high - y_low
   plot_height = _plot_height(x_span, y_span)

   if equal_scale:
      target_ratio = plot_height / PLOT_WIDTH
      window_ratio = y_span / x_span

      if window_ratio > target_ratio:
         x_low, x_high = _widened(x_low, x_high, y_span / target_ratio)
      elif window_ratio < target_ratio:
         y_low, y_high = _widened(y_low, y_high, x_span * target_ratio)

   return Layout(x_low, x_high, y_low, y_high, plot_height)


def _nice_step(span, steps, most):
   for step in steps:
      if span / step <= most:
         return step

   return steps[-1]


def _multiples(low, high, step):
   first = math.ceil(low / step - 1e-9)
   last = math.floor(high / step + 1e-9)

   return [index * step + 0.0 for index in range(first, last + 1)]


def tick_text(value):
   rounded = round(value, 6) + 0.0

   return str(int(rounded)) if rounded.is_integer() else repr(rounded)


def _visible_length(text):
   visible = re.sub(MATH_DELIMITER, "", text)
   visible = re.sub(LATEX_COMMAND, "x", visible)
   visible = re.sub(LATEX_MARKUP, "", visible)

   return len(visible.strip())


def _rounded_point(point):
   return [round(point[0], COORDINATE_DIGITS) + 0.0, round(point[1], COORDINATE_DIGITS) + 0.0]


def _unit(vector):
   length = math.hypot(vector[0], vector[1])

   if length == 0:
      return None

   return (vector[0] / length, vector[1] / length)


def _plus(point, vector, scale=1.0):
   return (point[0] + vector[0] * scale, point[1] + vector[1] * scale)


def _path(points, closed=False, fill="none", part=MAIN, series=False):
   return {"type": "path", "points": list(points), "closed": closed, "fill": fill, "part": part, "series": series}


def _dot(at, is_open=False):
   return {"type": "dot", "at": at, "open": is_open}


def _text_part(at, text, offset, align):
   return {"type": "label", "at": at, "text": text, "offset": offset, "align": align}


def _clamped_label(layout, anchor, text, offset, align):
   """The label with its offset moved so its estimated box stays inside the view."""
   at = layout.clamped(anchor)
   view_x, view_y = layout.view(at)
   offset_x, offset_y = offset
   width = _visible_length(text) * CHARACTER_WIDTH
   left_by_align = {"start": 0, "middle": -width / 2, "end": -width}
   left = view_x + offset_x + left_by_align[align]
   right = left + width
   baseline = view_y + offset_y
   top = baseline - LINE_HEIGHT

   if left < 0:
      offset_x -= left
   elif right > VIEW_WIDTH:
      offset_x -= right - VIEW_WIDTH

   if top < 0:
      offset_y -= top
   elif baseline > layout.view_height:
      offset_y -= baseline - layout.view_height

   return _text_part(at, text, [round(offset_x, OFFSET_DIGITS) + 0.0, round(offset_y, OFFSET_DIGITS) + 0.0], align)


def _beside(layout, anchor, text):
   """Up and to the right of the element, or to the left and below where the view runs out."""
   at = layout.clamped(anchor)
   view_x, view_y = layout.view(at)
   width = _visible_length(text) * CHARACTER_WIDTH
   runs_out_right = view_x + LABEL_GAP + width > VIEW_WIDTH
   runs_out_top = view_y - LABEL_GAP - LINE_HEIGHT < 0
   align = "end" if runs_out_right else "start"
   offset_x = -LABEL_GAP if runs_out_right else LABEL_GAP
   offset_y = LABEL_GAP + LINE_HEIGHT if runs_out_top else -LABEL_GAP

   return _clamped_label(layout, at, text, (offset_x, offset_y), align)


def _centred(layout, anchor, text):
   return _clamped_label(layout, anchor, text, (0, CENTRE_DROP), "middle")


def _outward(layout, anchor, text, direction_in_view):
   offset = (direction_in_view[0] * OUTWARD_LABEL, direction_in_view[1] * OUTWARD_LABEL + CENTRE_DROP)

   return _clamped_label(layout, anchor, text, offset, "middle")


class _Scene:
   def __init__(self, figure, layout):
      self.kind = figure["kind"]
      self.layout = layout
      self.primitives = []
      self.point_count = 0
      self.numbers = {channel: [] for channel in NUMBER_CHANNELS}
      self.shown_curves = []
      self.texts = []
      self.curves = {}
      self.points = {}
      self.anchors = {}
      self.faded_at = {}
      self.erased_at = {}

      for step in figure["steps"]:
         for element_id in step.get("fade") or ():
            self.faded_at[element_id] = step["id"]

         for element_id in step.get("erase") or ():
            self.erased_at[element_id] = step["id"]

   def number(self, channel, element_id, value):
      self.numbers[channel].append(ShownNumber(element_id, float(value)))

   def coordinates(self, element_id, *points):
      for point in points:
         self.number("coordinates", element_id, point[0])
         self.number("coordinates", element_id, point[1])

   def text(self, element_id, part, text):
      self.texts.append(ShownText(element_id, part, text))

   def curve_value(self, curve_id, x):
      curve = self.curves[curve_id]
      is_outside_domain = x < curve.low or x > curve.high

      if is_outside_domain:
         raise FigureRefused(MALFORMED)

      y = expression.evaluate(curve.tree, {"x": x})

      if y is None:
         raise FigureRefused(MALFORMED)

      return y

   def point(self, value):
      if isinstance(value, (int, float)):
         return (float(value), 0.0)

      if isinstance(value, list):
         return (float(value[0]), float(value[1]))

      if isinstance(value, str):
         return self.points[value]

      x = float(value["x"])

      return (x, self.curve_value(value["on"], x))

   def target(self, value):
      is_element = isinstance(value, str)

      if not is_element:
         return self.point(value)

      if value not in self.anchors:
         raise FigureRefused(MALFORMED)

      return self.anchors[value]

   def facts(self):
      return FigureFacts(
         coordinates=tuple(self.numbers["coordinates"]),
         lines=tuple(self.numbers["lines"]),
         areas=tuple(self.numbers["areas"]),
         approximations=tuple(self.numbers["approximations"]),
         constants=tuple(self.numbers["constants"]),
         cells=tuple(self.numbers["cells"]),
         curves=tuple(self.shown_curves),
         texts=tuple(self.texts),
      )


def _escape_band(layout):
   return (layout.y_low - ESCAPE_HEIGHTS * layout.y_span, layout.y_high + ESCAPE_HEIGHTS * layout.y_span)


def _is_inside_band(layout, y):
   return layout.y_low <= y <= layout.y_high


def _breaks_between(layout, function, previous, current):
   """Neighbouring samples sit on either side of an asymptote when the value halfway between them is
   undefined or not between theirs. Only a step that leaves the window or jumps a quarter of its
   height is looked at, so a curve turning smoothly inside the window is never broken."""
   leaves_window = not _is_inside_band(layout, previous[1]) or not _is_inside_band(layout, current[1])
   jumps = abs(current[1] - previous[1]) > layout.y_span / 4
   is_suspect = leaves_window or jumps

   if not is_suspect:
      return False

   middle = function((previous[0] + current[0]) / 2)
   low = min(previous[1], current[1])
   high = max(previous[1], current[1])
   is_between = middle is not None and low <= middle <= high

   return not is_between


def _sampled_function(layout, function, low, high, samples=CURVE_SAMPLES):
   escape_low, escape_high = _escape_band(layout)
   segments = []
   current = []

   for index in range(samples):
      x = low + (high - low) * index / (samples - 1)
      y = function(x)
      is_kept = y is not None and escape_low <= y <= escape_high

      if not is_kept:
         segments.append(current)
         current = []
         continue

      point = (x, y)
      has_previous = len(current) > 0
      starts_new_piece = has_previous and _breaks_between(layout, function, current[-1], point)

      if starts_new_piece:
         segments.append(current)
         current = []

      current.append(point)

   segments.append(current)

   return [segment for segment in segments if len(segment) > 1]


def _split_path(layout, points):
   """A sampled path, None where a sample is undefined, broken there and beyond ten window extents."""
   escape_low, escape_high = _escape_band(layout)
   x_escape_low = layout.x_low - ESCAPE_HEIGHTS * layout.x_span
   x_escape_high = layout.x_high + ESCAPE_HEIGHTS * layout.x_span
   segments = []
   current = []

   for point in points:
      is_defined = point is not None
      is_near_across = is_defined and x_escape_low <= point[0] <= x_escape_high
      is_near = is_near_across and escape_low <= point[1] <= escape_high

      if is_near:
         current.append(point)
         continue

      segments.append(current)
      current = []

   segments.append(current)

   return [segment for segment in segments if len(segment) > 1]


def _along(points, share):
   index = min(len(points) - 1, int(share * (len(points) - 1)))

   return points[index]


def _anchor_on(segments, share=0.8):
   if not segments:
      return None

   longest = max(segments, key=len)

   return _along(longest, share)


def _clip_line(layout, origin, direction):
   """The part of the line through origin along direction inside the window, or None."""
   low_parameter = -math.inf
   high_parameter = math.inf
   bounds = ((direction[0], origin[0], layout.x_low, layout.x_high), (direction[1], origin[1], layout.y_low, layout.y_high))

   for delta, start, low, high in bounds:
      if delta == 0:
         is_outside = start < low or start > high

         if is_outside:
            return None

         continue

      first = (low - start) / delta
      second = (high - start) / delta
      low_parameter = max(low_parameter, min(first, second))
      high_parameter = min(high_parameter, max(first, second))

   if low_parameter > high_parameter:
      return None

   return [_plus(origin, direction, low_parameter), _plus(origin, direction, high_parameter)]


def _line_numbers(origin, direction):
   """The slope, y-intercept and x-intercept a line shows, as far as it has them."""
   is_vertical = direction[0] == 0

   if is_vertical:
      return [origin[0]]

   slope = direction[1] / direction[0]
   y_intercept = origin[1] - slope * origin[0]
   numbers = [slope, y_intercept]

   if slope != 0:
      numbers.append(-y_intercept / slope)

   return numbers


def _line_parts(scene, element_id, origin, direction):
   clipped = _clip_line(scene.layout, origin, direction)

   for value in _line_numbers(origin, direction):
      scene.number("lines", element_id, value)

   if clipped is None:
      return [], None

   start, end = clipped
   anchor = (start[0] + 0.85 * (end[0] - start[0]), start[1] + 0.85 * (end[1] - start[1]))

   return [_path(clipped)], anchor


def _curve(scene, element):
   value = element["curve"]
   is_plain = isinstance(value, str)
   text = value if is_plain else value["y"]
   domain = None if is_plain else value.get("domain")
   tree = expression.parse(text, CURVE_VARIABLES)
   domain_low, domain_high = domain if domain is not None else (-math.inf, math.inf)
   low = max(scene.layout.x_low, domain_low)
   high = min(scene.layout.x_high, domain_high)
   scene.curves[element["id"]] = _Curve(tree, domain_low, domain_high)
   is_constant = not expression.variables_of(tree)

   if is_constant:
      constant = expression.evaluate(tree, {})

      if constant is not None:
         scene.number("constants", element["id"], constant)

   is_visible = low < high

   if not is_visible:
      return [], None

   if not is_constant:
      scene.shown_curves.append(ShownCurve(element["id"], tree, "x", low, high))

   segments = _sampled_function(scene.layout, lambda x: expression.evaluate(tree, {"x": x}), low, high)

   return [_path(segment, series=True) for segment in segments], _anchor_on(segments)


def _parametric(scene, element):
   value = element["parametric"]
   x_tree = expression.parse(value["x"], PARAMETRIC_VARIABLES)
   y_tree = expression.parse(value["y"], PARAMETRIC_VARIABLES)
   low, high = value["t"]
   points = []

   for index in range(PATH_SAMPLES):
      t = low + (high - low) * index / (PATH_SAMPLES - 1)
      x = expression.evaluate(x_tree, {"t": t})
      y = expression.evaluate(y_tree, {"t": t})
      is_defined = x is not None and y is not None
      points.append((x, y) if is_defined else None)

   segments = _split_path(scene.layout, points)

   return [_path(segment, series=True) for segment in segments], _anchor_on(segments)


def _polar(scene, element):
   value = element["polar"]
   tree = expression.parse(value["r"], POLAR_VARIABLES)
   low, high = value["theta"]
   points = []

   for index in range(PATH_SAMPLES):
      theta = low + (high - low) * index / (PATH_SAMPLES - 1)
      radius = expression.evaluate(tree, {"theta": theta})
      points.append(None if radius is None else (radius * math.cos(theta), radius * math.sin(theta)))

   segments = _split_path(scene.layout, points)

   return [_path(segment, series=True) for segment in segments], _anchor_on(segments)


def _point(scene, element):
   at = scene.point(element["point"])
   scene.points[element["id"]] = at
   scene.coordinates(element["id"], at)

   return [_dot(at, element.get("open", False))], at


def _line(scene, element):
   value = element["line"]

   if "through" in value:
      first, second = (scene.point(point) for point in value["through"])
      direction = (second[0] - first[0], second[1] - first[1])
      scene.coordinates(element["id"], first, second)
   else:
      first = scene.point(value["point"])
      direction = (1.0, float(value["slope"]))
      scene.coordinates(element["id"], first)

   if _unit(direction) is None:
      raise FigureRefused(MALFORMED)

   return _line_parts(scene, element["id"], first, direction)


def _segment(scene, element):
   first, second = (scene.point(point) for point in element["segment"])
   scene.coordinates(element["id"], first, second)
   middle = ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)

   return [_path([first, second])], middle


def _secant(scene, element):
   value = element["secant"]
   first_x, second_x = value["x"]
   first = (float(first_x), scene.curve_value(value["on"], first_x))
   second = (float(second_x), scene.curve_value(value["on"], second_x))
   scene.coordinates(element["id"], first, second)
   direction = (second[0] - first[0], second[1] - first[1])

   return _line_parts(scene, element["id"], first, direction)


def _tangent_slope(scene, curve_id, x):
   step = DERIVATIVE_STEP * max(1.0, abs(x))
   ahead = scene.curve_value(curve_id, x + step)
   behind = scene.curve_value(curve_id, x - step)

   return (ahead - behind) / (2 * step)


def _tangent(scene, element):
   value = element["tangent"]
   x = float(value["x"])
   touching = (x, scene.curve_value(value["on"], x))
   slope = _tangent_slope(scene, value["on"], x)
   direction = (1.0, slope)
   scene.coordinates(element["id"], touching)
   has_length = "length" in value

   if not has_length:
      return _line_parts(scene, element["id"], touching, direction)

   for number in _line_numbers(touching, direction):
      scene.number("lines", element["id"], number)

   unit = _unit(direction)
   half = value["length"] / 2
   start = _plus(touching, unit, -half)
   end = _plus(touching, unit, half)

   return [_path([start, end])], end


def _vline(scene, element):
   x = float(element["vline"])
   scene.number("lines", element["id"], x)

   return [_path([(x, scene.layout.y_low), (x, scene.layout.y_high)])], (x, scene.layout.y_high)


def _hline(scene, element):
   y = float(element["hline"])
   scene.number("lines", element["id"], y)

   return [_path([(scene.layout.x_low, y), (scene.layout.x_high, y)])], (scene.layout.x_high, y)


def _simpson(function, low, high, intervals=AREA_INTERVALS):
   width = (high - low) / intervals
   total = function(low) + function(high)

   for index in range(1, intervals):
      weight = 4 if index % 2 == 1 else 2
      total += weight * function(low + index * width)

   return total * width / 3


def _bisected_root(function, low, high):
   low_value = function(low)

   for _ in range(ROOT_BISECTIONS):
      middle = (low + high) / 2
      middle_value = function(middle)
      has_same_sign = (middle_value > 0) == (low_value > 0)

      if has_same_sign:
         low, low_value = middle, middle_value
      else:
         high = middle

   return (low + high) / 2


def _breakpoints(function, low, high):
   """The ends of the interval and every place between where the function changes sign."""
   grid = [low + (high - low) * index / (CURVE_SAMPLES - 1) for index in range(CURVE_SAMPLES)]
   values = [function(x) for x in grid]
   points = [low]

   for index in range(1, len(grid)):
      previous_value = values[index - 1]
      value = values[index]
      is_interior_zero = value == 0 and previous_value != 0 and index < len(grid) - 1
      changes_sign = previous_value * value < 0

      if is_interior_zero:
         points.append(grid[index])
      elif changes_sign:
         points.append(_bisected_root(function, grid[index - 1], grid[index]))

   points.append(high)

   return sorted(set(points)), grid


def _strict(function):
   def defined(x):
      value = function(x)

      if value is None:
         raise FigureRefused(MALFORMED)

      return value

   return defined


def _clamped_polygon(layout, points):
   return [layout.clamped(point) for point in points]


def _area(scene, element):
   value = element["area"]
   low = float(value["from"])
   high = float(value["to"])
   is_between = "between" in value
   upper_id, lower_id = value["between"] if is_between else (value["under"], None)
   upper = _strict(lambda x: scene.curve_value(upper_id, x))
   lower = _strict(lambda x: scene.curve_value(lower_id, x)) if is_between else (lambda x: 0.0)
   height = _strict(lambda x: upper(x) - lower(x))
   breakpoints, grid = _breakpoints(height, low, high)
   parts = []
   labels = []
   signed = 0.0
   absolute = 0.0
   largest = None

   for piece_low, piece_high in zip(breakpoints, breakpoints[1:]):
      inside = [x for x in grid if piece_low < x < piece_high]
      xs = [piece_low] + inside + [piece_high]
      middle = (piece_low + piece_high) / 2
      integral = _simpson(height, piece_low, piece_high)
      is_below = height(middle) < 0
      outline = [(x, upper(x)) for x in xs] + [(x, lower(x)) for x in reversed(xs)]
      fill = "region_below" if is_below else "region"
      parts.append(_path(_clamped_polygon(scene.layout, outline), closed=True, fill=fill))
      labels.append(((middle, (upper(middle) + lower(middle)) / 2), "\\(-\\)" if is_below else "\\(+\\)", is_below))
      signed += integral
      absolute += abs(integral)
      is_largest = largest is None or abs(integral) > largest[0]

      if is_largest:
         largest = (abs(integral), (middle, max(upper(middle), lower(middle))))

   scene.number("areas", element["id"], signed)
   scene.number("areas", element["id"], absolute)
   has_below_part = any(is_below for _at, _text, is_below in labels)

   if has_below_part:
      for at, text, _is_below in labels:
         parts.append(_centred(scene.layout, at, text))

   return parts, largest[1] if largest is not None else None


def _riemann(scene, element):
   value = element["riemann"]
   low = float(value["from"])
   high = float(value["to"])
   count = value["n"]
   rule = value["rule"]
   curve = _strict(lambda x: scene.curve_value(value["on"], x))
   width = (high - low) / count
   parts = []
   dots = []
   total = 0.0

   for index in range(count):
      left = low + index * width
      right = left + width

      if rule == "trapezoid":
         left_height = curve(left)
         right_height = curve(right)
         outline = [(left, 0.0), (left, left_height), (right, right_height), (right, 0.0)]
         piece_total = (left_height + right_height) / 2 * width
         is_below = left_height + right_height < 0
         dots.append((left, left_height))

         if index == count - 1:
            dots.append((right, right_height))
      else:
         sample = {"left": left, "right": right, "midpoint": (left + right) / 2}[rule]
         sample_height = curve(sample)
         outline = [(left, 0.0), (left, sample_height), (right, sample_height), (right, 0.0)]
         piece_total = sample_height * width
         is_below = sample_height < 0
         dots.append((sample, sample_height))

      fill = "region_below" if is_below else "region"
      parts.append(_path(_clamped_polygon(scene.layout, outline), closed=True, fill=fill))
      total += piece_total

   scene.number("approximations", element["id"], total)
   scene.coordinates(element["id"], *dots)
   parts.extend(_dot(dot) for dot in dots)
   middle_piece = parts[count // 2]["points"]

   return parts, max(middle_piece[1:3], key=lambda point: point[1])


def _lattice(low, high):
   step = _nice_step(high - low, LATTICE_STEPS, SLOPE_FIELD_PER_AXIS - 1)

   return _multiples(low, high, step), step


def _slope_field(scene, element):
   layout = scene.layout
   tree = expression.parse(element["slope_field"]["dy"], FIELD_VARIABLES)
   xs, x_step = _lattice(layout.x_low, layout.x_high)
   ys, y_step = _lattice(layout.y_low, layout.y_high)
   x_scale = PLOT_WIDTH / layout.x_span
   y_scale = layout.plot_height / layout.y_span
   half_length = SLOPE_SEGMENT_SHARE * min(x_step * x_scale, y_step * y_scale) / 2
   parts = []

   for x in xs:
      for y in ys:
         slope = expression.evaluate(tree, {"x": x, "y": y})

         if slope is None:
            continue

         direction = _unit((x_scale, -slope * y_scale))
         centre = layout.view((x, y))
         start = layout.world(_plus(centre, direction, -half_length))
         end = layout.world(_plus(centre, direction, half_length))
         parts.append(_path([start, end]))

   return parts, (layout.x_high, layout.y_high)


def _slope(tree, x, y):
   return expression.evaluate(tree, {"x": x, "y": y})


def _runge_kutta_step(tree, x, y, step):
   first = _slope(tree, x, y)

   if first is None:
      return None

   second = _slope(tree, x + step / 2, y + step / 2 * first)

   if second is None:
      return None

   third = _slope(tree, x + step / 2, y + step / 2 * second)

   if third is None:
      return None

   fourth = _slope(tree, x + step, y + step * third)

   if fourth is None:
      return None

   return y + step / 6 * (first + 2 * second + 2 * third + fourth)


def _traced(scene, tree, start, step, count):
   escape_low, escape_high = _escape_band(scene.layout)
   x, y = start
   points = [start]

   for _ in range(count):
      y = _runge_kutta_step(tree, x, y, step)
      x += step
      has_left = y is None or not escape_low <= y <= escape_high

      if has_left:
         break

      points.append((x, y))

   return points


def _solution(scene, element):
   value = element["solution"]
   tree = expression.parse(value["dy"], FIELD_VARIABLES)
   start = scene.point(value["through"])
   low = min(start[0], scene.layout.x_low)
   high = max(start[0], scene.layout.x_high)
   steps = PATH_SAMPLES - 1
   step = (high - low) / steps
   forward_steps = round(steps * (high - start[0]) / (high - low))
   backward_steps = steps - forward_steps
   forward = _traced(scene, tree, start, step, forward_steps)
   backward = _traced(scene, tree, start, -step, backward_steps)
   points = list(reversed(backward[1:])) + forward

   if len(points) < 2:
      return [], start

   return [_path(points, series=True)], _along(points, 0.8)


def _euler(scene, element):
   value = element["euler"]
   tree = expression.parse(value["dy"], FIELD_VARIABLES)
   x, y = scene.point(value["start"])
   step = float(value["h"])
   points = [(x, y)]

   for _ in range(value["n"]):
      slope = _slope(tree, x, y)

      if slope is None:
         raise FigureRefused(MALFORMED)

      y = y + step * slope
      x = x + step
      points.append((x, y))

   scene.coordinates(element["id"], *points)

   return [_path(points)] + [_dot(point) for point in points], points[-1]


def _sequence(scene, element):
   value = element["sequence"]
   tree = expression.parse(value["a"], SEQUENCE_VARIABLES)
   first, last = value["n"]
   adds_up = value.get("sums", False)
   running = 0.0
   dots = []

   for index in range(first, last + 1):
      term = expression.evaluate(tree, {"n": index})

      if term is None:
         raise FigureRefused(MALFORMED)

      running += term
      shown = running if adds_up else term
      dots.append((float(index), shown))
      scene.number("coordinates", element["id"], shown)

   return [_dot(dot) for dot in dots], dots[-1]


def _vector(scene, element):
   value = element["vector"]
   start = scene.point(value["from"])

   if "to" in value:
      end = scene.point(value["to"])
   else:
      horizontal, vertical = value["components"]
      end = (start[0] + horizontal, start[1] + vertical)
      scene.number("coordinates", element["id"], horizontal)
      scene.number("coordinates", element["id"], vertical)

   scene.coordinates(element["id"], start, end)
   parts = [_path([start, end])]

   if value.get("legs", False):
      corner = (end[0], start[1])
      parts.append(_path([start, corner], part=GUIDE))
      parts.append(_path([corner, end], part=GUIDE))

   return parts, end


def _circle_points(centre, radius, start_degrees, sweep_degrees, samples):
   points = []

   for index in range(samples):
      angle = math.radians(start_degrees + sweep_degrees * index / (samples - 1))
      points.append((centre[0] + radius * math.cos(angle), centre[1] + radius * math.sin(angle)))

   return points


def _circle(scene, element):
   value = element["circle"]
   centre = scene.point(value["center"])
   radius = float(value["radius"])
   scene.coordinates(element["id"], centre)
   scene.number("coordinates", element["id"], radius)
   points = _circle_points(centre, radius, 0, 360, PATH_SAMPLES)[:-1]
   anchor = (centre[0] + radius * math.cos(math.pi / 4), centre[1] + radius * math.sin(math.pi / 4))

   return [_path(points, closed=True)], anchor


def _arc(scene, element):
   value = element["arc"]
   centre = scene.point(value["center"])
   radius = float(value["radius"])
   start = float(value["from"])
   end = float(value["to"])

   while end <= start:
      end += 360

   sweep = min(end - start, 360)
   samples = max(9, math.ceil(PATH_SAMPLES * sweep / 360))
   scene.coordinates(element["id"], centre)
   scene.number("coordinates", element["id"], radius)
   points = _circle_points(centre, radius, start, sweep, samples)

   return [_path(points)], _along(points, 0.5)


def _view_directions(scene, vertex, first, second):
   layout = scene.layout
   vertex_view = layout.view(vertex)
   first_view = layout.view(first)
   second_view = layout.view(second)
   first_direction = _unit((first_view[0] - vertex_view[0], first_view[1] - vertex_view[1]))
   second_direction = _unit((second_view[0] - vertex_view[0], second_view[1] - vertex_view[1]))
   is_degenerate = first_direction is None or second_direction is None

   if is_degenerate:
      raise FigureRefused(MALFORMED)

   return vertex_view, first_direction, second_direction


def _angle(scene, element):
   value = element["angle"]
   vertex = scene.point(value["at"])
   vertex_view, first_direction, second_direction = _view_directions(
      scene, vertex, scene.point(value["from"]), scene.point(value["to"])
   )
   start = math.atan2(first_direction[1], first_direction[0])
   sweep = (math.atan2(second_direction[1], second_direction[0]) - start) % (2 * math.pi)

   if sweep > math.pi:
      start += sweep
      sweep = 2 * math.pi - sweep

   arc = []

   for index in range(ANGLE_SAMPLES):
      angle = start + sweep * index / (ANGLE_SAMPLES - 1)
      arc.append(scene.layout.world(_plus(vertex_view, (math.cos(angle), math.sin(angle)), ANGLE_RADIUS)))

   bisector = start + sweep / 2
   anchor = scene.layout.world(_plus(vertex_view, (math.cos(bisector), math.sin(bisector)), ANGLE_LABEL_RADIUS))

   return [_path(arc)], anchor


def _right_angle_mark(scene, vertex_view, first_direction, second_direction, part=MARK):
   corner_one = _plus(vertex_view, first_direction, RIGHT_ANGLE_SIDE)
   corner_two = _plus(corner_one, second_direction, RIGHT_ANGLE_SIDE)
   corner_three = _plus(vertex_view, second_direction, RIGHT_ANGLE_SIDE)
   points = [scene.layout.world(point) for point in (corner_one, corner_two, corner_three)]

   return _path(points, part=part)


def _right_angle(scene, element):
   value = element["right_angle"]
   vertex = scene.point(value["at"])
   vertex_view, first_direction, second_direction = _view_directions(
      scene, vertex, scene.point(value["from"]), scene.point(value["to"])
   )
   outward = _unit(_plus(first_direction, second_direction)) or first_direction
   anchor = scene.layout.world(_plus(vertex_view, outward, 2 * RIGHT_ANGLE_SIDE))

   return [_right_angle_mark(scene, vertex_view, first_direction, second_direction, part=MAIN)], anchor


def _box(scene, element):
   value = element["box"]
   corner = scene.point(value["at"])
   width = float(value["width"])
   height = float(value["height"])
   corners = [
      corner,
      (corner[0] + width, corner[1]),
      (corner[0] + width, corner[1] + height),
      (corner[0], corner[1] + height),
   ]
   scene.coordinates(element["id"], *corners)
   scene.number("coordinates", element["id"], width)
   scene.number("coordinates", element["id"], height)
   parts = [_path(corners, closed=True)]
   text = value.get("text")

   if text is not None:
      scene.text(element["id"], "box text", text)
      centre = (corner[0] + width / 2, corner[1] + height / 2)
      parts.append(_centred(scene.layout, centre, text))

   return parts, corners[3]


def _rotated(points, pivot, degrees):
   angle = math.radians(degrees)
   cosine = math.cos(angle)
   sine = math.sin(angle)
   turned = []

   for x, y in points:
      dx = x - pivot[0]
      dy = y - pivot[1]
      turned.append((pivot[0] + dx * cosine - dy * sine, pivot[1] + dx * sine + dy * cosine))

   return turned


def _triangle_vertices(scene, element_id, value):
   kind = value["kind"]

   if kind == "scalene":
      vertices = [scene.point(point) for point in value["vertices"]]
   else:
      corner = scene.point(value["at"])

      if kind == "equilateral":
         side = float(value["side"])
         base, height = side, side * math.sqrt(3) / 2
         scene.number("coordinates", element_id, side)
      else:
         base, height = float(value["base"]), float(value["height"])
         scene.number("coordinates", element_id, base)
         scene.number("coordinates", element_id, height)

      apex_x = 0.0 if kind == "right" else base / 2
      vertices = [corner, (corner[0] + base, corner[1]), (corner[0] + apex_x, corner[1] + height)]

   return _rotated(vertices, vertices[0], float(value.get("rotate", 0)))


def _equal_side_tick(scene, first, second):
   layout = scene.layout
   first_view = layout.view(first)
   second_view = layout.view(second)
   middle = ((first_view[0] + second_view[0]) / 2, (first_view[1] + second_view[1]) / 2)
   along = _unit((second_view[0] - first_view[0], second_view[1] - first_view[1]))

   if along is None:
      raise FigureRefused(MALFORMED)

   across = (-along[1], along[0])
   ends = [_plus(middle, across, -EQUAL_SIDE_TICK), _plus(middle, across, EQUAL_SIDE_TICK)]

   return _path([layout.world(point) for point in ends], part=MARK)


def _triangle(scene, element):
   value = element["triangle"]
   layout = scene.layout
   vertices = _triangle_vertices(scene, element["id"], value)
   scene.coordinates(element["id"], *vertices)
   parts = [_path(vertices, closed=True)]
   sides = list(zip(vertices, vertices[1:] + vertices[:1]))

   if value["kind"] == "right":
      vertex_view, first_direction, second_direction = _view_directions(scene, *vertices)
      parts.append(_right_angle_mark(scene, vertex_view, first_direction, second_direction))
   elif value["kind"] == "isosceles":
      parts.extend(_equal_side_tick(scene, *side) for side in sides[1:])
   elif value["kind"] == "equilateral":
      parts.extend(_equal_side_tick(scene, *side) for side in sides)

   centre_view = layout.view((sum(x for x, _y in vertices) / 3, sum(y for _x, y in vertices) / 3))

   for vertex, name in zip(vertices, value.get("names") or ()):
      vertex_view = layout.view(vertex)
      outward = _unit((vertex_view[0] - centre_view[0], vertex_view[1] - centre_view[1])) or (0.0, -1.0)
      scene.text(element["id"], "vertex name", name)
      parts.append(_outward(layout, vertex, name, outward))

   for (first, second), side_label in zip(sides, value.get("sides") or ()):
      middle = ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)
      middle_view = layout.view(middle)
      outward = _unit((middle_view[0] - centre_view[0], middle_view[1] - centre_view[1])) or (0.0, -1.0)
      scene.text(element["id"], "side label", side_label)
      parts.append(_outward(layout, middle, side_label, outward))

   return parts, vertices[2]


def _polygon(scene, element):
   vertices = [scene.point(point) for point in element["polygon"]]
   scene.coordinates(element["id"], *vertices)

   return [_path(vertices, closed=True)], vertices[0]


def _brace_parts(scene, element_id, start, end, text, side):
   layout = scene.layout
   start_view = layout.view(start)
   end_view = layout.view(end)
   along = _unit((end_view[0] - start_view[0], end_view[1] - start_view[1]))

   if along is None:
      raise FigureRefused(MALFORMED)

   left = (along[1], -along[0])
   normal = left if side == "left" else (-left[0], -left[1])
   middle = ((start_view[0] + end_view[0]) / 2, (start_view[1] + end_view[1]) / 2)
   outline = [
      _plus(start_view, normal, BRACE_START),
      _plus(start_view, normal, BRACE_DEPTH),
      _plus(middle, normal, BRACE_DEPTH),
      _plus(middle, normal, BRACE_DEPTH + BRACE_TIP),
      _plus(middle, normal, BRACE_DEPTH),
      _plus(end_view, normal, BRACE_DEPTH),
      _plus(end_view, normal, BRACE_START),
   ]
   tip = layout.world(outline[3])
   parts = [_path([layout.world(point) for point in outline])]

   if text is not None:
      scene.text(element_id, "brace text", text)
      parts.append(_outward(layout, tip, text, normal))

   return parts, tip


def _brace(scene, element):
   value = element["brace"]
   start = scene.point(value["from"])
   end = scene.point(value["to"])

   return _brace_parts(scene, element["id"], start, end, value.get("text"), value.get("side", "left"))


def _text(scene, element):
   value = element["text"]
   at = scene.point(value["at"])
   scene.text(element["id"], "text", value["text"])

   return [_centred(scene.layout, at, value["text"])], at


def _leader(scene, at, target):
   layout = scene.layout
   at_view = layout.view(at)
   target_view = layout.view(target)
   direction = _unit((target_view[0] - at_view[0], target_view[1] - at_view[1]))
   is_long_enough = direction is not None and math.dist(at_view, target_view) > LEADER_GAP + LEADER_END_GAP

   if not is_long_enough:
      return []

   start = layout.world(_plus(at_view, direction, LEADER_GAP))
   end = layout.world(_plus(target_view, direction, -LEADER_END_GAP))

   return [_path([start, end])]


def _target_point(scene, element_id, target):
   resolved = scene.target(target)
   is_written_out = not isinstance(target, str)

   if is_written_out:
      if scene.kind == NUMBER_LINE:
         scene.number("coordinates", element_id, resolved[0])
      else:
         scene.coordinates(element_id, resolved)

   return resolved


def _callout(scene, element):
   value = element["callout"]
   target = _target_point(scene, element["id"], value["target"])
   at = scene.point(value["at"])
   scene.text(element["id"], "callout", value["text"])

   return _leader(scene, at, target) + [_centred(scene.layout, at, value["text"])], at


def _ring_path(scene, target):
   centre = scene.layout.view(target)
   points = []

   for index in range(RING_SAMPLES - 1):
      angle = 2 * math.pi * index / (RING_SAMPLES - 1)
      points.append(scene.layout.world(_plus(centre, (math.cos(angle), math.sin(angle)), RING_RADIUS)))

   return _path(points, closed=True)


def _ring(scene, element):
   target = _target_point(scene, element["id"], element["ring"]["target"])

   return [_ring_path(scene, target)], target


def _line_point(scene, element):
   position = float(element["point"])
   at = (position, 0.0)
   scene.points[element["id"]] = at
   scene.number("coordinates", element["id"], position)

   return [_dot(at, element.get("open", False))], at


def _interval(scene, element):
   value = element["interval"]
   layout = scene.layout
   low = value["from"]
   high = value["to"]
   open_low, open_high = value.get("open", [False, False])
   start = layout.x_low if low is None else float(low)
   end = layout.x_high if high is None else float(high)
   arrow = {(True, True): "both", (True, False): "start", (False, True): "end", (False, False): "none"}
   path = _path([(start, 0.0), (end, 0.0)])
   path["arrow"] = arrow[(low is None, high is None)]
   parts = [path]

   for bound, is_open in ((low, open_low), (high, open_high)):
      if bound is not None:
         scene.number("coordinates", element["id"], bound)
         parts.append(_dot((float(bound), 0.0), is_open))

   return parts, ((start + end) / 2, 0.0)


def _signs(scene, element, row):
   value = element["signs"]
   layout = scene.layout
   level = float(row)
   critical_values = [float(point) for point in value["at"]]
   undefined_values = set(value.get("undefined") or ())
   parts = [_path([(layout.x_low, level), (layout.x_high, level)], part=MARK)]
   scene.text(element["id"], "sign row name", value["name"])
   parts.append(_clamped_label(layout, (layout.x_low, level), value["name"], (2, -SIGN_ROW_NAME_RISE), "start"))

   for point in critical_values:
      scene.number("coordinates", element["id"], point)
      parts.append(_path([(point, 0.0), (point, level)], part=GUIDE))
      parts.append(_dot((point, level), point in undefined_values))

   edges = [layout.x_low] + critical_values + [layout.x_high]

   for (low, high), sign in zip(zip(edges, edges[1:]), value["signs"]):
      text = "\\(+\\)" if sign == "+" else "\\(-\\)"
      parts.append(_clamped_label(layout, ((low + high) / 2, level), text, (0, -LABEL_GAP), "middle"))

   return parts, (layout.x_low, level)


def _line_text(scene, element):
   value = element["text"]
   at = scene.point(value["at"])
   scene.text(element["id"], "text", value["text"])

   return [_clamped_label(scene.layout, at, value["text"], (0, -OUTWARD_LABEL), "middle")], at


def _line_brace(scene, element):
   value = element["brace"]
   start = (float(value["from"]), 0.0)
   end = (float(value["to"]), 0.0)

   return _brace_parts(scene, element["id"], start, end, value.get("text"), value.get("side", "right"))


def _line_callout(scene, element):
   value = element["callout"]
   target = _target_point(scene, element["id"], value["target"])
   raised = scene.layout.world(_plus(scene.layout.view((float(value["at"]), 0.0)), (0.0, -1.0), CALLOUT_RISE))
   scene.text(element["id"], "callout", value["text"])

   return _leader(scene, raised, target) + [_centred(scene.layout, raised, value["text"])], raised


def _line_segment(scene, element):
   first, second = (float(point) for point in element["segment"])
   scene.number("coordinates", element["id"], first)
   scene.number("coordinates", element["id"], second)

   return [_path([(first, 0.0), (second, 0.0)])], ((first + second) / 2, 0.0)


GRAPH_SHAPES = {
   "curve": _curve,
   "parametric": _parametric,
   "polar": _polar,
   "point": _point,
   "line": _line,
   "segment": _segment,
   "secant": _secant,
   "tangent": _tangent,
   "vline": _vline,
   "hline": _hline,
   "area": _area,
   "riemann": _riemann,
   "slope_field": _slope_field,
   "solution": _solution,
   "euler": _euler,
   "sequence": _sequence,
   "vector": _vector,
   "circle": _circle,
   "arc": _arc,
   "angle": _angle,
   "right_angle": _right_angle,
   "box": _box,
   "triangle": _triangle,
   "polygon": _polygon,
   "brace": _brace,
   "text": _text,
   "callout": _callout,
   "ring": _ring,
}

NUMBER_LINE_SHAPES = {
   "point": _line_point,
   "interval": _interval,
   "text": _line_text,
   "brace": _line_brace,
   "callout": _line_callout,
   "ring": _ring,
   "segment": _line_segment,
}

CENTRED_LABEL_SHAPES = ("angle",)


def _role_of(element):
   return element.get("role") or CONSTRUCTED


def _stroke_for(element, shape, part):
   if part == MARK:
      return dict(MARK_STROKE)

   if part == GUIDE:
      return dict(GUIDE_STROKE)

   role = _role_of(element)
   chosen = element.get("stroke") or {}
   is_dashed = role == ERROR or shape in DASHED_SHAPES
   weight = "thin" if shape in FILL_SHAPES else ROLE_WEIGHTS[role]

   return {
      "style": chosen.get("style", "dashed" if is_dashed else "solid"),
      "weight": chosen.get("weight", weight),
      "arrow": chosen.get("arrow", "end" if shape in ARROW_SHAPES else "none"),
      "highlighter": chosen.get("highlighter", role == HIGHLIGHT),
   }


def _series_arrow(arrow, index, count):
   """A path broken into pieces keeps a start arrow on its first piece and an end arrow on its last."""
   has_start = arrow in ("start", "both") and index == 0
   has_end = arrow in ("end", "both") and index == count - 1

   if has_start and has_end:
      return "both"

   if has_start:
      return "start"

   return "end" if has_end else "none"


def _primitive(part, step_id, element_id, role, stroke, faded_at, erased_at):
   primitive = {"type": part["type"], "step": step_id, "element": element_id, "role": role}

   if part["type"] == "path":
      primitive.update(
         points=[_rounded_point(point) for point in part["points"]],
         closed=part["closed"],
         fill=part["fill"],
         style=stroke["style"],
         weight=stroke["weight"],
         arrow=stroke["arrow"],
         highlighter=stroke["highlighter"],
      )
   elif part["type"] == "dot":
      primitive.update(at=_rounded_point(part["at"]), open=part["open"])
   elif part["type"] == "label":
      primitive.update(at=_rounded_point(part["at"]), offset=part["offset"], align=part["align"], text=part["text"])
   else:
      primitive.update(row=part["row"], column=part["column"])

      if part.get("text") is not None:
         primitive["text"] = part["text"]

   primitive.update(faded_at=faded_at, erased_at=erased_at)

   return primitive


def _emit(scene, step_id, element, shape, parts):
   element_id = element["id"]
   default_role = HIGHLIGHT if scene.kind == TABLE else CONSTRUCTED
   role = element.get("role") or default_role
   faded_at = scene.faded_at.get(element_id)
   erased_at = scene.erased_at.get(element_id)
   series_count = sum(1 for part in parts if part.get("series"))
   series_index = 0

   for part in parts:
      stroke = None

      if part["type"] == "path":
         stroke = _stroke_for(element, shape, part["part"])

         if part["closed"]:
            stroke["arrow"] = "none"
         elif "arrow" in part:
            stroke["arrow"] = part["arrow"]
         elif part["series"]:
            stroke["arrow"] = _series_arrow(stroke["arrow"], series_index, series_count)
            series_index += 1

         scene.point_count += len(part["points"])
      elif part["type"] in ("dot", "label"):
         scene.point_count += 1

      scene.primitives.append(_primitive(part, step_id, element_id, role, stroke, faded_at, erased_at))


def _number_line_step(layout):
   """The finest gridline step whose numbers fit side by side along the line."""
   for step in GRID_STEPS:
      values = _multiples(layout.x_low, layout.x_high, step)
      widest = max((len(tick_text(value)) for value in values), default=0) * CHARACTER_WIDTH
      spacing = step / layout.x_span * PLOT_WIDTH
      has_few_enough = len(values) <= MAXIMUM_GRIDLINES_PER_AXIS + 1
      has_room = spacing >= widest + LABEL_GAP

      if has_few_enough and has_room:
         return step

   return GRID_STEPS[-1]


def _frame_parts(scene):
   """The line, ticks and tick numbers of a number line, which the client does not draw itself."""
   layout = scene.layout
   parts = []
   axis = _path([(layout.x_low, 0.0), (layout.x_high, 0.0)])
   axis["stroke"] = AXIS_STROKE
   parts.append(axis)
   step = _number_line_step(layout)
   tick_rise = layout.y_span / layout.plot_height * NUMBER_LINE_TICK

   for value in _multiples(layout.x_low, layout.x_high, step):
      tick = _path([(value, -tick_rise), (value, tick_rise)])
      tick["stroke"] = MARK_STROKE
      parts.append(tick)
      parts.append(_clamped_label(layout, (value, 0.0), tick_text(value), (0, TICK_LABEL_DROP), "middle"))

   return parts


def _emit_frame(scene, step_id):
   for part in _frame_parts(scene):
      stroke = dict(part.get("stroke", MARK_STROKE))
      is_path = part["type"] == "path"

      if is_path:
         scene.point_count += len(part["points"])
      else:
         scene.point_count += 1

      scene.primitives.append(_primitive(part, step_id, FRAME_ELEMENT, GIVEN, stroke, None, None))


def _table_parts(scene, element):
   shape = shape_of(element)
   value = element[shape]
   row = value.get("row")
   column = value.get("column")

   if "cell" in value:
      row, column = value["cell"]

   text = value.get("text") if shape == "callout" else element.get("label")

   if shape == "callout":
      scene.text(element["id"], "callout", text)

   return shape, [{"type": "cell", "row": row, "column": column, "text": text}]


def _cell_number(text):
   plain = re.sub(MATH_DELIMITER, " ", text).strip()

   try:
      tree = expression.parse(plain, ())
   except expression.ExpressionRefused:
      return None

   return expression.evaluate(tree, {})


def _table_facts(scene, figure):
   for column_index, column in enumerate(figure["columns"]):
      scene.text(f"column {column_index}", "column", column)

   for row_index, row in enumerate(figure["rows"]):
      for column_index, cell in enumerate(row):
         place = f"row {row_index}, column {column_index}"
         scene.text(place, "cell", cell)
         value = _cell_number(cell)

         if value is not None:
            scene.number("cells", place, value)


def _check_budget(scene, started, clock, budget):
   is_late = clock() - started > budget
   has_too_many_points = scene.point_count > MAX_POINTS
   has_too_many_primitives = len(scene.primitives) > MAX_PRIMITIVES

   is_oversized = is_late or has_too_many_points or has_too_many_primitives

   if is_oversized:
      raise FigureRefused(OVERSIZED)


def _figure_texts(scene, figure):
   scene.text("figure", "title", figure["title"])
   scene.text("figure", "description", figure["description"])

   for step in figure["steps"]:
      scene.text(step["id"], "caption", step["caption"])

   for axis, title in (figure.get("axes") or {}).items():
      scene.text("figure", f"{axis} axis title", title)

   for _step_id, element in elements_in_order(figure):
      if "label" in element:
         scene.text(element["id"], "label", element["label"])


def _layout_of(figure):
   kind = figure["kind"]

   if kind == TABLE:
      return None, False

   x_range = figure["window"]["x"]

   if kind == NUMBER_LINE:
      rows = sum(1 for _step_id, element in elements_in_order(figure) if "signs" in element)

      return layout_for(x_range, (-1.0, rows + 1.0), False), False

   has_polar = any("polar" in element for _step_id, element in elements_in_order(figure))
   equal_scale = kind == DIAGRAM or has_polar

   return layout_for(x_range, figure["window"]["y"], equal_scale), equal_scale


def _compiled_element(scene, element, shape, sign_rows):
   if scene.kind == TABLE:
      return _table_parts(scene, element)

   if shape == "signs":
      return shape, _signs(scene, element, sign_rows)

   compilers = NUMBER_LINE_SHAPES if scene.kind == NUMBER_LINE else GRAPH_SHAPES

   return shape, compilers[shape](scene, element)


def _render_spec(figure, scene, layout, equal_scale, figure_id):
   kind = figure["kind"]
   is_graph = kind == GRAPH
   has_layout = layout is not None
   axes = figure.get("axes") or {}
   window = None
   view = None

   if has_layout:
      window = {
         "x": [round(layout.x_low, 6) + 0.0, round(layout.x_high, 6) + 0.0],
         "y": [round(layout.y_low, 6) + 0.0, round(layout.y_high, 6) + 0.0],
      }
      view = {"width": VIEW_WIDTH, "height": round(layout.view_height, 3), "padding": PLOT_PADDING}

   return {
      "id": figure_id,
      "kind": kind,
      "title": figure["title"],
      "description": figure["description"],
      "window": window,
      "view": view,
      "axes": {"x": axes.get("x", "x"), "y": axes.get("y", "y")} if is_graph else None,
      "grid": figure.get("grid", True) if is_graph else False,
      "equal_scale": equal_scale,
      "steps": [{"id": step["id"], "caption": step["caption"]} for step in figure["steps"]],
      "columns": list(figure["columns"]) if kind == TABLE else None,
      "rows": [list(row) for row in figure["rows"]] if kind == TABLE else None,
      "primitives": scene.primitives,
   }


def compile_figure(figure, figure_id="figure", clock=time.monotonic, budget=COMPILE_BUDGET_SECONDS):
   """(render_spec, facts) for a figure read by read_figure, or FigureRefused(reason)."""
   started = clock()
   layout, equal_scale = _layout_of(figure)
   scene = _Scene(figure, layout)
   _figure_texts(scene, figure)

   if scene.kind == TABLE:
      _table_facts(scene, figure)

   if scene.kind == NUMBER_LINE:
      _emit_frame(scene, figure["steps"][0]["id"])

   sign_rows = 0

   for step_id, element in elements_in_order(figure):
      shape = shape_of(element)
      sign_rows += 1 if shape == "signs" else 0

      try:
         shape, compiled = _compiled_element(scene, element, shape, sign_rows)
      except expression.ExpressionRefused as refused:
         raise FigureRefused(refused.reason) from None

      if scene.kind == TABLE:
         _emit(scene, step_id, element, shape, compiled)
         _check_budget(scene, started, clock, budget)
         continue

      parts, anchor = compiled
      has_label = "label" in element and anchor is not None

      if anchor is not None:
         scene.anchors[element["id"]] = anchor

      if has_label:
         place = _centred if shape in CENTRED_LABEL_SHAPES else _beside
         parts = parts + [place(scene.layout, anchor, element["label"])]

      _emit(scene, step_id, element, shape, parts)
      _check_budget(scene, started, clock, budget)

   return _render_spec(figure, scene, layout, equal_scale, figure_id), scene.facts()
