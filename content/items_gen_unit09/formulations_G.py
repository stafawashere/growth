"""Answers to the unit 9 generated items in stems_G.json, computed from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24, from the
stem text, figure data and choice lists in stems_G.json and nothing else: no key, worked solution
or template was seen. Decimal answers are returned at full precision and statement answers are the
text of the choice the computation selects, or a list when zero or several choices hold up.
"""
import json
import re
from pathlib import Path

import mpmath
import sympy
from sympy import Rational, cos, pi, sin

from tools.key_recheck import polar_slope, t, theta

mpmath.mp.dps = 30

# Choice texts copied from stems_G.json when the file was written, so it runs where no stems file is.
CHOICES = {
   "09008-00": [
      "The particle moves toward the x-axis for \\( 0 < t < 1 \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 0 < t < 1.170 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 3 \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 1.170 < t < 3 \\), because \\( y'(t) \\) is negative there."
   ],
   "09008-01": [
      "The particle moves toward the y-axis for \\( 1.345 < t < \\frac{5}{2} \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 1.345 < t < \\frac{5}{2} \\), because \\( x(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( \\sqrt{2} < t < \\frac{5}{2} \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the y-axis for no t with \\( 0 < t < \\frac{5}{2} \\), because \\( x(t) \\) is positive there."
   ],
   "09008-02": [
      "The particle moves toward the x-axis for \\( 0 < t < 0.450 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 1 \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 0 < t < 3 \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 0.450 < t < 3 \\), because \\( y'(t) \\) is negative there."
   ],
   "09008-03": [
      "The particle moves toward the y-axis for \\( 0 < t < 1.395 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 0 < t < 1.395 \\), because \\( x(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( \\sqrt{2} < t < \\frac{5}{2} \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the y-axis for no t with \\( 0 < t < \\frac{5}{2} \\), because \\( x(t) \\) is positive there."
   ],
   "09008-04": [
      "The particle moves toward the y-axis for \\( 1.345 < t < 2 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 1.345 < t < 2 \\), because \\( x(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( \\sqrt{2} < t < 2 \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the y-axis for no t with \\( 0 < t < 2 \\), because \\( x(t) \\) is positive there."
   ],
   "09008-05": [
      "The particle moves toward the x-axis for \\( 0 < t < 1 \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 0 < t < 1.030 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < \\frac{5}{2} \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 1.030 < t < \\frac{5}{2} \\), because \\( y'(t) \\) is negative there."
   ],
   "09008-06": [
      "The particle moves toward the y-axis for \\( 0 < t < 0.450 \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < 1 \\), because \\( y'(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( 0 < t < 2 \\), because \\( x(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0.450 < t < 2 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there."
   ],
   "09008-07": [
      "The particle moves toward the y-axis for \\( 1.345 < t < 3 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 1.345 < t < 3 \\), because \\( x(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( \\sqrt{2} < t < 3 \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the y-axis for no t with \\( 0 < t < 3 \\), because \\( x(t) \\) is positive there."
   ],
   "09008-08": [
      "The particle moves toward the x-axis for \\( 0 < t < 0.915 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 0.915 \\), because \\( y(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( \\sqrt{3} < t < \\frac{5}{2} \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the x-axis for no t with \\( 0 < t < \\frac{5}{2} \\), because \\( y(t) \\) is positive there."
   ],
   "09008-09": [
      "The particle moves toward the x-axis for \\( 0 < t < 1.252 \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 0 < t < 3 \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 0 < t < \\sqrt{2} \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 1.252 < t < 3 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there."
   ],
   "09008-10": [
      "The particle moves toward the x-axis for \\( 0 < t < 1.345 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 2 \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 0 < t < \\sqrt{3} \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 1.345 < t < 2 \\), because \\( y'(t) \\) is negative there."
   ],
   "09008-11": [
      "The particle moves toward the x-axis for \\( 0 < t < 1.282 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 2 \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 0 < t < \\sqrt{2} \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 1.282 < t < 2 \\), because \\( y'(t) \\) is negative there."
   ],
   "09008-12": [
      "The particle moves toward the y-axis for \\( 0 < t < 0.915 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 0 < t < 1 \\), because \\( y'(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( 0 < t < \\frac{5}{2} \\), because \\( x(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0.915 < t < \\frac{5}{2} \\), because \\( x'(t) \\) is negative there."
   ],
   "09008-13": [
      "The particle moves toward the x-axis for \\( 0 < t < 1.030 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 1.030 \\), because \\( y(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( \\sqrt{3} < t < \\frac{5}{2} \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the x-axis for no t with \\( 0 < t < \\frac{5}{2} \\), because \\( y(t) \\) is positive there."
   ],
   "09008-14": [
      "The particle moves toward the x-axis for \\( 0 < t < 0.915 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 2 \\), because \\( y(t) \\) is negative there.",
      "The particle moves toward the x-axis for \\( 0 < t < \\sqrt{2} \\), because \\( x'(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 0.915 < t < 2 \\), because \\( y'(t) \\) is negative there."
   ],
   "09008-15": [
      "The particle moves toward the y-axis for \\( 0 < t < 1.395 \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < 3 \\), because \\( x(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < \\sqrt{3} \\), because \\( y'(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( 1.395 < t < 3 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there."
   ],
   "09008-16": [
      "The particle moves toward the y-axis for \\( 1.170 < t < 3 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 1.170 < t < 3 \\), because \\( x(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( \\sqrt{2} < t < 3 \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the y-axis for no t with \\( 0 < t < 3 \\), because \\( x(t) \\) is positive there."
   ],
   "09008-17": [
      "The particle moves toward the x-axis for \\( 1.170 < t < 2 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 1.170 < t < 2 \\), because \\( y(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( \\sqrt{2} < t < 2 \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the x-axis for no t with \\( 0 < t < 2 \\), because \\( y(t) \\) is positive there."
   ],
   "09008-18": [
      "The particle moves toward the y-axis for \\( 0 < t < 1.170 \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < 2 \\), because \\( x(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < \\sqrt{3} \\), because \\( y'(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( 1.170 < t < 2 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there."
   ],
   "09008-19": [
      "The particle moves toward the x-axis for \\( 0 < t < 0.739 \\), because \\( y(t) \\) and \\( y'(t) \\) have opposite signs there.",
      "The particle moves toward the x-axis for \\( 0 < t < 0.739 \\), because \\( y(t) \\) is positive there.",
      "The particle moves toward the x-axis for \\( 1 < t < 3 \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the x-axis for no t with \\( 0 < t < 3 \\), because \\( y(t) \\) is positive there."
   ],
   "09008-20": [
      "The particle moves toward the y-axis for \\( 0 < t < 0.915 \\), because \\( x'(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < 2 \\), because \\( x(t) \\) is negative there.",
      "The particle moves toward the y-axis for \\( 0 < t < \\sqrt{3} \\), because \\( y'(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( 0.915 < t < 2 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there."
   ],
   "09008-21": [
      "The particle moves toward the y-axis for \\( 0 < t < 0.739 \\), because \\( x(t) \\) and \\( x'(t) \\) have opposite signs there.",
      "The particle moves toward the y-axis for \\( 0 < t < 0.739 \\), because \\( x(t) \\) is positive there.",
      "The particle moves toward the y-axis for \\( \\sqrt{3} < t < 2 \\), because \\( y'(t) \\) is negative there.",
      "The particle moves toward the y-axis for no t with \\( 0 < t < 2 \\), because \\( x(t) \\) is positive there."
   ],
   "99005-00": [
      "\\( v(1.2) \\approx \\left\\langle -2.001,\\ 3.600 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -7.327,\\ -7.363 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -7.363,\\ -7.327 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle 0.058,\\ 0.130 \\right\\rangle \\)"
   ],
   "99005-01": [
      "\\( v(0.8) \\approx \\left\\langle -0.005,\\ 0.209 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle -10.415,\\ 1.049 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle -2.796,\\ 1.500 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 1.049,\\ -10.415 \\right\\rangle \\)"
   ],
   "99005-02": [
      "\\( v(1.2) \\approx \\left\\langle -0.682,\\ 1.500 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -2.350,\\ -7.073 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -7.073,\\ -2.350 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle 0.050,\\ 0.082 \\right\\rangle \\)"
   ],
   "99005-03": [
      "\\( v(0.8) \\approx \\left\\langle -1.422,\\ 3.175 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 0.013,\\ 0.053 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 0.619,\\ 0.750 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 3.175,\\ -1.422 \\right\\rangle \\)"
   ],
   "99005-04": [
      "\\( v(0.5) \\approx \\left\\langle -0.008,\\ 0.314 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle -15.689,\\ 2.074 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle -6.732,\\ 2.000 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle 2.074,\\ -15.689 \\right\\rangle \\)"
   ],
   "99005-05": [
      "\\( v(0.8) \\approx \\left\\langle -22.958,\\ 10.702 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 0.218,\\ 0.233 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 10.702,\\ -22.958 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 3.670,\\ 3.200 \\right\\rangle \\)"
   ],
   "99005-06": [
      "\\( v(1.2) \\approx \\left\\langle -0.010,\\ 0.139 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -0.950,\\ 4.626 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -4.053,\\ 2.000 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle 4.626,\\ -0.950 \\right\\rangle \\)"
   ],
   "99005-07": [
      "\\( v(0.8) \\approx \\left\\langle -20.284,\\ 8.944 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 0.162,\\ 0.231 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 2.752,\\ 3.200 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 8.944,\\ -20.284 \\right\\rangle \\)"
   ],
   "99005-08": [
      "\\( v(1.8) \\approx \\left\\langle -0.505,\\ 0.798 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle 0.009,\\ 0.009 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle 0.311,\\ 0.500 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle 0.798,\\ -0.505 \\right\\rangle \\)"
   ],
   "99005-09": [
      "\\( v(0.8) \\approx \\left\\langle -11.473,\\ 11.393 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 0.080,\\ 0.212 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 11.393,\\ -11.473 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 2.753,\\ 2.400 \\right\\rangle \\)"
   ],
   "99005-10": [
      "\\( v(0.8) \\approx \\left\\langle -5.822,\\ 4.596 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 0.104,\\ 0.031 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 2.174,\\ 1.500 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 4.596,\\ -5.822 \\right\\rangle \\)"
   ],
   "99005-11": [
      "\\( v(1.8) \\approx \\left\\langle -3.125,\\ -4.817 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle -4.817,\\ -3.125 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle 0.263,\\ 0.236 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle 2.383,\\ 5.400 \\right\\rangle \\)"
   ],
   "99005-12": [
      "\\( v(1.5) \\approx \\left\\langle -0.001,\\ 0.070 \\right\\rangle \\)",
      "\\( v(1.5) \\approx \\left\\langle -0.682,\\ 0.500 \\right\\rangle \\)",
      "\\( v(1.5) \\approx \\left\\langle -3.042,\\ 2.266 \\right\\rangle \\)",
      "\\( v(1.5) \\approx \\left\\langle 2.266,\\ -3.042 \\right\\rangle \\)"
   ],
   "99005-13": [
      "\\( v(0.8) \\approx \\left\\langle 0.056,\\ 0.056 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 1.560,\\ 4.949 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 3.038,\\ 0.800 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 4.949,\\ 1.560 \\right\\rangle \\)"
   ],
   "99005-14": [
      "\\( v(0.8) \\approx \\left\\langle -0.001,\\ 0.105 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle -0.847,\\ 0.750 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle -3.939,\\ 4.258 \\right\\rangle \\)",
      "\\( v(0.8) \\approx \\left\\langle 4.258,\\ -3.939 \\right\\rangle \\)"
   ],
   "99005-15": [
      "\\( v(2.5) \\approx \\left\\langle -0.225,\\ 0.750 \\right\\rangle \\)",
      "\\( v(2.5) \\approx \\left\\langle -1.103,\\ -2.762 \\right\\rangle \\)",
      "\\( v(2.5) \\approx \\left\\langle -2.762,\\ -1.103 \\right\\rangle \\)",
      "\\( v(2.5) \\approx \\left\\langle 0.012,\\ 0.040 \\right\\rangle \\)"
   ],
   "99005-16": [
      "\\( v(0.5) \\approx \\left\\langle 0.039,\\ 0.026 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle 1.814,\\ 2.298 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle 2.211,\\ 0.750 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle 2.298,\\ 1.814 \\right\\rangle \\)"
   ],
   "99005-17": [
      "\\( v(2.5) \\approx \\left\\langle -0.003,\\ 0.124 \\right\\rangle \\)",
      "\\( v(2.5) \\approx \\left\\langle -0.021,\\ 0.261 \\right\\rangle \\)",
      "\\( v(2.5) \\approx \\left\\langle -0.124,\\ 2.500 \\right\\rangle \\)",
      "\\( v(2.5) \\approx \\left\\langle 0.124,\\ -0.003 \\right\\rangle \\)"
   ],
   "99005-18": [
      "\\( v(1.2) \\approx \\left\\langle -0.009,\\ 0.139 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -2.600,\\ 1.283 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle -2.702,\\ 2.000 \\right\\rangle \\)",
      "\\( v(1.2) \\approx \\left\\langle 1.283,\\ -2.600 \\right\\rangle \\)"
   ],
   "99005-19": [
      "\\( v(1.8) \\approx \\left\\langle -0.007,\\ 0.104 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle -0.808,\\ 1.036 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle -1.282,\\ 1.500 \\right\\rangle \\)",
      "\\( v(1.8) \\approx \\left\\langle 1.036,\\ -0.808 \\right\\rangle \\)"
   ],
   "99005-20": [
      "\\( v(0.5) \\approx \\left\\langle -0.006,\\ 0.279 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle -13.735,\\ 4.819 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle -3.366,\\ 2.000 \\right\\rangle \\)",
      "\\( v(0.5) \\approx \\left\\langle 4.819,\\ -13.735 \\right\\rangle \\)"
   ],
   "99005-21": [
      "\\( v(1.5) \\approx \\left\\langle -3.915,\\ 3.304 \\right\\rangle \\)",
      "\\( v(1.5) \\approx \\left\\langle 0.052,\\ 0.041 \\right\\rangle \\)",
      "\\( v(1.5) \\approx \\left\\langle 1.294,\\ 0.750 \\right\\rangle \\)",
      "\\( v(1.5) \\approx \\left\\langle 3.304,\\ -3.915 \\right\\rangle \\)"
   ]
}

