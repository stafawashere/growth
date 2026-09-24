"""Blind re-solve of stems_V.json (unit 5 generated items), written from the stems and figure data alone.

Written by claude-opus-5-5, a blind solver working on the operator's delegation of 2026-09-24, without
seeing any key, worked solution or template. Each curve-identification item carries the three curves
as exact polynomial coefficients read from its figure (checked against the plotted points) and its
four choices; the answer is every choice whose labelling makes each curve the derivative of the one
above it. Each box item passes its own sheet size and height cap.
"""
import re

import sympy

from tools.key_recheck import x


def curve_polynomial(ascending_coefficients):
   return sum(sympy.Rational(coefficient) * x**power for power, coefficient in enumerate(ascending_coefficients))


def labelling_from_choice(choice_text):
   pairs = re.findall(r"urve (\w) is the graph of \\\( (\w'*) \\\)", choice_text)

   return {function_name: label for label, function_name in pairs}


def labelling_is_consistent(curves, labelling, top_name, middle_name, bottom_name):
   top = curve_polynomial(curves[labelling[top_name]])
   middle = curve_polynomial(curves[labelling[middle_name]])
   bottom = curve_polynomial(curves[labelling[bottom_name]])
   middle_is_derivative = sympy.expand(sympy.diff(top, x) - middle) == 0
   bottom_is_derivative = sympy.expand(sympy.diff(middle, x) - bottom) == 0

   return middle_is_derivative and bottom_is_derivative


def identify_curves(family, curves, choices):
   names = {"derivative": ("f", "f'", "f''"), "antiderivative": ("K", "G", "g")}[family]
   consistent = []

   for choice_text in choices:
      labelling = labelling_from_choice(choice_text)
      names_present = all(name in labelling for name in names)

      if names_present and labelling_is_consistent(curves, labelling, *names):
         consistent.append(choice_text)

   if len(consistent) == 1:
      return consistent[0]

   return consistent


def box_max_volume(length, width, max_height=None):
   """Largest x (length - 2x)(width - 2x) for 0 <= x <= min(width / 2, max_height)."""
   side = sympy.Symbol("side", nonnegative=True)
   volume = side * (length - 2 * side) * (width - 2 * side)
   upper = sympy.Rational(min(length, width), 2)

   if max_height is not None:
      upper = sympy.Min(upper, max_height)

   stationary = sympy.solve(sympy.diff(volume, side), side)
   inside = [point for point in stationary if point.is_real and bool(point > 0) and bool(point < upper)]
   candidates = [sympy.Integer(0), upper] + inside

   return max((sympy.nsimplify(volume.subs(side, point)) for point in candidates), key=lambda value: float(value))


