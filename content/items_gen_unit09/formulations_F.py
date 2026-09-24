"""Blind formulations for the unit 9 generated items in stems_F.json.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24. No key, candidate, template or worked solution was read. Calculator answers are
returned at full precision and statement items return the text of the choice the mathematics
selects, copied from the stems file.
"""
import re

import mpmath
import sympy
from sympy import Rational, cos, exp, ln, sin, sqrt

from tools.key_recheck import t

mpmath.mp.dps = 30

PRECISION = 30
DISPLAY_TOLERANCE = 0.0005 + 1e-9
ROOT_SCAN_STEPS = 4000

CHOICES = {
   "09002-00": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -6 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = 18 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 6 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 9 \\) there.",
   ],
   "09002-01": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -12 \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -24 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = 24 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = 24 \\) there.",
   ],
   "09002-02": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -18 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = 10 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 18 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{5}{2} \\) there.",
   ],
   "09002-03": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = -8 \\) there.",
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -2 \\) there.",
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -4 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 2 \\) there.",
   ],
   "09002-04": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -4 \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -8 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = 16 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 4 \\) there.",
   ],
   "09002-05": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -1 \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -8 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = 16 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = 2 \\) there.",
   ],
   "09002-06": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -2 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = 8 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 2 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 4 \\) there.",
   ],
   "09002-07": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -12 \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -2 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = 8 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 12 \\) there.",
   ],
   "09002-08": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = -14 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 1 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{1}{2} \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{7}{2} \\) there.",
   ],
   "09002-09": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -10 \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -12 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = 20 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = 12 \\) there.",
   ],
   "09002-10": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = -26 \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = - \\frac{13}{2} \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{1}{2} \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{1}{8} \\) there.",
   ],
   "09002-11": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = -12 \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -3 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 3 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{3}{2} \\) there.",
   ],
   "09002-12": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = -12 \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -12 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 12 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 3 \\) there.",
   ],
   "09002-13": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = -16 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 1 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 2 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 4 \\) there.",
   ],
   "09002-14": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -12 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = 12 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 12 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 3 \\) there.",
   ],
   "09002-15": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -2 \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -7 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = 14 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 2 \\) there.",
   ],
   "09002-16": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = -16 \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -4 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 4 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 8 \\) there.",
   ],
   "09002-17": [
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dt^{2}} = -18 \\) there.",
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -6 \\) there.",
      "The curve is concave down at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = -9 \\) there.",
      "The curve is concave up at t = -1, because \\( \\frac{d^{2}y}{dx^{2}} = 6 \\) there.",
   ],
   "09002-18": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = -26 \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = - \\frac{1}{2} \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{13}{2} \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{1}{8} \\) there.",
   ],
   "09002-19": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = -14 \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = -18 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = 18 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = 7 \\) there.",
   ],
   "09002-20": [
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = - \\frac{3}{2} \\) there.",
      "The curve is concave down at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = -6 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dt^{2}} = 6 \\) there.",
      "The curve is concave up at t = 1, because \\( \\frac{d^{2}y}{dx^{2}} = 6 \\) there.",
   ],
   "09002-21": [
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = - \\frac{13}{2} \\) there.",
      "The curve is concave down at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = - \\frac{1}{8} \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dt^{2}} = 26 \\) there.",
      "The curve is concave up at t = 2, because \\( \\frac{d^{2}y}{dx^{2}} = \\frac{1}{2} \\) there.",
   ],
   "09004-00": [
      "\\( \\left\\langle -0.720, -0.934 \\right\\rangle \\)",
      "\\( \\left\\langle -0.934, -0.720 \\right\\rangle \\)",
      "\\( \\left\\langle 4.400, -0.934 \\right\\rangle \\)",
      "\\( \\left\\langle 4.400, 4.498 \\right\\rangle \\)",
   ],
   "09004-01": [
      "\\( \\left\\langle 3.200, 1.847 \\right\\rangle \\)",
      "\\( \\left\\langle 3.200, 4.304 \\right\\rangle \\)",
      "\\( \\left\\langle 3.840, 4.304 \\right\\rangle \\)",
      "\\( \\left\\langle 4.304, 3.840 \\right\\rangle \\)",
   ],
   "09004-02": [
      "\\( x''(\\frac{1}{2}) \\approx -1.400 \\) and \\( y''(\\frac{1}{2}) \\approx 3.078 \\)",
      "\\( x''(\\frac{1}{2}) \\approx -1.400 \\) and \\( y''(\\frac{1}{2}) \\approx 7.173 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 1.920 \\) and \\( y''(\\frac{1}{2}) \\approx 7.173 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 7.173 \\) and \\( y''(\\frac{1}{2}) \\approx 1.920 \\)",
   ],
   "09004-03": [
      "\\( x''(2) \\approx -0.240 \\) and \\( y''(2) \\approx -0.623 \\)",
      "\\( x''(2) \\approx -0.623 \\) and \\( y''(2) \\approx -0.240 \\)",
      "\\( x''(2) \\approx 3.800 \\) and \\( y''(2) \\approx -0.623 \\)",
      "\\( x''(2) \\approx 3.800 \\) and \\( y''(2) \\approx 2.998 \\)",
   ],
   "09004-04": [
      "\\( x''(\\frac{1}{2}) \\approx 1.699 \\) and \\( y''(\\frac{1}{2}) \\approx -0.600 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 2.880 \\) and \\( y''(\\frac{1}{2}) \\approx 3.677 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 3.677 \\) and \\( y''(\\frac{1}{2}) \\approx -0.600 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 3.677 \\) and \\( y''(\\frac{1}{2}) \\approx 2.880 \\)",
   ],
   "09004-05": [
      "\\( x''(1) \\approx 0.000 \\) and \\( y''(1) \\approx 4.819 \\)",
      "\\( x''(1) \\approx 2.000 \\) and \\( y''(1) \\approx 4.819 \\)",
      "\\( x''(1) \\approx 2.000 \\) and \\( y''(1) \\approx 5.402 \\)",
      "\\( x''(1) \\approx 4.819 \\) and \\( y''(1) \\approx 0.000 \\)",
   ],
   "09004-06": [
      "\\( \\left\\langle -0.799, -1.384 \\right\\rangle \\)",
      "\\( \\left\\langle -1.384, -0.799 \\right\\rangle \\)",
      "\\( \\left\\langle 3.759, -1.384 \\right\\rangle \\)",
      "\\( \\left\\langle 3.759, 1.377 \\right\\rangle \\)",
   ],
   "09004-07": [
      "\\( \\left\\langle -2.000, 5.728 \\right\\rangle \\)",
      "\\( \\left\\langle -2.000, 5.872 \\right\\rangle \\)",
      "\\( \\left\\langle 0.000, 5.728 \\right\\rangle \\)",
      "\\( \\left\\langle 5.728, 0.000 \\right\\rangle \\)",
   ],
   "09004-08": [
      "\\( \\left\\langle -0.799, -3.652 \\right\\rangle \\)",
      "\\( \\left\\langle -3.652, -0.799 \\right\\rangle \\)",
      "\\( \\left\\langle 3.759, -3.652 \\right\\rangle \\)",
      "\\( \\left\\langle 3.759, 3.354 \\right\\rangle \\)",
   ],
   "09004-09": [
      "\\( \\left\\langle -0.799, -1.752 \\right\\rangle \\)",
      "\\( \\left\\langle -1.752, -0.799 \\right\\rangle \\)",
      "\\( \\left\\langle 4.759, -1.752 \\right\\rangle \\)",
      "\\( \\left\\langle 4.759, 2.089 \\right\\rangle \\)",
   ],
   "09004-10": [
      "\\( x''(\\frac{1}{2}) \\approx 2.173 \\) and \\( y''(\\frac{1}{2}) \\approx 3.400 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 2.880 \\) and \\( y''(\\frac{1}{2}) \\approx 4.521 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 4.521 \\) and \\( y''(\\frac{1}{2}) \\approx 2.880 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 4.521 \\) and \\( y''(\\frac{1}{2}) \\approx 3.400 \\)",
   ],
   "09004-11": [
      "\\( \\left\\langle 0.000, 3.169 \\right\\rangle \\)",
      "\\( \\left\\langle 3.000, 2.775 \\right\\rangle \\)",
      "\\( \\left\\langle 3.000, 3.169 \\right\\rangle \\)",
      "\\( \\left\\langle 3.169, 0.000 \\right\\rangle \\)",
   ],
   "09004-12": [
      "\\( x''(\\frac{3}{2}) \\approx -0.947 \\) and \\( y''(\\frac{3}{2}) \\approx 0.932 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 0.932 \\) and \\( y''(\\frac{3}{2}) \\approx -0.947 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 0.932 \\) and \\( y''(\\frac{3}{2}) \\approx 6.692 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 2.903 \\) and \\( y''(\\frac{3}{2}) \\approx 6.692 \\)",
   ],
   "09004-13": [
      "\\( \\left\\langle -0.710, 0.665 \\right\\rangle \\)",
      "\\( \\left\\langle 0.665, -0.710 \\right\\rangle \\)",
      "\\( \\left\\langle 0.769, 0.665 \\right\\rangle \\)",
      "\\( \\left\\langle 0.769, 1.645 \\right\\rangle \\)",
   ],
   "09004-14": [
      "\\( x''(\\frac{3}{2}) \\approx -0.710 \\) and \\( y''(\\frac{3}{2}) \\approx 2.659 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 2.659 \\) and \\( y''(\\frac{3}{2}) \\approx -0.710 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 2.659 \\) and \\( y''(\\frac{3}{2}) \\approx 0.769 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 6.578 \\) and \\( y''(\\frac{3}{2}) \\approx 0.769 \\)",
   ],
   "09004-15": [
      "\\( x''(\\frac{3}{2}) \\approx -0.947 \\) and \\( y''(\\frac{3}{2}) \\approx 1.397 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 1.397 \\) and \\( y''(\\frac{3}{2}) \\approx -0.947 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 2.692 \\) and \\( y''(\\frac{3}{2}) \\approx 1.397 \\)",
      "\\( x''(\\frac{3}{2}) \\approx 2.692 \\) and \\( y''(\\frac{3}{2}) \\approx 4.354 \\)",
   ],
   "09004-16": [
      "\\( x''(\\frac{1}{2}) \\approx 2.400 \\) and \\( y''(\\frac{1}{2}) \\approx 1.231 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 2.400 \\) and \\( y''(\\frac{1}{2}) \\approx 2.869 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 2.869 \\) and \\( y''(\\frac{1}{2}) \\approx 2.880 \\)",
      "\\( x''(\\frac{1}{2}) \\approx 2.880 \\) and \\( y''(\\frac{1}{2}) \\approx 2.869 \\)",
   ],
   "09004-17": [
      "\\( x''(\\frac{5}{2}) \\approx -0.599 \\) and \\( y''(\\frac{5}{2}) \\approx -8.759 \\)",
      "\\( x''(\\frac{5}{2}) \\approx -8.759 \\) and \\( y''(\\frac{5}{2}) \\approx -0.599 \\)",
      "\\( x''(\\frac{5}{2}) \\approx 4.069 \\) and \\( y''(\\frac{5}{2}) \\approx -8.759 \\)",
      "\\( x''(\\frac{5}{2}) \\approx 4.069 \\) and \\( y''(\\frac{5}{2}) \\approx 10.444 \\)",
   ],
   "09004-18": [
      "\\( \\left\\langle 1.435, 1.920 \\right\\rangle \\)",
      "\\( \\left\\langle 1.920, 1.435 \\right\\rangle \\)",
      "\\( \\left\\langle 4.600, 0.616 \\right\\rangle \\)",
      "\\( \\left\\langle 4.600, 1.435 \\right\\rangle \\)",
   ],
   "09004-19": [
      "\\( \\left\\langle -0.220, -0.960 \\right\\rangle \\)",
      "\\( \\left\\langle -0.220, 4.200 \\right\\rangle \\)",
      "\\( \\left\\langle -0.960, -0.220 \\right\\rangle \\)",
      "\\( \\left\\langle 1.771, 4.200 \\right\\rangle \\)",
   ],
   "09004-20": [
      "\\( \\left\\langle -0.710, 1.206 \\right\\rangle \\)",
      "\\( \\left\\langle 1.206, -0.710 \\right\\rangle \\)",
      "\\( \\left\\langle 4.769, 1.206 \\right\\rangle \\)",
      "\\( \\left\\langle 4.769, 2.112 \\right\\rangle \\)",
   ],
   "09004-21": [
      "\\( \\left\\langle 0.200, 1.087 \\right\\rangle \\)",
      "\\( \\left\\langle 0.200, 2.260 \\right\\rangle \\)",
      "\\( \\left\\langle 2.260, 3.840 \\right\\rangle \\)",
      "\\( \\left\\langle 3.840, 2.260 \\right\\rangle \\)",
   ],
}


