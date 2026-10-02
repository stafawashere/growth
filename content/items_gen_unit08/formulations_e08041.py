"""Blind re-solve of stems_e08041.json (BC-QA-08014, arc length of a graph), written from the stems alone."""
import re

import mpmath
import sympy
from sympy import E, Rational, exp, ln, sqrt
from sympy.parsing.sympy_parser import (
   implicit_multiplication_application,
   parse_expr,
   standard_transformations,
)

from tools.key_recheck import derivative, x

ITEM_PREFIX = "ITM-GEN-"

WORKING_DIGITS = 40
SAMPLE_COUNT = 7
SAMPLE_TOLERANCE = sympy.Float("1e-20")

CHOICE_PATTERN = re.compile(r"\\int_\{(?P<lower>[^}]*)\}\^\{(?P<upper>[^}]*)\}(?P<integrand>.*)\\,dx")
PARSER_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)


def read_braced_group(text, start):
   depth = 0

   for position in range(start, len(text)):
      character = text[position]

      if character == "{":
         depth += 1
      elif character == "}":
         depth -= 1

         if depth == 0:
            return text[start + 1:position], position + 1

   raise ValueError(f"unbalanced braces in {text!r}")


def latex_to_python(text):
   pieces = []
   position = 0

   while position < len(text):
      remainder = text[position:]

      if remainder.startswith("\\frac"):
         numerator, position = read_braced_group(text, position + len("\\frac"))
         denominator, position = read_braced_group(text, position)
         pieces.append(f"(({latex_to_python(numerator)})/({latex_to_python(denominator)}))")
      elif remainder.startswith("\\sqrt"):
         radicand, position = read_braced_group(text, position + len("\\sqrt"))
         pieces.append(f"sqrt({latex_to_python(radicand)})")
      elif remainder.startswith("\\ln"):
         argument, position = read_braced_group(text, position + len("\\ln"))
         pieces.append(f"log({latex_to_python(argument)})")
      elif remainder.startswith("\\left("):
         pieces.append("(")
         position += len("\\left(")
      elif remainder.startswith("\\right)"):
         pieces.append(")")
         position += len("\\right)")
      elif remainder.startswith("^"):
         exponent, position = read_braced_group(text, position + 1)
         pieces.append(f"**({latex_to_python(exponent)})")
      elif remainder.startswith("{"):
         group, position = read_braced_group(text, position)
         pieces.append(f"({latex_to_python(group)})")
      else:
         pieces.append(text[position])
         position += 1

   return "".join(pieces)


def parse_latex_expression(text):
   python_text = latex_to_python(text.strip())

   return parse_expr(python_text, local_dict={"x": x, "e": E}, transformations=PARSER_TRANSFORMATIONS)


def parse_integral_choice(choice):
   match = CHOICE_PATTERN.search(choice)

   if match is None:
      raise ValueError(f"not a definite integral in x: {choice!r}")

   lower = parse_latex_expression(match.group("lower"))
   upper = parse_latex_expression(match.group("upper"))
   integrand = parse_latex_expression(match.group("integrand"))

   return lower, upper, integrand


def arc_length_integrand(function):
   return sqrt(1 + derivative(function) ** 2)


def agrees_on_interval(left, right, lower, upper):
   if sympy.simplify(left - right) == 0:
      return True

   step = (upper - lower) / (SAMPLE_COUNT + 1)
   sample_points = [lower + step * index for index in range(1, SAMPLE_COUNT + 1)]

   for point in sample_points:
      difference = sympy.N((left - right).subs(x, point), WORKING_DIGITS)
      is_far_apart = abs(difference) > SAMPLE_TOLERANCE

      if is_far_apart:
         return False

   return True


def arc_length_choice(function, lower, upper, choices):
   expected_integrand = arc_length_integrand(function)
   correct_choices = []

   for choice in choices:
      choice_lower, choice_upper, choice_integrand = parse_integral_choice(choice)
      has_same_lower = sympy.simplify(choice_lower - lower) == 0
      has_same_upper = sympy.simplify(choice_upper - upper) == 0
      has_same_bounds = has_same_lower and has_same_upper
      has_same_integrand = has_same_bounds and agrees_on_interval(choice_integrand, expected_integrand, lower, upper)
      is_arc_length_integral = has_same_bounds and has_same_integrand

      if is_arc_length_integral:
         correct_choices.append(choice)

   if not correct_choices:
      raise ValueError("no choice is the arc length integral")

   if len(correct_choices) == 1:
      return correct_choices[0]

   return correct_choices


