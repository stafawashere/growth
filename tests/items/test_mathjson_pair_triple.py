"""app/items/mathjson.py: the MathLive field (Compute Engine 0.24) writes integral bounds as
Triple and two-element tuples as Pair, and to_sympy reads both the way it reads Tuple."""
import sympy

from app.items.mathjson import to_sympy

APP_INTEGRAL = [
   "Integrate",
   ["Add", ["Multiply", "t", ["Exp", ["Negate", ["Divide", "t", 2]]]], 5],
   ["Triple", "t", 0, 4.5],
]


def test_triple_bounds_from_the_app_read_as_an_integral_over_t():
   integral = to_sympy(APP_INTEGRAL)
   (variable, lower, upper), = integral.limits

   assert isinstance(integral, sympy.Integral)
   assert variable.name == "t"
   assert lower == 0
   assert upper == sympy.Float(4.5)
   assert abs(float(integral.evalf()) - 25.129810) < 1e-6


def test_pair_reads_as_a_tuple():
   assert to_sympy(["Pair", 1, "x"]) == sympy.Tuple(1, sympy.Symbol("x"))


def test_plain_triple_reads_as_a_tuple():
   assert to_sympy(["Triple", 1, 2, "y"]) == sympy.Tuple(1, 2, sympy.Symbol("y"))