def full_precision(value):
   return sympy.Float(sympy.N(value, PRECISION), PRECISION)


def shows_value(displayed, computed):
   return abs(float(displayed) - float(computed)) <= DISPLAY_TOLERANCE


def tangent_slope(x_rate, y_position, at):
   slope = sympy.diff(y_position, t) / x_rate

   return full_precision(slope.subs(t, at))


def tangent_slope_from_position(x_position, y_position, at):
   return tangent_slope(sympy.diff(x_position, t), y_position, at)


def second_derivative_dx(x_position, y_position, at):
   slope = sympy.diff(y_position, t) / sympy.diff(x_position, t)
   second = sympy.diff(slope, t) / sympy.diff(x_position, t)

   return sympy.nsimplify(sympy.simplify(second.subs(t, at)))


def latex_number(text):
   cleaned = text.replace(" ", "")
   is_negative = cleaned.startswith("-")
   magnitude_text = cleaned.lstrip("-")
   fraction = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", magnitude_text)

   if fraction:
      magnitude = Rational(int(fraction.group(1)), int(fraction.group(2)))
   else:
      magnitude = sympy.Integer(int(magnitude_text))

   return -magnitude if is_negative else magnitude


CONCAVITY_PATTERN = re.compile(
   r"concave (up|down) at t = -?\d+, because \\\( \\frac\{d\^\{2\}y\}\{d([xt])\^\{2\}\} = (.+?) \\\) there"
)