def arc_length_value(function, lower, upper):
   integrand = sympy.lambdify(x, arc_length_integrand(function), "mpmath")

   with mpmath.workdps(WORKING_DIGITS):
      length = mpmath.quad(integrand, [lower, upper])

      return sympy.Float(length, WORKING_DIGITS)


CHOICES_23 = [
   "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{1}^{5} \\left(\\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)\\,dx \\)",
   "\\( \\int_{1}^{5} \\sqrt{1 + \\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}}\\,dx \\)",
   "\\( \\int_{1}^{5} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
]

CHOICES_26 = [
   "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{5 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{3}^{5} \\left(\\frac{5 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)\\,dx \\)",
   "\\( \\int_{3}^{5} \\sqrt{1 + \\frac{5 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}}\\,dx \\)",
   "\\( \\int_{3}^{5} \\sqrt{1 + \\left(\\frac{5 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
]

CHOICES_27 = [
   "\\( \\int_{0}^{4} \\sqrt{1 + \\left(\\frac{\\ln{\\left(x \\right)}}{2} + \\frac{1}{2}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{2}^{4} \\left(\\frac{\\ln{\\left(x \\right)}}{2} + \\frac{1}{2}\\right)\\,dx \\)",
   "\\( \\int_{2}^{4} \\sqrt{1 + \\frac{\\ln{\\left(x \\right)}}{2} + \\frac{1}{2}}\\,dx \\)",
   "\\( \\int_{2}^{4} \\sqrt{1 + \\left(\\frac{\\ln{\\left(x \\right)}}{2} + \\frac{1}{2}\\right)^{2}}\\,dx \\)",
]

CHOICES_28 = [
   "\\( \\int_{0}^{6} \\sqrt{1 + \\left(\\ln{\\left(x \\right)} + 1\\right)^{2}}\\,dx \\)",
   "\\( \\int_{2}^{6} \\left(\\ln{\\left(x \\right)} + 1\\right)\\,dx \\)",
   "\\( \\int_{2}^{6} \\sqrt{1 + \\left(\\ln{\\left(x \\right)} + 1\\right)^{2}}\\,dx \\)",
   "\\( \\int_{2}^{6} \\sqrt{1 + \\ln{\\left(x \\right)} + 1}\\,dx \\)",
]

CHOICES_31 = [
   "\\( \\int_{0}^{7} \\sqrt{1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{3}^{7} \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)\\,dx \\)",
   "\\( \\int_{3}^{7} \\sqrt{1 + \\frac{3 x + 2}{2 \\sqrt{x + 1}}}\\,dx \\)",
   "\\( \\int_{3}^{7} \\sqrt{1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
]

CHOICES_33 = [
   "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{2}^{5} \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)\\,dx \\)",
   "\\( \\int_{2}^{5} \\sqrt{1 + \\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}}\\,dx \\)",
   "\\( \\int_{2}^{5} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}}\\,dx \\)",
]

CHOICES_34 = [
   "\\( \\int_{0}^{3} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{1}^{3} \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)\\,dx \\)",
   "\\( \\int_{1}^{3} \\sqrt{1 + \\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}}\\,dx \\)",
   "\\( \\int_{1}^{3} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
]

CHOICES_36 = [
   "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{1}^{5} \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)\\,dx \\)",
   "\\( \\int_{1}^{5} \\sqrt{1 + \\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}}\\,dx \\)",
   "\\( \\int_{1}^{5} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}}\\,dx \\)",
]

CHOICES_37 = [
   "\\( \\int_{0}^{7} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{3}^{7} \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)\\,dx \\)",
   "\\( \\int_{3}^{7} \\sqrt{1 + \\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{8}}\\,dx \\)",
   "\\( \\int_{3}^{7} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
]

