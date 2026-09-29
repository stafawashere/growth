"""Stems of the unit 6 generated items in archetypes 06008, 06009, 06011 and 06016 from stems_s15.json,
each written as the SymPy computation of the answer it asks for, from the stem alone."""
import sympy
from sympy import Abs, Rational, cos, exp, log, oo, pi, sqrt

from tools.key_recheck import definite_integral, equivalent, x

w, s = sympy.symbols("w s")
t = sympy.Symbol("t")

CHOICES_BY_ID = {
   "ITM-GEN-06011-22": [
      "The integral converges to \\( - 18 \\sqrt{34} \\).",
      "The integral converges to \\( - 6 \\sqrt{34} \\).",
      "The integral converges to \\( \\infty - 6 \\sqrt{34} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-23": [
      "The integral converges to \\( - \\frac{4}{111} \\).",
      "The integral converges to \\( - \\frac{4}{37} \\).",
      "The integral converges to \\( \\infty - \\frac{4}{111} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-24": [
      "The integral converges to \\( \\frac{1}{17} \\).",
      "The integral converges to \\( \\frac{1}{2} \\).",
      "The integral converges to \\( \\frac{1}{4} \\).",
      "The integral converges to \\( \\frac{2}{17} \\).",
   ],
   "ITM-GEN-06011-25": [
      "The integral converges to \\( - \\frac{4}{189} \\).",
      "The integral converges to \\( - \\frac{4}{63} \\).",
      "The integral converges to \\( \\infty - \\frac{4}{189} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-26": [
      "The integral converges to \\( \\frac{3}{4} \\).",
      "The integral converges to \\( \\frac{3}{68} \\).",
      "The integral converges to \\( \\frac{9}{4} \\).",
      "The integral converges to \\( \\frac{9}{68} \\).",
   ],
   "ITM-GEN-06011-27": [
      "The integral converges to \\( \\frac{3}{20} \\).",
      "The integral converges to \\( \\frac{3}{40} \\).",
      "The integral converges to \\( \\frac{3}{4} \\).",
      "The integral converges to \\( \\frac{3}{8} \\).",
   ],
   "ITM-GEN-06011-28": [
      "The integral converges to \\( 16 \\sqrt{37} \\).",
      "The integral converges to \\( 32 - 16 \\sqrt{3} \\).",
      "The integral converges to \\( \\frac{16 \\sqrt{37}}{3} \\).",
      "The integral converges to \\( \\frac{32}{3} - \\frac{16 \\sqrt{3}}{3} \\).",
   ],
   "ITM-GEN-06011-29": [
      "The integral converges to \\( \\frac{5}{14} \\).",
      "The integral converges to \\( \\frac{5}{28} \\).",
      "The integral converges to \\( \\frac{5}{3} \\).",
      "The integral converges to \\( \\frac{5}{6} \\).",
   ],
   "ITM-GEN-06011-30": [
      "The integral converges to \\( - \\frac{1}{2} \\).",
      "The integral converges to \\( - \\frac{1}{4} \\).",
      "The integral converges to \\( \\infty - \\frac{1}{4} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-31": [
      "The integral converges to \\( - \\frac{2}{3} \\).",
      "The integral converges to \\( - \\frac{4}{3} \\).",
      "The integral converges to \\( \\infty - \\frac{2}{3} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-32": [
      "The integral converges to \\( - 16 \\sqrt{13} \\).",
      "The integral converges to \\( - 8 \\sqrt{13} \\).",
      "The integral converges to \\( \\infty - 8 \\sqrt{13} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-33": [
      "The integral converges to \\( - 4 \\sqrt{10} \\).",
      "The integral converges to \\( - 8 \\sqrt{10} \\).",
      "The integral converges to \\( \\infty - 4 \\sqrt{10} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-34": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( \\frac{1}{35} \\).",
      "The integral converges to \\( \\frac{1}{3} \\).",
      "The integral converges to \\( \\frac{3}{35} \\).",
   ],
   "ITM-GEN-06011-35": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( 2 \\).",
      "The integral converges to \\( 2 \\sqrt{15} \\).",
      "The integral converges to \\( \\sqrt{15} \\).",
   ],
   "ITM-GEN-06011-36": [
      "The integral converges to \\( - 16 \\sqrt{6} \\).",
      "The integral converges to \\( - \\frac{16 \\sqrt{6}}{3} \\).",
      "The integral converges to \\( \\infty - \\frac{16 \\sqrt{6}}{3} \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-37": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( 2 \\).",
      "The integral converges to \\( \\frac{1}{3} \\).",
      "The integral converges to \\( \\frac{1}{6} \\).",
   ],
   "ITM-GEN-06011-38": [
      "The integral converges to \\( \\frac{5}{13} \\).",
      "The integral converges to \\( \\frac{5}{2} \\).",
      "The integral converges to \\( \\frac{5}{39} \\).",
      "The integral converges to \\( \\frac{5}{6} \\).",
   ],
   "ITM-GEN-06011-39": [
      "The integral converges to \\( \\frac{3}{11} \\).",
      "The integral converges to \\( \\frac{3}{2} \\).",
      "The integral converges to \\( \\frac{9}{11} \\).",
      "The integral converges to \\( \\frac{9}{2} \\).",
   ],
   "ITM-GEN-06011-40": [
      "The integral converges to \\( - 8 \\sqrt{3} + 8 \\sqrt{5} \\).",
      "The integral converges to \\( - \\frac{8 \\sqrt{3}}{3} + \\frac{8 \\sqrt{5}}{3} \\).",
      "The integral converges to \\( 56 \\sqrt{2} \\).",
      "The integral converges to \\( \\frac{56 \\sqrt{2}}{3} \\).",
   ],
   "ITM-GEN-06011-41": [
      "The integral converges to \\( -24 \\).",
      "The integral converges to \\( -8 \\).",
      "The integral converges to \\( \\infty - 8 \\).",
      "The integral diverges.",
   ],
   "ITM-GEN-06011-42": [
      "The integral converges to \\( 12 - 6 \\sqrt{3} \\).",
      "The integral converges to \\( 3 \\sqrt{7} \\).",
      "The integral converges to \\( 6 - 3 \\sqrt{3} \\).",
      "The integral converges to \\( 6 \\sqrt{7} \\).",
   ],
   "ITM-GEN-06011-43": [
      "The integral converges to \\( 7 \\).",
      "The integral converges to \\( \\frac{7}{24} \\).",
      "The integral converges to \\( \\frac{7}{3} \\).",
      "The integral converges to \\( \\frac{7}{8} \\).",
   ],
}

DIVERGES = "diverges"
NONSENSE = "nonsense"


def antiderivative(integrand, variable=x):
   return sympy.integrate(integrand, variable)


def substitution_integral(integrand, lower=None, upper=None):
   is_indefinite = lower is None

   if is_indefinite:
      return antiderivative(integrand)

   return sympy.simplify(definite_integral(integrand, lower, upper))


def parts_integral(integrand, variable, lower=None, upper=None):
   is_indefinite = lower is None

   if is_indefinite:
      return antiderivative(integrand, variable)

   return sympy.simplify(definite_integral(integrand, lower, upper, variable))


def improper_choice(item_id, integrand, lower, upper, choice_values):
   """choice_values lines up with the item's choices: an exact value, DIVERGES, or NONSENSE for
   a choice that names no real number."""
   value = definite_integral(integrand, lower, upper)
   is_divergent = value.has(oo, -oo, sympy.zoo, sympy.nan) or not value.is_finite
   choices = CHOICES_BY_ID[item_id]
   matching = []

   for text, choice_value in zip(choices, choice_values):
      if choice_value == NONSENSE:
         continue

      if choice_value == DIVERGES:
         if is_divergent:
            matching.append(text)

         continue

      is_match = not is_divergent and equivalent(value, choice_value)

      if is_match:
         matching.append(text)

   if len(matching) == 1:
      return matching[0]

   return matching


def divided_log_integral(numerator, denominator):
   """Long division first, so the logarithm keeps its absolute value."""
   quotient, remainder = sympy.div(numerator, denominator, x)
   linear_coefficient = sympy.Poly(denominator, x).LC()
   log_part = remainder / linear_coefficient * log(Abs(denominator))

   return sympy.integrate(quotient, x) + log_part


def exponential_parts(coefficient, rate):
   return antiderivative(coefficient * x * exp(rate * x))


BY_SUFFIX = {
   "06008-05": lambda: substitution_integral(7 * x * cos(2 * x**2 + 3), 0, 1),
   "06008-06": lambda: substitution_integral(4 * x**2 * cos(2 * x**3 + 3)),
   "06008-07": lambda: substitution_integral(9 * x**2 * cos(x**3 + 4), 0, 1),
   "06008-08": lambda: substitution_integral(7 * x**2 * exp(2 * x**3 + 2)),
   "06008-09": lambda: substitution_integral(4 * x**2 * cos(x**3 + 1), 0, 2),

   "06009-05": lambda: parts_integral(-5 * w * exp(2 * w), w),
   "06009-06": lambda: parts_integral(-5 * t * cos(5 * t), t, 0, pi / 15),
   "06009-07": lambda: parts_integral(2 * x * exp(2 * x), x, 0, 1),
   "06009-08": lambda: parts_integral(w * exp(4 * w), w, 0, 2),
   "06009-09": lambda: parts_integral(3 * s * cos(5 * s), s),

   "06011-22": lambda: improper_choice("ITM-GEN-06011-22", 9 * x**2 / sqrt(x**3 + 7), 3, oo, [-18 * sqrt(34), -6 * sqrt(34), NONSENSE, DIVERGES]),
   "06011-23": lambda: improper_choice("ITM-GEN-06011-23", 4 * x**2 / (x**3 - 27)**2, 3, 4, [Rational(-4, 111), Rational(-4, 37), NONSENSE, DIVERGES]),
   "06011-24": lambda: improper_choice("ITM-GEN-06011-24", 2 * x / (x**2 + 1)**2, 4, oo, [Rational(1, 17), Rational(1, 2), Rational(1, 4), Rational(2, 17)]),
   "06011-25": lambda: improper_choice("ITM-GEN-06011-25", 4 * x**2 / (x**3 - 1)**2, 1, 4, [Rational(-4, 189), Rational(-4, 63), NONSENSE, DIVERGES]),
   "06011-26": lambda: improper_choice("ITM-GEN-06011-26", 9 * x**2 / (x**3 + 4)**2, 4, oo, [Rational(3, 4), Rational(3, 68), Rational(9, 4), Rational(9, 68)]),
   "06011-27": lambda: improper_choice("ITM-GEN-06011-27", 3 * x / (x**2 + 4)**2, 4, oo, [Rational(3, 20), Rational(3, 40), Rational(3, 4), Rational(3, 8)]),
   "06011-28": lambda: improper_choice("ITM-GEN-06011-28", 8 * x**2 / sqrt(x**3 - 27), 3, 4, [16 * sqrt(37), 32 - 16 * sqrt(3), 16 * sqrt(37) / 3, Rational(32, 3) - 16 * sqrt(3) / 3]),
   "06011-29": lambda: improper_choice("ITM-GEN-06011-29", 5 * x / (x**2 + 5)**2, 3, oo, [Rational(5, 14), Rational(5, 28), Rational(5, 3), Rational(5, 6)]),
   "06011-30": lambda: improper_choice("ITM-GEN-06011-30", 6 * x / (x**2 - 4)**2, 2, 4, [Rational(-1, 2), Rational(-1, 4), NONSENSE, DIVERGES]),
   "06011-31": lambda: improper_choice("ITM-GEN-06011-31", 4 * x / (x**2 - 1)**2, 1, 2, [Rational(-2, 3), Rational(-4, 3), NONSENSE, DIVERGES]),
   "06011-32": lambda: improper_choice("ITM-GEN-06011-32", 8 * x / sqrt(x**2 + 4), 3, oo, [-16 * sqrt(13), -8 * sqrt(13), NONSENSE, DIVERGES]),
   "06011-33": lambda: improper_choice("ITM-GEN-06011-33", 4 * x / sqrt(x**2 + 6), 2, oo, [-4 * sqrt(10), -8 * sqrt(10), NONSENSE, DIVERGES]),
   "06011-34": lambda: improper_choice("ITM-GEN-06011-34", 3 * x**2 / (x**3 + 8)**2, 3, oo, [1, Rational(1, 35), Rational(1, 3), Rational(3, 35)]),
   "06011-35": lambda: improper_choice("ITM-GEN-06011-35", x / sqrt(x**2 - 1), 1, 4, [1, 2, 2 * sqrt(15), sqrt(15)]),
   "06011-36": lambda: improper_choice("ITM-GEN-06011-36", 8 * x**2 / sqrt(x**3 + 5), 1, oo, [-16 * sqrt(6), -16 * sqrt(6) / 3, NONSENSE, DIVERGES]),
   "06011-37": lambda: improper_choice("ITM-GEN-06011-37", 2 * x / (x**2 + 5)**2, 1, oo, [1, 2, Rational(1, 3), Rational(1, 6)]),
   "06011-38": lambda: improper_choice("ITM-GEN-06011-38", 5 * x**2 / (x**3 + 5)**2, 2, oo, [Rational(5, 13), Rational(5, 2), Rational(5, 39), Rational(5, 6)]),
   "06011-39": lambda: improper_choice("ITM-GEN-06011-39", 9 * x**2 / (x**3 + 3)**2, 2, oo, [Rational(3, 11), Rational(3, 2), Rational(9, 11), Rational(9, 2)]),
   "06011-40": lambda: improper_choice("ITM-GEN-06011-40", 4 * x**2 / sqrt(x**3 - 27), 3, 5, [-8 * sqrt(3) + 8 * sqrt(5), -8 * sqrt(3) / 3 + 8 * sqrt(5) / 3, 56 * sqrt(2), 56 * sqrt(2) / 3]),
   "06011-41": lambda: improper_choice("ITM-GEN-06011-41", 2 * x**2 / sqrt(x**3 + 9), 3, oo, [-24, -8, NONSENSE, DIVERGES]),
   "06011-42": lambda: improper_choice("ITM-GEN-06011-42", 3 * x / sqrt(x**2 - 9), 3, 4, [12 - 6 * sqrt(3), 3 * sqrt(7), 6 - 3 * sqrt(3), 6 * sqrt(7)]),
   "06011-43": lambda: improper_choice("ITM-GEN-06011-43", 7 * x**2 / (x**3 + 7)**2, 1, oo, [7, Rational(7, 24), Rational(7, 3), Rational(7, 8)]),

   "06016-22": lambda: exponential_parts(2, 1),
   "06016-23": lambda: divided_log_integral(5 * x**2 + 30, x - 3),
   "06016-24": lambda: divided_log_integral(6 * x**2 + 6, x + 1),
   "06016-25": lambda: exponential_parts(4, -1),
   "06016-26": lambda: divided_log_integral(3 * x**2 + 9, x - 2),
   "06016-27": lambda: exponential_parts(5, -3),
   "06016-28": lambda: exponential_parts(2, 2),
   "06016-29": lambda: divided_log_integral(6 * x**2 + 24, x - 2),
   "06016-30": lambda: divided_log_integral(2 * x**2 + 16, x + 5),
   "06016-31": lambda: divided_log_integral(6 * x**2 + 12, x - 1),
   "06016-32": lambda: exponential_parts(6, 2),
   "06016-33": lambda: divided_log_integral(5 * x**2 + 10, x + 4),
   "06016-34": lambda: divided_log_integral(2 * x**2 + 6, x - 1),
   "06016-35": lambda: divided_log_integral(x**2 + 2, x - 2),
   "06016-36": lambda: divided_log_integral(5 * x**2 + 40, x + 2),
   "06016-37": lambda: divided_log_integral(4 * x**2 + 20, x - 5),
   "06016-38": lambda: exponential_parts(6, -2),
   "06016-39": lambda: exponential_parts(6, 4),
   "06016-40": lambda: divided_log_integral(2 * x**2 + 16, x - 3),
   "06016-41": lambda: divided_log_integral(4 * x**2 + 20, x + 4),
   "06016-42": lambda: exponential_parts(6, 3),
   "06016-43": lambda: exponential_parts(1, 1),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