GRID_POINTS = 4000
ROUNDED_TOLERANCE = 0.0005 + 1e-12
EXACT_TOLERANCE = 1e-9
TIE_TOLERANCE = 1e-9
CHOICE_INTERVAL = re.compile(r"\\\( (.+?) < t < (.+?) \\\)")
CHOICE_VECTOR = re.compile(r"\\left\\langle (-?[\d.]+),\\ (-?[\d.]+) \\right\\rangle")
THREE_DECIMALS = re.compile(r"^-?\d+\.\d{3}$")


def numeric(expression, variable):
   return sympy.lambdify(variable, expression, "mpmath")


def full_precision(value):
   return sympy.Float(value, 30)


def grid(left, right, count=GRID_POINTS):
   left = mpmath.mpf(sympy.N(left, 30))
   right = mpmath.mpf(sympy.N(right, 30))
   step = (right - left) / count

   return [left + index * step for index in range(count + 1)]


def roots_in(function, left, right):
   """Every sign change of function on [left, right], refined by bisection."""
   points = grid(left, right)
   values = [function(point) for point in points]
   found = []

   for index in range(len(points) - 1):
      is_zero_at_point = values[index] == 0

      if is_zero_at_point:
         found.append(points[index])
         continue

      changes_sign = values[index] * values[index + 1] < 0

      if changes_sign:
         bracket = (points[index], points[index + 1])
         found.append(mpmath.findroot(function, bracket, solver="anderson"))

   return found