CHOICES_38 = [
   "\\( \\int_{0}^{2} \\sqrt{1 + \\left(\\frac{5 \\ln{\\left(x \\right)}}{2} + \\frac{5}{2}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{1}^{2} \\left(\\frac{5 \\ln{\\left(x \\right)}}{2} + \\frac{5}{2}\\right)\\,dx \\)",
   "\\( \\int_{1}^{2} \\sqrt{1 + \\frac{5 \\ln{\\left(x \\right)}}{2} + \\frac{5}{2}}\\,dx \\)",
   "\\( \\int_{1}^{2} \\sqrt{1 + \\left(\\frac{5 \\ln{\\left(x \\right)}}{2} + \\frac{5}{2}\\right)^{2}}\\,dx \\)",
]

CHOICES_40 = [
   "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{2}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{3}^{5} \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{2}\\right)\\,dx \\)",
   "\\( \\int_{3}^{5} \\sqrt{1 + \\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{2}}\\,dx \\)",
   "\\( \\int_{3}^{5} \\sqrt{1 + \\left(\\frac{\\left(x + 4\\right) e^{\\frac{x}{4}}}{2}\\right)^{2}}\\,dx \\)",
]

CHOICES_41 = [
   "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
   "\\( \\int_{1}^{5} \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)\\,dx \\)",
   "\\( \\int_{1}^{5} \\sqrt{1 + \\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}}\\,dx \\)",
   "\\( \\int_{1}^{5} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
]

CHOICES_43 = [
   "\\( \\int_{0}^{6} \\sqrt{1 + \\left(2 \\ln{\\left(x \\right)} + 2\\right)^{2}}\\,dx \\)",
   "\\( \\int_{3}^{6} \\left(2 \\ln{\\left(x \\right)} + 2\\right)\\,dx \\)",
   "\\( \\int_{3}^{6} \\sqrt{1 + 2 \\ln{\\left(x \\right)} + 2}\\,dx \\)",
   "\\( \\int_{3}^{6} \\sqrt{1 + \\left(2 \\ln{\\left(x \\right)} + 2\\right)^{2}}\\,dx \\)",
]

BY_SUFFIX = {
   "08014-22": lambda: arc_length_value(Rational(3, 2) * x * exp(x / 4), 3, 5),
   "08014-23": lambda: arc_length_choice(Rational(3, 2) * x * sqrt(x + 1), 1, 5, CHOICES_23),
   "08014-24": lambda: arc_length_value(Rational(3, 2) * x * ln(x), 1, 5),
   "08014-25": lambda: arc_length_value(2 * x * sqrt(x + 1), 2, 5),
   "08014-26": lambda: arc_length_choice(Rational(5, 2) * x * exp(x / 4), 3, 5, CHOICES_26),
   "08014-27": lambda: arc_length_choice(x * ln(x) / 2, 2, 4, CHOICES_27),
   "08014-28": lambda: arc_length_choice(x * ln(x), 2, 6, CHOICES_28),
   "08014-29": lambda: arc_length_value(Rational(3, 2) * x * exp(x / 4), 3, 6),
   "08014-30": lambda: arc_length_value(3 * x * ln(x), 3, 6),
   "08014-31": lambda: arc_length_choice(x * sqrt(x + 1), 3, 7, CHOICES_31),
   "08014-32": lambda: arc_length_value(x * ln(x), 2, 4),
   "08014-33": lambda: arc_length_choice(x * exp(x / 4), 2, 5, CHOICES_33),
   "08014-34": lambda: arc_length_choice(Rational(3, 2) * x * exp(x / 4), 1, 3, CHOICES_34),
   "08014-35": lambda: arc_length_value(Rational(3, 2) * x * ln(x), 2, 6),
   "08014-36": lambda: arc_length_choice(x * exp(x / 4), 1, 5, CHOICES_36),
   "08014-37": lambda: arc_length_choice(x * exp(x / 4) / 2, 3, 7, CHOICES_37),
   "08014-38": lambda: arc_length_choice(Rational(5, 2) * x * ln(x), 1, 2, CHOICES_38),
   "08014-39": lambda: arc_length_value(x * exp(x / 4) / 2, 3, 6),
   "08014-40": lambda: arc_length_choice(2 * x * exp(x / 4), 3, 5, CHOICES_40),
   "08014-41": lambda: arc_length_choice(Rational(3, 2) * x * exp(x / 4), 1, 5, CHOICES_41),
   "08014-42": lambda: arc_length_value(Rational(3, 2) * x * ln(x), 3, 4),
   "08014-43": lambda: arc_length_choice(2 * x * ln(x), 3, 6, CHOICES_43),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}