BY_SUFFIX = {
   "05009-40": lambda: identify_curves(
      "derivative",
      {"A": ["-5/4", "0", "-1/2", "1/9"], "B": ["-1", "2/3"], "C": ["0", "-1", "1/3"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
      ],
   ),
   "05009-41": lambda: identify_curves(
      "antiderivative",
      {"A": ["1", "-6", "0", "2/9"], "B": ["-6", "0", "2/3"], "C": ["0", "4/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      ],
   ),
   "05009-42": lambda: identify_curves(
      "antiderivative",
      {"A": ["-91/36", "-2", "7/6", "-1/9"], "B": ["-2", "7/3", "-1/3"], "C": ["7/3", "-2/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      ],
   ),
   "05009-43": lambda: identify_curves(
      "antiderivative",
      {"A": ["0", "-2", "2/3"], "B": ["3/2", "0", "-1", "2/9"], "C": ["-2", "4/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-44": lambda: identify_curves(
      "antiderivative",
      {"A": ["-3/2", "-1", "1/2"], "B": ["-1/6", "-3/2", "-1/2", "1/6"], "C": ["-1", "1"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-45": lambda: identify_curves(
      "derivative",
      {"A": ["-5/3", "-3", "-2", "-1/3"], "B": ["-3", "-4", "-1"], "C": ["-4", "-2"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
      ],
   ),
   "05009-46": lambda: identify_curves(
      "derivative",
      {"A": ["49/18", "-4/3", "-1/3", "2/9"], "B": ["-2/3", "4/3"], "C": ["-4/3", "-2/3", "2/3"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
      ],
   ),
   "05009-47": lambda: identify_curves(
      "derivative",
      {"A": ["-17/8", "0", "3/4", "1/6"], "B": ["0", "3/2", "1/2"], "C": ["3/2", "1"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
      ],
   ),
   "05009-48": lambda: identify_curves(
      "antiderivative",
      {"A": ["0", "-2", "1/3"], "B": ["-2", "2/3"], "C": ["5", "0", "-1", "1/9"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      ],
   ),
   "05009-49": lambda: identify_curves(
      "antiderivative",
      {"A": ["-1", "-2/3", "1/3"], "B": ["29/9", "-1", "-1/3", "1/9"], "C": ["-2/3", "2/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-50": lambda: identify_curves(
      "antiderivative",
      {"A": ["4/3", "-4/3"], "B": ["16/3", "4/3", "-2/3"], "C": ["-52/9", "16/3", "2/3", "-2/9"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-51": lambda: identify_curves(
      "antiderivative",
      {"A": ["5/2", "-1"], "B": ["-2", "5/2", "-1/2"], "C": ["19/24", "-2", "5/4", "-1/6"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-52": lambda: identify_curves(
      "derivative",
      {"A": ["-1/3", "-2/3"], "B": ["2", "-1/3", "-1/3"], "C": ["109/36", "2", "-1/6", "-1/9"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
      ],
   ),
   "05009-53": lambda: identify_curves(
      "antiderivative",
      {"A": ["0", "-10/3", "2", "-2/9"], "B": ["4", "-4/3"], "C": ["-10/3", "4", "-2/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-54": lambda: identify_curves(
      "antiderivative",
      {"A": ["-8/3", "0", "2/3"], "B": ["-2", "-8/3", "0", "2/9"], "C": ["0", "4/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-55": lambda: identify_curves(
      "derivative",
      {"A": ["-4", "-4/3"], "B": ["-3", "-16/3", "-2", "-2/9"], "C": ["-16/3", "-4", "-2/3"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
      ],
   ),
   "05009-56": lambda: identify_curves(
      "antiderivative",
      {"A": ["2/3", "-4/3"], "B": ["4/3", "2/3", "-2/3"], "C": ["-13/18", "4/3", "1/3", "-2/9"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-57": lambda: identify_curves(
      "derivative",
      {"A": ["1", "-2/3"], "B": ["0", "1", "-1/3"], "C": ["1/4", "0", "1/2", "-1/9"]},
      [
         "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
         "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
         "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
      ],
   ),
   "05009-58": lambda: identify_curves(
      "antiderivative",
      {"A": ["-4/3", "-1", "1/3"], "B": ["-1", "2/3"], "C": ["15/4", "-4/3", "-1/2", "1/9"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      ],
   ),
   "05009-59": lambda: identify_curves(
      "antiderivative",
      {"A": ["0", "-4/3", "-2/3"], "B": ["-4/3", "-4/3"], "C": ["13/9", "0", "-2/3", "-2/9"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      ],
   ),
   "05009-60": lambda: identify_curves(
      "antiderivative",
      {"A": ["-1", "-1/2", "1/2"], "B": ["61/24", "-1", "-1/4", "1/6"], "C": ["-1/2", "1"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-61": lambda: identify_curves(
      "antiderivative",
      {"A": ["-2", "-2"], "B": ["26/3", "8", "-1", "-1/3"], "C": ["8", "-2", "-1"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-62": lambda: identify_curves(
      "antiderivative",
      {"A": ["-13/36", "-2/3", "1/6", "1/9"], "B": ["1/3", "2/3"], "C": ["-2/3", "1/3", "1/3"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
      ],
   ),
   "05009-63": lambda: identify_curves(
      "antiderivative",
      {"A": ["0", "-2", "-1/2"], "B": ["-2", "-1"], "C": ["2/3", "0", "-1", "-1/6"]},
      [
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
         "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
         "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
         "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      ],
   ),

   "05011-40": lambda: box_max_volume(72, 45),
   "05011-41": lambda: box_max_volume(54, 54),
   "05011-42": lambda: box_max_volume(72, 45),
   "05011-43": lambda: box_max_volume(72, 72),
   "05011-44": lambda: box_max_volume(72, 45, max_height=2),
   "05011-45": lambda: box_max_volume(36, 36, max_height=1),
   "05011-46": lambda: box_max_volume(72, 45),
   "05011-47": lambda: box_max_volume(60, 60, max_height=2),
   "05011-48": lambda: box_max_volume(48, 48, max_height=3),
   "05011-49": lambda: box_max_volume(80, 50),
   "05011-50": lambda: box_max_volume(72, 45),
   "05011-51": lambda: box_max_volume(78, 78),
   "05011-52": lambda: box_max_volume(56, 35),
   "05011-53": lambda: box_max_volume(48, 18, max_height=2),
   "05011-54": lambda: box_max_volume(78, 78, max_height=1),
   "05011-55": lambda: box_max_volume(64, 40, max_height=7),
   "05011-56": lambda: box_max_volume(30, 30),
   "05011-57": lambda: box_max_volume(42, 42, max_height=6),
   "05011-58": lambda: box_max_volume(54, 54, max_height=6),
   "05011-59": lambda: box_max_volume(78, 78, max_height=5),
   "05011-60": lambda: box_max_volume(56, 35, max_height=5),
   "05011-61": lambda: box_max_volume(72, 72, max_height=8),
   "05011-62": lambda: box_max_volume(66, 66),
   "05011-63": lambda: box_max_volume(42, 42, max_height=3),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
