"""Blind answers for the unit 6 generated items in stems_R.json, one SymPy computation per stem.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, without seeing any key, worked solution or template. Definite integrals are exact
values; indefinite integrals are an antiderivative plus the constant C.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import sympy
from sympy import cos, exp

from tools.key_recheck import INTEGRATION_CONSTANT, definite_integral, x


def exact_integral(integrand, lower, upper):
   return sympy.simplify(definite_integral(integrand, lower, upper))


def antiderivative(integrand):
   return sympy.integrate(integrand, x) + INTEGRATION_CONSTANT


def partial_fraction_antiderivative(integrand):
   # Corrected by the lead on review, 2026-09-24: SymPy writes log(x - a), which is not real for
   # x < a; an antiderivative over the reals carries the absolute value.
   found = sympy.integrate(sympy.apart(integrand, x), x)
   real_logs = found.replace(sympy.log, lambda argument: sympy.log(sympy.Abs(argument)))

   return real_logs + INTEGRATION_CONSTANT


BY_SUFFIX = {
   "06008-00": lambda: exact_integral(3*x*cos(x**2 + 4), 0, 2),
   "06008-01": lambda: antiderivative(3*x**2*cos(2*x**3 + 2)),
   "06008-02": lambda: exact_integral(9*x**2*exp(2*x**3 + 2), 0, 1),
   "06008-03": lambda: antiderivative(x*cos(2*x**2 + 1)),
   "06008-04": lambda: antiderivative(x**2*exp(2*x**3 + 1)),

   "06010-00": lambda: partial_fraction_antiderivative(64 / (5*x**2 - 18*x - 35)),
   "06010-01": lambda: partial_fraction_antiderivative((4*x**2 - 11*x + 106) / (4*x**2 - 11*x - 20)),
   "06010-02": lambda: partial_fraction_antiderivative((5*x**2 - 17*x - 81) / (5*x**2 - 17*x - 12)),
   "06010-03": lambda: partial_fraction_antiderivative((3*x**2 - 5*x + 67) / (3*x**2 - 5*x - 28)),
   "06010-04": lambda: partial_fraction_antiderivative(-26 / (2*x**2 - 7*x - 15)),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
