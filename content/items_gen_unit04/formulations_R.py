"""Blind answers for the unit 4 generated items in stems_R.json, one SymPy computation per stem.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, without seeing any key, worked solution or template. Each statement item is decided by
computing the velocity, acceleration, sign intervals or rate the stem asks for and returning the
one choice, copied below, that states that result with a valid reason; a list means no choice or
more than one choice fits.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import sympy
from sympy import Rational, exp

from tools.key_recheck import t

CHOICES = {
   "04003-00": [
      "The speed is -5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 18 \\) have opposite signs.",
      "The speed is 11 meters per second, and it is increasing at that time, because \\( v(1) = -11 \\) and \\( a(1) = -5 \\) have the same sign.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 18 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is increasing at that time, because \\( a(1) = 18 \\) is positive, so the particle is speeding up.",
   ],
   "04003-01": [
      "The speed is -1 meters per second, and it is increasing at that time, because \\( v(1) = -1 \\) and \\( a(1) = -8 \\) have the same sign.",
      "The speed is 1 meters per second, and it is decreasing at that time, because \\( a(1) = -8 \\) is negative, so the particle is slowing down.",
      "The speed is 1 meters per second, and it is increasing at that time, because \\( v(1) = -1 \\) and \\( a(1) = -8 \\) have the same sign.",
      "The speed is 8 meters per second, and it is increasing at that time, because \\( v(1) = -8 \\) and \\( a(1) = -12 \\) have the same sign.",
   ],
   "04003-02": [
      "The speed is -9 meters per second, and it is decreasing at that time, because \\( v(1) = -9 \\) and \\( a(1) = 2 \\) have opposite signs.",
      "The speed is 15 meters per second, and it is increasing at that time, because \\( v(1) = -15 \\) and \\( a(1) = -9 \\) have the same sign.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( v(1) = -9 \\) and \\( a(1) = 2 \\) have opposite signs.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( a(1) = 2 \\) is positive, so the particle is speeding up.",
   ],
   "04003-03": [
      "The speed is 14 meters per second, and it is increasing at that time, because \\( v(3) = -14 \\) and \\( a(3) = -6 \\) have the same sign.",
      "The speed is 53 meters per second, and it is increasing at that time, because \\( v(3) = 53 \\) and \\( a(3) = 6 \\) have the same sign.",
      "The speed is 6 meters per second, and it is decreasing at that time, because \\( v(3) = 6 \\) and \\( a(3) = -14 \\) have opposite signs.",
      "The speed is 6 meters per second, and it is decreasing at that time, because \\( v(3) = 6 \\) and \\( a(3) = -6 \\) have opposite signs.",
   ],
   "04003-04": [
      "The speed is 14 meters per second, and it is increasing at that time, because \\( v(2) = -14 \\) and \\( a(2) = -6 \\) have the same sign.",
      "The speed is 35 meters per second, and it is increasing at that time, because \\( v(2) = 35 \\) and \\( a(2) = 9 \\) have the same sign.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( v(2) = 9 \\) and \\( a(2) = -14 \\) have opposite signs.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( v(2) = 9 \\) and \\( a(2) = -6 \\) have opposite signs.",
   ],
   "04003-05": [
      "The speed is 14 meters per second, and it is decreasing at that time, because \\( v(2) = -14 \\) and \\( a(2) = 6 \\) have opposite signs.",
      "The speed is 20 meters per second, and it is increasing at that time, because \\( v(2) = 20 \\) and \\( a(2) = 12 \\) have the same sign.",
      "The speed is 6 meters per second, and it is increasing at that time, because \\( v(2) = 6 \\) and \\( a(2) = 12 \\) have the same sign.",
      "The speed is 6 meters per second, and it is increasing at that time, because \\( v(2) = 6 \\) and \\( a(2) = 20 \\) have the same sign.",
   ],
   "04003-06": [
      "The speed is -9 meters per second, and it is increasing at that time, because \\( v(3) = -9 \\) and \\( a(3) = -24 \\) have the same sign.",
      "The speed is 51 meters per second, and it is decreasing at that time, because \\( v(3) = 51 \\) and \\( a(3) = -9 \\) have opposite signs.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( a(3) = -24 \\) is negative, so the particle is slowing down.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( v(3) = -9 \\) and \\( a(3) = -24 \\) have the same sign.",
   ],
   "04003-07": [
      "The speed is -7 meters per second, and it is decreasing at that time, because \\( v(1) = -7 \\) and \\( a(1) = 4 \\) have opposite signs.",
      "The speed is 3 meters per second, and it is increasing at that time, because \\( v(1) = -3 \\) and \\( a(1) = -7 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( v(1) = -7 \\) and \\( a(1) = 4 \\) have opposite signs.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( a(1) = 4 \\) is positive, so the particle is speeding up.",
   ],
   "04003-08": [
      "The speed is -5 meters per second, and it is decreasing at that time, because \\( v(3) = -5 \\) and \\( a(3) = 22 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(3) = -5 \\) and \\( a(3) = 22 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is increasing at that time, because \\( a(3) = 22 \\) is positive, so the particle is speeding up.",
      "The speed is 89 meters per second, and it is increasing at that time, because \\( v(3) = -89 \\) and \\( a(3) = -5 \\) have the same sign.",
   ],
   "04003-09": [
      "The speed is -2 meters per second, and it is increasing at that time, because \\( v(3) = -2 \\) and \\( a(3) = -40 \\) have the same sign.",
      "The speed is 2 meters per second, and it is decreasing at that time, because \\( a(3) = -40 \\) is negative, so the particle is slowing down.",
      "The speed is 2 meters per second, and it is increasing at that time, because \\( v(3) = -2 \\) and \\( a(3) = -40 \\) have the same sign.",
      "The speed is 40 meters per second, and it is increasing at that time, because \\( v(3) = -40 \\) and \\( a(3) = -32 \\) have the same sign.",
   ],
   "04003-10": [
      "The speed is -8 meters per second, and it is increasing at that time, because \\( v(1) = -8 \\) and \\( a(1) = -2 \\) have the same sign.",
      "The speed is 2 meters per second, and it is increasing at that time, because \\( v(1) = -2 \\) and \\( a(1) = -8 \\) have the same sign.",
      "The speed is 8 meters per second, and it is decreasing at that time, because \\( a(1) = -2 \\) is negative, so the particle is slowing down.",
      "The speed is 8 meters per second, and it is increasing at that time, because \\( v(1) = -8 \\) and \\( a(1) = -2 \\) have the same sign.",
   ],
   "04003-11": [
      "The speed is 30 meters per second, and it is increasing at that time, because \\( v(3) = -30 \\) and \\( a(3) = -12 \\) have the same sign.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(3) = 5 \\) and \\( a(3) = -12 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(3) = 5 \\) and \\( a(3) = -30 \\) have opposite signs.",
      "The speed is 91 meters per second, and it is increasing at that time, because \\( v(3) = 91 \\) and \\( a(3) = 5 \\) have the same sign.",
   ],
   "04003-12": [
      "The speed is -3 meters per second, and it is increasing at that time, because \\( v(3) = -3 \\) and \\( a(3) = -30 \\) have the same sign.",
      "The speed is 3 meters per second, and it is decreasing at that time, because \\( a(3) = -30 \\) is negative, so the particle is slowing down.",
      "The speed is 3 meters per second, and it is increasing at that time, because \\( v(3) = -3 \\) and \\( a(3) = -30 \\) have the same sign.",
      "The speed is 72 meters per second, and it is decreasing at that time, because \\( v(3) = 72 \\) and \\( a(3) = -3 \\) have opposite signs.",
   ],
   "04003-13": [
      "The speed is -5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 10 \\) have opposite signs.",
      "The speed is 15 meters per second, and it is increasing at that time, because \\( v(1) = -15 \\) and \\( a(1) = -5 \\) have the same sign.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 10 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is increasing at that time, because \\( a(1) = 10 \\) is positive, so the particle is speeding up.",
   ],
   "04003-14": [
      "The speed is -7 meters per second, and it is increasing at that time, because \\( v(2) = -7 \\) and \\( a(2) = -14 \\) have the same sign.",
      "The speed is 14 meters per second, and it is increasing at that time, because \\( v(2) = -14 \\) and \\( a(2) = -18 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( a(2) = -14 \\) is negative, so the particle is slowing down.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( v(2) = -7 \\) and \\( a(2) = -14 \\) have the same sign.",
   ],
   "04003-15": [
      "The speed is -7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 10 \\) have opposite signs.",
      "The speed is 40 meters per second, and it is increasing at that time, because \\( v(3) = -40 \\) and \\( a(3) = -7 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 10 \\) have opposite signs.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( a(3) = 10 \\) is positive, so the particle is speeding up.",
   ],
   "04003-16": [
      "The speed is -7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 47 \\) have opposite signs.",
      "The speed is 47 meters per second, and it is increasing at that time, because \\( v(3) = 47 \\) and \\( a(3) = 26 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 47 \\) have opposite signs.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( a(3) = 47 \\) is positive, so the particle is speeding up.",
   ],
   "04003-17": [
      "The speed is -1 meters per second, and it is increasing at that time, because \\( v(3) = -1 \\) and \\( a(3) = -28 \\) have the same sign.",
      "The speed is 1 meters per second, and it is decreasing at that time, because \\( a(3) = -28 \\) is negative, so the particle is slowing down.",
      "The speed is 1 meters per second, and it is increasing at that time, because \\( v(3) = -1 \\) and \\( a(3) = -28 \\) have the same sign.",
      "The speed is 69 meters per second, and it is decreasing at that time, because \\( v(3) = 69 \\) and \\( a(3) = -1 \\) have opposite signs.",
   ],
   "04003-18": [
      "The speed is -4 meters per second, and it is decreasing at that time, because \\( v(2) = -4 \\) and \\( a(2) = 40 \\) have opposite signs.",
      "The speed is 4 meters per second, and it is decreasing at that time, because \\( v(2) = -4 \\) and \\( a(2) = 40 \\) have opposite signs.",
      "The speed is 4 meters per second, and it is increasing at that time, because \\( a(2) = 40 \\) is positive, so the particle is speeding up.",
      "The speed is 40 meters per second, and it is increasing at that time, because \\( v(2) = 40 \\) and \\( a(2) = 30 \\) have the same sign.",
   ],
   "04003-19": [
      "The speed is -4 meters per second, and it is increasing at that time, because \\( v(1) = -4 \\) and \\( a(1) = -14 \\) have the same sign.",
      "The speed is 2 meters per second, and it is decreasing at that time, because \\( v(1) = 2 \\) and \\( a(1) = -4 \\) have opposite signs.",
      "The speed is 4 meters per second, and it is decreasing at that time, because \\( a(1) = -14 \\) is negative, so the particle is slowing down.",
      "The speed is 4 meters per second, and it is increasing at that time, because \\( v(1) = -4 \\) and \\( a(1) = -14 \\) have the same sign.",
   ],
   "04003-20": [
      "The speed is 10 meters per second, and it is decreasing at that time, because \\( v(2) = -10 \\) and \\( a(2) = 9 \\) have opposite signs.",
      "The speed is 24 meters per second, and it is increasing at that time, because \\( v(2) = 24 \\) and \\( a(2) = 12 \\) have the same sign.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( v(2) = 9 \\) and \\( a(2) = 12 \\) have the same sign.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( v(2) = 9 \\) and \\( a(2) = 24 \\) have the same sign.",
   ],
   "04003-21": [
      "The speed is 10 meters per second, and it is increasing at that time, because \\( v(1) = 10 \\) and \\( a(1) = 8 \\) have the same sign.",
      "The speed is 4 meters per second, and it is increasing at that time, because \\( v(1) = -4 \\) and \\( a(1) = -12 \\) have the same sign.",
      "The speed is 8 meters per second, and it is decreasing at that time, because \\( v(1) = 8 \\) and \\( a(1) = -12 \\) have opposite signs.",
      "The speed is 8 meters per second, and it is decreasing at that time, because \\( v(1) = 8 \\) and \\( a(1) = -4 \\) have opposite signs.",
   ],
   "04004-00": [
      "The particle is moving to the left exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 5\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, \\frac{11}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left exactly on \\( \\left(3, 8\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(3, \\frac{13}{3}\\right) \\), because \\( v(t) < 0 \\) there.",
   ],
   "04004-01": [
      "The particle is moving to the right exactly on \\( \\left(0, 1\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{2}{3}\\right) \\), because v(t) is increasing there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{1}{3}, 1\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is never moving to the right for \\( 0 < t < 7 \\), because \\( x(t) > 0 \\) at no time in that interval.",
   ],
   "04004-02": [
      "The particle is moving to the right exactly on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 9\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{11}{3}\\right) \\) and \\( \\left(5, 9\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(3, 5\\right) \\) and \\( \\left(5, 9\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{13}{3}, 9\\right) \\), because v(t) is increasing there.",
   ],
   "04004-03": [
      "The particle is moving to the right exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(\\frac{11}{3}, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(4, 10\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{10}{3}, 10\\right) \\), because v(t) is increasing there.",
   ],
   "04004-04": [
      "The particle is moving to the left exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(\\frac{11}{3}, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(4, 7\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{10}{3}, 7\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-05": [
      "The particle is moving to the right exactly on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 6\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{7}{3}\\right) \\) and \\( \\left(5, 6\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(1, 5\\right) \\) and \\( \\left(5, 6\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{11}{3}, 6\\right) \\), because v(t) is increasing there.",
   ],
   "04004-06": [
      "The particle is moving to the right exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(\\frac{10}{3}, 8\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, 2\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(4, 8\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{8}{3}, 8\\right) \\), because v(t) is increasing there.",
   ],
   "04004-07": [
      "The particle is moving to the left exactly on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, \\frac{7}{3}\\right) \\) and \\( \\left(5, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(1, 5\\right) \\) and \\( \\left(5, 7\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{11}{3}, 7\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-08": [
      "The particle is moving to the left exactly on \\( \\left(0, 1\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, \\frac{5}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{4}{3}, 2\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is never moving to the left for \\( 0 < t < 10 \\), because \\( v(t) < 0 \\) at no time in that interval.",
   ],
   "04004-09": [
      "The particle is moving to the left exactly on \\( \\left(0, 4\\right) \\) and \\( \\left(4, 9\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, 4\\right) \\) and \\( \\left(4, 9\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, \\frac{4}{3}\\right) \\) and \\( \\left(4, 9\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{8}{3}, 9\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-10": [
      "The particle is moving to the left exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(1, 2\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, \\frac{4}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left exactly on \\( \\left(1, \\frac{5}{3}\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is never moving to the left for \\( 0 < t < 9 \\), because \\( v(t) < 0 \\) at no time in that interval.",
   ],
   "04004-11": [
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{10}{3}\\right) \\), because v(t) is increasing there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{5}{3}, 5\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is never moving to the right for \\( 0 < t < 10 \\), because \\( v(t) > 0 \\) at no time in that interval.",
      "The particle is never moving to the right for \\( 0 < t < 10 \\), because \\( x(t) > 0 \\) at no time in that interval.",
   ],
   "04004-12": [
      "The particle is moving to the right exactly on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 8\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{11}{3}\\right) \\) and \\( \\left(5, 8\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(3, 5\\right) \\) and \\( \\left(5, 8\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{13}{3}, 8\\right) \\), because v(t) is increasing there.",
   ],
   "04004-13": [
      "The particle is moving to the right exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(\\frac{7}{3}, 7\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, 1\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(3, 7\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{5}{3}, 7\\right) \\), because v(t) is increasing there.",
   ],
   "04004-14": [
      "The particle is moving to the right exactly on \\( \\left(0, 4\\right) \\) and \\( \\left(\\frac{16}{3}, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, 4\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(6, 10\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{14}{3}, 10\\right) \\), because v(t) is increasing there.",
   ],
   "04004-15": [
      "The particle is moving to the right exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(1, 5\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{1}{3}\\right) \\) and \\( \\left(1, 5\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(1, 5\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{2}{3}, 5\\right) \\), because v(t) is increasing there.",
   ],
   "04004-16": [
      "The particle is moving to the right exactly on \\( \\left(0, 4\\right) \\) and \\( \\left(\\frac{16}{3}, 7\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, 4\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(6, 7\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{14}{3}, 7\\right) \\), because v(t) is increasing there.",
   ],
   "04004-17": [
      "The particle is moving to the left exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(\\frac{11}{3}, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(4, 7\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{10}{3}, 7\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-18": [
      "The particle is moving to the left exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(\\frac{14}{3}, 9\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, 2\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(6, 9\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{10}{3}, 9\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-19": [
      "The particle is moving to the left exactly on \\( \\left(0, 1\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left exactly on \\( \\left(0, \\frac{5}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left exactly on \\( \\left(\\frac{4}{3}, 2\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is never moving to the left for \\( 0 < t < 6 \\), because \\( v(t) < 0 \\) at no time in that interval.",
   ],
   "04004-20": [
      "The particle is moving to the right exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 4\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, \\frac{10}{3}\\right) \\), because v(t) is increasing there.",
      "The particle is moving to the right exactly on \\( \\left(3, \\frac{11}{3}\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is never moving to the right for \\( 0 < t < 9 \\), because \\( v(t) > 0 \\) at no time in that interval.",
   ],
   "04004-21": [
      "The particle is moving to the right exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(\\frac{10}{3}, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(0, 2\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(4, 10\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right exactly on \\( \\left(\\frac{8}{3}, 10\\right) \\), because v(t) is increasing there.",
   ],
   "04005-00": [
      "\\( H'(3) = -3.543 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 3.543 degrees Celsius per minute.",
      "\\( H'(3) = -3.543 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 3.543 minutes per degree Celsius.",
      "\\( H'(3) = -3.543 \\), so at time t = 3 minutes the temperature of the liquid is moving with a velocity of -3.543 degrees Celsius per minute.",
      "\\( H'(3) = -3.543 \\), so when the temperature of the liquid is 3 degrees Celsius it is decreasing at a rate of 3.543 degrees Celsius per minute.",
   ],
   "04005-01": [
      "\\( N'(4) = -2.274 \\), so at time t = 4 minutes the number of people inside the museum is decreasing at a rate of 2.274 minutes per person.",
      "\\( N'(4) = -2.274 \\), so at time t = 4 minutes the number of people inside the museum is decreasing at a rate of 2.274 people per minute.",
      "\\( N'(4) = -2.274 \\), so at time t = 4 minutes the number of people inside the museum is moving with a velocity of -2.274 people per minute.",
      "\\( N'(4) = -2.274 \\), so when the number of people inside the museum is 4 people it is decreasing at a rate of 2.274 people per minute.",
   ],
   "04005-02": [
      "\\( H'(5) = 3.639 \\), so at time t = 5 minutes the temperature of the liquid is increasing at a rate of 3.639 degrees Celsius per minute.",
      "\\( H'(5) = 3.639 \\), so at time t = 5 minutes the temperature of the liquid is increasing at a rate of 3.639 minutes per degree Celsius.",
      "\\( H'(5) = 3.639 \\), so at time t = 5 minutes the temperature of the liquid is moving with a velocity of 3.639 degrees Celsius per minute.",
      "\\( H'(5) = 3.639 \\), so when the temperature of the liquid is 5 degrees Celsius it is increasing at a rate of 3.639 degrees Celsius per minute.",
   ],
   "04005-03": [
      "\\( B'(9) = 3.253 \\), so at time t = 9 minutes the charge stored in the battery is increasing at a rate of 3.253 minutes per watt-hour.",
      "\\( B'(9) = 3.253 \\), so at time t = 9 minutes the charge stored in the battery is increasing at a rate of 3.253 watt-hours per minute.",
      "\\( B'(9) = 3.253 \\), so at time t = 9 minutes the charge stored in the battery is moving with a velocity of 3.253 watt-hours per minute.",
      "\\( B'(9) = 3.253 \\), so when the charge stored in the battery is 9 watt-hours it is increasing at a rate of 3.253 watt-hours per minute.",
   ],
   "04005-04": [
      "\\( B'(5) = 3.639 \\), so at time t = 5 minutes the charge stored in the battery is increasing at a rate of 3.639 minutes per watt-hour.",
      "\\( B'(5) = 3.639 \\), so at time t = 5 minutes the charge stored in the battery is increasing at a rate of 3.639 watt-hours per minute.",
      "\\( B'(5) = 3.639 \\), so at time t = 5 minutes the charge stored in the battery is moving with a velocity of 3.639 watt-hours per minute.",
      "\\( B'(5) = 3.639 \\), so when the charge stored in the battery is 5 watt-hours it is increasing at a rate of 3.639 watt-hours per minute.",
   ],
   "04005-05": [
      "\\( C'(8) = 2.529 \\), so at time t = 8 hours the concentration of the medicine is increasing at a rate of 2.529 hours per milligram per liter.",
      "\\( C'(8) = 2.529 \\), so at time t = 8 hours the concentration of the medicine is increasing at a rate of 2.529 milligrams per liter per hour.",
      "\\( C'(8) = 2.529 \\), so at time t = 8 hours the concentration of the medicine is moving with a velocity of 2.529 milligrams per liter per hour.",
      "\\( C'(8) = 2.529 \\), so when the concentration of the medicine is 8 milligrams per liter it is increasing at a rate of 2.529 milligrams per liter per hour.",
   ],
   "04005-06": [
      "\\( L'(7) = 2.558 \\), so at time t = 7 days the level of the pollutant is increasing at a rate of 2.558 days per part per billion.",
      "\\( L'(7) = 2.558 \\), so at time t = 7 days the level of the pollutant is increasing at a rate of 2.558 parts per billion per day.",
      "\\( L'(7) = 2.558 \\), so at time t = 7 days the level of the pollutant is moving with a velocity of 2.558 parts per billion per day.",
      "\\( L'(7) = 2.558 \\), so when the level of the pollutant is 7 parts per billion it is increasing at a rate of 2.558 parts per billion per day.",
   ],
   "04005-07": [
      "\\( W'(6) = -4.044 \\), so at time t = 6 hours the amount of water in the tank is decreasing at a rate of 4.044 hours per hundred gallons.",
      "\\( W'(6) = -4.044 \\), so at time t = 6 hours the amount of water in the tank is decreasing at a rate of 4.044 hundreds of gallons per hour.",
      "\\( W'(6) = -4.044 \\), so at time t = 6 hours the amount of water in the tank is moving with a velocity of -4.044 hundreds of gallons per hour.",
      "\\( W'(6) = -4.044 \\), so when the amount of water in the tank is 6 hundreds of gallons it is decreasing at a rate of 4.044 hundreds of gallons per hour.",
   ],
   "04005-08": [
      "\\( C'(2) = 9.384 \\), so at time t = 2 hours the concentration of the medicine is increasing at a rate of 9.384 hours per milligram per liter.",
      "\\( C'(2) = 9.384 \\), so at time t = 2 hours the concentration of the medicine is increasing at a rate of 9.384 milligrams per liter per hour.",
      "\\( C'(2) = 9.384 \\), so at time t = 2 hours the concentration of the medicine is moving with a velocity of 9.384 milligrams per liter per hour.",
      "\\( C'(2) = 9.384 \\), so when the concentration of the medicine is 2 milligrams per liter it is increasing at a rate of 9.384 milligrams per liter per hour.",
   ],
   "04005-09": [
      "\\( C'(6) = 3.372 \\), so at time t = 6 hours the concentration of the medicine is increasing at a rate of 3.372 hours per milligram per liter.",
      "\\( C'(6) = 3.372 \\), so at time t = 6 hours the concentration of the medicine is increasing at a rate of 3.372 milligrams per liter per hour.",
      "\\( C'(6) = 3.372 \\), so at time t = 6 hours the concentration of the medicine is moving with a velocity of 3.372 milligrams per liter per hour.",
      "\\( C'(6) = 3.372 \\), so when the concentration of the medicine is 6 milligrams per liter it is increasing at a rate of 3.372 milligrams per liter per hour.",
   ],
   "04005-10": [
      "\\( H'(3) = -4.868 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 4.868 degrees Celsius per minute.",
      "\\( H'(3) = -4.868 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 4.868 minutes per degree Celsius.",
      "\\( H'(3) = -4.868 \\), so at time t = 3 minutes the temperature of the liquid is moving with a velocity of -4.868 degrees Celsius per minute.",
      "\\( H'(3) = -4.868 \\), so when the temperature of the liquid is 3 degrees Celsius it is decreasing at a rate of 4.868 degrees Celsius per minute.",
   ],
   "04005-11": [
      "\\( B'(5) = -4.708 \\), so at time t = 5 minutes the charge stored in the battery is decreasing at a rate of 4.708 minutes per watt-hour.",
      "\\( B'(5) = -4.708 \\), so at time t = 5 minutes the charge stored in the battery is decreasing at a rate of 4.708 watt-hours per minute.",
      "\\( B'(5) = -4.708 \\), so at time t = 5 minutes the charge stored in the battery is moving with a velocity of -4.708 watt-hours per minute.",
      "\\( B'(5) = -4.708 \\), so when the charge stored in the battery is 5 watt-hours it is decreasing at a rate of 4.708 watt-hours per minute.",
   ],
   "04005-12": [
      "\\( W'(9) = -0.787 \\), so at time t = 9 hours the amount of water in the tank is decreasing at a rate of 0.787 hours per hundred gallons.",
      "\\( W'(9) = -0.787 \\), so at time t = 9 hours the amount of water in the tank is decreasing at a rate of 0.787 hundreds of gallons per hour.",
      "\\( W'(9) = -0.787 \\), so at time t = 9 hours the amount of water in the tank is moving with a velocity of -0.787 hundreds of gallons per hour.",
      "\\( W'(9) = -0.787 \\), so when the amount of water in the tank is 9 hundreds of gallons it is decreasing at a rate of 0.787 hundreds of gallons per hour.",
   ],
   "04005-13": [
      "\\( H'(7) = 3.476 \\), so at time t = 7 minutes the temperature of the liquid is increasing at a rate of 3.476 degrees Celsius per minute.",
      "\\( H'(7) = 3.476 \\), so at time t = 7 minutes the temperature of the liquid is increasing at a rate of 3.476 minutes per degree Celsius.",
      "\\( H'(7) = 3.476 \\), so at time t = 7 minutes the temperature of the liquid is moving with a velocity of 3.476 degrees Celsius per minute.",
      "\\( H'(7) = 3.476 \\), so when the temperature of the liquid is 7 degrees Celsius it is increasing at a rate of 3.476 degrees Celsius per minute.",
   ],
   "04005-14": [
      "\\( N'(3) = 3.842 \\), so at time t = 3 minutes the number of people inside the museum is increasing at a rate of 3.842 minutes per person.",
      "\\( N'(3) = 3.842 \\), so at time t = 3 minutes the number of people inside the museum is increasing at a rate of 3.842 people per minute.",
      "\\( N'(3) = 3.842 \\), so at time t = 3 minutes the number of people inside the museum is moving with a velocity of 3.842 people per minute.",
      "\\( N'(3) = 3.842 \\), so when the number of people inside the museum is 3 people it is increasing at a rate of 3.842 people per minute.",
   ],
   "04005-15": [
      "\\( W'(7) = 2.325 \\), so at time t = 7 hours the amount of water in the tank is increasing at a rate of 2.325 hours per hundred gallons.",
      "\\( W'(7) = 2.325 \\), so at time t = 7 hours the amount of water in the tank is increasing at a rate of 2.325 hundreds of gallons per hour.",
      "\\( W'(7) = 2.325 \\), so at time t = 7 hours the amount of water in the tank is moving with a velocity of 2.325 hundreds of gallons per hour.",
      "\\( W'(7) = 2.325 \\), so when the amount of water in the tank is 7 hundreds of gallons it is increasing at a rate of 2.325 hundreds of gallons per hour.",
   ],
   "04005-16": [
      "\\( L'(5) = 4.782 \\), so at time t = 5 days the level of the pollutant is increasing at a rate of 4.782 days per part per billion.",
      "\\( L'(5) = 4.782 \\), so at time t = 5 days the level of the pollutant is increasing at a rate of 4.782 parts per billion per day.",
      "\\( L'(5) = 4.782 \\), so at time t = 5 days the level of the pollutant is moving with a velocity of 4.782 parts per billion per day.",
      "\\( L'(5) = 4.782 \\), so when the level of the pollutant is 5 parts per billion it is increasing at a rate of 4.782 parts per billion per day.",
   ],
   "04005-17": [
      "\\( B'(4) = -5.841 \\), so at time t = 4 minutes the charge stored in the battery is decreasing at a rate of 5.841 minutes per watt-hour.",
      "\\( B'(4) = -5.841 \\), so at time t = 4 minutes the charge stored in the battery is decreasing at a rate of 5.841 watt-hours per minute.",
      "\\( B'(4) = -5.841 \\), so at time t = 4 minutes the charge stored in the battery is moving with a velocity of -5.841 watt-hours per minute.",
      "\\( B'(4) = -5.841 \\), so when the charge stored in the battery is 4 watt-hours it is decreasing at a rate of 5.841 watt-hours per minute.",
   ],
   "04005-18": [
      "\\( B'(6) = -1.769 \\), so at time t = 6 minutes the charge stored in the battery is decreasing at a rate of 1.769 minutes per watt-hour.",
      "\\( B'(6) = -1.769 \\), so at time t = 6 minutes the charge stored in the battery is decreasing at a rate of 1.769 watt-hours per minute.",
      "\\( B'(6) = -1.769 \\), so at time t = 6 minutes the charge stored in the battery is moving with a velocity of -1.769 watt-hours per minute.",
      "\\( B'(6) = -1.769 \\), so when the charge stored in the battery is 6 watt-hours it is decreasing at a rate of 1.769 watt-hours per minute.",
   ],
   "04005-19": [
      "\\( H'(4) = 4.180 \\), so at time t = 4 minutes the temperature of the liquid is increasing at a rate of 4.180 degrees Celsius per minute.",
      "\\( H'(4) = 4.180 \\), so at time t = 4 minutes the temperature of the liquid is increasing at a rate of 4.180 minutes per degree Celsius.",
      "\\( H'(4) = 4.180 \\), so at time t = 4 minutes the temperature of the liquid is moving with a velocity of 4.180 degrees Celsius per minute.",
      "\\( H'(4) = 4.180 \\), so when the temperature of the liquid is 4 degrees Celsius it is increasing at a rate of 4.180 degrees Celsius per minute.",
   ],
   "04005-20": [
      "\\( H'(8) = 2.471 \\), so at time t = 8 minutes the temperature of the liquid is increasing at a rate of 2.471 degrees Celsius per minute.",
      "\\( H'(8) = 2.471 \\), so at time t = 8 minutes the temperature of the liquid is increasing at a rate of 2.471 minutes per degree Celsius.",
      "\\( H'(8) = 2.471 \\), so at time t = 8 minutes the temperature of the liquid is moving with a velocity of 2.471 degrees Celsius per minute.",
      "\\( H'(8) = 2.471 \\), so when the temperature of the liquid is 8 degrees Celsius it is increasing at a rate of 2.471 degrees Celsius per minute.",
   ],
   "04005-21": [
      "\\( C'(3) = 6.571 \\), so at time t = 3 hours the concentration of the medicine is increasing at a rate of 6.571 hours per milligram per liter.",
      "\\( C'(3) = 6.571 \\), so at time t = 3 hours the concentration of the medicine is increasing at a rate of 6.571 milligrams per liter per hour.",
      "\\( C'(3) = 6.571 \\), so at time t = 3 hours the concentration of the medicine is moving with a velocity of 6.571 milligrams per liter per hour.",
      "\\( C'(3) = 6.571 \\), so when the concentration of the medicine is 3 milligrams per liter it is increasing at a rate of 6.571 milligrams per liter per hour.",
   ],
}


def pick(suffix, is_correct):
   matching = [choice for choice in CHOICES[suffix] if is_correct(choice)]
   has_one_match = len(matching) == 1

   if has_one_match:
      return matching[0]

   return matching


def latex_number(text):
   cleaned = text.strip()
   fraction = re.fullmatch(r"(-\s*)?\\frac\{(\d+)\}\{(\d+)\}", cleaned)

   if fraction:
      sign = -1 if fraction.group(1) else 1

      return sign * Rational(int(fraction.group(2)), int(fraction.group(3)))

   return Rational(cleaned)


def stated_intervals(text):
   pairs = re.findall(r"\\left\((.+?), (.+?)\\right\)", text)

   return [(latex_number(left), latex_number(right)) for left, right in pairs]


def interval_pairs(solution_set):
   pieces = solution_set.args if isinstance(solution_set, sympy.Union) else (solution_set,)
   pairs = []

   for piece in pieces:
      if piece.is_empty:
         continue

      is_open_interval = isinstance(piece, sympy.Interval) and piece.left_open and piece.right_open

      if not is_open_interval:
         raise ValueError(f"unexpected piece {piece}")

      pairs.append((piece.inf, piece.sup))

   return sorted(pairs)


def speed_statement(suffix, expression, given, at):
   """Speed is |v|; it increases when v and a share a sign and decreases when they differ."""
   velocity = sympy.diff(expression, t) if given == "position" else expression
   acceleration = sympy.diff(velocity, t)
   velocity_value = velocity.subs(t, at)
   acceleration_value = acceleration.subs(t, at)
   signs_agree = velocity_value * acceleration_value > 0
   signs_differ = velocity_value * acceleration_value < 0

   if signs_agree:
      trend, relation = "increasing", "have the same sign"
   elif signs_differ:
      trend, relation = "decreasing", "have opposite signs"
   else:
      raise ValueError("speed trend undecided when v or a is 0")

   expected = (
      f"The speed is {abs(velocity_value)} meters per second, and it is {trend} at that time, "
      f"because \\( v({at}) = {velocity_value} \\) and \\( a({at}) = {acceleration_value} \\) {relation}."
   )

   return pick(suffix, lambda text: text == expected)


def direction_statement(suffix, position, end, direction):
   """The particle moves right where v(t) > 0 and left where v(t) < 0, on 0 < t < end."""
   velocity = sympy.diff(position, t)
   condition = velocity > 0 if direction == "right" else velocity < 0
   inequality = ">" if direction == "right" else "<"
   solution_set = sympy.solveset(condition, t, sympy.Interval.open(0, end))
   intervals = interval_pairs(solution_set)
   has_no_motion = len(intervals) == 0

   def is_correct(text):
      if has_no_motion:
         says_never = f"is never moving to the {direction}" in text
         cites_velocity = f"because \\( v(t) {inequality} 0 \\) at no time" in text

         return says_never and cites_velocity

      states_intervals = stated_intervals(text) == intervals
      cites_velocity = text.endswith(f"because \\( v(t) {inequality} 0 \\) there.")
      names_direction = f"moving to the {direction} exactly on" in text

      return states_intervals and cites_velocity and names_direction

   return pick(suffix, is_correct)


def rate_statement(suffix, expression, given, at, rate_unit, time_unit):
   """The derivative at time at, read as a rate of change of the quantity in rate_unit."""
   rate = sympy.diff(expression, t) if given == "amount" else expression
   value = sympy.N(rate.subs(t, at), 30)
   shown = f"{float(value):.3f}"
   magnitude = f"{abs(float(value)):.3f}"
   trend = "increasing" if value > 0 else "decreasing"

   def is_correct(text):
      states_value = f"= {shown} \\), so at time t = {at} {time_unit} the " in text
      reads_rate = text.endswith(f"is {trend} at a rate of {magnitude} {rate_unit}.")

      return states_value and reads_rate

   return pick(suffix, is_correct)


def speed(suffix, expression, at, given="position"):
   return suffix, lambda: speed_statement(suffix, expression, given, at)


def direction(suffix, position, end, way):
   return suffix, lambda: direction_statement(suffix, position, end, way)


def rate(suffix, expression, given, at, rate_unit, time_unit):
   return suffix, lambda: rate_statement(suffix, expression, given, at, rate_unit, time_unit)


CELSIUS = "degrees Celsius per minute"
PEOPLE = "people per minute"
CHARGE = "watt-hours per minute"
DOSE = "milligrams per liter per hour"
POLLUTANT = "parts per billion per day"
WATER = "hundreds of gallons per hour"

ITEMS = [
   speed("04003-00", 2*t**3 + 3*t**2 - 17*t + 1, 1),
   speed("04003-01", -t**3 - 3*t**2 + t + 2, 1, "velocity"),
   speed("04003-02", t**3 - 2*t**2 - 8*t - 6, 1),
   speed("04003-03", -t**3 + 2*t**2 + 21*t - 1, 3),
   speed("04003-04", -t**3 - t**2 + 25*t - 3, 2),
   speed("04003-05", 2*t**3 - 2*t**2 - 10*t - 2, 2),
   speed("04003-06", -t**3 - 3*t**2 + 36*t - 3, 3),
   speed("04003-07", t**3 - t**2 - 8*t + 5, 1),
   speed("04003-08", t**3 + 2*t**2 - 44*t - 2, 3),
   speed("04003-09", -2*t**3 + 2*t**2 + 2*t + 28, 3, "velocity"),
   speed("04003-10", -t**3 - t**2 + 3*t - 9, 1, "velocity"),
   speed("04003-11", -2*t**3 + 3*t**2 + 41*t - 5, 3),
   speed("04003-12", -2*t**3 + 3*t**2 + 33*t, 3),
   speed("04003-13", t**3 + 2*t**2 - 12*t - 6, 1),
   speed("04003-14", -2*t**3 + 3*t**2 - 2*t + 1, 2, "velocity"),
   speed("04003-15", t**3 - 4*t**2 - 10*t - 1, 3),
   speed("04003-16", t**3 + 4*t**2 - 4*t - 58, 3, "velocity"),
   speed("04003-17", -2*t**3 + 4*t**2 + 29*t, 3),
   speed("04003-18", 2*t**3 + 3*t**2 + 4*t - 40, 2, "velocity"),
   speed("04003-19", -2*t**3 - t**2 + 4*t + 1, 1),
   speed("04003-20", 2*t**3 - 15*t + 4, 2),
   speed("04003-21", -2*t**3 + 4*t**2 + 6*t + 2, 1),

   direction("04004-00", 3*(t - 5)*(t - 3)**2, 8, "left"),
   direction("04004-01", -t*(t - 1)**2, 7, "right"),
   direction("04004-02", (t - 5)**2*(t - 3), 9, "right"),
   direction("04004-03", (t - 4)*(t - 3)**2, 10, "right"),
   direction("04004-04", -2*(t - 4)*(t - 3)**2, 7, "left"),
   direction("04004-05", (t - 5)**2*(t - 1), 6, "right"),
   direction("04004-06", (t - 4)*(t - 2)**2, 8, "right"),
   direction("04004-07", -3*(t - 5)**2*(t - 1), 7, "left"),
   direction("04004-08", 2*(t - 2)**2*(t - 1), 10, "left"),
   direction("04004-09", -t*(t - 4)**2, 9, "left"),
   direction("04004-10", 2*(t - 2)*(t - 1)**2, 9, "left"),
   direction("04004-11", -t*(t - 5)**2, 10, "right"),
   direction("04004-12", 2*(t - 5)**2*(t - 3), 8, "right"),
   direction("04004-13", 2*(t - 3)*(t - 1)**2, 7, "right"),
   direction("04004-14", 3*(t - 6)*(t - 4)**2, 10, "right"),
   direction("04004-15", t*(t - 1)**2, 5, "right"),
   direction("04004-16", (t - 6)*(t - 4)**2, 7, "right"),
   direction("04004-17", -2*(t - 4)*(t - 3)**2, 7, "left"),
   direction("04004-18", -2*(t - 6)*(t - 2)**2, 9, "left"),
   direction("04004-19", 3*(t - 2)**2*(t - 1), 6, "left"),
   direction("04004-20", -(t - 4)*(t - 3)**2, 9, "right"),
   direction("04004-21", (t - 4)*(t - 2)**2, 10, "right"),

   rate("04005-00", 40 + 30*exp(-t/4), "amount", 3, CELSIUS, "minutes"),
   rate("04005-01", -Rational(15, 4)*exp(-t/8), "rate", 4, PEOPLE, "minutes"),
   rate("04005-02", 110 - 60*exp(-t/10), "amount", 5, CELSIUS, "minutes"),
   rate("04005-03", 8*exp(-t/10), "rate", 9, CHARGE, "minutes"),
   rate("04005-04", 105 - 60*exp(-t/10), "amount", 5, CHARGE, "minutes"),
   rate("04005-05", 100 - 55*exp(-t/8), "amount", 8, DOSE, "hours"),
   rate("04005-06", 85 - 55*exp(-t/12), "amount", 7, POLLUTANT, "days"),
   rate("04005-07", -Rational(20, 3)*exp(-t/12), "rate", 6, WATER, "hours"),
   rate("04005-08", 120 - 70*exp(-t/5), "amount", 2, DOSE, "hours"),
   rate("04005-09", 95 - 55*exp(-t/6), "amount", 6, DOSE, "hours"),
   rate("04005-10", 60 + 75*exp(-t/12), "amount", 3, CELSIUS, "minutes"),
   rate("04005-11", -Rational(65, 6)*exp(-t/6), "rate", 5, CHARGE, "minutes"),
   rate("04005-12", 10 + 20*exp(-t/12), "amount", 9, WATER, "hours"),
   rate("04005-13", 7*exp(-t/10), "rate", 7, CELSIUS, "minutes"),
   rate("04005-14", 80 - 35*exp(-t/5), "amount", 3, PEOPLE, "minutes"),
   rate("04005-15", Rational(25, 6)*exp(-t/12), "rate", 7, WATER, "hours"),
   rate("04005-16", 13*exp(-t/5), "rate", 5, POLLUTANT, "days"),
   rate("04005-17", -13*exp(-t/5), "rate", 4, CHARGE, "minutes"),
   rate("04005-18", -Rational(35, 12)*exp(-t/12), "rate", 6, CHARGE, "minutes"),
   rate("04005-19", 100 - 70*exp(-t/12), "amount", 4, CELSIUS, "minutes"),
   rate("04005-20", 115 - 55*exp(-t/10), "amount", 8, CELSIUS, "minutes"),
   rate("04005-21", Rational(65, 6)*exp(-t/6), "rate", 3, DOSE, "hours"),
]

BY_SUFFIX = dict(ITEMS)

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
