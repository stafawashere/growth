"""Each unit 3 item in stems batch s15, written as the SymPy computation of the answer its stem asks for."""
import sympy
from sympy import Rational, acos, asin, atan, sqrt

from tools.key_recheck import derivative, x


def product_derivative_at(expression, at):
   return sympy.nsimplify(sympy.simplify(derivative(expression).subs(x, at)))


def inverse_trig_derivative(inverse_function, argument):
   return sympy.simplify(derivative(inverse_function(argument)))


BY_SUFFIX = {
   "03001-12": lambda: product_derivative_at(5 * x**2 * (23 - 2 * x**2) ** 3, 3),
   "03001-13": lambda: product_derivative_at(5 * x**2 * sqrt(18 - 2 * x**2), -1),
   "03001-14": lambda: product_derivative_at(x**2 * sqrt(2 * x**2 + 17), 2),
   "03001-15": lambda: product_derivative_at(5 * x**2 * sqrt(22 - 2 * x**2), -3),
   "03001-16": lambda: product_derivative_at(4 * x**2 * sqrt(2 * x**2 - 17), 3),
   "03001-17": lambda: product_derivative_at(4 * x**2 * (12 - 2 * x**2) ** 2, -2),
   "03001-18": lambda: product_derivative_at(2 * x**2 * (6 - 2 * x**2) ** 3, 1),
   "03001-19": lambda: product_derivative_at(x * sqrt(3 * x**2 + 6), 1),
   "03001-20": lambda: product_derivative_at(4 * x * sqrt(2 * x**2 - 2), 3),
   "03001-21": lambda: product_derivative_at(3 * x**2 * sqrt(19 - 2 * x**2), 3),
   "03001-22": lambda: product_derivative_at(x * sqrt(3 * x**2 - 11), 3),
   "03001-23": lambda: product_derivative_at(5 * x * (19 - 2 * x**2) ** 4, -3),

   "03010-00": lambda: inverse_trig_derivative(acos, (2 * x - 5) / Rational(11)),
   "03010-01": lambda: inverse_trig_derivative(atan, (2 * x - 2) / Rational(9)),
   "03010-02": lambda: inverse_trig_derivative(atan, (4 - 3 * x) / Rational(2)),
   "03010-03": lambda: inverse_trig_derivative(acos, (5 * x - 7) / Rational(7)),
   "03010-04": lambda: inverse_trig_derivative(acos, (-2 * x - 1) / Rational(11)),
   "03010-05": lambda: inverse_trig_derivative(acos, (-3 * x - 6) / Rational(2)),
   "03010-06": lambda: inverse_trig_derivative(acos, (4 * x + 7) / Rational(9)),
   "03010-07": lambda: inverse_trig_derivative(acos, (-2 * x - 10) / Rational(5)),
   "03010-08": lambda: inverse_trig_derivative(asin, 2 * x / Rational(11)),
   "03010-09": lambda: inverse_trig_derivative(acos, (-3 * x - 5) / Rational(11)),
   "03010-10": lambda: inverse_trig_derivative(atan, (1 - 2 * x) / Rational(5)),
   "03010-11": lambda: inverse_trig_derivative(acos, (2 * x + 1) / Rational(5)),
   "03010-12": lambda: inverse_trig_derivative(atan, (4 - 3 * x) / Rational(8)),
   "03010-13": lambda: inverse_trig_derivative(atan, (-4 * x - 9) / Rational(5)),
   "03010-14": lambda: inverse_trig_derivative(atan, (-3 * x - 9) / Rational(10)),
   "03010-15": lambda: inverse_trig_derivative(atan, (3 - 3 * x) / Rational(10)),
   "03010-16": lambda: inverse_trig_derivative(atan, 2 * x / Rational(3)),
   "03010-17": lambda: inverse_trig_derivative(asin, (-3 * x - 3) / Rational(2)),
   "03010-18": lambda: inverse_trig_derivative(atan, (-2 * x - 8) / Rational(9)),
   "03010-19": lambda: inverse_trig_derivative(acos, (3 * x - 1) / Rational(2)),
   "03010-20": lambda: inverse_trig_derivative(acos, (5 * x + 4) / Rational(4)),
   "03010-21": lambda: inverse_trig_derivative(asin, (3 * x + 2) / Rational(4)),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