def concavity_choice(x_position, y_position, at, suffix):
   value = second_derivative_dx(x_position, y_position, at)
   true_direction = "up" if value > 0 else "down"
   correct = []

   for text in CHOICES[suffix]:
      parsed = CONCAVITY_PATTERN.search(text)
      direction, variable, shown = parsed.group(1), parsed.group(2), latex_number(parsed.group(3))
      is_dx_derivative = variable == "x"
      has_value = sympy.simplify(shown - value) == 0
      has_direction = direction == true_direction
      is_correct = is_dx_derivative and has_value and has_direction

      if is_correct:
         correct.append(text)

   return correct[0] if len(correct) == 1 else correct


def curve_length(x_position, y_position, start, end):
   speed = sqrt(sympy.diff(x_position, t) ** 2 + sympy.diff(y_position, t) ** 2)

   return distance_travelled(speed, start, end)


def distance_travelled(speed, start, end):
   speed_function = sympy.lambdify(t, speed, "mpmath")
   value = mpmath.quad(speed_function, [start, end])

   return full_precision(value)


def speed_integral_from_velocity(x_velocity, y_velocity, start, end):
   return distance_travelled(sqrt(x_velocity ** 2 + y_velocity ** 2), start, end)


def acceleration_components(at, x_position=None, x_velocity=None, y_position=None, y_velocity=None):
   if x_velocity is None:
      x_velocity = sympy.diff(x_position, t)

   if y_velocity is None:
      y_velocity = sympy.diff(y_position, t)

   x_acceleration = sympy.diff(x_velocity, t).subs(t, at)
   y_acceleration = sympy.diff(y_velocity, t).subs(t, at)

   return float(sympy.N(x_acceleration, PRECISION)), float(sympy.N(y_acceleration, PRECISION))


