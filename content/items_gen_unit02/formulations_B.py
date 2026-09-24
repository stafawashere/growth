"""Answers to the unit 2 generated items in stems_B.json, computed from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24, from the
stem text, figure tables and choice lists in stems_B.json only, never from a stored key, template
or worked solution. A statement item returns the text of the choice that the computation selects,
and a three-decimal item returns its value at 30 significant digits, unrounded.
"""

import sympy
from sympy import Rational, cos, cot, csc, exp, ln, pi, sec, sin, sqrt, tan

from tools.key_recheck import derivative, tangent_line, x

ITEM_PREFIX = "ITM-GEN-"
NUMERIC_DIGITS = 30

t = sympy.Symbol("t")


def single_choice(item_id, predicate):
   matching = [choice for choice in CHOICES_BY_ID[item_id] if predicate(choice)]
   is_unique = len(matching) == 1

   if is_unique:
      return matching[0]

   return matching


def derivative_function(expression):
   return sympy.simplify(derivative(expression))


def exact_derivative_value(expression, at):
   return sympy.simplify(derivative(expression).subs(x, at))


def product_rule_value(f_value, f_slope, g_value, g_slope):
   return sympy.Integer(f_slope * g_value + f_value * g_slope)


def quotient_rule_value(f_value, f_slope, g_value, g_slope):
   return Rational(f_slope * g_value - f_value * g_slope, g_value**2)


def tangent_line_at(expression, at, stated_point=None):
   has_stated_point = stated_point is not None

   if has_stated_point:
      lies_on_graph = expression.subs(x, stated_point[0]) == stated_point[1]

      if not lies_on_graph:
         raise ValueError(f"{stated_point} is not on the graph")

   return tangent_line(expression, at)


def notation_statement(item_id, dependent, independent, order):
   """The one reading that is a derivative of the dependent quantity with respect to the
   independent one, evaluated at the given input rather than constant, a quotient or a square."""
   if order == 1:
      meaning = f"the rate of change of {dependent} with respect to {independent} when"
   else:
      meaning = f"with respect to {independent}, of the rate of change of {dependent} when"

   def is_correct_reading(choice):
      is_constant_reading = "the same at every" in choice
      is_quotient_reading = "divided by" in choice
      is_square_reading = "square" in choice

      return meaning in choice and not (is_constant_reading or is_quotient_reading or is_square_reading)

   return single_choice(item_id, is_correct_reading)


def model_rate(log_shift, sine_coefficient, sine_divisor, constant, at):
   amount = ln(t + log_shift) + sine_coefficient * sin(t**2 / sine_divisor) + constant
   rate = sympy.diff(amount, t).subs(t, sympy.nsimplify(at))

   return sympy.N(rate, NUMERIC_DIGITS)