def total_distance(x_velocity, y_velocity, start, end):
   speed = numeric(sympy.sqrt(x_velocity**2 + y_velocity**2), t)
   pieces = grid(start, end, 16)

   return full_precision(mpmath.quad(speed, pieces))


def interval_endpoint_matches(text, true_value):
   text = text.strip()
   is_rounded = bool(THREE_DECIMALS.match(text))

   if is_rounded:
      return abs(float(text) - float(true_value)) <= ROUNDED_TOLERANCE

   exact = sympy.sympify(text.replace("\\sqrt{", "sqrt(").replace("\\frac{", "(").replace("}{", ")/(").replace("}", ")"))

   return abs(float(exact) - float(true_value)) <= EXACT_TOLERANCE


def approaching_intervals(coordinate, start, end):
   """Open subintervals of (start, end) on which coordinate and its derivative have opposite signs."""
   position = numeric(coordinate, t)
   velocity = numeric(sympy.diff(coordinate, t), t)
   cuts = sorted(set(roots_in(position, start, end) + roots_in(velocity, start, end)))
   left_end = mpmath.mpf(sympy.N(start, 30))
   right_end = mpmath.mpf(sympy.N(end, 30))
   boundaries = [left_end] + [cut for cut in cuts if left_end < cut < right_end] + [right_end]
   intervals = []

   for left, right in zip(boundaries, boundaries[1:]):
      middle = (left + right) / 2
      is_approaching = position(middle) * velocity(middle) < 0

      if not is_approaching:
         continue

      continues_previous = bool(intervals) and intervals[-1][1] == left

      if continues_previous:
         intervals[-1] = (intervals[-1][0], right)
      else:
         intervals.append((left, right))

   return intervals


def choice_intervals(choice):
   claim = choice.split(", because")[0]

   if "for no t" in claim:
      return []

   return CHOICE_INTERVAL.findall(claim)


def same_intervals(claimed, computed):
   if len(claimed) != len(computed):
      return False

   return all(
      interval_endpoint_matches(claimed_left, true_left) and interval_endpoint_matches(claimed_right, true_right)
      for (claimed_left, claimed_right), (true_left, true_right) in zip(claimed, computed)
   )


def moving_toward_axis(x_position, y_position, start, end, axis, choices):
   """Toward the x-axis means |y| decreasing, so y and y' of opposite signs; likewise x for the y-axis."""
   coordinate_name = "y" if axis == "x" else "x"
   coordinate = y_position if axis == "x" else x_position
   computed = approaching_intervals(coordinate, start, end)
   sound_reason = f"because \\( {coordinate_name}(t) \\) and \\( {coordinate_name}'(t) \\) have opposite signs there"

   right_set = [choice for choice in choices if same_intervals(choice_intervals(choice), computed)]
   right_set_and_reason = [choice for choice in right_set if sound_reason in choice]

   if len(right_set_and_reason) == 1:
      return right_set_and_reason[0]

   if len(right_set) == 1:
      return right_set[0]

   return right_set


def polar_radius_rate(radius, at):
   return full_precision(sympy.N(sympy.diff(radius, theta).subs(theta, at), 30))


def radius_time_rate(radius, angle_of_time, at):
   times = [root for root in sympy.solve(sympy.Eq(angle_of_time, at), t) if root.is_real]
   rates = {sympy.N(sympy.diff(radius, theta).subs(theta, at) * sympy.diff(angle_of_time, t).subs(t, time), 30) for time in times}

   if len(rates) != 1:
      return [full_precision(rate) for rate in rates]

   return full_precision(rates.pop())


def axis_distance(radius, axis):
   """Distance to the named axis: |x| for the y-axis, |y| for the x-axis."""
   coordinate = radius * cos(theta) if axis == "y" else radius * sin(theta)

   return coordinate


def farthest_from_axis(radius, left, right, axis):
   coordinate = axis_distance(radius, axis)
   distance = numeric(sympy.Abs(coordinate), theta)
   rate = numeric(sympy.diff(coordinate, theta), theta)
   left_end = mpmath.mpf(sympy.N(left, 30))
   right_end = mpmath.mpf(sympy.N(right, 30))
   candidates = [left_end, right_end] + [root for root in roots_in(rate, left, right) if left_end < root < right_end]
   best = max(distance(candidate) for candidate in candidates)
   winners = [candidate for candidate in candidates if best - distance(candidate) <= TIE_TOLERANCE]

   if len(winners) == 1:
      return full_precision(winners[0])

   return [full_precision(winner) for winner in winners]


def half_integral_of_square(radius, lower, upper):
   return sympy.simplify(sympy.integrate(radius**2, (theta, lower, upper)) / 2)


def one_petal_area(radius, petal_count):
   zeros = sorted(sympy.solveset(radius, theta, sympy.Interval.Ropen(0, 2 * pi)), key=lambda value: float(value))
   petal = half_integral_of_square(radius, zeros[0], zeros[1])
   traversal = pi if petal_count % 2 == 1 else 2 * pi
   per_petal = half_integral_of_square(radius, 0, traversal) / petal_count
   agrees_with_count = sympy.simplify(petal - per_petal) == 0

   if not agrees_with_count:
      raise ValueError(f"petal area {petal} disagrees with {petal_count} petals")

   return petal


def stays_positive(radius, lower, upper):
   values = numeric(radius, theta)

   return all(values(point) > 0 for point in grid(lower, upper))


def area_between_rays(radius, lower, upper):
   if not stays_positive(radius, lower, upper):
      raise ValueError("the radius changes sign between the rays")

   return half_integral_of_square(radius, lower, upper)


def enclosed_area(radius):
   if not stays_positive(radius, 0, 2 * pi):
      raise ValueError("the curve passes through the pole")

   return half_integral_of_square(radius, 0, 2 * pi)


