"""Blind answers for the polar items in stems_R.json of the unit 9 bank, one SymPy computation per stem.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, without seeing any key, worked solution or template. Each stem gives dy/dx and dy/dtheta
at a point P, so dx/dtheta = (dy/dtheta) / (dy/dx) there, without differentiating the polar equation.
"""
import sympy
from sympy import Rational, sqrt


def dx_dtheta(slope, dy_dtheta):
   return sympy.radsimp(sympy.nsimplify(dy_dtheta) / sympy.nsimplify(slope))


R = Rational

BY_SUFFIX = {
   "99001-00": lambda: dx_dtheta(2*sqrt(3)/7, -2*sqrt(3)),
   "99001-01": lambda: dx_dtheta(-R(20, 13) + 21*sqrt(3)/13, -5*sqrt(3)/2 - 1),
   "99001-02": lambda: dx_dtheta(-28*sqrt(3)/109 - R(45, 109), 5*sqrt(3)/2 + R(9, 2)),
   "99001-03": lambda: dx_dtheta(sqrt(2)/3 + 1, -9*sqrt(2)/2 - 3),
   "99001-04": lambda: dx_dtheta(-1 - sqrt(2)/8, -4*sqrt(2) - 1),
   "99001-05": lambda: dx_dtheta(-11*sqrt(3)/21, -R(11, 2)),
   "99001-06": lambda: dx_dtheta(-4*sqrt(3)/9, 4),
   "99001-07": lambda: dx_dtheta(-R(9, 7) - 3*sqrt(2)/7, -3*sqrt(2)),
   "99001-08": lambda: dx_dtheta(11*sqrt(3)/21, -R(11, 2)),
   "99001-09": lambda: dx_dtheta(1 - 3*sqrt(2), -3 + sqrt(2)/2),
   "99001-10": lambda: dx_dtheta(R(20, 13) - 21*sqrt(3)/13, 1 + 5*sqrt(3)/2),
   "99001-11": lambda: dx_dtheta(3*sqrt(2)/5 + 1, -5*sqrt(2)/2 - 3),
   "99001-12": lambda: dx_dtheta(-11*sqrt(3), 11*sqrt(3)/2),
   "99001-13": lambda: dx_dtheta(7*sqrt(3)/5, -7*sqrt(3)/2),
   "99001-14": lambda: dx_dtheta(-4 - 5*sqrt(3)/3, 1 - 3*sqrt(3)/2),
   "99001-15": lambda: dx_dtheta(R(4, 11) + 3*sqrt(3)/11, -2 - sqrt(3)),
   "99001-16": lambda: dx_dtheta(8*sqrt(3)/33 + R(5, 11), R(5, 2) + 3*sqrt(3)/2),
   "99001-17": lambda: dx_dtheta(-R(40, 59) - 9*sqrt(3)/59, -2*sqrt(3) - R(5, 2)),
   "99001-18": lambda: dx_dtheta(4*sqrt(3)/3, -4),
   "99001-19": lambda: dx_dtheta(sqrt(3)/27, -R(1, 2)),
   "99001-20": lambda: dx_dtheta(-15*sqrt(3)/13 - R(8, 13), -1 + 4*sqrt(3)),
   "99001-21": lambda: dx_dtheta(-sqrt(3)/5, -3),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