CHOICES_BY_ID = {
   "ITM-GEN-02012-00": [
      "\\( \\frac{T(5)}{5} = 7 \\), so the temperature divided by the distance along the rod when x = 5 is 7 degrees Celsius per meter.",
      "\\( \\frac{dT}{dx} = 7 \\), so the rate of change of the temperature with respect to the distance along the rod, the same at every x, is 7 degrees Celsius per meter.",
      "\\( \\left. \\frac{dT}{dx} \\right|_{x=5} = 7 \\), so the rate of change of the temperature with respect to the distance along the rod when x = 5 is 7 degrees Celsius per meter.",
      "\\( \\left. \\frac{dx}{dT} \\right|_{x=5} = 7 \\), so the rate of change of the distance along the rod with respect to the temperature when x = 5 is 7 meters per degree Celsius.",
   ],
   "ITM-GEN-02012-01": [
      "\\( \\frac{f(2)}{2} = 7 \\), so y divided by x when x = 2 is 7.",
      "\\( f'(2) = 7 \\), so the rate of change of x with respect to y when x = 2 is 7.",
      "\\( f'(2) = 7 \\), so the rate of change of y with respect to x when x = 2 is 7.",
      "\\( f'(x) = 7 \\), so the rate of change of y with respect to x, the same at every x, is 7.",
   ],
   "ITM-GEN-02012-02": [
      "\\( \\frac{g(9)}{9} = -7 \\), so w divided by t when t = 9 is -7.",
      "\\( g'(9) = -7 \\), so the rate of change of t with respect to w when t = 9 is -7.",
      "\\( g'(9) = -7 \\), so the rate of change of w with respect to t when t = 9 is -7.",
      "\\( g'(t) = -7 \\), so the rate of change of w with respect to t, the same at every t, is -7.",
   ],
   "ITM-GEN-02012-03": [
      "\\( \\frac{H(9)}{9} = 12 \\), so the height of the balloon divided by time when t = 9 is 12 meters per second.",
      "\\( \\frac{dH}{dt} = 12 \\), so the rate of change of the height of the balloon with respect to time, the same at every t, is 12 meters per second.",
      "\\( \\left. \\frac{dH}{dt} \\right|_{t=9} = 12 \\), so the rate of change of the height of the balloon with respect to time when t = 9 is 12 meters per second.",
      "\\( \\left. \\frac{dt}{dH} \\right|_{t=9} = 12 \\), so the rate of change of time with respect to the height of the balloon when t = 9 is 12 seconds per meter.",
   ],
   "ITM-GEN-02012-04": [
      "\\( \\left(g'(8)\\right)^{2} = 12 \\), so the square of the rate of change of w with respect to t when t = 8 is 12.",
      "\\( g''(8) = 12 \\), so the rate of change, with respect to t, of the rate of change of w when t = 8 is 12.",
      "\\( g''(8) = 12 \\), so the rate of change, with respect to w, of the rate of change of t when t = 8 is 12.",
      "\\( g''(t) = 12 \\), so the rate of change, with respect to t, of the rate of change of w, the same at every t, is 12.",
   ],
   "ITM-GEN-02012-05": [
      "\\( \\frac{dw}{dt} = -11 \\), so the rate of change of w with respect to t, the same at every t, is -11.",
      "\\( \\frac{g(5)}{5} = -11 \\), so w divided by t when t = 5 is -11.",
      "\\( \\left. \\frac{dt}{dw} \\right|_{t=5} = -11 \\), so the rate of change of t with respect to w when t = 5 is -11.",
      "\\( \\left. \\frac{dw}{dt} \\right|_{t=5} = -11 \\), so the rate of change of w with respect to t when t = 5 is -11.",
   ],
   "ITM-GEN-02012-06": [
      "\\( \\frac{d^{2}s}{du^{2}} = 11 \\), so the rate of change, with respect to u, of the rate of change of s, the same at every u, is 11.",
      "\\( \\left(\\frac{ds}{du}\\right)^{2} = 11 \\text{ at } u = 1 \\), so the square of the rate of change of s with respect to u when u = 1 is 11.",
      "\\( \\left. \\frac{d^{2}s}{du^{2}} \\right|_{u=1} = 11 \\), so the rate of change, with respect to u, of the rate of change of s when u = 1 is 11.",
      "\\( \\left. \\frac{d^{2}u}{ds^{2}} \\right|_{u=1} = 11 \\), so the rate of change, with respect to s, of the rate of change of u when u = 1 is 11.",
   ],
   "ITM-GEN-02012-07": [
      "\\( \\left(f'(2)\\right)^{2} = 1 \\), so the square of the rate of change of y with respect to x when x = 2 is 1.",
      "\\( f''(2) = 1 \\), so the rate of change, with respect to x, of the rate of change of y when x = 2 is 1.",
      "\\( f''(2) = 1 \\), so the rate of change, with respect to y, of the rate of change of x when x = 2 is 1.",
      "\\( f''(x) = 1 \\), so the rate of change, with respect to x, of the rate of change of y, the same at every x, is 1.",
   ],
   "ITM-GEN-02012-08": [
      "\\( \\left(f'(8)\\right)^{2} = 7 \\), so the square of the rate of change of y with respect to x when x = 8 is 7.",
      "\\( f''(8) = 7 \\), so the rate of change, with respect to x, of the rate of change of y when x = 8 is 7.",
      "\\( f''(8) = 7 \\), so the rate of change, with respect to y, of the rate of change of x when x = 8 is 7.",
      "\\( f''(x) = 7 \\), so the rate of change, with respect to x, of the rate of change of y, the same at every x, is 7.",
   ],
   "ITM-GEN-02012-09": [
      "\\( \\frac{P(1)}{1} = -1 \\), so the number of bacteria divided by time when t = 1 is -1 thousand bacteria per hour.",
      "\\( \\frac{dP}{dt} = -1 \\), so the rate of change of the number of bacteria with respect to time, the same at every t, is -1 thousand bacteria per hour.",
      "\\( \\left. \\frac{dP}{dt} \\right|_{t=1} = -1 \\), so the rate of change of the number of bacteria with respect to time when t = 1 is -1 thousand bacteria per hour.",
      "\\( \\left. \\frac{dt}{dP} \\right|_{t=1} = -1 \\), so the rate of change of time with respect to the number of bacteria when t = 1 is -1 hours per thousand bacteria.",
   ],
   "ITM-GEN-02012-10": [
      "\\( \\frac{dy}{dx} = 8 \\), so the rate of change of y with respect to x, the same at every x, is 8.",
      "\\( \\frac{f(3)}{3} = 8 \\), so y divided by x when x = 3 is 8.",
      "\\( \\left. \\frac{dx}{dy} \\right|_{x=3} = 8 \\), so the rate of change of x with respect to y when x = 3 is 8.",
      "\\( \\left. \\frac{dy}{dx} \\right|_{x=3} = 8 \\), so the rate of change of y with respect to x when x = 3 is 8.",
   ],
   "ITM-GEN-02012-11": [
      "\\( \\frac{d^{2}y}{dx^{2}} = 3 \\), so the rate of change, with respect to x, of the rate of change of y, the same at every x, is 3.",
      "\\( \\left(\\frac{dy}{dx}\\right)^{2} = 3 \\text{ at } x = 4 \\), so the square of the rate of change of y with respect to x when x = 4 is 3.",
      "\\( \\left. \\frac{d^{2}x}{dy^{2}} \\right|_{x=4} = 3 \\), so the rate of change, with respect to y, of the rate of change of x when x = 4 is 3.",
      "\\( \\left. \\frac{d^{2}y}{dx^{2}} \\right|_{x=4} = 3 \\), so the rate of change, with respect to x, of the rate of change of y when x = 4 is 3.",
   ],
   "ITM-GEN-02012-12": [
      "\\( H'(2) = 1 \\), so the rate of change of the height of the balloon with respect to time when t = 2 is 1 meters per second.",
      "\\( H'(2) = 1 \\), so the rate of change of time with respect to the height of the balloon when t = 2 is 1 seconds per meter.",
      "\\( H'(t) = 1 \\), so the rate of change of the height of the balloon with respect to time, the same at every t, is 1 meters per second.",
      "\\( \\frac{H(2)}{2} = 1 \\), so the height of the balloon divided by time when t = 2 is 1 meters per second.",
   ],
   "ITM-GEN-02012-13": [
      "\\( \\frac{d^{2}V}{dt^{2}} = 8 \\), so the rate of change, with respect to time, of the rate of change of the volume of water, the same at every t, is 8 liters per minute per minute.",
      "\\( \\left(\\frac{dV}{dt}\\right)^{2} = 8 \\text{ at } t = 6 \\), so the square of the rate of change of the volume of water with respect to time when t = 6 is 8 liters squared per minute squared.",
      "\\( \\left. \\frac{d^{2}V}{dt^{2}} \\right|_{t=6} = 8 \\), so the rate of change, with respect to time, of the rate of change of the volume of water when t = 6 is 8 liters per minute per minute.",
      "\\( \\left. \\frac{d^{2}t}{dV^{2}} \\right|_{t=6} = 8 \\), so the rate of change, with respect to the volume of water, of the rate of change of time when t = 6 is 8 minutes per liter per liter.",
   ],
   "ITM-GEN-02012-14": [
      "\\( \\frac{k(3)}{3} = 6 \\), so r divided by z when z = 3 is 6.",
      "\\( k'(3) = 6 \\), so the rate of change of r with respect to z when z = 3 is 6.",
      "\\( k'(3) = 6 \\), so the rate of change of z with respect to r when z = 3 is 6.",
      "\\( k'(z) = 6 \\), so the rate of change of r with respect to z, the same at every z, is 6.",
   ],
   "ITM-GEN-02012-15": [
      "\\( \\frac{T(1)}{1} = 2 \\), so the temperature divided by the distance along the rod when x = 1 is 2 degrees Celsius per meter.",
      "\\( \\frac{dT}{dx} = 2 \\), so the rate of change of the temperature with respect to the distance along the rod, the same at every x, is 2 degrees Celsius per meter.",
      "\\( \\left. \\frac{dT}{dx} \\right|_{x=1} = 2 \\), so the rate of change of the temperature with respect to the distance along the rod when x = 1 is 2 degrees Celsius per meter.",
      "\\( \\left. \\frac{dx}{dT} \\right|_{x=1} = 2 \\), so the rate of change of the distance along the rod with respect to the temperature when x = 1 is 2 meters per degree Celsius.",
   ],
   "ITM-GEN-02012-16": [
      "\\( \\frac{H(9)}{9} = 11 \\), so the height of the balloon divided by time when t = 9 is 11 meters per second.",
      "\\( \\frac{dH}{dt} = 11 \\), so the rate of change of the height of the balloon with respect to time, the same at every t, is 11 meters per second.",
      "\\( \\left. \\frac{dH}{dt} \\right|_{t=9} = 11 \\), so the rate of change of the height of the balloon with respect to time when t = 9 is 11 meters per second.",
      "\\( \\left. \\frac{dt}{dH} \\right|_{t=9} = 11 \\), so the rate of change of time with respect to the height of the balloon when t = 9 is 11 seconds per meter.",
   ],
   "ITM-GEN-02012-17": [
      "\\( \\frac{dw}{dt} = -8 \\), so the rate of change of w with respect to t, the same at every t, is -8.",
      "\\( \\frac{g(6)}{6} = -8 \\), so w divided by t when t = 6 is -8.",
      "\\( \\left. \\frac{dt}{dw} \\right|_{t=6} = -8 \\), so the rate of change of t with respect to w when t = 6 is -8.",
      "\\( \\left. \\frac{dw}{dt} \\right|_{t=6} = -8 \\), so the rate of change of w with respect to t when t = 6 is -8.",
   ],
   "ITM-GEN-02012-18": [
      "\\( \\left(k'(8)\\right)^{2} = 11 \\), so the square of the rate of change of r with respect to z when z = 8 is 11.",
      "\\( k''(8) = 11 \\), so the rate of change, with respect to r, of the rate of change of z when z = 8 is 11.",
      "\\( k''(8) = 11 \\), so the rate of change, with respect to z, of the rate of change of r when z = 8 is 11.",
      "\\( k''(z) = 11 \\), so the rate of change, with respect to z, of the rate of change of r, the same at every z, is 11.",
   ],
   "ITM-GEN-02012-19": [
      "\\( \\frac{dw}{dt} = -11 \\), so the rate of change of w with respect to t, the same at every t, is -11.",
      "\\( \\frac{g(3)}{3} = -11 \\), so w divided by t when t = 3 is -11.",
      "\\( \\left. \\frac{dt}{dw} \\right|_{t=3} = -11 \\), so the rate of change of t with respect to w when t = 3 is -11.",
      "\\( \\left. \\frac{dw}{dt} \\right|_{t=3} = -11 \\), so the rate of change of w with respect to t when t = 3 is -11.",
   ],
   "ITM-GEN-02012-20": [
      "\\( \\frac{k(4)}{4} = 1 \\), so r divided by z when z = 4 is 1.",
      "\\( k'(4) = 1 \\), so the rate of change of r with respect to z when z = 4 is 1.",
      "\\( k'(4) = 1 \\), so the rate of change of z with respect to r when z = 4 is 1.",
      "\\( k'(z) = 1 \\), so the rate of change of r with respect to z, the same at every z, is 1.",
   ],
   "ITM-GEN-02012-21": [
      "\\( \\left(h'(2)\\right)^{2} = 12 \\), so the square of the rate of change of s with respect to u when u = 2 is 12.",
      "\\( h''(2) = 12 \\), so the rate of change, with respect to s, of the rate of change of u when u = 2 is 12.",
      "\\( h''(2) = 12 \\), so the rate of change, with respect to u, of the rate of change of s when u = 2 is 12.",
      "\\( h''(u) = 12 \\), so the rate of change, with respect to u, of the rate of change of s, the same at every u, is 12.",
   ],
}