def inside_curve_outside_circle(radius, circle_radius):
   """Half the integral of r^2 - c^2 wherever r > c; an inner loop never reaches the circle."""
   values = numeric(radius, theta)
   deepest_inner_loop = max(-values(point) for point in grid(0, 2 * pi))
   inner_loop_reaches_circle = deepest_inner_loop >= float(circle_radius)

   if inner_loop_reaches_circle:
      raise ValueError("an inner loop reaches the circle")

   excess = numeric(radius**2 - circle_radius**2, theta)
   crossings = roots_in(lambda angle: values(angle) - mpmath.mpf(sympy.N(circle_radius, 30)), 0, 2 * pi)
   boundaries = [mpmath.mpf(0)] + crossings + [2 * mpmath.pi]
   area = mpmath.mpf(0)

   for left, right in zip(boundaries, boundaries[1:]):
      is_outside_circle = excess((left + right) / 2) > 0

      if is_outside_circle:
         area += mpmath.quad(excess, [left, right]) / 2

   return full_precision(area)


def x_rate_from_slope(radius, slope, y_rate):
   """dy/dx = (dy/dtheta) / (dx/dtheta), so dx/dtheta = (dy/dtheta) / (dy/dx) whatever the curve."""
   return y_rate / slope


def coordinate_rate(radius, coordinate_name, at):
   coordinate = radius * cos(theta) if coordinate_name == "x" else radius * sin(theta)

   return full_precision(sympy.N(sympy.diff(coordinate, theta).subs(theta, at), 30))


def exact_tangent_slope(radius, at):
   return polar_slope(radius, at)


def time_at_coordinate(radius, angle_of_time, start, end, coordinate_name, target):
   coordinate = radius * cos(theta) if coordinate_name == "x" else radius * sin(theta)
   along_time = coordinate.subs(theta, angle_of_time) - target
   times = roots_in(numeric(along_time, t), start, end)

   if len(times) == 1:
      return full_precision(times[0])

   return [full_precision(time) for time in times]


def velocity_choice(radius, angle_of_time, at, choices):
   along_time = radius.subs(theta, angle_of_time)
   x_velocity = sympy.diff(along_time * cos(angle_of_time), t).subs(t, at)
   y_velocity = sympy.diff(along_time * sin(angle_of_time), t).subs(t, at)
   true_components = (float(sympy.N(x_velocity, 30)), float(sympy.N(y_velocity, 30)))
   matching = []

   for choice in choices:
      shown = CHOICE_VECTOR.search(choice).groups()
      components_match = all(abs(float(text) - value) <= ROUNDED_TOLERANCE for text, value in zip(shown, true_components))

      if components_match:
         matching.append(choice)

   if len(matching) == 1:
      return matching[0]

   return matching


def ray_gap_rate(first_radius, second_radius, at):
   """D = |r1 - r2| along the ray, so dD/dtheta carries the sign of r1 - r2."""
   gap = first_radius - second_radius
   sign = sympy.sign(sympy.N(gap.subs(theta, at), 30))

   return full_precision(sympy.N(sign * sympy.diff(gap, theta).subs(theta, at), 30))


