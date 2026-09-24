"""Each agent-drafted polar tangent item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. The slope is dy/dx with
x = r cos(theta) and y = r sin(theta). An edited stem needs its entry rewritten the same way
before the recheck can pass. app/items/ingest.py loads only .json records, so this file never
reaches the bank.
"""
from sympy import cos, exp, pi, sin

from tools.key_recheck import polar_slope, theta

ITEM_PREFIX = "ITM-AGT-"

BY_SUFFIX = {
   "99003-00": lambda: polar_slope(2 + sin(theta), pi / 6),
   "99003-01": lambda: polar_slope(1 + cos(theta), pi / 3),
   "99003-02": lambda: polar_slope(3*cos(2*theta), pi / 6),
   "99003-03": lambda: polar_slope(2*sin(3*theta), pi / 4),
   "99003-04": lambda: polar_slope(theta, pi / 2),
   "99003-05": lambda: polar_slope(theta, pi / 4),
   "99003-06": lambda: polar_slope(exp(theta), pi / 3),
   "99003-07": lambda: polar_slope(4*cos(theta), pi / 6),
   "99003-08": lambda: polar_slope(1 + 2*sin(theta), pi / 6),
   "99003-09": lambda: polar_slope(sin(2*theta), pi / 6),
   "99003-10": lambda: polar_slope(1 - sin(theta), pi / 3),
   "99003-11": lambda: polar_slope(2*theta, pi),
   "99003-12": lambda: polar_slope(3*sin(theta), pi / 3),
   "99003-13": lambda: polar_slope(4*sin(2*theta), pi / 6),
   "99003-14": lambda: polar_slope(2 + cos(theta), pi / 2),
   "99003-15": lambda: polar_slope(3 - 2*cos(theta), pi / 3),
   "99003-16": lambda: polar_slope(cos(2*theta), pi / 3),
   "99003-17": lambda: polar_slope(1 + 2*cos(2*theta), pi / 6),
   "99003-18": lambda: polar_slope(2*sin(2*theta), pi / 3),
   "99003-19": lambda: polar_slope(2 + 2*sin(theta), pi / 3),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