def acceleration_choice(suffix, at, **components):
   x_acceleration, y_acceleration = acceleration_components(at, **components)
   correct = []

   for text in CHOICES[suffix]:
      shown = re.findall(r"-?\d+\.\d{3}", text)
      has_two_values = len(shown) == 2
      is_correct = has_two_values and shows_value(shown[0], x_acceleration) and shows_value(shown[1], y_acceleration)

      if is_correct:
         correct.append(text)

   return correct[0] if len(correct) == 1 else correct


def position_component(velocity_component, start_time, start_value, end_time):
   velocity_function = sympy.lambdify(t, velocity_component, "mpmath")
   displacement = mpmath.quad(velocity_function, [start_time, end_time])

   return full_precision(start_value + displacement)


def speed_at(x_velocity, y_velocity, at):
   speed = sqrt(x_velocity ** 2 + y_velocity ** 2)

   return full_precision(speed.subs(t, at))


def first_time_at_speed(x_velocity, y_velocity, target_speed, search_end=20):
   gap = sympy.lambdify(t, sqrt(x_velocity ** 2 + y_velocity ** 2) - target_speed, "mpmath")
   step = mpmath.mpf(search_end) / ROOT_SCAN_STEPS
   previous_time = step
   previous_gap = gap(previous_time)

   for index in range(2, ROOT_SCAN_STEPS + 1):
      current_time = step * index
      current_gap = gap(current_time)
      has_crossed = previous_gap * current_gap <= 0

      if has_crossed:
         return full_precision(mpmath.findroot(gap, (previous_time, current_time), solver="anderson"))

      previous_time, previous_gap = current_time, current_gap

   raise ValueError("speed never reaches the target")