BY_SUFFIX = {
   "09007-00": lambda: total_distance(5*cos(3*t/2), t**2 - 1, 0, 3),
   "09007-01": lambda: total_distance(cos(t), 2*t**2 - 4, 0, 2),
   "09007-02": lambda: total_distance(5*cos(t), 3*t**2 - 6, 0, Rational(5, 2)),
   "09007-03": lambda: total_distance(2*cos(2*t), 2*t**2 - 2, 0, 2),
   "09007-04": lambda: total_distance(5*cos(3*t/2), 2*t**2 - 6, 0, 2),
   "09007-05": lambda: total_distance(3*cos(t), 2*t**2 - 4, 0, Rational(5, 2)),
   "09007-06": lambda: total_distance(2*cos(3*t/2), 3*t**2 - 3, 0, 2),
   "09007-07": lambda: total_distance(cos(t), 3*t**2 - 3, 0, 2),
   "09007-08": lambda: total_distance(5*cos(t), 3*t**2 - 3, 0, 2),
   "09007-09": lambda: total_distance(5*cos(3*t/2), 3*t**2 - 6, 0, 3),
   "09007-10": lambda: total_distance(cos(2*t), t**2 - 1, 0, 2),
   "09007-11": lambda: total_distance(3*cos(t), t**2 - 1, 0, 2),
   "09007-12": lambda: total_distance(3*cos(2*t), 3*t**2 - 6, 0, 3),
   "09007-13": lambda: total_distance(cos(t), 3*t**2 - 12, 0, 3),
   "09007-14": lambda: total_distance(6*cos(2*t), 3*t**2 - 6, 0, 3),
   "09007-15": lambda: total_distance(4*cos(3*t/2), t**2 - 4, 0, Rational(5, 2)),
   "09007-16": lambda: total_distance(6*cos(t), 2*t**2 - 2, 0, 2),
   "09007-17": lambda: total_distance(2*cos(2*t), t**2 - 3, 0, 3),
   "09007-18": lambda: total_distance(4*cos(2*t), 3*t**2 - 9, 0, 3),
   "09007-19": lambda: total_distance(6*cos(t), 2*t**2 - 8, 0, Rational(5, 2)),
   "09007-20": lambda: total_distance(2*cos(3*t/2), t**2 - 3, 0, Rational(5, 2)),
   "09007-21": lambda: total_distance(2*cos(3*t/2), t**2 - 1, 0, 3),

   "09008-00": lambda: moving_toward_axis(-t**3/3 + t, -t**2/2 + 3*sin(t) - 8, 0, 3, "x", CHOICES["09008-00"]),
   "09008-01": lambda: moving_toward_axis(-t**2/3 + 4*sin(t) + 5, -t**3/3 + 2*t, 0, Rational(5, 2), "y", CHOICES["09008-01"]),
   "09008-02": lambda: moving_toward_axis(-t**3/3 + t, -t**2 + sin(t) - 6, 0, 3, "x", CHOICES["09008-02"]),
   "09008-03": lambda: moving_toward_axis(t**2/4 - 4*sin(t) + 7, -t**3/3 + 2*t, 0, Rational(5, 2), "y", CHOICES["09008-03"]),
   "09008-04": lambda: moving_toward_axis(-t**2/3 + 4*sin(t) + 5, -t**3/3 + 2*t, 0, 2, "y", CHOICES["09008-04"]),
   "09008-05": lambda: moving_toward_axis(-t**3/3 + t, -t**2 + 4*sin(t) - 6, 0, Rational(5, 2), "x", CHOICES["09008-05"]),
   "09008-06": lambda: moving_toward_axis(t**2 - sin(t) - 6, -t**3/3 + t, 0, 2, "y", CHOICES["09008-06"]),
   "09008-07": lambda: moving_toward_axis(-t**2/3 + 4*sin(t) + 6, -t**3/3 + 2*t, 0, 3, "y", CHOICES["09008-07"]),
   "09008-08": lambda: moving_toward_axis(-t**3/3 + 3*t, t**2 - 3*sin(t) + 6, 0, Rational(5, 2), "x", CHOICES["09008-08"]),
   "09008-09": lambda: moving_toward_axis(-t**3/3 + 2*t, t**2/2 - 4*sin(t) - 8, 0, 3, "x", CHOICES["09008-09"]),
   "09008-10": lambda: moving_toward_axis(-t**3/3 + 3*t, -t**2/4 + 3*sin(t) - 6, 0, 2, "x", CHOICES["09008-10"]),
   "09008-11": lambda: moving_toward_axis(-t**3/3 + 2*t, -t**2/3 + 3*sin(t) - 7, 0, 2, "x", CHOICES["09008-11"]),
   "09008-12": lambda: moving_toward_axis(-t**2 + 3*sin(t) - 8, -t**3/3 + t, 0, Rational(5, 2), "y", CHOICES["09008-12"]),
   "09008-13": lambda: moving_toward_axis(-t**3/3 + 3*t, t**2/4 - sin(t) + 4, 0, Rational(5, 2), "x", CHOICES["09008-13"]),
   "09008-14": lambda: moving_toward_axis(-t**3/3 + 2*t, -t**2/3 + sin(t) - 5, 0, 2, "x", CHOICES["09008-14"]),
   "09008-15": lambda: moving_toward_axis(t**2/4 - 4*sin(t) - 7, -t**3/3 + 3*t, 0, 3, "y", CHOICES["09008-15"]),
   "09008-16": lambda: moving_toward_axis(-t**2/2 + 3*sin(t) + 7, -t**3/3 + 2*t, 0, 3, "y", CHOICES["09008-16"]),
   "09008-17": lambda: moving_toward_axis(-t**3/3 + 2*t, -t**2/2 + 3*sin(t) + 6, 0, 2, "x", CHOICES["09008-17"]),
   "09008-18": lambda: moving_toward_axis(t**2/3 - 2*sin(t) - 4, -t**3/3 + 3*t, 0, 2, "y", CHOICES["09008-18"]),
   "09008-19": lambda: moving_toward_axis(-t**3/3 + t, t**2 - 2*sin(t) + 5, 0, 3, "x", CHOICES["09008-19"]),
   "09008-20": lambda: moving_toward_axis(t**2/3 - sin(t) - 3, -t**3/3 + 3*t, 0, 2, "y", CHOICES["09008-20"]),
   "09008-21": lambda: moving_toward_axis(t**2/2 - sin(t) + 6, -t**3/3 + 3*t, 0, 2, "y", CHOICES["09008-21"]),

   "09009-00": lambda: polar_radius_rate(theta*sin(theta/2) + 2, Rational("0.4")),
   "09009-01": lambda: polar_radius_rate(2*theta*sin(theta) + 5, Rational("0.8")),
   "09009-02": lambda: polar_radius_rate(3*theta*cos(2*theta) + 5, Rational("2.3")),
   "09009-03": lambda: polar_radius_rate(2*theta*sin(theta/2) + 4, Rational("1.2")),
   "09009-04": lambda: polar_radius_rate(3*theta*cos(theta) + 6, Rational("1.1")),
   "09009-05": lambda: polar_radius_rate(2*theta*cos(2*theta) + 5, Rational("1.2")),
   "09009-06": lambda: polar_radius_rate(3*theta*cos(theta) + 2, Rational("0.7")),
   "09009-07": lambda: polar_radius_rate(3*theta*sin(3*theta) + 3, Rational("1.2")),
   "09009-08": lambda: polar_radius_rate(3*theta*sin(3*theta) + 3, Rational("0.5")),
   "09009-09": lambda: polar_radius_rate(theta*sin(2*theta) + 3, Rational("0.7")),
   "09009-10": lambda: polar_radius_rate(theta*cos(2*theta) + 6, Rational("2.3")),
   "09009-11": lambda: polar_radius_rate(2*theta*sin(theta/2) + 5, Rational("1.2")),
   "09009-12": lambda: polar_radius_rate(theta*cos(theta) + 2, Rational("0.7")),
   "09009-13": lambda: polar_radius_rate(3*theta*sin(3*theta) + 1, Rational("0.5")),
   "09009-14": lambda: polar_radius_rate(2*theta*sin(3*theta) + 3, Rational("0.5")),
   "09009-15": lambda: polar_radius_rate(3*theta*cos(theta/2) + 3, Rational("1.9")),
   "09009-16": lambda: polar_radius_rate(theta*cos(3*theta) + 4, Rational("0.5")),
   "09009-17": lambda: polar_radius_rate(2*theta*cos(3*theta) + 4, Rational("1.7")),
   "09009-18": lambda: polar_radius_rate(2*theta*cos(2*theta) + 3, Rational("1.7")),
   "09009-19": lambda: polar_radius_rate(3*theta*cos(theta) + 5, Rational("0.5")),
   "09009-20": lambda: polar_radius_rate(2*theta*sin(2*theta) + 2, Rational("2.3")),
   "09009-21": lambda: polar_radius_rate(3*theta*sin(theta/2) + 2, Rational("0.8")),

   "09010-00": lambda: radius_time_rate(4*cos(2*theta) + 5, 3*t, Rational("1.8")),
   "09010-01": lambda: radius_time_rate(4*cos(theta) + 7, 3*t, Rational("0.6")),
   "09010-02": lambda: radius_time_rate(2*cos(theta) + 7, t/2, Rational("1.8")),
   "09010-03": lambda: radius_time_rate(2*sin(theta) + 6, t/2, Rational("0.9")),
   "09010-04": lambda: radius_time_rate(2*sin(3*theta) + 6, 3*t/2, Rational("1.3")),
   "09010-05": lambda: radius_time_rate(4*cos(3*theta) + 7, t/2, Rational("0.6")),
   "09010-06": lambda: radius_time_rate(cos(2*theta) + 4, t/2, Rational("0.7")),
   "09010-07": lambda: radius_time_rate(2*sin(theta) + 6, 3*t/2, Rational("1.4")),
   "09010-08": lambda: radius_time_rate(cos(2*theta) + 6, 2*t, Rational("0.9")),
   "09010-09": lambda: radius_time_rate(2*sin(2*theta) + 5, 3*t, Rational("1.9")),
   "09010-10": lambda: radius_time_rate(2*sin(2*theta) + 3, 3*t/2, Rational("1.8")),
   "09010-11": lambda: radius_time_rate(4*sin(2*theta) + 6, 3*t, Rational("0.7")),
   "09010-12": lambda: radius_time_rate(4*sin(theta) + 5, 5*t/2, Rational("0.3")),
   "09010-13": lambda: radius_time_rate(2*cos(2*theta) + 5, 5*t/2, Rational("1.1")),
   "09010-14": lambda: radius_time_rate(cos(2*theta) + 7, 3*t/2, Rational("0.3")),
   "09010-15": lambda: radius_time_rate(sin(theta) + 2, t/2, Rational("1.8")),
   "09010-16": lambda: radius_time_rate(2*cos(2*theta) + 3, 2*t, Rational("1.1")),
   "09010-17": lambda: radius_time_rate(3*cos(2*theta) + 6, t/2, Rational("1.9")),
   "09010-18": lambda: radius_time_rate(2*cos(2*theta) + 3, t/2, Rational("0.4")),
   "09010-19": lambda: radius_time_rate(3*cos(2*theta) + 7, 2*t, Rational("1.9")),
   "09010-20": lambda: radius_time_rate(cos(theta) + 7, 2*t, Rational("0.4")),
   "09010-21": lambda: radius_time_rate(2*cos(3*theta) + 3, 2*t, Rational("0.6")),

   "09011-00": lambda: farthest_from_axis(sin(theta) + 2, 0, Rational("2.1"), "y"),
   "09011-01": lambda: farthest_from_axis(7 - 4*cos(theta), Rational("1.9"), Rational("3.6"), "x"),
   "09011-02": lambda: farthest_from_axis(5 - 3*cos(theta), Rational("1.7"), Rational("3.4"), "x"),
   "09011-03": lambda: farthest_from_axis(9 - 8*cos(theta), Rational("1.8"), Rational("3.5"), "x"),
   "09011-04": lambda: farthest_from_axis(3*sin(theta) + 4, Rational("0.2"), Rational("2.05"), "y"),
   "09011-05": lambda: farthest_from_axis(3 - 2*cos(theta), Rational("1.9"), Rational("3.65"), "x"),
   "09011-06": lambda: farthest_from_axis(4*sin(theta) + 8, 0, Rational("1.9"), "y"),
   "09011-07": lambda: farthest_from_axis(8 - 4*cos(theta), Rational("1.8"), Rational("3.45"), "x"),
   "09011-08": lambda: farthest_from_axis(6*sin(theta) + 9, Rational("0.1"), Rational("1.9"), "y"),
   "09011-09": lambda: farthest_from_axis(3*sin(theta) + 6, Rational("0.1"), Rational("1.75"), "y"),
   "09011-10": lambda: farthest_from_axis(8 - 5*cos(theta), Rational("1.7"), Rational("3.5"), "x"),
   "09011-11": lambda: farthest_from_axis(8 - 5*cos(theta), Rational("1.8"), Rational("3.35"), "x"),
   "09011-12": lambda: farthest_from_axis(5*sin(theta) + 7, Rational("0.2"), Rational("1.85"), "y"),
   "09011-13": lambda: farthest_from_axis(3 - 2*cos(theta), Rational("1.85"), Rational("3.3"), "x"),
   "09011-14": lambda: farthest_from_axis(4*sin(theta) + 5, Rational("0.1"), Rational("1.95"), "y"),
   "09011-15": lambda: farthest_from_axis(2 - cos(theta), Rational("1.75"), Rational("3.7"), "x"),
   "09011-16": lambda: farthest_from_axis(3 - 2*cos(theta), Rational("1.7"), Rational("3.35"), "x"),
   "09011-17": lambda: farthest_from_axis(5*sin(theta) + 8, Rational("0.3"), Rational("1.9"), "y"),
   "09011-18": lambda: farthest_from_axis(sin(theta) + 2, Rational("0.15"), Rational("1.95"), "y"),
   "09011-19": lambda: farthest_from_axis(9 - 5*cos(theta), Rational("1.75"), Rational("3.35"), "x"),
   "09011-20": lambda: farthest_from_axis(sin(theta) + 2, Rational("0.3"), Rational("1.85"), "y"),
   "09011-21": lambda: farthest_from_axis(2 - cos(theta), Rational("1.7"), Rational("3.55"), "x"),

   "09012-00": lambda: area_between_rays(4*sin(4*theta) + 6, 3*pi/2, 2*pi),
   "09012-01": lambda: one_petal_area(3*sin(4*theta), 8),
   "09012-02": lambda: one_petal_area(6*sin(2*theta), 4),
   "09012-03": lambda: one_petal_area(2*cos(3*theta), 3),
   "09012-04": lambda: one_petal_area(5*cos(3*theta), 3),
   "09012-05": lambda: one_petal_area(3*cos(4*theta), 8),
   "09012-06": lambda: one_petal_area(4*cos(4*theta), 8),
   "09012-07": lambda: one_petal_area(3*cos(3*theta), 3),
   "09012-08": lambda: area_between_rays(2*cos(2*theta) + 5, 3*pi/2, 2*pi),
   "09012-09": lambda: enclosed_area(sin(4*theta) + 5),
   "09012-10": lambda: area_between_rays(cos(4*theta) + 3, pi, 3*pi/2),
   "09012-11": lambda: one_petal_area(2*sin(4*theta), 8),
   "09012-12": lambda: one_petal_area(6*cos(2*theta), 4),
   "09012-13": lambda: area_between_rays(5*cos(2*theta) + 8, 3*pi/2, 2*pi),
   "09012-14": lambda: one_petal_area(4*cos(2*theta), 4),
   "09012-15": lambda: enclosed_area(sin(3*theta) + 3),
   "09012-16": lambda: one_petal_area(sin(2*theta), 4),
   "09012-17": lambda: one_petal_area(3*sin(2*theta), 4),
   "09012-18": lambda: one_petal_area(2*sin(2*theta), 4),
   "09012-19": lambda: one_petal_area(cos(4*theta), 8),
   "09012-20": lambda: area_between_rays(4*cos(4*theta) + 9, pi, 3*pi/2),
   "09012-21": lambda: one_petal_area(4*sin(3*theta), 3),

   "09013-00": lambda: inside_curve_outside_circle(4 - 6*cos(theta), Rational(13, 2)),
   "09013-01": lambda: inside_curve_outside_circle(4*sin(theta) + 1, 4),
   "09013-02": lambda: inside_curve_outside_circle(7*sin(theta) + 3, 6),
   "09013-03": lambda: inside_curve_outside_circle(5 - 4*sin(theta), 8),
   "09013-04": lambda: inside_curve_outside_circle(3*sin(theta) + 6, 7),
   "09013-05": lambda: inside_curve_outside_circle(8*sin(theta) + 5, 9),
   "09013-06": lambda: inside_curve_outside_circle(2 - 5*sin(theta), Rational(11, 2)),
   "09013-07": lambda: inside_curve_outside_circle(6 - cos(theta), Rational(13, 2)),
   "09013-08": lambda: inside_curve_outside_circle(cos(theta) + 6, Rational(13, 2)),
   "09013-09": lambda: inside_curve_outside_circle(3*sin(theta) + 6, Rational(15, 2)),
   "09013-10": lambda: inside_curve_outside_circle(6*sin(theta) + 3, Rational(9, 2)),
   "09013-11": lambda: inside_curve_outside_circle(8 - cos(theta), Rational(17, 2)),
   "09013-12": lambda: inside_curve_outside_circle(5 - 7*cos(theta), Rational(11, 2)),
   "09013-13": lambda: inside_curve_outside_circle(4 - 8*cos(theta), Rational(13, 2)),
   "09013-14": lambda: inside_curve_outside_circle(8*cos(theta) + 1, Rational(17, 2)),
   "09013-15": lambda: inside_curve_outside_circle(6 - 6*sin(theta), 8),
   "09013-16": lambda: inside_curve_outside_circle(3 - 3*cos(theta), Rational(7, 2)),
   "09013-17": lambda: inside_curve_outside_circle(6*sin(theta) + 5, 7),
   "09013-18": lambda: inside_curve_outside_circle(7 - 4*sin(theta), Rational(15, 2)),
   "09013-19": lambda: inside_curve_outside_circle(7*cos(theta) + 3, Rational(17, 2)),
   "09013-20": lambda: inside_curve_outside_circle(5 - 8*cos(theta), 9),
   "09013-21": lambda: inside_curve_outside_circle(3*cos(theta) + 5, Rational(15, 2)),

   "99001-00": lambda: x_rate_from_slope(4*sin(2*theta), Rational("-0.6"), Rational("1.3")),
   "99001-01": lambda: x_rate_from_slope(5*sin(2*theta), Rational("-0.8"), Rational("0.3")),
   "99001-02": lambda: x_rate_from_slope(theta + 3, Rational("0.8"), Rational("3.7")),
   "99001-03": lambda: x_rate_from_slope(3*sin(2*theta), Rational("2.5"), Rational("1.3")),
   "99001-04": lambda: x_rate_from_slope(2*cos(theta) + 5, Rational("0.6"), Rational("3.1")),
   "99001-05": lambda: x_rate_from_slope(2*cos(theta) + 2, Rational("1.6"), Rational("1.3")),
   "99001-06": lambda: x_rate_from_slope(2*cos(theta) + 4, Rational("1.6"), Rational("0.3")),
   "99001-07": lambda: x_rate_from_slope(2*cos(theta) + 4, Rational("-0.4"), Rational("-1.3")),
   "99001-08": lambda: x_rate_from_slope(2*cos(theta) + 2, Rational("2.5"), Rational("1.3")),
   "99001-09": lambda: x_rate_from_slope(theta + 2, Rational("-2.5"), Rational("-0.3")),
   "99001-10": lambda: x_rate_from_slope(2*cos(theta) + 3, Rational("-1.6"), Rational("1.3")),
   "99001-11": lambda: x_rate_from_slope(theta + 3, Rational("1.25"), Rational("-0.7")),
   "99001-12": lambda: x_rate_from_slope(4*sin(2*theta), Rational("1.6"), Rational("1.7")),
   "99001-13": lambda: x_rate_from_slope(2*cos(theta) + 3, Rational("2.5"), Rational("-0.3")),
   "99001-14": lambda: x_rate_from_slope(2*cos(theta) + 2, Rational("1.6"), Rational("-1.7")),
   "99001-15": lambda: x_rate_from_slope(5*sin(2*theta), Rational("-1.6"), Rational("4.5")),
   "99001-16": lambda: x_rate_from_slope(theta + 3, Rational("-1.25"), Rational("1.7")),
   "99001-17": lambda: x_rate_from_slope(4*sin(2*theta), Rational("1.6"), Rational("-0.7")),
   "99001-18": lambda: x_rate_from_slope(theta + 4, Rational("1.6"), Rational("4.5")),
   "99001-19": lambda: x_rate_from_slope(theta + 2, Rational("-0.8"), Rational("4.5")),
   "99001-20": lambda: x_rate_from_slope(4*sin(2*theta), Rational("0.6"), Rational("-1.7")),
   "99001-21": lambda: x_rate_from_slope(4*sin(2*theta), Rational("0.6"), Rational("-1.3")),

   "99002-00": lambda: coordinate_rate(sin(theta) + 6, "x", Rational("0.4")),
   "99002-01": lambda: coordinate_rate(3*cos(3*theta) + 6, "y", Rational("1.3")),
   "99002-02": lambda: coordinate_rate(2*cos(3*theta) + 3, "y", Rational("0.3")),
   "99002-03": lambda: coordinate_rate(2*cos(2*theta) + 5, "y", Rational("1.1")),
   "99002-04": lambda: coordinate_rate(3*cos(2*theta) + 6, "x", Rational("1.4")),
   "99002-05": lambda: coordinate_rate(3*cos(2*theta) + 6, "x", Rational("0.9")),
   "99002-06": lambda: coordinate_rate(4*sin(2*theta) + 4, "x", Rational("0.6")),
   "99002-07": lambda: coordinate_rate(3*sin(theta) + 2, "y", Rational("0.3")),
   "99002-08": lambda: coordinate_rate(cos(3*theta) + 5, "x", Rational("0.4")),
   "99002-09": lambda: coordinate_rate(2*cos(2*theta) + 2, "y", Rational("1.4")),
   "99002-10": lambda: coordinate_rate(2*sin(theta) + 4, "x", Rational("2.2")),
   "99002-11": lambda: coordinate_rate(2*cos(3*theta) + 4, "y", Rational("1.7")),
   "99002-12": lambda: coordinate_rate(4*cos(2*theta) + 3, "x", Rational("1.3")),
   "99002-13": lambda: coordinate_rate(2*sin(2*theta) + 2, "x", Rational("0.4")),
   "99002-14": lambda: coordinate_rate(2*cos(2*theta) + 1, "y", Rational("1.7")),
   "99002-15": lambda: coordinate_rate(sin(3*theta) + 6, "x", Rational("0.4")),
   "99002-16": lambda: coordinate_rate(cos(theta) + 3, "y", Rational("1.1")),
   "99002-17": lambda: coordinate_rate(sin(3*theta) + 1, "y", Rational("0.6")),
   "99002-18": lambda: coordinate_rate(2*sin(theta) + 1, "x", Rational("2.2")),
   "99002-19": lambda: coordinate_rate(3*cos(theta) + 5, "y", Rational("1.4")),
   "99002-20": lambda: coordinate_rate(3*sin(2*theta) + 3, "y", Rational("1.4")),
   "99002-21": lambda: coordinate_rate(sin(2*theta) + 4, "y", Rational("0.3")),

   "99003-00": lambda: exact_tangent_slope(5*sin(2*theta) + 1, pi/3),
   "99003-01": lambda: exact_tangent_slope(11 - 3*sin(2*theta), 4*pi/3),
   "99003-02": lambda: exact_tangent_slope(9 - 7*cos(2*theta), 5*pi/3),
   "99003-03": lambda: exact_tangent_slope(7*cos(2*theta) + 1, 5*pi/6),
   "99003-04": lambda: exact_tangent_slope(3 - 2*cos(2*theta), pi/6),

   "99004-00": lambda: time_at_coordinate(6*cos(theta) + 6, pi*t/4, 0, 2, "x", 9),
   "99004-01": lambda: time_at_coordinate(5*cos(theta) + 3, pi*t/8, 0, 4, "x", 6),
   "99004-02": lambda: time_at_coordinate(2*sin(theta) + 5, pi*t/10, 0, 5, "y", Rational("5.8")),
   "99004-03": lambda: time_at_coordinate(3*sin(theta) + 3, pi*t/6, 0, 3, "y", Rational("5.4")),
   "99004-04": lambda: time_at_coordinate(5*cos(theta) + 4, pi*t/12, 0, 6, "x", 8),
   "99004-05": lambda: time_at_coordinate(6*cos(theta) + 6, pi*t/8, 0, 4, "x", 9),
   "99004-06": lambda: time_at_coordinate(sin(theta) + 5, pi*t/10, 0, 5, "y", Rational("5.8")),
   "99004-07": lambda: time_at_coordinate(4*sin(theta) + 5, pi*t/8, 0, 4, "y", Rational("7.4")),
   "99004-08": lambda: time_at_coordinate(2*cos(theta) + 2, pi*t/12, 0, 6, "x", Rational("3.2")),
   "99004-09": lambda: time_at_coordinate(4*cos(theta) + 5, pi*t/10, 0, 5, "x", 7),
   "99004-10": lambda: time_at_coordinate(sin(theta) + 4, pi*t/8, 0, 4, "y", Rational("4.2")),
   "99004-11": lambda: time_at_coordinate(4*sin(theta) + 2, pi*t/6, 0, 3, "y", Rational("3.6")),
   "99004-12": lambda: time_at_coordinate(3*sin(theta) + 1, pi*t/10, 0, 5, "y", Rational("3.4")),
   "99004-13": lambda: time_at_coordinate(6*sin(theta) + 6, pi*t/10, 0, 5, "y", Rational("7.2")),
   "99004-14": lambda: time_at_coordinate(4*sin(theta) + 3, pi*t/8, 0, 4, "y", Rational("4.6")),
   "99004-15": lambda: time_at_coordinate(3*sin(theta) + 2, pi*t/6, 0, 3, "y", Rational("4.4")),
   "99004-16": lambda: time_at_coordinate(2*sin(theta) + 1, pi*t/4, 0, 2, "y", Rational("2.6")),
   "99004-17": lambda: time_at_coordinate(2*cos(theta) + 6, pi*t/12, 0, 6, "x", Rational("6.4")),
   "99004-18": lambda: time_at_coordinate(sin(theta) + 5, pi*t/10, 0, 5, "y", Rational("5.6")),
   "99004-19": lambda: time_at_coordinate(4*sin(theta) + 1, pi*t/12, 0, 6, "y", Rational("2.6")),
   "99004-20": lambda: time_at_coordinate(3*cos(theta) + 2, pi*t/10, 0, 5, "x", Rational("3.8")),
   "99004-21": lambda: time_at_coordinate(2*sin(theta) + 4, pi*t/10, 0, 5, "y", Rational("5.6")),

   "99005-00": lambda: velocity_choice(sin(theta) + 2, 3*t**2/2, Rational("1.2"), CHOICES["99005-00"]),
   "99005-01": lambda: velocity_choice(2*cos(theta) + 6, 3*t/2, Rational("0.8"), CHOICES["99005-01"]),
   "99005-02": lambda: velocity_choice(2*sin(theta) + 3, 3*t/2, Rational("1.2"), CHOICES["99005-02"]),
   "99005-03": lambda: velocity_choice(sin(theta) + 4, 3*t/4, Rational("0.8"), CHOICES["99005-03"]),
   "99005-04": lambda: velocity_choice(4*cos(theta) + 5, 2*t, Rational("0.5"), CHOICES["99005-04"]),
   "99005-05": lambda: velocity_choice(4*sin(theta) + 4, 2*t**2, Rational("0.8"), CHOICES["99005-05"]),
   "99005-06": lambda: velocity_choice(3*cos(theta) + 1, 2*t, Rational("1.2"), CHOICES["99005-06"]),
   "99005-07": lambda: velocity_choice(3*sin(theta) + 4, 2*t**2, Rational("0.8"), CHOICES["99005-07"]),
   "99005-08": lambda: velocity_choice(sin(theta) + 1, t/2, Rational("1.8"), CHOICES["99005-08"]),
   "99005-09": lambda: velocity_choice(2*sin(theta) + 5, 3*t**2/2, Rational("0.8"), CHOICES["99005-09"]),
   "99005-10": lambda: velocity_choice(4*sin(theta) + 1, 3*t/2, Rational("0.8"), CHOICES["99005-10"]),
   "99005-11": lambda: velocity_choice(3*sin(theta) + 2, 3*t**2/2, Rational("1.8"), CHOICES["99005-11"]),
   "99005-12": lambda: velocity_choice(2*cos(theta) + 6, t/2, Rational("1.5"), CHOICES["99005-12"]),
   "99005-13": lambda: velocity_choice(4*sin(theta) + 4, t**2/2, Rational("0.8"), CHOICES["99005-13"]),
   "99005-14": lambda: velocity_choice(2*cos(theta) + 6, 3*t/4, Rational("0.8"), CHOICES["99005-14"]),
   "99005-15": lambda: velocity_choice(sin(theta) + 3, 3*t/4, Rational("2.5"), CHOICES["99005-15"]),
   "99005-16": lambda: velocity_choice(3*sin(theta) + 2, 3*t**2/4, Rational("0.5"), CHOICES["99005-16"]),
   "99005-17": lambda: velocity_choice(3*cos(theta) + 3, t**2/2, Rational("2.5"), CHOICES["99005-17"]),
   "99005-18": lambda: velocity_choice(2*cos(theta) + 2, 2*t, Rational("1.2"), CHOICES["99005-18"]),
   "99005-19": lambda: velocity_choice(2*cos(theta) + 2, 3*t/2, Rational("1.8"), CHOICES["99005-19"]),
   "99005-20": lambda: velocity_choice(2*cos(theta) + 6, 2*t, Rational("0.5"), CHOICES["99005-20"]),
   "99005-21": lambda: velocity_choice(4*sin(theta) + 3, 3*t/4, Rational("1.5"), CHOICES["99005-21"]),

   "99006-00": lambda: ray_gap_rate(-2*theta*sin(theta) + 12, 3*sin(theta) + 2, Rational("1.2")),
   "99006-01": lambda: ray_gap_rate(-2*theta*sin(theta) + 12, 3*sin(theta) + 3, Rational("1.4")),
   "99006-02": lambda: ray_gap_rate(2*theta*sin(theta) + 6, 2*cos(theta) + 2, Rational("1.2")),
   "99006-03": lambda: ray_gap_rate(-theta*sin(theta) + 10, cos(theta) + 3, Rational("0.5")),
   "99006-04": lambda: ray_gap_rate(-2*theta*sin(theta) + 8, sin(theta) + 1, Rational("1.4")),
   "99006-05": lambda: ray_gap_rate(2*theta*sin(theta) + 7, 3*cos(theta) + 2, Rational("1.2")),
   "99006-06": lambda: ray_gap_rate(-theta*sin(theta) + 8, 2*cos(theta) + 2, Rational("1.4")),
   "99006-07": lambda: ray_gap_rate(theta*sin(theta) + 9, sin(theta) + 3, Rational("0.3")),
   "99006-08": lambda: ray_gap_rate(2*theta*sin(theta) + 6, sin(theta) + 1, Rational("1.2")),
   "99006-09": lambda: ray_gap_rate(3*theta*sin(theta) + 10, 3*cos(theta) + 2, Rational("0.5")),
   "99006-10": lambda: ray_gap_rate(3*theta*sin(theta) + 12, 2*cos(theta) + 3, Rational("0.9")),
   "99006-11": lambda: ray_gap_rate(2*theta*sin(theta) + 10, 2*sin(theta) + 4, Rational("0.7")),
   "99006-12": lambda: ray_gap_rate(-theta*sin(theta) + 9, 2*cos(theta) + 3, Rational("1.1")),
   "99006-13": lambda: ray_gap_rate(-theta*sin(theta) + 12, 2*cos(theta) + 2, Rational("0.3")),
   "99006-14": lambda: ray_gap_rate(-theta*sin(theta) + 7, cos(theta) + 1, Rational("1.2")),
   "99006-15": lambda: ray_gap_rate(3*theta*sin(theta) + 12, 2*sin(theta) + 3, Rational("0.5")),
   "99006-16": lambda: ray_gap_rate(theta*sin(theta) + 7, sin(theta) + 4, Rational("0.9")),
   "99006-17": lambda: ray_gap_rate(2*theta*sin(theta) + 12, cos(theta) + 2, Rational("0.7")),
   "99006-18": lambda: ray_gap_rate(3*theta*sin(theta) + 10, 2*sin(theta) + 2, Rational("0.3")),
   "99006-19": lambda: ray_gap_rate(2*theta*sin(theta) + 12, 2*sin(theta) + 4, Rational("1.2")),
   "99006-20": lambda: ray_gap_rate(2*theta*sin(theta) + 8, 2*cos(theta) + 3, Rational("1.1")),
   "99006-21": lambda: ray_gap_rate(-theta*sin(theta) + 9, 2*cos(theta) + 1, Rational("0.7")),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
