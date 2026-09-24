"""What a template module builds from one draw, and the helpers templates share.

A template module in app/generation/templates/ exposes ARCHETYPE_ID, TEMPLATE_VERSION, SPEC (the
archetype's parameter spec, proposed to the registry through data/staging) and
build(names) -> Instance, where names holds the draw and its derived values. Everything else an
item record carries (ids, option letters and order, skills, dial settings, provenance) is written
by app/generation/instantiate.py, never by the template.
"""
import math as pymath
from dataclasses import dataclass, field

import mpmath
import sympy

FIGURE_SAMPLES = 161
QUADRATURE_DIGITS = 25


@dataclass
class Step:
   text: str
   value: object = None
   point_type_id: str = None
   rule: str = None


@dataclass
class Key:
   form: str
   value: object = None
   label: str = None
   decimals: int = None
   units: str = None


@dataclass
class Distractor:
   error_path: str
   derivation: str
   value: object = None
   label: str = None
   mechanism: str = None


@dataclass
class Instance:
   stem: str
   key: Key
   steps: list
   distractors: list
   representation: str
   calculator_status: str
   figure: dict = None
   setup_required: bool = False
   command_verb: str = None
   notes: dict = field(default_factory=dict)


def tex(expression):
   """LaTeX for an expression, with the logarithm printed as ln the way the course writes it."""
   return sympy.latex(sympy.sympify(expression), ln_notation=True)


def inline(expression):
   return rf"\( {tex(expression)} \)"


def math(text):
   return rf"\( {text} \)"


def three_decimals(value):
   """A calculator answer as the course reports it: rounded, not truncated, to three places."""
   return sympy.Float(round(float(sympy.N(value, 30)), 3), 15)


def numeric_integral(integrand, variable, low, high, breakpoints=()):
   """A calculator's definite integral, by mpmath quadrature at 25 digits, split at any
   breakpoints where the integrand has a kink so the quadrature converges."""
   function = sympy.lambdify(variable, integrand, modules="mpmath")
   points = [low] + sorted(breakpoints) + [high]

   with mpmath.workdps(QUADRATURE_DIGITS):
      total = mpmath.quad(function, [mpmath.mpf(sympy.N(point, QUADRATURE_DIGITS)) for point in points])

   return sympy.Float(total, 20)


def numeric_roots(expression, variable, low, high, pieces=400):
   """The real zeros of expression on (low, high), found the way a graphing calculator finds
   them: sign changes on a fine grid, each refined by bisection-safeguarded root finding."""
   function = sympy.lambdify(variable, expression, modules="mpmath")
   roots = []

   with mpmath.workdps(QUADRATURE_DIGITS):
      left = mpmath.mpf(sympy.N(low, QUADRATURE_DIGITS))
      width = (mpmath.mpf(sympy.N(high, QUADRATURE_DIGITS)) - left) / pieces

      for index in range(pieces):
         a_point = left + index * width
         b_point = a_point + width
         a_value = function(a_point)
         b_value = function(b_point)
         changes_sign = a_value * b_value < 0

         if changes_sign:
            roots.append(sympy.Float(mpmath.findroot(function, (a_point, b_point), solver="anderson"), 20))

   return roots


def decimal_text(value):
   return f"{float(value):.3f}"


def _finite_float(value):
   try:
      number = complex(value)
   except (TypeError, ValueError):
      return None

   is_real = abs(number.imag) < 1e-9
   is_finite = is_real and pymath.isfinite(number.real)

   return number.real if is_finite else None


def sample_curve(expression, variable, low, high, samples=FIGURE_SAMPLES, y_limit=None):
   """Polyline segments of y = expression over [low, high], broken where the value is undefined
   or leaves the window, so the renderer never joins across an asymptote."""
   function = sympy.lambdify(variable, expression, modules="math")
   low_value = float(low)
   high_value = float(high)
   segments = []
   current = []

   for index in range(samples):
      x_value = low_value + (high_value - low_value) * index / (samples - 1)

      try:
         y_value = _finite_float(function(x_value))
      except (ValueError, ZeroDivisionError, OverflowError):
         y_value = None

      leaves_window = y_value is not None and y_limit is not None and abs(y_value) > y_limit

      if y_value is None or leaves_window:
         if len(current) > 1:
            segments.append(current)

         current = []
         continue

      current.append([round(x_value, 4), round(y_value, 4)])

   if len(current) > 1:
      segments.append(current)

   return segments


def sample_parametric(x_expression, y_expression, variable, low, high, samples=FIGURE_SAMPLES):
   x_function = sympy.lambdify(variable, x_expression, modules="math")
   y_function = sympy.lambdify(variable, y_expression, modules="math")
   points = []

   for index in range(samples):
      parameter = float(low) + (float(high) - float(low)) * index / (samples - 1)
      points.append([round(x_function(parameter), 4), round(y_function(parameter), 4)])

   return [points]


def sample_polar(radius, variable, low, high, samples=FIGURE_SAMPLES):
   x_expression = radius * sympy.cos(variable)
   y_expression = radius * sympy.sin(variable)

   return sample_parametric(x_expression, y_expression, variable, low, high, samples)


def label(text, x_value, y_value):
   return {"text": text, "anchor": [float(x_value), float(y_value)], "placement": "inside"}


def point_mark(x_value, y_value, is_open=False):
   return {"type": "open_point" if is_open else "point", "at": [float(x_value), float(y_value)]}


def segment_mark(start, end, style="solid"):
   return {
      "type": "segment",
      "from": [float(start[0]), float(start[1])],
      "to": [float(end[0]), float(end[1])],
      "style": style,
   }


def figure(kind, domain, range_, curves=(), marks=(), labels=(), axis_titles=("x", "y"), gridlines=True,
           alt="", fills=()):
   return {
      "kind": kind,
      "domain": [float(domain[0]), float(domain[1])],
      "range": [float(range_[0]), float(range_[1])],
      "curves": [{"segments": segments, "style": "solid"} for segments in curves],
      "fills": [{"points": points} for points in fills],
      "marks": list(marks),
      "labels": list(labels),
      "gridlines": gridlines,
      "axis_titles": list(axis_titles),
      "alt": alt,
   }


def table_figure(columns, rows, alt=""):
   """A table is a figure too, so it renders as a table and not as a sentence of numbers."""
   return {
      "kind": "table",
      "columns": [str(column) for column in columns],
      "rows": [[str(cell) for cell in row] for row in rows],
      "labels": [],
      "alt": alt,
   }


def slope_segments(slope, x_symbol, y_symbol, xs, ys, half_length=0.3):
   """Short segments of the given slope at each lattice point, as a slope field draws them."""
   marks = []

   for x_value in xs:
      for y_value in ys:
         value = _finite_float(sympy.sympify(slope).subs({x_symbol: x_value, y_symbol: y_value}))

         if value is None:
            continue

         dx = half_length / pymath.sqrt(1 + value * value)
         dy = value * dx
         start = (float(x_value) - dx, float(y_value) - dy)
         end = (float(x_value) + dx, float(y_value) + dy)
         marks.append(segment_mark(start, end))

   return marks
