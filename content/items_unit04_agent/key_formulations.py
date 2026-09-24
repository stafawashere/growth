"""Each agent-drafted Unit 4 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. A rate stated as "decreasing at
a rate of r" enters as -r. A function known only through f, f' and f'' at a point is stood in for
by the quadratic with those values, which fixes every limit here because each depends on at most
those values. An edited stem needs its entry rewritten the same way before the recheck can pass.
app/items/ingest.py loads only .json records, so this file never reaches the bank.
"""
from sympy import cos, exp, ln, sin, sqrt

from tools.key_recheck import function_with_values, limit_at, related_rate, x, y

ITEM_PREFIX = "ITM-AGT-"


def known_function(center, values):
   return function_with_values(center, values)


BY_SUFFIX = {
   "04007-00": lambda: related_rate(x**2 + x*y + y**2 - 7, (1, 2), 3, known="x"),
   "04007-01": lambda: related_rate(x**3 + y**3 - 9, (1, 2), 4, known="x"),
   "04007-02": lambda: related_rate(x*y**2 - 12, (3, 2), -1, known="y"),
   "04007-03": lambda: related_rate(x**2*y - 18, (3, 2), 2, known="x"),
   "04007-04": lambda: related_rate(x**2 + y**2 - 25, (3, 4), -2, known="x"),
   "04007-05": lambda: related_rate(x**2 - 3*x*y + y**2 + 1, (2, 1), 2, known="y"),
   "04007-06": lambda: related_rate(x*y + y**2 - 6, (1, 2), 5, known="x"),
   "04007-07": lambda: related_rate(x**2 + 4*y**2 - 20, (4, 1), 3, known="y"),
   "04007-08": lambda: related_rate(-x*y + y**3 - 6, (1, 2), -4, known="x"),
   "04007-09": lambda: related_rate(sqrt(x) + sqrt(y) - 5, (4, 9), 6, known="x"),
   "04007-10": lambda: related_rate(x*y - 8, (2, 4), -3, known="x"),
   "04007-11": lambda: related_rate(2*x**2 + x*y - y**2 - 8, (2, 0), 4, known="y"),
   "04007-12": lambda: related_rate(x**3 + x*y**2 - 10, (1, 3), -2, known="y"),
   "04007-13": lambda: related_rate(-x**3 + y**2 - 1, (2, 3), 2, known="x"),
   "04007-14": lambda: related_rate(x**2 + x*y - 10, (2, 3), -5, known="y"),
   "04007-15": lambda: related_rate(x**2 - y**2 - 16, (5, 3), 5, known="y"),
   "04007-16": lambda: related_rate(3*x**2 - 2*x*y + y**2 - 11, (1, -2), 3, known="x"),
   "04007-17": lambda: related_rate(x**2*y**2 - 36, (2, 3), -4, known="x"),
   "04007-18": lambda: related_rate(x*exp(y) - 2, (2, 0), 4, known="x"),
   "04007-19": lambda: related_rate(x**2 - 4*x + y**2 + 6*y - 12, (5, 1), -3, known="y"),

   "04009-00": lambda: limit_at((exp(2*x) - 1 - 2*x) / (x**2 + x**3), 0),
   "04009-02": lambda: limit_at((ln(1 + x) - x) / (x**2 + x**3), 0),
   "04009-04": lambda: limit_at((x*ln(x) - x + 1) / (x**3 - 2*x**2 + x), 1),
   "04009-06": lambda: limit_at((exp(x) - cos(x) - x) / (x**2 + x**3), 0),
   "04009-08": lambda: limit_at((x**3 - 3*x**2 + 4) / (x**3 - 4*x**2 + 4*x), 2),
   "04009-10": lambda: limit_at((1 - cos(x)) / (x**2 + x**3), 0),
   "04009-12": lambda: limit_at((exp(x) - 1 - sin(x)) / (x*(exp(x) - 1)), 0),
   "04009-14": lambda: limit_at((sin(2*x) - 2*x) / (x**3 + x**4), 0),
   "04009-16": lambda: limit_at((exp(3*x) - 3*x - 1) / (1 - cos(x) + x**3), 0),
   "04009-18": lambda: limit_at((x**4 - 4*x + 3) / (x**3 - 3*x + 2), 1),

   "04009-01": lambda: limit_at((known_function(1, [4, 2, 6]).subs(x, 3*x - 2) - 4) / (x**2 - 1), 1),
   "04009-03": lambda: limit_at(x*known_function(0, [5, -2, 4]) / (exp(x) - 1), 0),
   "04009-05": lambda: limit_at((known_function(3, [2, 2, 1]).subs(x, x**2 - 6) - 2) / ln(x - 2), 3),
   "04009-07": lambda: limit_at((exp(known_function(0, [0, 2, 1])) - 1) / (x**2 + 2*x), 0),
   "04009-09": lambda: limit_at((known_function(1, [5, -2, 3]).subs(x, x**2) - 5) / ln(x), 1),
   "04009-11": lambda: limit_at(known_function(0, [6, -3, 2])*sin(x) / (x**2 + 3*x), 0),
   "04009-13": lambda: limit_at((x*known_function(2, [4, -1, 3]) - 8) / (x**2 - 4), 2),
   "04009-15": lambda: limit_at((known_function(0, [3, -1, 2])**2 - 9) / (x**2 + 2*x), 0),
   "04009-17": lambda: limit_at((sqrt(known_function(2, [9, 12, 2])) - 3) / (x**2 - 2*x), 2),
   "04009-19": lambda: limit_at((known_function(0, [2, 4, -1]).subs(x, x**2 + 3*x) - 2) / (exp(2*x) - 1), 0),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
