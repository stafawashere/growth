"""Each agent-drafted Unit 3 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. An edited stem needs its entry
rewritten the same way before the recheck can pass again. app/items/ingest.py loads only .json
records, so this file never reaches the bank.
"""
import sympy
from sympy import cos, exp, ln, sin, sqrt, tan

from tools.key_recheck import derivative, x

ITEM_PREFIX = "ITM-AGT-"


def derivative_at_zero(expression):
   return sympy.simplify(derivative(expression).subs(x, 0))


BY_SUFFIX = {
   "03009-00": lambda: derivative(3**x * sin(3*x)**2),
   "03009-01": lambda: derivative(2**x * cos(2*x)**3),
   "03009-02": lambda: derivative(exp(x) * sqrt(1 + sin(4*x))),
   "03009-03": lambda: derivative(5**x * exp(cos(x**2))),
   "03009-04": lambda: derivative(2**x * ln(2 + sin(3*x))),
   "03009-05": lambda: derivative(3**x * tan(5*x)**2),
   "03009-06": lambda: derivative(exp(x) * exp(sin(3*x))),
   "03009-07": lambda: derivative(5**x * (1 + sin(4*x))**2),
   "03009-08": lambda: derivative(exp(sin(5*x)) / 3**x),
   "03009-09": lambda: derivative(sin(3*x)**2 / 2**x),
   "03009-10": lambda: derivative(cos(2*x)**3 / exp(x)),
   "03009-11": lambda: derivative(sqrt(1 + sin(4*x)) / 5**x),
   "03009-12": lambda: derivative((1 + sin(2*x))**3 / 3**x),

   "03009-13": lambda: derivative_at_zero(2**x * (1 + sin(2*x))**3),
   "03009-14": lambda: derivative_at_zero(3**x * exp(sin(3*x))),
   "03009-15": lambda: derivative_at_zero(5**x * sqrt(1 + sin(6*x))),
   "03009-16": lambda: derivative_at_zero((1 + sin(4*x))**2 / 2**x),
   "03009-17": lambda: derivative_at_zero((1 + sin(2*x))**3 / 3**x),
   "03009-18": lambda: derivative_at_zero(exp(sin(5*x)) / 5**x),
   "03009-19": lambda: derivative_at_zero(2**x * ln(2 + sin(3*x))),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