BY_SUFFIX = {
   "02006-00": lambda: derivative_function(9*x**6 - 3 + 5 / x**2),
   "02006-01": lambda: derivative_function(6*sqrt(x) - 9*x**4 + 1),
   "02006-02": lambda: derivative_function(-6*x**4 + 1 + 6 / x**3),
   "02006-03": lambda: derivative_function(-4*x**Rational(1, 3) - 6*x**2 + 1),
   "02006-04": lambda: derivative_function(5*sqrt(x) - 2*x**6 - 6),
   "02006-05": lambda: derivative_function(-8*x**5 - 7 + 7 / x),
   "02006-06": lambda: derivative_function(-6*x**Rational(1, 3) - 2*x**2 + 3),
   "02006-07": lambda: derivative_function(4*sqrt(x) + 3*x**4 - 6),
   "02006-08": lambda: derivative_function(x**5 - 4 - 8 / x),
   "02006-09": lambda: derivative_function(-2*sqrt(x) - 2*x**3 - 8),
   "02006-10": lambda: derivative_function(3*x**5 - 2 - 6 / x**2),
   "02006-11": lambda: derivative_function(6*x**5 - 2 - 2 / x),

   "02007-00": lambda: derivative_function(exp(x) + 3*ln(x) + sin(x) - 5*cos(x) + 6),
   "02007-01": lambda: exact_derivative_value(3*exp(x) + 4*ln(x) + 2*sin(x) - 4*cos(x) - 3, pi / 6),
   "02007-02": lambda: derivative_function(exp(x) - 5*ln(x) + sin(x) - cos(x) + 9),
   "02007-03": lambda: derivative_function(-3*exp(x) + 5*ln(x) + 4*sin(x) - 5*cos(x) + 5),
   "02007-04": lambda: exact_derivative_value(-5*exp(x) + 3*ln(x) + 4*sin(x) - 6*cos(x) + 3, 2*pi / 3),
   "02007-05": lambda: derivative_function(-5*exp(x) - 5*ln(x) + 2*sin(x) - 6*cos(x) + 1),
   "02007-06": lambda: derivative_function(-exp(x) - 5*ln(x) - 4*sin(x) + 3*cos(x) + 2),
   "02007-07": lambda: exact_derivative_value(-2*exp(x) + 5*ln(x) + sin(x) - 5*cos(x) - 2, pi / 2),
   "02007-08": lambda: exact_derivative_value(4*exp(x) - 5*ln(x) - 6*sin(x) - 5*cos(x) - 1, pi / 3),
   "02007-09": lambda: exact_derivative_value(-4*exp(x) + 4*ln(x) + sin(x) + 2*cos(x) - 3, pi / 6),
   "02007-10": lambda: exact_derivative_value(-2*exp(x) + 5*ln(x) + 3*sin(x) - cos(x) + 3, pi / 6),
   "02007-11": lambda: derivative_function(-2*exp(x) + 2*ln(x) - 5*sin(x) - cos(x) + 5),

   "02008-00": lambda: exact_derivative_value((4*x - 4) / cos(x), pi / 3),
   "02008-01": lambda: exact_derivative_value((10 - 2*x**2) / sin(x), pi / 4),
   "02008-02": lambda: exact_derivative_value((6*x**2 + 7) / cos(x), pi / 3),
   "02008-03": lambda: exact_derivative_value((10 - 6*x**2) / sin(x), pi / 6),
   "02008-04": lambda: exact_derivative_value((-4*x - 2) / cos(x), pi / 6),
   "02008-05": lambda: exact_derivative_value((x - 11) / sin(x), pi / 3),
   "02008-06": lambda: exact_derivative_value((2*x**2 + 11) / sin(x), pi / 6),
   "02008-07": lambda: exact_derivative_value((-7*x - 7) / sin(x), pi / 3),
   "02008-08": lambda: exact_derivative_value((3*x + 3) / sin(x), pi / 3),
   "02008-09": lambda: exact_derivative_value((6 - 3*x) / cos(x), pi / 6),
   "02008-10": lambda: exact_derivative_value((4 - 6*x) / cos(x), pi / 3),
   "02008-11": lambda: exact_derivative_value((x - 10) / cos(x), pi / 6),

   "02009-00": lambda: quotient_rule_value(-1, 2, -5, -2),
   "02009-01": lambda: product_rule_value(-5, 5, -4, 5),
   "02009-02": lambda: product_rule_value(4, -2, -3, 1),
   "02009-03": lambda: quotient_rule_value(5, -4, -2, 1),
   "02009-04": lambda: product_rule_value(4, -1, -5, -3),

   "02010-00": lambda: derivative_function(2*cot(x) + 5*sec(x)),
   "02010-01": lambda: exact_derivative_value(-cot(x) + 2*sec(x), pi / 4),
   "02010-02": lambda: derivative_function(5*tan(x) - 2*csc(x)),
   "02010-03": lambda: exact_derivative_value(tan(x) + 5*csc(x), pi / 4),
   "02010-04": lambda: derivative_function(2*tan(x) - 4*csc(x)),
   "02010-05": lambda: exact_derivative_value(-2*csc(x) - 5*sec(x), pi / 6),
   "02010-06": lambda: derivative_function(-4*tan(x) - 5*csc(x)),
   "02010-07": lambda: exact_derivative_value(2*cot(x) + 5*sec(x), pi / 4),
   "02010-08": lambda: derivative_function(-tan(x) - cot(x)),
   "02010-09": lambda: derivative_function(-5*tan(x) - 4*csc(x)),
   "02010-10": lambda: derivative_function(-4*tan(x) + 2*csc(x)),
   "02010-11": lambda: exact_derivative_value(-csc(x) + sec(x), 2*pi / 3),

   "02011-00": lambda: tangent_line_at(-4*x**2 + 6*x + 2, 3),
   "02011-01": lambda: tangent_line_at(-4*x**2 - 6*x + 1, 1),
   "02011-02": lambda: tangent_line_at(-4*x**2 - x + 9, -1, (-1, 6)),
   "02011-03": lambda: tangent_line_at(-2*x**2 - 6*x - 3, -2),
   "02011-04": lambda: tangent_line_at(3*x**2 - 6*x - 9, -2, (-2, 15)),
   "02011-05": lambda: tangent_line_at(x**2 + x + 2, 2, (2, 8)),
   "02011-06": lambda: tangent_line_at(-3*x**2 - 4*x + 8, 3, (3, -31)),
   "02011-07": lambda: tangent_line_at(3*x**2 + 4*x + 7, -2, (-2, 11)),
   "02011-08": lambda: tangent_line_at(x**2 - 3*x + 5, -1),
   "02011-09": lambda: tangent_line_at(-4*x**2 + 5*x + 8, 3, (3, -13)),
   "02011-10": lambda: tangent_line_at(x**2 - 4*x - 8, -3),
   "02011-11": lambda: tangent_line_at(-4*x**2 + 6*x - 3, -1),

   "02012-00": lambda: notation_statement("ITM-GEN-02012-00", "the temperature", "the distance along the rod", 1),
   "02012-01": lambda: notation_statement("ITM-GEN-02012-01", "y", "x", 1),
   "02012-02": lambda: notation_statement("ITM-GEN-02012-02", "w", "t", 1),
   "02012-03": lambda: notation_statement("ITM-GEN-02012-03", "the height of the balloon", "time", 1),
   "02012-04": lambda: notation_statement("ITM-GEN-02012-04", "w", "t", 2),
   "02012-05": lambda: notation_statement("ITM-GEN-02012-05", "w", "t", 1),
   "02012-06": lambda: notation_statement("ITM-GEN-02012-06", "s", "u", 2),
   "02012-07": lambda: notation_statement("ITM-GEN-02012-07", "y", "x", 2),
   "02012-08": lambda: notation_statement("ITM-GEN-02012-08", "y", "x", 2),
   "02012-09": lambda: notation_statement("ITM-GEN-02012-09", "the number of bacteria", "time", 1),
   "02012-10": lambda: notation_statement("ITM-GEN-02012-10", "y", "x", 1),
   "02012-11": lambda: notation_statement("ITM-GEN-02012-11", "y", "x", 2),
   "02012-12": lambda: notation_statement("ITM-GEN-02012-12", "the height of the balloon", "time", 1),
   "02012-13": lambda: notation_statement("ITM-GEN-02012-13", "the volume of water", "time", 2),
   "02012-14": lambda: notation_statement("ITM-GEN-02012-14", "r", "z", 1),
   "02012-15": lambda: notation_statement("ITM-GEN-02012-15", "the temperature", "the distance along the rod", 1),
   "02012-16": lambda: notation_statement("ITM-GEN-02012-16", "the height of the balloon", "time", 1),
   "02012-17": lambda: notation_statement("ITM-GEN-02012-17", "w", "t", 1),
   "02012-18": lambda: notation_statement("ITM-GEN-02012-18", "r", "z", 2),
   "02012-19": lambda: notation_statement("ITM-GEN-02012-19", "w", "t", 1),
   "02012-20": lambda: notation_statement("ITM-GEN-02012-20", "r", "z", 1),
   "02012-21": lambda: notation_statement("ITM-GEN-02012-21", "s", "u", 2),

   "02013-00": lambda: model_rate(1, -2, 4, 22, 3),
   "02013-01": lambda: model_rate(1, 4, 5, 27, 3),
   "02013-02": lambda: model_rate(1, -3, 2, 27, 1),
   "02013-03": lambda: model_rate(1, 4, 4, 22, 1),
   "02013-04": lambda: model_rate(1, 4, 4, 21, 1),
   "02013-05": lambda: model_rate(1, 2, 2, 21, 3),
   "02013-06": lambda: model_rate(1, 2, 4, 20, 3),
   "02013-07": lambda: model_rate(1, -4, 3, 30, "2.5"),
   "02013-08": lambda: model_rate(1, -4, 5, 25, 2),
   "02013-09": lambda: model_rate(1, -4, 4, 27, 1),
   "02013-10": lambda: model_rate(1, -2, 3, 25, 1),
   "02013-11": lambda: model_rate(1, -3, 4, 26, 3),
   "02013-12": lambda: model_rate(1, 2, 4, 27, 3),
   "02013-13": lambda: model_rate(1, -3, 5, 29, 2),
   "02013-14": lambda: model_rate(1, -4, 2, 28, 1),
   "02013-15": lambda: model_rate(1, 4, 2, 22, "1.5"),
   "02013-16": lambda: model_rate(1, -2, 4, 25, 3),
   "02013-17": lambda: model_rate(1, -3, 2, 24, 3),
   "02013-18": lambda: model_rate(1, 3, 3, 28, "1.5"),
   "02013-19": lambda: model_rate(1, 2, 3, 28, 3),
   "02013-20": lambda: model_rate(1, -2, 2, 24, "2.5"),
   "02013-21": lambda: model_rate(1, 2, 5, 23, 2),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
