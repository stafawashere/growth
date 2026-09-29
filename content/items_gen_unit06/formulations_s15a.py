"""Stems of BC-QA-06017, BC-QA-06018 and BC-QA-06019 in stems_s15.json, written as the SymPy
computation of the answer each asks for, from the stem and figure alone."""
import sympy
from sympy import Rational, asin, atan, sqrt

from tools.key_recheck import trapezoidal_sum, x


def piecewise_linear_value(vertices, at):
   at = sympy.nsimplify(at)

   for (left_input, left_value), (right_input, right_value) in zip(vertices, vertices[1:]):
      is_inside = left_input <= at <= right_input

      if is_inside:
         slope = Rational(right_value - left_value, right_input - left_input)
         return left_value + slope * (at - left_input)

   raise ValueError(f"{at} outside the graph")


def equal_width_sum(function_value, lower, upper, count, rule):
   width = Rational(upper - lower, count)
   left_endpoints = [lower + index * width for index in range(count)]

   if rule == "left":
      return width * sum(function_value(point) for point in left_endpoints)

   if rule == "right":
      return width * sum(function_value(point + width) for point in left_endpoints)

   if rule == "midpoint":
      return width * sum(function_value(point + width / 2) for point in left_endpoints)

   if rule == "trapezoidal":
      nodes = left_endpoints + [sympy.Integer(upper)]
      return trapezoidal_sum([(node, function_value(node)) for node in nodes])

   raise ValueError(rule)


def sum_for_expression(expression, lower, upper, count, rule):
   return equal_width_sum(lambda point: expression.subs(x, point), lower, upper, count, rule)


def sum_for_graph(vertices, lower, upper, count, rule):
   return equal_width_sum(lambda point: piecewise_linear_value(vertices, point), lower, upper, count, rule)


def checked_antiderivative(antiderivative, integrand):
   difference = sympy.simplify(sympy.diff(antiderivative, x) - integrand)

   if difference != 0:
      raise ValueError(f"{antiderivative} does not differentiate to {integrand}")

   return antiderivative


def arctangent_antiderivative(numerator, quadratic):
   """numerator / (x^2 + b x + c) with a positive completed-square constant."""
   linear_coefficient = quadratic.coeff(x, 1)
   shift = -linear_coefficient / 2
   squared_radius = sympy.expand(quadratic.subs(x, shift))
   radius = sqrt(squared_radius)
   antiderivative = numerator / radius * atan((x - shift) / radius)

   return checked_antiderivative(antiderivative, numerator / quadratic)


def arcsine_antiderivative(numerator, radicand):
   """numerator / sqrt(radicand) where radicand = r^2 - (x - h)^2."""
   linear_coefficient = radicand.coeff(x, 1)
   shift = linear_coefficient / 2
   squared_radius = sympy.expand(radicand.subs(x, shift))
   radius = sqrt(squared_radius)
   antiderivative = numerator * asin((x - shift) / radius)

   return checked_antiderivative(antiderivative, numerator / sqrt(radicand))


def power_rule_antiderivative(integrand):
   expanded = sympy.expand(integrand)

   return checked_antiderivative(sympy.integrate(expanded, x), integrand)


def graph(*values):
   return list(enumerate(values))