LOG_TERM = ln(t ** 2 + 1)
LOG_RATE = 2 * t / (t ** 2 + 1)
ROOT_T = sqrt(t) * exp(-t / 2)


def velocity_x(amplitude, divisor):
   return amplitude * cos(t ** 2 / divisor)


BY_SUFFIX = {
   "09001-00": lambda: tangent_slope_from_position(2*t + LOG_TERM, 6 * cos(2 * t**2 / 3), 2),
   "09001-01": lambda: tangent_slope_from_position(t + LOG_TERM, 5 * cos(2 * t**2 / 3), 1),
   "09001-02": lambda: tangent_slope(LOG_RATE + 4, 4 * exp(-2 * t**2 / 3), 2),
   "09001-03": lambda: tangent_slope_from_position(2*t + LOG_TERM, 3 * exp(-3 * t**2 / 4), 2),
   "09001-04": lambda: tangent_slope_from_position(4*t + LOG_TERM, 6 * exp(-3 * t**2 / 4), 2),
   "09001-05": lambda: tangent_slope_from_position(3*t + LOG_TERM, 6 * exp(-t**2 / 4), Rational(3, 2)),
   "09001-06": lambda: tangent_slope(LOG_RATE + 1, 2 * sin(t**2 / 4), Rational(3, 2)),
   "09001-07": lambda: tangent_slope(LOG_RATE + 1, 5 * sin(t**2 / 4), 3),
   "09001-08": lambda: tangent_slope(LOG_RATE + 1, 4 * cos(3 * t**2 / 4), 2),
   "09001-09": lambda: tangent_slope(LOG_RATE + 4, 3 * cos(2 * t**2 / 3), 1),
   "09001-10": lambda: tangent_slope(LOG_RATE + 2, 4 * cos(t**2 / 4), 3),
   "09001-11": lambda: tangent_slope_from_position(3*t + LOG_TERM, 4 * exp(-t**2 / 2), Rational(3, 2)),
   "09001-12": lambda: tangent_slope(LOG_RATE + 3, 5 * exp(-t**2 / 4), Rational(3, 2)),
   "09001-13": lambda: tangent_slope(LOG_RATE + 2, 2 * sin(t**2 / 3), Rational(5, 2)),
   "09001-14": lambda: tangent_slope(LOG_RATE + 3, 6 * exp(-t**2 / 3), Rational(5, 2)),
   "09001-15": lambda: tangent_slope(LOG_RATE + 2, 2 * cos(2 * t**2 / 3), 2),
   "09001-16": lambda: tangent_slope_from_position(t + LOG_TERM, 5 * sin(t**2 / 3), Rational(5, 2)),
   "09001-17": lambda: tangent_slope(LOG_RATE + 1, 2 * sin(2 * t**2 / 3), 2),
   "09001-18": lambda: tangent_slope(LOG_RATE + 1, 3 * cos(t**2 / 3), Rational(5, 2)),
   "09001-19": lambda: tangent_slope_from_position(3*t + LOG_TERM, 2 * cos(t**2 / 2), Rational(3, 2)),
   "09001-20": lambda: tangent_slope_from_position(t + LOG_TERM, 5 * cos(t**2 / 4), Rational(3, 2)),
   "09001-21": lambda: tangent_slope_from_position(2*t + LOG_TERM, 5 * cos(t**2 / 4), Rational(3, 2)),

   "09002-00": lambda: concavity_choice(t**2 + t + 2, -2*t**3 + 3*t**2, -1, "09002-00"),
   "09002-01": lambda: concavity_choice(-t**2 + 3*t + 1, 2*t**3 - 2, 2, "09002-01"),
   "09002-02": lambda: concavity_choice(2*t**2 + 3*t, -t**3 + 2*t**2 + 1, -1, "09002-02"),
   "09002-03": lambda: concavity_choice(t**2 + t - 3, t**3 - t**2 + 2, -1, "09002-03"),
   "09002-04": lambda: concavity_choice(-t**2 + t - 3, 2*t**3 + 2*t**2 + 1, 1, "09002-04"),
   "09002-05": lambda: concavity_choice(-t**2 + 2*t + 3, t**3 + 2*t**2 - 2, 2, "09002-05"),
   "09002-06": lambda: concavity_choice(t**2 + t - 3, -t**3 + t**2 + 3, -1, "09002-06"),
   "09002-07": lambda: concavity_choice(-2*t**2 + 3*t + 1, t**3 + t**2 - 1, 1, "09002-07"),
   "09002-08": lambda: concavity_choice(-2*t**2 - 2*t, 2*t**3 - t**2 + 1, -1, "09002-08"),
   "09002-09": lambda: concavity_choice(-t**2 + 3*t - 1, 2*t**3 - 2*t**2 - 3, 2, "09002-09"),
   "09002-10": lambda: concavity_choice(2*t**2 - 4*t + 1, -2*t**3 - t**2 - 2, 2, "09002-10"),
   "09002-11": lambda: concavity_choice(2*t**2 - 2*t + 1, -t**3 - 3*t**2, 1, "09002-11"),
   "09002-12": lambda: concavity_choice(-2*t**2 + 3*t + 1, -2*t**3 - 3, 1, "09002-12"),
   "09002-13": lambda: concavity_choice(-2*t**2 - 2*t + 1, 2*t**3 - 2*t**2 + 3, -1, "09002-13"),
   "09002-14": lambda: concavity_choice(2*t**2 + 3*t + 3, 3 - 2*t**3, -1, "09002-14"),
   "09002-15": lambda: concavity_choice(-t**2 + t + 2, 2*t**3 + t**2 - 2, 1, "09002-15"),
   "09002-16": lambda: concavity_choice(-t**2 + t - 2, -2*t**3 - 2*t**2 + 2, 1, "09002-16"),
   "09002-17": lambda: concavity_choice(t**2 + t - 1, 2*t**3 - 3*t**2, -1, "09002-17"),
   "09002-18": lambda: concavity_choice(-2*t**2 + 4*t - 3, -2*t**3 - t**2 - 1, 2, "09002-18"),
   "09002-19": lambda: concavity_choice(-t**2 + 3*t - 2, -t**3 - t**2 + 3, 2, "09002-19"),
   "09002-20": lambda: concavity_choice(-2*t**2 + 3*t - 3, t**3 - 3, 1, "09002-20"),
   "09002-21": lambda: concavity_choice(-2*t**2 + 4*t - 2, 2*t**3 + t**2 + 1, 2, "09002-21"),

   "09003-00": lambda: curve_length(3 * t**2, 2 * sin(2*t), 0, Rational(3, 2)),
   "09003-01": lambda: curve_length(2 * t**2, 3 * sin(t / 2), 0, Rational(5, 2)),
   "09003-02": lambda: speed_integral_from_velocity(2*t, 2 * cos(2*t), 0, Rational(5, 2)),
   "09003-03": lambda: curve_length(t**2, 2 * sin(t), 0, Rational(3, 2)),
   "09003-04": lambda: speed_integral_from_velocity(5*t, 5 * cos(t), 0, Rational(5, 2)),
   "09003-05": lambda: curve_length(3 * t**2 / 2, 2 * sin(2*t), 0, Rational(3, 2)),
   "09003-06": lambda: speed_integral_from_velocity(6*t, 3 * cos(t), 0, 3),
   "09003-07": lambda: speed_integral_from_velocity(2*t, 10 * cos(2*t), 0, 2),
   "09003-08": lambda: curve_length(3 * t**2 / 2, 5 * sin(t), 0, 3),
   "09003-09": lambda: curve_length(4 * t**2, 3 * sin(t / 2), 0, 2),
   "09003-10": lambda: speed_integral_from_velocity(5*t, cos(t / 2), 0, Rational(5, 2)),
   "09003-11": lambda: speed_integral_from_velocity(4*t, 5 * cos(t), 0, 2),
   "09003-12": lambda: speed_integral_from_velocity(3*t, 2 * cos(t), 0, 1),
   "09003-13": lambda: curve_length(3 * t**2, 4 * sin(2*t), 0, Rational(5, 2)),
   "09003-14": lambda: speed_integral_from_velocity(5*t, cos(t / 2), 0, 3),
   "09003-15": lambda: curve_length(5 * t**2 / 2, sin(2*t), 0, 2),
   "09003-16": lambda: speed_integral_from_velocity(2*t, 5 * cos(t / 2) / 2, 0, Rational(5, 2)),
   "09003-17": lambda: curve_length(5 * t**2 / 2, 3 * sin(2*t), 0, Rational(3, 2)),
   "09003-18": lambda: speed_integral_from_velocity(2*t, 4 * cos(2*t), 0, 1),
   "09003-19": lambda: speed_integral_from_velocity(5*t, 3 * cos(t), 0, 3),
   "09003-20": lambda: curve_length(t**2, sin(t / 2), 0, 3),
   "09003-21": lambda: curve_length(5 * t**2 / 2, 3 * sin(t), 0, 3),

   "09004-00": lambda: acceleration_choice("09004-00", 2, x_position=2*t + 3*LOG_TERM, y_velocity=3 * exp(t/4) * sin(t)),
   "09004-01": lambda: acceleration_choice("09004-01", Rational(1, 2), x_position=4*LOG_TERM, y_velocity=3 * exp(t/2) * sin(t)),
   "09004-02": lambda: acceleration_choice("09004-02", Rational(1, 2), x_position=-3*t + 2*LOG_TERM, y_velocity=5 * exp(t/2) * sin(t)),
   "09004-03": lambda: acceleration_choice("09004-03", 2, x_position=3*t + LOG_TERM, y_velocity=2 * exp(t/4) * sin(t)),
   "09004-04": lambda: acceleration_choice("09004-04", Rational(1, 2), x_velocity=3 * exp(t/3) * sin(t), y_position=-3*t + 3*LOG_TERM),
   "09004-05": lambda: acceleration_choice("09004-05", 1, x_position=2*LOG_TERM, y_velocity=5 * exp(t/4) * sin(t)),
   "09004-06": lambda: acceleration_choice("09004-06", Rational(5, 2), x_position=t + 4*LOG_TERM, y_velocity=exp(t/3) * sin(t)),
   "09004-07": lambda: acceleration_choice("09004-07", 1, x_position=-3*t + LOG_TERM, y_velocity=5 * exp(t/3) * sin(t)),
   "09004-08": lambda: acceleration_choice("09004-08", Rational(5, 2), x_position=t + 4*LOG_TERM, y_velocity=3 * exp(t/4) * sin(t)),
   "09004-09": lambda: acceleration_choice("09004-09", Rational(5, 2), x_position=2*t + 4*LOG_TERM, y_velocity=exp(t/2) * sin(t)),
   "09004-10": lambda: acceleration_choice("09004-10", Rational(1, 2), x_velocity=4 * exp(t/4) * sin(t), y_position=t + 3*LOG_TERM),
   "09004-11": lambda: acceleration_choice("09004-11", 1, x_position=-t + 4*LOG_TERM, y_velocity=2 * exp(t/2) * sin(t)),
   "09004-12": lambda: acceleration_choice("09004-12", Rational(3, 2), x_velocity=2 * exp(t/4) * sin(t), y_position=3*t + 4*LOG_TERM),
   "09004-13": lambda: acceleration_choice("09004-13", Rational(3, 2), x_position=-2*t + 3*LOG_TERM, y_velocity=exp(t/3) * sin(t)),
   "09004-14": lambda: acceleration_choice("09004-14", Rational(3, 2), x_velocity=4 * exp(t/3) * sin(t), y_position=-2*t + 3*LOG_TERM),
   "09004-15": lambda: acceleration_choice("09004-15", Rational(3, 2), x_position=-t + 4*LOG_TERM, y_velocity=3 * exp(t/4) * sin(t)),
   "09004-16": lambda: acceleration_choice("09004-16", Rational(1, 2), x_position=3*LOG_TERM, y_velocity=2 * exp(t/2) * sin(t)),
   "09004-17": lambda: acceleration_choice("09004-17", Rational(5, 2), x_position=2*t + 3*LOG_TERM, y_velocity=5 * exp(t/2) * sin(t)),
   "09004-18": lambda: acceleration_choice("09004-18", Rational(1, 2), x_position=3*t + 2*LOG_TERM, y_velocity=exp(t/2) * sin(t)),
   "09004-19": lambda: acceleration_choice("09004-19", 2, x_velocity=exp(t/3) * sin(t), y_position=t + 4*LOG_TERM),
   "09004-20": lambda: acceleration_choice("09004-20", Rational(3, 2), x_position=2*t + 3*LOG_TERM, y_velocity=exp(t/2) * sin(t)),
   "09004-21": lambda: acceleration_choice("09004-21", Rational(1, 2), x_position=-3*t + 4*LOG_TERM, y_velocity=2 * exp(t/4) * sin(t)),

   "09005-00": lambda: position_component(velocity_x(4, 4), 3, -1, 1),
   "09005-01": lambda: position_component(2 * ROOT_T, 3, -1, 1),
   "09005-02": lambda: position_component(ROOT_T, 1, 3, 3),
   "09005-03": lambda: position_component(velocity_x(4, 4), 1, -2, 3),
   "09005-04": lambda: position_component(4 * ROOT_T, 1, 2, 2),
   "09005-05": lambda: position_component(ROOT_T, 2, 3, 1),
   "09005-06": lambda: position_component(ROOT_T, 3, -3, 1),
   "09005-07": lambda: position_component(velocity_x(6, 4), 3, -2, 2),
   "09005-08": lambda: position_component(velocity_x(2, 2), 2, -4, 1),
   "09005-09": lambda: position_component(3 * ROOT_T, 2, 3, 3),
   "09005-10": lambda: position_component(velocity_x(5, 4), 3, 4, 1),
   "09005-11": lambda: position_component(4 * ROOT_T, 3, -2, 5),
   "09005-12": lambda: position_component(velocity_x(3, 4), 3, -4, 4),
   "09005-13": lambda: position_component(velocity_x(5, 3), 3, 5, 5),
   "09005-14": lambda: position_component(2 * ROOT_T, 1, 3, 2),
   "09005-15": lambda: position_component(velocity_x(2, 3), 1, 1, 3),
   "09005-16": lambda: position_component(velocity_x(3, 4), 2, 4, 3),
   "09005-17": lambda: position_component(velocity_x(4, 2), 3, 5, 5),
   "09005-18": lambda: position_component(ROOT_T, 1, 2, 3),
   "09005-19": lambda: position_component(4 * ROOT_T, 3, -1, 4),
   "09005-20": lambda: position_component(velocity_x(6, 4), 2, -1, 4),
   "09005-21": lambda: position_component(3 * ROOT_T, 3, -5, 5),

   "09006-00": lambda: first_time_at_speed(6 * cos(t / 2), 2 * t**2, 8),
   "09006-01": lambda: speed_at(6 * cos(t / 2), 3 * t**2 / 2, Rational(1, 2)),
   "09006-02": lambda: speed_at(5 * cos(t / 2), 3 * t**2 / 2, Rational(5, 4)),
   "09006-03": lambda: first_time_at_speed(2 * cos(t / 2), 4 * t**2, 6),
   "09006-04": lambda: first_time_at_speed(5 * cos(t / 2), 2 * t**2, 7),
   "09006-05": lambda: speed_at(2 * cos(t / 2), 5 * t**2 / 2, Rational(1, 2)),
   "09006-06": lambda: first_time_at_speed(5 * cos(t), 4 * t**2, 8),
   "09006-07": lambda: first_time_at_speed(2 * cos(t / 2), 5 * t**2 / 2, 7),
   "09006-08": lambda: first_time_at_speed(3 * cos(t), 3 * t**2, 5),
   "09006-09": lambda: speed_at(2 * cos(t), 2 * t**2, Rational(5, 4)),
   "09006-10": lambda: speed_at(4 * cos(t), 5 * t**2 / 2, Rational(1, 2)),
   "09006-11": lambda: first_time_at_speed(4 * cos(t), 2 * t**2, 7),
   "09006-12": lambda: speed_at(2 * cos(t), 4 * t**2, Rational(5, 4)),
   "09006-13": lambda: speed_at(4 * cos(t), 3 * t**2 / 2, Rational(3, 2)),
   "09006-14": lambda: first_time_at_speed(3 * cos(t / 2), 3 * t**2 / 2, 6),
   "09006-15": lambda: speed_at(4 * cos(t / 2), 3 * t**2 / 2, Rational(5, 4)),
   "09006-16": lambda: speed_at(3 * cos(t), 3 * t**2, Rational(1, 2)),
   "09006-17": lambda: first_time_at_speed(4 * cos(t), 2 * t**2, 6),
   "09006-18": lambda: speed_at(4 * cos(t / 2), 3 * t**2, Rational(5, 4)),
   "09006-19": lambda: speed_at(5 * cos(t), 5 * t**2 / 2, Rational(3, 2)),
   "09006-20": lambda: first_time_at_speed(4 * cos(t), 3 * t**2 / 2, 6),
   "09006-21": lambda: speed_at(3 * cos(t), 3 * t**2 / 2, Rational(3, 4)),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