BY_SUFFIX = {
   "06017-00": lambda: sum_for_graph(graph(-2, 2, 2, 6, 0, 5, 6, 6, 0), 0, 8, 4, "left"),
   "06017-01": lambda: sum_for_graph(graph(0, 1, -2, 0, -2, 4, -1, -1, 1), 0, 8, 4, "left"),
   "06017-02": lambda: sum_for_graph(graph(6, 3, 4, 6, 2, -1, 1, 2, 2), 0, 8, 4, "left"),
   "06017-03": lambda: sum_for_expression(2 * x**2 + 3, 1, 5, 2, "trapezoidal"),
   "06017-04": lambda: sum_for_expression(3 * x**2 + 5, 0, 9, 3, "midpoint"),
   "06017-05": lambda: sum_for_expression(1 - 3 * x**2, 4, 10, 3, "right"),
   "06017-06": lambda: sum_for_expression(x**2 + 8, 4, 10, 3, "trapezoidal"),
   "06017-07": lambda: sum_for_graph(graph(5, 4, 2, 2, 5, -1, 1, 4, 0), 0, 8, 4, "midpoint"),
   "06017-08": lambda: sum_for_expression(2 - x**2, 1, 2, 2, "right"),
   "06017-09": lambda: sum_for_expression(7 - x**2, 4, 12, 4, "trapezoidal"),
   "06017-10": lambda: sum_for_expression(8 - 3 * x**2, 2, 14, 4, "right"),
   "06017-11": lambda: sum_for_graph(graph(-2, 4, 3, 0, 0, 0, 5, 5, 0), 0, 8, 4, "left"),
   "06017-12": lambda: sum_for_expression(x**2 + 8, 1, 7, 3, "midpoint"),
   "06017-13": lambda: sum_for_expression(x**2 + 8, 4, 12, 4, "right"),
   "06017-14": lambda: sum_for_expression(3 * x**2 + 5, 3, 9, 2, "trapezoidal"),
   "06017-15": lambda: sum_for_graph(graph(0, -1, 4, 4, 5, 3, 3, 3, 1), 0, 8, 4, "right"),
   "06017-16": lambda: sum_for_graph(graph(0, -1, -1, 3, 5, -2, 6, -1, -2), 0, 8, 4, "left"),
   "06017-17": lambda: sum_for_expression(x**2 + 4, 1, 7, 2, "trapezoidal"),
   "06017-18": lambda: sum_for_expression(6 - 3 * x**2, 1, 5, 2, "midpoint"),
   "06017-19": lambda: sum_for_expression(2 * x**2 + 8, 2, 6, 2, "left"),
   "06017-20": lambda: sum_for_expression(2 * x**2 + 6, 3, 9, 2, "right"),
   "06017-21": lambda: sum_for_expression(x**2 + 5, 0, 8, 4, "trapezoidal"),

   "06018-00": lambda: arctangent_antiderivative(11, x**2 + 25),
   "06018-01": lambda: arcsine_antiderivative(7, 4 - x**2),
   "06018-02": lambda: arcsine_antiderivative(5, -x**2 - 10 * x + 56),
   "06018-03": lambda: arctangent_antiderivative(5, x**2 + 2 * x + 82),
   "06018-04": lambda: arcsine_antiderivative(5, 81 - x**2),
   "06018-05": lambda: arctangent_antiderivative(12, x**2 + 4 * x + 29),
   "06018-06": lambda: arctangent_antiderivative(4, x**2 + 36),
   "06018-07": lambda: arctangent_antiderivative(12, x**2 + 16),
   "06018-08": lambda: arctangent_antiderivative(10, x**2 - 6 * x + 13),
   "06018-09": lambda: arcsine_antiderivative(10, -x**2 - 8 * x - 12),
   "06018-10": lambda: arcsine_antiderivative(3, -x**2 - 2 * x + 15),
   "06018-11": lambda: arcsine_antiderivative(11, -x**2 - 6 * x - 5),
   "06018-12": lambda: arcsine_antiderivative(5, -x**2 + 10 * x + 24),
   "06018-13": lambda: arctangent_antiderivative(11, x**2 - 6 * x + 45),
   "06018-14": lambda: arctangent_antiderivative(8, x**2 + 4),
   "06018-15": lambda: arctangent_antiderivative(9, x**2 + 16),
   "06018-16": lambda: arcsine_antiderivative(12, 64 - x**2),
   "06018-17": lambda: arctangent_antiderivative(8, x**2 - 6 * x + 34),
   "06018-18": lambda: arcsine_antiderivative(6, 25 - x**2),
   "06018-19": lambda: arctangent_antiderivative(4, x**2 + 64),
   "06018-20": lambda: arctangent_antiderivative(11, x**2 + 9),
   "06018-21": lambda: arcsine_antiderivative(8, 49 - x**2),

   "06019-00": lambda: power_rule_antiderivative((x - 3) * (x + 4)),
   "06019-01": lambda: power_rule_antiderivative((3 * x**4 + 3) / x**3),
   "06019-02": lambda: power_rule_antiderivative((x - 5) * (3 * x + 5)),
   "06019-03": lambda: power_rule_antiderivative((3 * x - 4) / sqrt(x)),
   "06019-04": lambda: power_rule_antiderivative((2 * x**3 + 4) / x**2),
   "06019-05": lambda: power_rule_antiderivative((x - 3) * (2 * x - 4)),
   "06019-06": lambda: power_rule_antiderivative((x + 6) * (2 * x + 4)),
   "06019-07": lambda: power_rule_antiderivative((x - 5) * (4 * x - 1)),
   "06019-08": lambda: power_rule_antiderivative((x - 4) / sqrt(x)),
   "06019-09": lambda: power_rule_antiderivative((x + 1) * (x + 6)),
   "06019-10": lambda: power_rule_antiderivative((2 * x - 4) / sqrt(x)),
   "06019-11": lambda: power_rule_antiderivative((x + 5) * (2 * x + 5)),
   "06019-12": lambda: power_rule_antiderivative((4 * x - 2) / sqrt(x)),
   "06019-13": lambda: power_rule_antiderivative((x - 6) * (3 * x - 1)),
   "06019-14": lambda: power_rule_antiderivative((3 * x - 1) / sqrt(x)),
   "06019-15": lambda: power_rule_antiderivative((x - 3) * (x - 2)),
   "06019-16": lambda: power_rule_antiderivative((x - 6) * (x - 3)),
   "06019-17": lambda: power_rule_antiderivative((x - 4) * (4 * x + 5)),
   "06019-18": lambda: power_rule_antiderivative((x + 2) * (4 * x + 6)),
   "06019-19": lambda: power_rule_antiderivative((x + 6) * (4 * x - 1)),
   "06019-20": lambda: power_rule_antiderivative((x + 4) * (2 * x + 5)),
   "06019-21": lambda: power_rule_antiderivative((4 * x + 3) / sqrt(x)),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
