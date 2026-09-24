"""Blind re-solve of the unit 7 generated items in stems_E.json, written from the stems alone.

Written by claude-opus-5-5 on the operator's delegation of 2026-09-24, reading only stems_E.json,
the verifier prompt, the unit 10 key_formulations.py for format and tools/key_recheck.py for its
helpers. No key, worked solution or template was seen. A statement item returns the text of the
choice whose content matches the mathematics computed here. The choice texts are copied into
this file so it runs without the stems file.
"""
import re

import sympy
from sympy import E, Rational, cos, exp, log, oo, sin, sqrt
from sympy.parsing.sympy_parser import (
   convert_xor,
   implicit_multiplication,
   parse_expr,
   standard_transformations,
)

from tools.key_recheck import (
   euler_approximation,
   is_solution,
   particular_solutions,
   second_derivative_along_solution,
   t,
   x,
   y,
)

P, C, H, T, k = sympy.symbols("P C H T k")

CHOICES_BY_SUFFIX = {
   "07001-00": [
      "The solution curve through \\( (0, 0) \\) falls across the whole window, flattening toward the line \\( P = -2 \\) from above as t increases, and never touches the line \\( P = -2 \\).",
      "The solution curve through \\( (0, 0) \\) rises across the whole window, flattening toward the line \\( P = -2 \\) from above as t decreases, and never touches the line \\( P = -2 \\).",
      "The solution curve through \\( (0, 0) \\) rises across the whole window, leaving the line \\( P = -2 \\) at a finite value of t after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (0, 0) \\) rises across the whole window, passing through the line \\( P = -2 \\), and continuing on its other side.",
   ],
   "07001-01": [
      "The solution curve through \\( (2, 1) \\) falls across the whole window, flattening toward the line \\( y = 3 \\) from below as x decreases, and never touches the line \\( y = 3 \\).",
      "The solution curve through \\( (2, 1) \\) rises across the whole window, flattening toward the line \\( y = 3 \\) from below as x increases, and never touches the line \\( y = 3 \\).",
      "The solution curve through \\( (2, 1) \\) rises across the whole window, passing through the line \\( y = 3 \\), and continuing on its other side.",
      "The solution curve through \\( (2, 1) \\) rises across the whole window, reaching the line \\( y = 3 \\) at a finite value of x and then running along it, so it meets the line in a corner.",
   ],
   "07001-02": [
      "The solution curve through \\( (-1, 5) \\) falls across the whole window, flattening toward the line \\( y = 3 \\) from above as t increases, and never touches the line \\( y = 3 \\).",
      "The solution curve through \\( (-1, 5) \\) falls across the whole window, passing through the line \\( y = 3 \\), and continuing on its other side.",
      "The solution curve through \\( (-1, 5) \\) falls across the whole window, reaching the line \\( y = 3 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-1, 5) \\) rises across the whole window, flattening toward the line \\( y = 3 \\) from above as t decreases, and never touches the line \\( y = 3 \\).",
   ],
   "07001-03": [
      "The solution curve through \\( (0, 0) \\) falls across the whole window, flattening toward the line \\( P = 1 \\) from below as t decreases, and never touches the line \\( P = 1 \\).",
      "The solution curve through \\( (0, 0) \\) falls across the whole window, leaving the line \\( P = 1 \\) at a finite value of t after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (0, 0) \\) falls across the whole window, passing through the line \\( P = 1 \\), and continuing on its other side.",
      "The solution curve through \\( (0, 0) \\) rises across the whole window, flattening toward the line \\( P = 1 \\) from below as t increases, and never touches the line \\( P = 1 \\).",
   ],
   "07001-04": [
      "The solution curve through \\( (1, -2) \\) falls across the whole window, flattening toward the line \\( P = -1 \\) from below as t decreases, and never touches the line \\( P = -1 \\).",
      "The solution curve through \\( (1, -2) \\) rises across the whole window, flattening toward the line \\( P = -1 \\) from below as t increases, and never touches the line \\( P = -1 \\).",
      "The solution curve through \\( (1, -2) \\) rises across the whole window, passing through the line \\( P = -1 \\), and continuing on its other side.",
      "The solution curve through \\( (1, -2) \\) rises across the whole window, reaching the line \\( P = -1 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
   ],
   "07001-05": [
      "The solution curve through \\( (0, -2) \\) falls across the whole window, flattening toward the line \\( y = 0 \\) from below as x decreases, and never touches the line \\( y = 0 \\).",
      "The solution curve through \\( (0, -2) \\) rises across the whole window, flattening toward the line \\( y = 0 \\) from below as x increases, and never touches the line \\( y = 0 \\).",
      "The solution curve through \\( (0, -2) \\) rises across the whole window, passing through the line \\( y = 0 \\), and continuing on its other side.",
      "The solution curve through \\( (0, -2) \\) rises across the whole window, reaching the line \\( y = 0 \\) at a finite value of x and then running along it, so it meets the line in a corner.",
   ],
   "07001-06": [
      "The solution curve through \\( (1, 2) \\) falls across the whole window, flattening toward the line \\( y = 1 \\) from above as x increases, and never touches the line \\( y = 1 \\).",
      "The solution curve through \\( (1, 2) \\) falls across the whole window, passing through the line \\( y = 1 \\), and continuing on its other side.",
      "The solution curve through \\( (1, 2) \\) falls across the whole window, reaching the line \\( y = 1 \\) at a finite value of x and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (1, 2) \\) rises across the whole window, flattening toward the line \\( y = 1 \\) from above as x decreases, and never touches the line \\( y = 1 \\).",
   ],
   "07001-07": [
      "The solution curve through \\( (2, 0) \\) falls across the whole window, flattening toward the line \\( y = 2 \\) from below as t decreases, and never touches the line \\( y = 2 \\).",
      "The solution curve through \\( (2, 0) \\) rises across the whole window, flattening toward the line \\( y = 2 \\) from below as t increases, and never touches the line \\( y = 2 \\).",
      "The solution curve through \\( (2, 0) \\) rises across the whole window, passing through the line \\( y = 2 \\), and continuing on its other side.",
      "The solution curve through \\( (2, 0) \\) rises across the whole window, reaching the line \\( y = 2 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
   ],
   "07001-08": [
      "The solution curve through \\( (-2, 6) \\) falls across the whole window, flattening toward the line \\( P = 4 \\) from above as t increases, and never touches the line \\( P = 4 \\).",
      "The solution curve through \\( (-2, 6) \\) falls across the whole window, passing through the line \\( P = 4 \\), and continuing on its other side.",
      "The solution curve through \\( (-2, 6) \\) falls across the whole window, reaching the line \\( P = 4 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-2, 6) \\) rises across the whole window, flattening toward the line \\( P = 4 \\) from above as t decreases, and never touches the line \\( P = 4 \\).",
   ],
   "07001-09": [
      "The solution curve through \\( (-2, 4) \\) falls across the whole window, flattening toward the line \\( P = 2 \\) from above as t increases, and never touches the line \\( P = 2 \\).",
      "The solution curve through \\( (-2, 4) \\) rises across the whole window, flattening toward the line \\( P = 2 \\) from above as t decreases, and never touches the line \\( P = 2 \\).",
      "The solution curve through \\( (-2, 4) \\) rises across the whole window, leaving the line \\( P = 2 \\) at a finite value of t after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-2, 4) \\) rises across the whole window, passing through the line \\( P = 2 \\), and continuing on its other side.",
   ],
   "07001-10": [
      "The solution curve through \\( (-2, 2) \\) falls across the whole window, flattening toward the line \\( y = 0 \\) from above as x increases, and never touches the line \\( y = 0 \\).",
      "The solution curve through \\( (-2, 2) \\) falls across the whole window, passing through the line \\( y = 0 \\), and continuing on its other side.",
      "The solution curve through \\( (-2, 2) \\) falls across the whole window, reaching the line \\( y = 0 \\) at a finite value of x and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-2, 2) \\) rises across the whole window, flattening toward the line \\( y = 0 \\) from above as x decreases, and never touches the line \\( y = 0 \\).",
   ],
   "07001-11": [
      "The solution curve through \\( (-2, 6) \\) falls across the whole window, flattening toward the line \\( y = 4 \\) from above as x increases, and never touches the line \\( y = 4 \\).",
      "The solution curve through \\( (-2, 6) \\) rises across the whole window, flattening toward the line \\( y = 4 \\) from above as x decreases, and never touches the line \\( y = 4 \\).",
      "The solution curve through \\( (-2, 6) \\) rises across the whole window, leaving the line \\( y = 4 \\) at a finite value of x after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-2, 6) \\) rises across the whole window, passing through the line \\( y = 4 \\), and continuing on its other side.",
   ],
   "07001-12": [
      "The solution curve through \\( (-1, 1) \\) falls across the whole window, flattening toward the line \\( y = 0 \\) from above as x increases, and never touches the line \\( y = 0 \\).",
      "The solution curve through \\( (-1, 1) \\) rises across the whole window, flattening toward the line \\( y = 0 \\) from above as x decreases, and never touches the line \\( y = 0 \\).",
      "The solution curve through \\( (-1, 1) \\) rises across the whole window, leaving the line \\( y = 0 \\) at a finite value of x after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-1, 1) \\) rises across the whole window, passing through the line \\( y = 0 \\), and continuing on its other side.",
   ],
   "07001-13": [
      "The solution curve through \\( (0, 2) \\) falls across the whole window, flattening toward the line \\( y = 0 \\) from above as x increases, and never touches the line \\( y = 0 \\).",
      "The solution curve through \\( (0, 2) \\) falls across the whole window, passing through the line \\( y = 0 \\), and continuing on its other side.",
      "The solution curve through \\( (0, 2) \\) falls across the whole window, reaching the line \\( y = 0 \\) at a finite value of x and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (0, 2) \\) rises across the whole window, flattening toward the line \\( y = 0 \\) from above as x decreases, and never touches the line \\( y = 0 \\).",
   ],
   "07001-14": [
      "The solution curve through \\( (2, 1) \\) falls across the whole window, flattening toward the line \\( y = 3 \\) from below as x decreases, and never touches the line \\( y = 3 \\).",
      "The solution curve through \\( (2, 1) \\) rises across the whole window, flattening toward the line \\( y = 3 \\) from below as x increases, and never touches the line \\( y = 3 \\).",
      "The solution curve through \\( (2, 1) \\) rises across the whole window, passing through the line \\( y = 3 \\), and continuing on its other side.",
      "The solution curve through \\( (2, 1) \\) rises across the whole window, reaching the line \\( y = 3 \\) at a finite value of x and then running along it, so it meets the line in a corner.",
   ],
   "07001-15": [
      "The solution curve through \\( (2, 0) \\) falls across the whole window, flattening toward the line \\( y = -1 \\) from above as t increases, and never touches the line \\( y = -1 \\).",
      "The solution curve through \\( (2, 0) \\) falls across the whole window, passing through the line \\( y = -1 \\), and continuing on its other side.",
      "The solution curve through \\( (2, 0) \\) falls across the whole window, reaching the line \\( y = -1 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (2, 0) \\) rises across the whole window, flattening toward the line \\( y = -1 \\) from above as t decreases, and never touches the line \\( y = -1 \\).",
   ],
   "07001-16": [
      "The solution curve through \\( (-1, 3) \\) falls across the whole window, flattening toward the line \\( P = 1 \\) from above as t increases, and never touches the line \\( P = 1 \\).",
      "The solution curve through \\( (-1, 3) \\) falls across the whole window, passing through the line \\( P = 1 \\), and continuing on its other side.",
      "The solution curve through \\( (-1, 3) \\) falls across the whole window, reaching the line \\( P = 1 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-1, 3) \\) rises across the whole window, flattening toward the line \\( P = 1 \\) from above as t decreases, and never touches the line \\( P = 1 \\).",
   ],
   "07001-17": [
      "The solution curve through \\( (-2, 1) \\) falls across the whole window, flattening toward the line \\( y = -1 \\) from above as t increases, and never touches the line \\( y = -1 \\).",
      "The solution curve through \\( (-2, 1) \\) falls across the whole window, passing through the line \\( y = -1 \\), and continuing on its other side.",
      "The solution curve through \\( (-2, 1) \\) falls across the whole window, reaching the line \\( y = -1 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-2, 1) \\) rises across the whole window, flattening toward the line \\( y = -1 \\) from above as t decreases, and never touches the line \\( y = -1 \\).",
   ],
   "07001-18": [
      "The solution curve through \\( (1, 5) \\) falls across the whole window, flattening toward the line \\( y = 4 \\) from above as t increases, and never touches the line \\( y = 4 \\).",
      "The solution curve through \\( (1, 5) \\) rises across the whole window, flattening toward the line \\( y = 4 \\) from above as t decreases, and never touches the line \\( y = 4 \\).",
      "The solution curve through \\( (1, 5) \\) rises across the whole window, leaving the line \\( y = 4 \\) at a finite value of t after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (1, 5) \\) rises across the whole window, passing through the line \\( y = 4 \\), and continuing on its other side.",
   ],
   "07001-19": [
      "The solution curve through \\( (-1, 1) \\) falls across the whole window, flattening toward the line \\( P = 3 \\) from below as t decreases, and never touches the line \\( P = 3 \\).",
      "The solution curve through \\( (-1, 1) \\) falls across the whole window, leaving the line \\( P = 3 \\) at a finite value of t after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-1, 1) \\) falls across the whole window, passing through the line \\( P = 3 \\), and continuing on its other side.",
      "The solution curve through \\( (-1, 1) \\) rises across the whole window, flattening toward the line \\( P = 3 \\) from below as t increases, and never touches the line \\( P = 3 \\).",
   ],
   "07001-20": [
      "The solution curve through \\( (2, -1) \\) falls across the whole window, flattening toward the line \\( P = -2 \\) from above as t increases, and never touches the line \\( P = -2 \\).",
      "The solution curve through \\( (2, -1) \\) falls across the whole window, passing through the line \\( P = -2 \\), and continuing on its other side.",
      "The solution curve through \\( (2, -1) \\) falls across the whole window, reaching the line \\( P = -2 \\) at a finite value of t and then running along it, so it meets the line in a corner.",
      "The solution curve through \\( (2, -1) \\) rises across the whole window, flattening toward the line \\( P = -2 \\) from above as t decreases, and never touches the line \\( P = -2 \\).",
   ],
   "07001-21": [
      "The solution curve through \\( (-1, -3) \\) falls across the whole window, flattening toward the line \\( y = -2 \\) from below as x decreases, and never touches the line \\( y = -2 \\).",
      "The solution curve through \\( (-1, -3) \\) falls across the whole window, leaving the line \\( y = -2 \\) at a finite value of x after running along it, so it meets the line in a corner.",
      "The solution curve through \\( (-1, -3) \\) falls across the whole window, passing through the line \\( y = -2 \\), and continuing on its other side.",
      "The solution curve through \\( (-1, -3) \\) rises across the whole window, flattening toward the line \\( y = -2 \\) from below as x increases, and never touches the line \\( y = -2 \\).",
   ],
   "07002-00": [
      "The segments are horizontal exactly along the line \\( P = 4 - 3 t \\), have positive slope where \\( P < 4 - 3 t \\), and have negative slope where \\( P > 4 - 3 t \\).",
      "The segments are horizontal exactly along the line \\( P = 4 - 3 t \\), have positive slope where \\( P > 4 - 3 t \\), and have negative slope where \\( P < 4 - 3 t \\).",
      "The segments are horizontal exactly along the line \\( P = 4 \\), have positive slope where \\( P < 4 \\), and have negative slope where \\( P > 4 \\).",
      "The segments are horizontal exactly along the line \\( t = 4 - 3 P \\), have positive slope where \\( t < 4 - 3 P \\), and have negative slope where \\( t > 4 - 3 P \\).",
   ],
   "07002-01": [
      "The segments are horizontal exactly along the line \\( P = 2 \\), have positive slope where \\( P < 2 \\), and have negative slope where \\( P > 2 \\).",
      "The segments are horizontal exactly along the line \\( P = t + 2 \\), have positive slope where \\( P < t + 2 \\), and have negative slope where \\( P > t + 2 \\).",
      "The segments are horizontal exactly along the line \\( P = t + 2 \\), have positive slope where \\( P > t + 2 \\), and have negative slope where \\( P < t + 2 \\).",
      "The segments are horizontal exactly along the line \\( t = P + 2 \\), have positive slope where \\( t < P + 2 \\), and have negative slope where \\( t > P + 2 \\).",
   ],
   "07002-02": [
      "The segments are horizontal exactly along the line \\( y = -1 \\), have positive slope where \\( y < -1 \\), and have negative slope where \\( y > -1 \\).",
      "The segments are horizontal exactly along the parabola \\( x = 3 y^{2} - 1 \\), have positive slope where \\( x < 3 y^{2} - 1 \\), and have negative slope where \\( x > 3 y^{2} - 1 \\).",
      "The segments are horizontal exactly along the parabola \\( y = 3 x^{2} - 1 \\), have positive slope where \\( y < 3 x^{2} - 1 \\), and have negative slope where \\( y > 3 x^{2} - 1 \\).",
      "The segments are horizontal exactly along the parabola \\( y = 3 x^{2} - 1 \\), have positive slope where \\( y > 3 x^{2} - 1 \\), and have negative slope where \\( y < 3 x^{2} - 1 \\).",
   ],
   "07002-03": [
      "The segments are horizontal exactly along the line \\( y = -4 \\), have positive slope where \\( y < -4 \\), and have negative slope where \\( y > -4 \\).",
      "The segments are horizontal exactly along the parabola \\( t = 2 y^{2} - 4 \\), have positive slope where \\( t < 2 y^{2} - 4 \\), and have negative slope where \\( t > 2 y^{2} - 4 \\).",
      "The segments are horizontal exactly along the parabola \\( y = 2 t^{2} - 4 \\), have positive slope where \\( y < 2 t^{2} - 4 \\), and have negative slope where \\( y > 2 t^{2} - 4 \\).",
      "The segments are horizontal exactly along the parabola \\( y = 2 t^{2} - 4 \\), have positive slope where \\( y > 2 t^{2} - 4 \\), and have negative slope where \\( y < 2 t^{2} - 4 \\).",
   ],
   "07002-04": [
      "The segments are horizontal exactly along the line \\( P = - t - 2 \\), have positive slope where \\( P < - t - 2 \\), and have negative slope where \\( P > - t - 2 \\).",
      "The segments are horizontal exactly along the line \\( P = - t - 2 \\), have positive slope where \\( P > - t - 2 \\), and have negative slope where \\( P < - t - 2 \\).",
      "The segments are horizontal exactly along the line \\( P = -2 \\), have positive slope where \\( P > -2 \\), and have negative slope where \\( P < -2 \\).",
      "The segments are horizontal exactly along the line \\( t = - P - 2 \\), have positive slope where \\( t > - P - 2 \\), and have negative slope where \\( t < - P - 2 \\).",
   ],
   "07002-05": [
      "The segments are horizontal exactly along the line \\( y = 1 \\), have positive slope where \\( y < 1 \\), and have negative slope where \\( y > 1 \\).",
      "The segments are horizontal exactly along the parabola \\( t = 2 y^{2} + 1 \\), have positive slope where \\( t < 2 y^{2} + 1 \\), and have negative slope where \\( t > 2 y^{2} + 1 \\).",
      "The segments are horizontal exactly along the parabola \\( y = 2 t^{2} + 1 \\), have positive slope where \\( y < 2 t^{2} + 1 \\), and have negative slope where \\( y > 2 t^{2} + 1 \\).",
      "The segments are horizontal exactly along the parabola \\( y = 2 t^{2} + 1 \\), have positive slope where \\( y > 2 t^{2} + 1 \\), and have negative slope where \\( y < 2 t^{2} + 1 \\).",
   ],
   "07002-06": [
      "The segments are horizontal exactly along the line \\( t = 3 y - 4 \\), have positive slope where \\( t > 3 y - 4 \\), and have negative slope where \\( t < 3 y - 4 \\).",
      "The segments are horizontal exactly along the line \\( y = -4 \\), have positive slope where \\( y > -4 \\), and have negative slope where \\( y < -4 \\).",
      "The segments are horizontal exactly along the line \\( y = 3 t - 4 \\), have positive slope where \\( y < 3 t - 4 \\), and have negative slope where \\( y > 3 t - 4 \\).",
      "The segments are horizontal exactly along the line \\( y = 3 t - 4 \\), have positive slope where \\( y > 3 t - 4 \\), and have negative slope where \\( y < 3 t - 4 \\).",
   ],
   "07002-07": [
      "The segments are horizontal exactly along the line \\( P = 4 \\), have positive slope where \\( P < 4 \\), and have negative slope where \\( P > 4 \\).",
      "The segments are horizontal exactly along the parabola \\( P = 4 - 3 t^{2} \\), have positive slope where \\( P < 4 - 3 t^{2} \\), and have negative slope where \\( P > 4 - 3 t^{2} \\).",
      "The segments are horizontal exactly along the parabola \\( P = 4 - 3 t^{2} \\), have positive slope where \\( P > 4 - 3 t^{2} \\), and have negative slope where \\( P < 4 - 3 t^{2} \\).",
      "The segments are horizontal exactly along the parabola \\( t = 4 - 3 P^{2} \\), have positive slope where \\( t < 4 - 3 P^{2} \\), and have negative slope where \\( t > 4 - 3 P^{2} \\).",
   ],
   "07002-08": [
      "The segments are horizontal exactly along the line \\( y = 5 \\), have positive slope where \\( y > 5 \\), and have negative slope where \\( y < 5 \\).",
      "The segments are horizontal exactly along the parabola \\( t = y^{2} + 5 \\), have positive slope where \\( t > y^{2} + 5 \\), and have negative slope where \\( t < y^{2} + 5 \\).",
      "The segments are horizontal exactly along the parabola \\( y = t^{2} + 5 \\), have positive slope where \\( y < t^{2} + 5 \\), and have negative slope where \\( y > t^{2} + 5 \\).",
      "The segments are horizontal exactly along the parabola \\( y = t^{2} + 5 \\), have positive slope where \\( y > t^{2} + 5 \\), and have negative slope where \\( y < t^{2} + 5 \\).",
   ],
   "07002-09": [
      "The segments are horizontal exactly along the line \\( P = 0 \\), have positive slope where \\( P < 0 \\), and have negative slope where \\( P > 0 \\).",
      "The segments are horizontal exactly along the line \\( P = 3 t \\), have positive slope where \\( P < 3 t \\), and have negative slope where \\( P > 3 t \\).",
      "The segments are horizontal exactly along the line \\( P = 3 t \\), have positive slope where \\( P > 3 t \\), and have negative slope where \\( P < 3 t \\).",
      "The segments are horizontal exactly along the line \\( t = 3 P \\), have positive slope where \\( t < 3 P \\), and have negative slope where \\( t > 3 P \\).",
   ],
   "07002-10": [
      "The segments are horizontal exactly along the line \\( P = 0 \\), have positive slope where \\( P > 0 \\), and have negative slope where \\( P < 0 \\).",
      "The segments are horizontal exactly along the parabola \\( P = 2 t^{2} \\), have positive slope where \\( P < 2 t^{2} \\), and have negative slope where \\( P > 2 t^{2} \\).",
      "The segments are horizontal exactly along the parabola \\( P = 2 t^{2} \\), have positive slope where \\( P > 2 t^{2} \\), and have negative slope where \\( P < 2 t^{2} \\).",
      "The segments are horizontal exactly along the parabola \\( t = 2 P^{2} \\), have positive slope where \\( t > 2 P^{2} \\), and have negative slope where \\( t < 2 P^{2} \\).",
   ],
   "07002-11": [
      "The segments are horizontal exactly along the line \\( P = 2 \\), have positive slope where \\( P < 2 \\), and have negative slope where \\( P > 2 \\).",
      "The segments are horizontal exactly along the line \\( P = 2 t + 2 \\), have positive slope where \\( P < 2 t + 2 \\), and have negative slope where \\( P > 2 t + 2 \\).",
      "The segments are horizontal exactly along the line \\( P = 2 t + 2 \\), have positive slope where \\( P > 2 t + 2 \\), and have negative slope where \\( P < 2 t + 2 \\).",
      "The segments are horizontal exactly along the line \\( t = 2 P + 2 \\), have positive slope where \\( t < 2 P + 2 \\), and have negative slope where \\( t > 2 P + 2 \\).",
   ],
   "07002-12": [
      "The segments are horizontal exactly along the line \\( x = 2 y \\), have positive slope where \\( x > 2 y \\), and have negative slope where \\( x < 2 y \\).",
      "The segments are horizontal exactly along the line \\( y = 0 \\), have positive slope where \\( y > 0 \\), and have negative slope where \\( y < 0 \\).",
      "The segments are horizontal exactly along the line \\( y = 2 x \\), have positive slope where \\( y < 2 x \\), and have negative slope where \\( y > 2 x \\).",
      "The segments are horizontal exactly along the line \\( y = 2 x \\), have positive slope where \\( y > 2 x \\), and have negative slope where \\( y < 2 x \\).",
   ],
   "07002-13": [
      "The segments are horizontal exactly along the line \\( t = 2 - 3 y \\), have positive slope where \\( t < 2 - 3 y \\), and have negative slope where \\( t > 2 - 3 y \\).",
      "The segments are horizontal exactly along the line \\( y = 2 - 3 t \\), have positive slope where \\( y < 2 - 3 t \\), and have negative slope where \\( y > 2 - 3 t \\).",
      "The segments are horizontal exactly along the line \\( y = 2 - 3 t \\), have positive slope where \\( y > 2 - 3 t \\), and have negative slope where \\( y < 2 - 3 t \\).",
      "The segments are horizontal exactly along the line \\( y = 2 \\), have positive slope where \\( y < 2 \\), and have negative slope where \\( y > 2 \\).",
   ],
   "07002-14": [
      "The segments are horizontal exactly along the line \\( t = 4 - 2 y \\), have positive slope where \\( t > 4 - 2 y \\), and have negative slope where \\( t < 4 - 2 y \\).",
      "The segments are horizontal exactly along the line \\( y = 4 - 2 t \\), have positive slope where \\( y < 4 - 2 t \\), and have negative slope where \\( y > 4 - 2 t \\).",
      "The segments are horizontal exactly along the line \\( y = 4 - 2 t \\), have positive slope where \\( y > 4 - 2 t \\), and have negative slope where \\( y < 4 - 2 t \\).",
      "The segments are horizontal exactly along the line \\( y = 4 \\), have positive slope where \\( y > 4 \\), and have negative slope where \\( y < 4 \\).",
   ],
   "07002-15": [
      "The segments are horizontal exactly along the line \\( P = 1 \\), have positive slope where \\( P > 1 \\), and have negative slope where \\( P < 1 \\).",
      "The segments are horizontal exactly along the parabola \\( P = 1 - t^{2} \\), have positive slope where \\( P < 1 - t^{2} \\), and have negative slope where \\( P > 1 - t^{2} \\).",
      "The segments are horizontal exactly along the parabola \\( P = 1 - t^{2} \\), have positive slope where \\( P > 1 - t^{2} \\), and have negative slope where \\( P < 1 - t^{2} \\).",
      "The segments are horizontal exactly along the parabola \\( t = 1 - P^{2} \\), have positive slope where \\( t > 1 - P^{2} \\), and have negative slope where \\( t < 1 - P^{2} \\).",
   ],
   "07002-16": [
      "The segments are horizontal exactly along the line \\( y = -3 \\), have positive slope where \\( y > -3 \\), and have negative slope where \\( y < -3 \\).",
      "The segments are horizontal exactly along the parabola \\( t = y^{2} - 3 \\), have positive slope where \\( t > y^{2} - 3 \\), and have negative slope where \\( t < y^{2} - 3 \\).",
      "The segments are horizontal exactly along the parabola \\( y = t^{2} - 3 \\), have positive slope where \\( y < t^{2} - 3 \\), and have negative slope where \\( y > t^{2} - 3 \\).",
      "The segments are horizontal exactly along the parabola \\( y = t^{2} - 3 \\), have positive slope where \\( y > t^{2} - 3 \\), and have negative slope where \\( y < t^{2} - 3 \\).",
   ],
   "07002-17": [
      "The segments are horizontal exactly along the line \\( x = 2 y - 3 \\), have positive slope where \\( x > 2 y - 3 \\), and have negative slope where \\( x < 2 y - 3 \\).",
      "The segments are horizontal exactly along the line \\( y = -3 \\), have positive slope where \\( y > -3 \\), and have negative slope where \\( y < -3 \\).",
      "The segments are horizontal exactly along the line \\( y = 2 x - 3 \\), have positive slope where \\( y < 2 x - 3 \\), and have negative slope where \\( y > 2 x - 3 \\).",
      "The segments are horizontal exactly along the line \\( y = 2 x - 3 \\), have positive slope where \\( y > 2 x - 3 \\), and have negative slope where \\( y < 2 x - 3 \\).",
   ],
   "07002-18": [
      "The segments are horizontal exactly along the line \\( y = -1 \\), have positive slope where \\( y < -1 \\), and have negative slope where \\( y > -1 \\).",
      "The segments are horizontal exactly along the parabola \\( x = - 3 y^{2} - 1 \\), have positive slope where \\( x < - 3 y^{2} - 1 \\), and have negative slope where \\( x > - 3 y^{2} - 1 \\).",
      "The segments are horizontal exactly along the parabola \\( y = - 3 x^{2} - 1 \\), have positive slope where \\( y < - 3 x^{2} - 1 \\), and have negative slope where \\( y > - 3 x^{2} - 1 \\).",
      "The segments are horizontal exactly along the parabola \\( y = - 3 x^{2} - 1 \\), have positive slope where \\( y > - 3 x^{2} - 1 \\), and have negative slope where \\( y < - 3 x^{2} - 1 \\).",
   ],
   "07002-19": [
      "The segments are horizontal exactly along the line \\( x = 1 - y \\), have positive slope where \\( x > 1 - y \\), and have negative slope where \\( x < 1 - y \\).",
      "The segments are horizontal exactly along the line \\( y = 1 - x \\), have positive slope where \\( y < 1 - x \\), and have negative slope where \\( y > 1 - x \\).",
      "The segments are horizontal exactly along the line \\( y = 1 - x \\), have positive slope where \\( y > 1 - x \\), and have negative slope where \\( y < 1 - x \\).",
      "The segments are horizontal exactly along the line \\( y = 1 \\), have positive slope where \\( y > 1 \\), and have negative slope where \\( y < 1 \\).",
   ],
   "07002-20": [
      "The segments are horizontal exactly along the line \\( P = 3 t + 5 \\), have positive slope where \\( P < 3 t + 5 \\), and have negative slope where \\( P > 3 t + 5 \\).",
      "The segments are horizontal exactly along the line \\( P = 3 t + 5 \\), have positive slope where \\( P > 3 t + 5 \\), and have negative slope where \\( P < 3 t + 5 \\).",
      "The segments are horizontal exactly along the line \\( P = 5 \\), have positive slope where \\( P < 5 \\), and have negative slope where \\( P > 5 \\).",
      "The segments are horizontal exactly along the line \\( t = 3 P + 5 \\), have positive slope where \\( t < 3 P + 5 \\), and have negative slope where \\( t > 3 P + 5 \\).",
   ],
   "07002-21": [
      "The segments are horizontal exactly along the line \\( t = 2 y + 1 \\), have positive slope where \\( t > 2 y + 1 \\), and have negative slope where \\( t < 2 y + 1 \\).",
      "The segments are horizontal exactly along the line \\( y = 1 \\), have positive slope where \\( y > 1 \\), and have negative slope where \\( y < 1 \\).",
      "The segments are horizontal exactly along the line \\( y = 2 t + 1 \\), have positive slope where \\( y < 2 t + 1 \\), and have negative slope where \\( y > 2 t + 1 \\).",
      "The segments are horizontal exactly along the line \\( y = 2 t + 1 \\), have positive slope where \\( y > 2 t + 1 \\), and have negative slope where \\( y < 2 t + 1 \\).",
   ],
   "07005-00": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
   ],
   "07005-01": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
   ],
   "07005-02": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
   ],
   "07005-03": [
      "An overestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-04": [
      "An overestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-05": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-06": [
      "An overestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-07": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-08": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
   ],
   "07005-09": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
   ],
   "07005-10": [
      "An overestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-11": [
      "An overestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-12": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
   ],
   "07005-13": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-14": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
   ],
   "07005-15": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-16": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
   ],
   "07005-17": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is negative for all x in the interval, so f is decreasing there.",
   ],
   "07005-18": [
      "An overestimate, because the second derivative of f is negative at the starting point, so the graph of f is concave down at that point.",
      "An overestimate, because the second derivative of f is negative for all x in the interval, so the graph of f is concave down there.",
      "An underestimate, because a tangent line approximation follows the slope at the point of tangency, and that slope is too steep for the rest of the interval.",
      "An underestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
   ],
   "07005-19": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-20": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07005-21": [
      "An overestimate, because each Euler step follows the tangent line at the start of the step, and that slope is too steep for the rest of the interval.",
      "An overestimate, because the first derivative of f is positive for all x in the interval, so f is increasing there.",
      "An underestimate, because the second derivative of f is positive at the starting point, so the graph of f is concave up at that point.",
      "An underestimate, because the second derivative of f is positive for all x in the interval, so the graph of f is concave up there.",
   ],
   "07006-00": [
      "\\( \\frac{dC}{dt} = 45 - C \\), with \\( C(0) = 35 \\)",
      "\\( \\frac{dC}{dt} = k\\left(45 - 35\\right) \\), with \\( C(0) = 35 \\)",
      "\\( \\frac{dC}{dt} = k\\left(45 - C\\right) \\), with \\( C(0) = 35 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 45\\right) \\), with \\( C(0) = 35 \\)",
   ],
   "07006-01": [
      "\\( \\frac{dC}{dt} = 65 - C \\), with \\( C(0) = 125 \\)",
      "\\( \\frac{dC}{dt} = k\\left(65 - 125\\right) \\), with \\( C(0) = 125 \\)",
      "\\( \\frac{dC}{dt} = k\\left(65 - C\\right) \\), with \\( C(0) = 125 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 65\\right) \\), with \\( C(0) = 125 \\)",
   ],
   "07006-02": [
      "\\( \\frac{dH}{dt} = 55 - H \\), with \\( H(0) = 20 \\)",
      "\\( \\frac{dH}{dt} = k\\left(55 - 20\\right) \\), with \\( H(0) = 20 \\)",
      "\\( \\frac{dH}{dt} = k\\left(55 - H\\right) \\), with \\( H(0) = 20 \\)",
      "\\( \\frac{dH}{dt} = k\\left(H - 55\\right) \\), with \\( H(0) = 20 \\)",
   ],
   "07006-03": [
      "\\( \\frac{dT}{dt} = 55 - T \\), with \\( T(0) = 45 \\)",
      "\\( \\frac{dT}{dt} = k\\left(55 - 45\\right) \\), with \\( T(0) = 45 \\)",
      "\\( \\frac{dT}{dt} = k\\left(55 - T\\right) \\), with \\( T(0) = 45 \\)",
      "\\( \\frac{dT}{dt} = k\\left(T - 55\\right) \\), with \\( T(0) = 45 \\)",
   ],
   "07006-04": [
      "\\( \\frac{dP}{dt} = 40 - P \\), with \\( P(0) = 20 \\)",
      "\\( \\frac{dP}{dt} = k\\left(40 - 20\\right) \\), with \\( P(0) = 20 \\)",
      "\\( \\frac{dP}{dt} = k\\left(40 - P\\right) \\), with \\( P(0) = 20 \\)",
      "\\( \\frac{dP}{dt} = k\\left(P - 40\\right) \\), with \\( P(0) = 20 \\)",
   ],
   "07006-05": [
      "\\( \\frac{dT}{dt} = 60 - T \\), with \\( T(0) = 5 \\)",
      "\\( \\frac{dT}{dt} = k\\left(60 - 5\\right) \\), with \\( T(0) = 5 \\)",
      "\\( \\frac{dT}{dt} = k\\left(60 - T\\right) \\), with \\( T(0) = 5 \\)",
      "\\( \\frac{dT}{dt} = k\\left(T - 60\\right) \\), with \\( T(0) = 5 \\)",
   ],
   "07006-06": [
      "\\( \\frac{dP}{dt} = 55 - P \\), with \\( P(0) = 40 \\)",
      "\\( \\frac{dP}{dt} = k\\left(55 - 40\\right) \\), with \\( P(0) = 40 \\)",
      "\\( \\frac{dP}{dt} = k\\left(55 - P\\right) \\), with \\( P(0) = 40 \\)",
      "\\( \\frac{dP}{dt} = k\\left(P - 55\\right) \\), with \\( P(0) = 40 \\)",
   ],
   "07006-07": [
      "\\( \\frac{dC}{dt} = 90 - C \\), with \\( C(0) = 50 \\)",
      "\\( \\frac{dC}{dt} = k\\left(90 - 50\\right) \\), with \\( C(0) = 50 \\)",
      "\\( \\frac{dC}{dt} = k\\left(90 - C\\right) \\), with \\( C(0) = 50 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 90\\right) \\), with \\( C(0) = 50 \\)",
   ],
   "07006-08": [
      "\\( \\frac{dP}{dt} = 60 - P \\), with \\( P(0) = 80 \\)",
      "\\( \\frac{dP}{dt} = k\\left(60 - 80\\right) \\), with \\( P(0) = 80 \\)",
      "\\( \\frac{dP}{dt} = k\\left(60 - P\\right) \\), with \\( P(0) = 80 \\)",
      "\\( \\frac{dP}{dt} = k\\left(P - 60\\right) \\), with \\( P(0) = 80 \\)",
   ],
   "07006-09": [
      "\\( \\frac{dP}{dt} = 25 - P \\), with \\( P(0) = 20 \\)",
      "\\( \\frac{dP}{dt} = k\\left(25 - 20\\right) \\), with \\( P(0) = 20 \\)",
      "\\( \\frac{dP}{dt} = k\\left(25 - P\\right) \\), with \\( P(0) = 20 \\)",
      "\\( \\frac{dP}{dt} = k\\left(P - 25\\right) \\), with \\( P(0) = 20 \\)",
   ],
   "07006-10": [
      "\\( \\frac{dC}{dt} = 75 - C \\), with \\( C(0) = 65 \\)",
      "\\( \\frac{dC}{dt} = k\\left(75 - 65\\right) \\), with \\( C(0) = 65 \\)",
      "\\( \\frac{dC}{dt} = k\\left(75 - C\\right) \\), with \\( C(0) = 65 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 75\\right) \\), with \\( C(0) = 65 \\)",
   ],
   "07006-11": [
      "\\( \\frac{dH}{dt} = 95 - H \\), with \\( H(0) = 60 \\)",
      "\\( \\frac{dH}{dt} = k\\left(95 - 60\\right) \\), with \\( H(0) = 60 \\)",
      "\\( \\frac{dH}{dt} = k\\left(95 - H\\right) \\), with \\( H(0) = 60 \\)",
      "\\( \\frac{dH}{dt} = k\\left(H - 95\\right) \\), with \\( H(0) = 60 \\)",
   ],
   "07006-12": [
      "\\( \\frac{dH}{dt} = 25 - H \\), with \\( H(0) = 5 \\)",
      "\\( \\frac{dH}{dt} = k\\left(25 - 5\\right) \\), with \\( H(0) = 5 \\)",
      "\\( \\frac{dH}{dt} = k\\left(25 - H\\right) \\), with \\( H(0) = 5 \\)",
      "\\( \\frac{dH}{dt} = k\\left(H - 25\\right) \\), with \\( H(0) = 5 \\)",
   ],
   "07006-13": [
      "\\( \\frac{dT}{dt} = 95 - T \\), with \\( T(0) = 145 \\)",
      "\\( \\frac{dT}{dt} = k\\left(95 - 145\\right) \\), with \\( T(0) = 145 \\)",
      "\\( \\frac{dT}{dt} = k\\left(95 - T\\right) \\), with \\( T(0) = 145 \\)",
      "\\( \\frac{dT}{dt} = k\\left(T - 95\\right) \\), with \\( T(0) = 145 \\)",
   ],
   "07006-14": [
      "\\( \\frac{dH}{dt} = 55 - H \\), with \\( H(0) = 80 \\)",
      "\\( \\frac{dH}{dt} = k\\left(55 - 80\\right) \\), with \\( H(0) = 80 \\)",
      "\\( \\frac{dH}{dt} = k\\left(55 - H\\right) \\), with \\( H(0) = 80 \\)",
      "\\( \\frac{dH}{dt} = k\\left(H - 55\\right) \\), with \\( H(0) = 80 \\)",
   ],
   "07006-15": [
      "\\( \\frac{dC}{dt} = 70 - C \\), with \\( C(0) = 15 \\)",
      "\\( \\frac{dC}{dt} = k\\left(70 - 15\\right) \\), with \\( C(0) = 15 \\)",
      "\\( \\frac{dC}{dt} = k\\left(70 - C\\right) \\), with \\( C(0) = 15 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 70\\right) \\), with \\( C(0) = 15 \\)",
   ],
   "07006-16": [
      "\\( \\frac{dT}{dt} = 95 - T \\), with \\( T(0) = 130 \\)",
      "\\( \\frac{dT}{dt} = k\\left(95 - 130\\right) \\), with \\( T(0) = 130 \\)",
      "\\( \\frac{dT}{dt} = k\\left(95 - T\\right) \\), with \\( T(0) = 130 \\)",
      "\\( \\frac{dT}{dt} = k\\left(T - 95\\right) \\), with \\( T(0) = 130 \\)",
   ],
   "07006-17": [
      "\\( \\frac{dH}{dt} = 90 - H \\), with \\( H(0) = 140 \\)",
      "\\( \\frac{dH}{dt} = k\\left(90 - 140\\right) \\), with \\( H(0) = 140 \\)",
      "\\( \\frac{dH}{dt} = k\\left(90 - H\\right) \\), with \\( H(0) = 140 \\)",
      "\\( \\frac{dH}{dt} = k\\left(H - 90\\right) \\), with \\( H(0) = 140 \\)",
   ],
   "07006-18": [
      "\\( \\frac{dC}{dt} = 80 - C \\), with \\( C(0) = 125 \\)",
      "\\( \\frac{dC}{dt} = k\\left(80 - 125\\right) \\), with \\( C(0) = 125 \\)",
      "\\( \\frac{dC}{dt} = k\\left(80 - C\\right) \\), with \\( C(0) = 125 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 80\\right) \\), with \\( C(0) = 125 \\)",
   ],
   "07006-19": [
      "\\( \\frac{dC}{dt} = 95 - C \\), with \\( C(0) = 35 \\)",
      "\\( \\frac{dC}{dt} = k\\left(95 - 35\\right) \\), with \\( C(0) = 35 \\)",
      "\\( \\frac{dC}{dt} = k\\left(95 - C\\right) \\), with \\( C(0) = 35 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 95\\right) \\), with \\( C(0) = 35 \\)",
   ],
   "07006-20": [
      "\\( \\frac{dC}{dt} = 90 - C \\), with \\( C(0) = 50 \\)",
      "\\( \\frac{dC}{dt} = k\\left(90 - 50\\right) \\), with \\( C(0) = 50 \\)",
      "\\( \\frac{dC}{dt} = k\\left(90 - C\\right) \\), with \\( C(0) = 50 \\)",
      "\\( \\frac{dC}{dt} = k\\left(C - 90\\right) \\), with \\( C(0) = 50 \\)",
   ],
   "07006-21": [
      "\\( \\frac{dT}{dt} = 75 - T \\), with \\( T(0) = 55 \\)",
      "\\( \\frac{dT}{dt} = k\\left(75 - 55\\right) \\), with \\( T(0) = 55 \\)",
      "\\( \\frac{dT}{dt} = k\\left(75 - T\\right) \\), with \\( T(0) = 55 \\)",
      "\\( \\frac{dT}{dt} = k\\left(T - 75\\right) \\), with \\( T(0) = 55 \\)",
   ],
   "07007-00": [
      "No. Substituting f(x) for y on both sides gives \\( 4 e^{2 x} - 2 \\) on the left and \\( 8 e^{2 x} \\) on the right, which are not equal.",
      "No. \\( f^{\\prime}(x) = 2\\left(f(x) + 2\\right) \\) for every x, but \\( f(0) = 2 \\), not 3.",
      "No. \\( f^{\\prime}(x) \\ne 2\\left(f(x) + 2\\right) \\) for the candidate, so f is not a solution of the equation.",
      "Yes. \\( f^{\\prime}(x) = 2\\left(f(x) + 2\\right) \\) for every x, so f is the particular solution.",
   ],
   "07007-01": [
      "No. Substituting f(x) for y on both sides gives \\( 2 - 3 e^{2 x} \\) on the left and \\( - 6 e^{2 x} \\) on the right, which are not equal.",
      "No. \\( f^{\\prime}(x) = 2\\left(f(x) - 2\\right) \\) for every x, but \\( f(0) = -1 \\), not -2.",
      "No. \\( f^{\\prime}(x) \\ne 2\\left(f(x) - 2\\right) \\) for the candidate, so f is not a solution of the equation.",
      "Yes. \\( f^{\\prime}(x) = 2\\left(f(x) - 2\\right) \\) for every x, so f is the particular solution.",
   ],
   "07007-02": [
      "No. Substituting f(x) for y on both sides gives \\( -4 + 4 e^{- 2 x} \\) on the left and \\( - 8 e^{- 2 x} \\) on the right, which are not equal.",
      "No. \\( f^{\\prime}(x) \\ne -2\\left(f(x) + 4\\right) \\) for the candidate, so f is not a solution of the equation.",
      "Yes. \\( f^{\\prime}(x) = -2\\left(f(x) + 4\\right) \\) for every x, and \\( f(0) = 0 \\).",
      "Yes. \\( f^{\\prime}(x) = -2\\left(f(x) + 4\\right) \\) for every x, so f is the only solution of the equation.",
   ],
   "07007-03": [
      "No. Substituting f(x) for y on both sides gives \\( -1 + e^{- x} \\) on the left and \\( - e^{- x} \\) on the right, which are not equal.",
      "No. \\( f^{\\prime}(x) \\ne -\\left(f(x) + 1\\right) \\) for the candidate, so f is not a solution of the equation.",
      "Yes. \\( f^{\\prime}(x) = -\\left(f(x) + 1\\right) \\) for every x, and \\( f(0) = 0 \\).",
      "Yes. \\( f^{\\prime}(x) = -\\left(f(x) + 1\\right) \\) for every x, so f is the only solution of the equation.",
   ],
   "07009-00": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 650 \\) fish.",
      "P approaches \\( 1300 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1300 \\) fish.",
      "P approaches \\( 1300 \\) fish as t increases without bound, and P is growing fastest when \\( P = 650 \\) fish.",
      "P approaches \\( 260 \\) fish as t increases without bound, and P is growing fastest when \\( P = 650 \\) fish.",
   ],
   "07009-01": [
      "P approaches \\( 0 \\) people as t increases without bound, and P is growing fastest when \\( P = 100 \\) people.",
      "P approaches \\( 200 \\) people as t increases without bound, and P is growing fastest when \\( P = 100 \\) people.",
      "P approaches \\( 200 \\) people as t increases without bound, and P is growing fastest when \\( P = 200 \\) people.",
      "P approaches \\( 40 \\) people as t increases without bound, and P is growing fastest when \\( P = 100 \\) people.",
   ],
   "07009-02": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 850 \\) fish.",
      "P approaches \\( 170 \\) fish as t increases without bound, and P is growing fastest when \\( P = 850 \\) fish.",
      "P approaches \\( 1700 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1700 \\) fish.",
      "P approaches \\( 1700 \\) fish as t increases without bound, and P is growing fastest when \\( P = 850 \\) fish.",
   ],
   "07009-03": [
      "P approaches \\( 0 \\) people as t increases without bound, and P is growing fastest when \\( P = 900 \\) people.",
      "P approaches \\( 1800 \\) people as t increases without bound, and P is growing fastest when \\( P = 1800 \\) people.",
      "P approaches \\( 1800 \\) people as t increases without bound, and P is growing fastest when \\( P = 900 \\) people.",
      "P approaches \\( 360 \\) people as t increases without bound, and P is growing fastest when \\( P = 900 \\) people.",
   ],
   "07009-04": [
      "P approaches \\( 0 \\) people as t increases without bound, and P is growing fastest when \\( P = 100 \\) people.",
      "P approaches \\( 200 \\) people as t increases without bound, and P is growing fastest when \\( P = 100 \\) people.",
      "P approaches \\( 200 \\) people as t increases without bound, and P is growing fastest when \\( P = 200 \\) people.",
      "P approaches \\( 60 \\) people as t increases without bound, and P is growing fastest when \\( P = 100 \\) people.",
   ],
   "07009-05": [
      "P approaches \\( 0 \\) people as t increases without bound, and P is growing fastest when \\( P = 900 \\) people.",
      "P approaches \\( 1800 \\) people as t increases without bound, and P is growing fastest when \\( P = 1800 \\) people.",
      "P approaches \\( 1800 \\) people as t increases without bound, and P is growing fastest when \\( P = 900 \\) people.",
      "P approaches \\( 360 \\) people as t increases without bound, and P is growing fastest when \\( P = 900 \\) people.",
   ],
   "07009-06": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 550 \\) fish.",
      "P approaches \\( 1100 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1100 \\) fish.",
      "P approaches \\( 1100 \\) fish as t increases without bound, and P is growing fastest when \\( P = 550 \\) fish.",
      "P approaches \\( 220 \\) fish as t increases without bound, and P is growing fastest when \\( P = 550 \\) fish.",
   ],
   "07009-07": [
      "P approaches \\( 0 \\) people as t increases without bound, and P is growing fastest when \\( P = 1000 \\) people.",
      "P approaches \\( 200 \\) people as t increases without bound, and P is growing fastest when \\( P = 1000 \\) people.",
      "P approaches \\( 2000 \\) people as t increases without bound, and P is growing fastest when \\( P = 1000 \\) people.",
      "P approaches \\( 2000 \\) people as t increases without bound, and P is growing fastest when \\( P = 2000 \\) people.",
   ],
   "07009-08": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 700 \\) fish.",
      "P approaches \\( 1400 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1400 \\) fish.",
      "P approaches \\( 1400 \\) fish as t increases without bound, and P is growing fastest when \\( P = 700 \\) fish.",
      "P approaches \\( 560 \\) fish as t increases without bound, and P is growing fastest when \\( P = 700 \\) fish.",
   ],
   "07009-09": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 250 \\) fish.",
      "P approaches \\( 100 \\) fish as t increases without bound, and P is growing fastest when \\( P = 250 \\) fish.",
      "P approaches \\( 500 \\) fish as t increases without bound, and P is growing fastest when \\( P = 250 \\) fish.",
      "P approaches \\( 500 \\) fish as t increases without bound, and P is growing fastest when \\( P = 500 \\) fish.",
   ],
   "07009-10": [
      "P approaches \\( 0 \\) deer as t increases without bound, and P is growing fastest when \\( P = 350 \\) deer.",
      "P approaches \\( 210 \\) deer as t increases without bound, and P is growing fastest when \\( P = 350 \\) deer.",
      "P approaches \\( 700 \\) deer as t increases without bound, and P is growing fastest when \\( P = 350 \\) deer.",
      "P approaches \\( 700 \\) deer as t increases without bound, and P is growing fastest when \\( P = 700 \\) deer.",
   ],
   "07009-11": [
      "P approaches \\( 0 \\) deer as t increases without bound, and P is growing fastest when \\( P = 250 \\) deer.",
      "P approaches \\( 200 \\) deer as t increases without bound, and P is growing fastest when \\( P = 250 \\) deer.",
      "P approaches \\( 500 \\) deer as t increases without bound, and P is growing fastest when \\( P = 250 \\) deer.",
      "P approaches \\( 500 \\) deer as t increases without bound, and P is growing fastest when \\( P = 500 \\) deer.",
   ],
   "07009-12": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 350 \\) fish.",
      "P approaches \\( 280 \\) fish as t increases without bound, and P is growing fastest when \\( P = 350 \\) fish.",
      "P approaches \\( 700 \\) fish as t increases without bound, and P is growing fastest when \\( P = 350 \\) fish.",
      "P approaches \\( 700 \\) fish as t increases without bound, and P is growing fastest when \\( P = 700 \\) fish.",
   ],
   "07009-13": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 850 \\) fish.",
      "P approaches \\( 1700 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1700 \\) fish.",
      "P approaches \\( 1700 \\) fish as t increases without bound, and P is growing fastest when \\( P = 850 \\) fish.",
      "P approaches \\( 340 \\) fish as t increases without bound, and P is growing fastest when \\( P = 850 \\) fish.",
   ],
   "07009-14": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 450 \\) fish.",
      "P approaches \\( 270 \\) fish as t increases without bound, and P is growing fastest when \\( P = 450 \\) fish.",
      "P approaches \\( 900 \\) fish as t increases without bound, and P is growing fastest when \\( P = 450 \\) fish.",
      "P approaches \\( 900 \\) fish as t increases without bound, and P is growing fastest when \\( P = 900 \\) fish.",
   ],
   "07009-15": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 400 \\) fish.",
      "P approaches \\( 80 \\) fish as t increases without bound, and P is growing fastest when \\( P = 400 \\) fish.",
      "P approaches \\( 800 \\) fish as t increases without bound, and P is growing fastest when \\( P = 400 \\) fish.",
      "P approaches \\( 800 \\) fish as t increases without bound, and P is growing fastest when \\( P = 800 \\) fish.",
   ],
   "07009-16": [
      "P approaches \\( 0 \\) deer as t increases without bound, and P is growing fastest when \\( P = 550 \\) deer.",
      "P approaches \\( 1100 \\) deer as t increases without bound, and P is growing fastest when \\( P = 1100 \\) deer.",
      "P approaches \\( 1100 \\) deer as t increases without bound, and P is growing fastest when \\( P = 550 \\) deer.",
      "P approaches \\( 220 \\) deer as t increases without bound, and P is growing fastest when \\( P = 550 \\) deer.",
   ],
   "07009-17": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 250 \\) fish.",
      "P approaches \\( 100 \\) fish as t increases without bound, and P is growing fastest when \\( P = 250 \\) fish.",
      "P approaches \\( 500 \\) fish as t increases without bound, and P is growing fastest when \\( P = 250 \\) fish.",
      "P approaches \\( 500 \\) fish as t increases without bound, and P is growing fastest when \\( P = 500 \\) fish.",
   ],
   "07009-18": [
      "P approaches \\( 0 \\) deer as t increases without bound, and P is growing fastest when \\( P = 150 \\) deer.",
      "P approaches \\( 300 \\) deer as t increases without bound, and P is growing fastest when \\( P = 150 \\) deer.",
      "P approaches \\( 300 \\) deer as t increases without bound, and P is growing fastest when \\( P = 300 \\) deer.",
      "P approaches \\( 75 \\) deer as t increases without bound, and P is growing fastest when \\( P = 150 \\) deer.",
   ],
   "07009-19": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 500 \\) fish.",
      "P approaches \\( 1000 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1000 \\) fish.",
      "P approaches \\( 1000 \\) fish as t increases without bound, and P is growing fastest when \\( P = 500 \\) fish.",
      "P approaches \\( 300 \\) fish as t increases without bound, and P is growing fastest when \\( P = 500 \\) fish.",
   ],
   "07009-20": [
      "P approaches \\( 0 \\) people as t increases without bound, and P is growing fastest when \\( P = 950 \\) people.",
      "P approaches \\( 1900 \\) people as t increases without bound, and P is growing fastest when \\( P = 1900 \\) people.",
      "P approaches \\( 1900 \\) people as t increases without bound, and P is growing fastest when \\( P = 950 \\) people.",
      "P approaches \\( 475 \\) people as t increases without bound, and P is growing fastest when \\( P = 950 \\) people.",
   ],
   "07009-21": [
      "P approaches \\( 0 \\) fish as t increases without bound, and P is growing fastest when \\( P = 800 \\) fish.",
      "P approaches \\( 1600 \\) fish as t increases without bound, and P is growing fastest when \\( P = 1600 \\) fish.",
      "P approaches \\( 1600 \\) fish as t increases without bound, and P is growing fastest when \\( P = 800 \\) fish.",
      "P approaches \\( 400 \\) fish as t increases without bound, and P is growing fastest when \\( P = 800 \\) fish.",
   ],
   "07010-00": [
      "The solution has a relative maximum at \\( x = 1 \\) and a relative minimum at \\( x = -1 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( x = 1 \\), because the derivative changes from positive to negative at \\( x = 1 \\).",
      "The solution has a relative minimum at \\( x = 1 \\), because the derivative changes from positive to negative at \\( x = 1 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y - 3 \\) is never 0 when \\( y < 3 \\).",
   ],
   "07010-01": [
      "The solution has a relative maximum at \\( x = 3 \\), because the derivative changes from negative to positive at \\( x = 3 \\).",
      "The solution has a relative minimum at \\( x = 3 \\) and a relative maximum at \\( x = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( x = 3 \\), because the derivative changes from negative to positive at \\( x = 3 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y \\) is never 0 when \\( y > 0 \\).",
   ],
   "07010-02": [
      "The solution has a relative maximum at \\( x = 2 \\), because the derivative changes from negative to positive at \\( x = 2 \\).",
      "The solution has a relative minimum at \\( x = 2 \\) and a relative maximum at \\( x = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( x = 2 \\), because the derivative changes from negative to positive at \\( x = 2 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y - 2 \\) is never 0 when \\( y > 2 \\).",
   ],
   "07010-03": [
      "The solution has a relative maximum at \\( x = 3 \\) and a relative minimum at \\( x = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( x = 3 \\), because the derivative changes from positive to negative at \\( x = 3 \\).",
      "The solution has a relative minimum at \\( x = 3 \\), because the derivative changes from positive to negative at \\( x = 3 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y + 3 \\) is never 0 when \\( y > -3 \\).",
   ],
   "07010-04": [
      "The solution has a relative maximum at \\( t = 5 \\) and a relative minimum at \\( t = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( t = 5 \\), because the derivative changes from positive to negative at \\( t = 5 \\).",
      "The solution has a relative minimum at \\( t = 5 \\), because the derivative changes from positive to negative at \\( t = 5 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y - 2 \\) is never 0 when \\( y < 2 \\).",
   ],
   "07010-05": [
      "The solution has a relative maximum at \\( t = 2 \\) and a relative minimum at \\( t = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( t = 2 \\), because the derivative changes from positive to negative at \\( t = 2 \\).",
      "The solution has a relative minimum at \\( t = 2 \\), because the derivative changes from positive to negative at \\( t = 2 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y - 3 \\) is never 0 when \\( y < 3 \\).",
   ],
   "07010-06": [
      "The solution has a relative maximum at \\( t = 1 \\), because the derivative changes from negative to positive at \\( t = 1 \\).",
      "The solution has a relative minimum at \\( t = 1 \\) and a relative maximum at \\( t = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 1 \\), because the derivative changes from negative to positive at \\( t = 1 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( P + 3 \\) is never 0 when \\( P < -3 \\).",
   ],
   "07010-07": [
      "The solution has a relative maximum at \\( x = 4 \\), because the derivative changes from negative to positive at \\( x = 4 \\).",
      "The solution has a relative minimum at \\( x = 4 \\) and a relative maximum at \\( x = -4 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( x = 4 \\), because the derivative changes from negative to positive at \\( x = 4 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y > -1 \\).",
   ],
   "07010-08": [
      "The solution has a relative maximum at \\( x = 1 \\) and a relative minimum at \\( x = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( x = 1 \\), because the derivative changes from positive to negative at \\( x = 1 \\).",
      "The solution has a relative minimum at \\( x = 1 \\), because the derivative changes from positive to negative at \\( x = 1 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y < -1 \\).",
   ],
   "07010-09": [
      "The solution has a relative maximum at \\( t = 5 \\), because the derivative changes from negative to positive at \\( t = 5 \\).",
      "The solution has a relative minimum at \\( t = 5 \\) and a relative maximum at \\( t = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 5 \\), because the derivative changes from negative to positive at \\( t = 5 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y < -1 \\).",
   ],
   "07010-10": [
      "The solution has a relative maximum at \\( t = 2 \\), because the derivative changes from negative to positive at \\( t = 2 \\).",
      "The solution has a relative minimum at \\( t = 2 \\) and a relative maximum at \\( t = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 2 \\), because the derivative changes from negative to positive at \\( t = 2 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( P + 2 \\) is never 0 when \\( P < -2 \\).",
   ],
   "07010-11": [
      "The solution has a relative maximum at \\( t = 4 \\), because the derivative changes from negative to positive at \\( t = 4 \\).",
      "The solution has a relative minimum at \\( t = 4 \\) and a relative maximum at \\( t = -1 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 4 \\), because the derivative changes from negative to positive at \\( t = 4 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y \\) is never 0 when \\( y > 0 \\).",
   ],
   "07010-12": [
      "The solution has a relative maximum at \\( t = 5 \\), because the derivative changes from negative to positive at \\( t = 5 \\).",
      "The solution has a relative minimum at \\( t = 5 \\) and a relative maximum at \\( t = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 5 \\), because the derivative changes from negative to positive at \\( t = 5 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y > -1 \\).",
   ],
   "07010-13": [
      "The solution has a relative maximum at \\( x = 1 \\), because the derivative changes from negative to positive at \\( x = 1 \\).",
      "The solution has a relative minimum at \\( x = 1 \\) and a relative maximum at \\( x = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( x = 1 \\), because the derivative changes from negative to positive at \\( x = 1 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y > -1 \\).",
   ],
   "07010-14": [
      "The solution has a relative maximum at \\( t = 4 \\) and a relative minimum at \\( t = -4 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( t = 4 \\), because the derivative changes from positive to negative at \\( t = 4 \\).",
      "The solution has a relative minimum at \\( t = 4 \\), because the derivative changes from positive to negative at \\( t = 4 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y < -1 \\).",
   ],
   "07010-15": [
      "The solution has a relative maximum at \\( t = 5 \\), because the derivative changes from negative to positive at \\( t = 5 \\).",
      "The solution has a relative minimum at \\( t = 5 \\) and a relative maximum at \\( t = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 5 \\), because the derivative changes from negative to positive at \\( t = 5 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 1 \\) is never 0 when \\( y > -1 \\).",
   ],
   "07010-16": [
      "The solution has a relative maximum at \\( t = 4 \\), because the derivative changes from negative to positive at \\( t = 4 \\).",
      "The solution has a relative minimum at \\( t = 4 \\) and a relative maximum at \\( t = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 4 \\), because the derivative changes from negative to positive at \\( t = 4 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 3 \\) is never 0 when \\( y > -3 \\).",
   ],
   "07010-17": [
      "The solution has a relative maximum at \\( t = 1 \\), because the derivative changes from negative to positive at \\( t = 1 \\).",
      "The solution has a relative minimum at \\( t = 1 \\) and a relative maximum at \\( t = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 1 \\), because the derivative changes from negative to positive at \\( t = 1 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 3 \\) is never 0 when \\( y > -3 \\).",
   ],
   "07010-18": [
      "The solution has a relative maximum at \\( t = 1 \\) and a relative minimum at \\( t = -3 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( t = 1 \\), because the derivative changes from positive to negative at \\( t = 1 \\).",
      "The solution has a relative minimum at \\( t = 1 \\), because the derivative changes from positive to negative at \\( t = 1 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 3 \\) is never 0 when \\( y > -3 \\).",
   ],
   "07010-19": [
      "The solution has a relative maximum at \\( t = 4 \\) and a relative minimum at \\( t = -1 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( t = 4 \\), because the derivative changes from positive to negative at \\( t = 4 \\).",
      "The solution has a relative minimum at \\( t = 4 \\), because the derivative changes from positive to negative at \\( t = 4 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( y + 3 \\) is never 0 when \\( y < -3 \\).",
   ],
   "07010-20": [
      "The solution has a relative maximum at \\( x = 1 \\) and a relative minimum at \\( x = -1 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative maximum at \\( x = 1 \\), because the derivative changes from positive to negative at \\( x = 1 \\).",
      "The solution has a relative minimum at \\( x = 1 \\), because the derivative changes from positive to negative at \\( x = 1 \\).",
      "The solution has no critical point for \\( x > 0 \\), because the factor \\( y - 1 \\) is never 0 when \\( y < 1 \\).",
   ],
   "07010-21": [
      "The solution has a relative maximum at \\( t = 2 \\), because the derivative changes from negative to positive at \\( t = 2 \\).",
      "The solution has a relative minimum at \\( t = 2 \\) and a relative maximum at \\( t = -2 \\), because the derivative changes sign at both inputs.",
      "The solution has a relative minimum at \\( t = 2 \\), because the derivative changes from negative to positive at \\( t = 2 \\).",
      "The solution has no critical point for \\( t > 0 \\), because the factor \\( P - 1 \\) is never 0 when \\( P > 1 \\).",
   ],
   "07011-00": [
      "\\( y = -1 + \\int_{3}^{x} \\sqrt{t^{4} + 1} \\)",
      "\\( y = -1 + \\int_{3}^{x} \\sqrt{t^{4} + 1}\\,dt \\)",
      "\\( y = \\int_{3}^{x} \\sqrt{t^{4} + 1}\\,dt \\)",
      "\\( y = \\sqrt{x^{4} + 1} - \\sqrt{82} - 1 \\)",
   ],
   "07011-01": [
      "\\( y = -1 + \\int_{1}^{x} \\sin{\\left(t^{2} \\right)} \\)",
      "\\( y = -1 + \\int_{1}^{x} \\sin{\\left(t^{2} \\right)}\\,dt \\)",
      "\\( y = \\int_{1}^{x} \\sin{\\left(t^{2} \\right)}\\,dt \\)",
      "\\( y = \\sin{\\left(x^{2} \\right)} - 1 - \\sin{\\left(1 \\right)} \\)",
   ],
   "07011-02": [
      "\\( y = - \\frac{1}{2} + \\int_{0}^{x} \\cos{\\left(t^{2} \\right)} \\)",
      "\\( y = - \\frac{1}{2} + \\int_{0}^{x} \\cos{\\left(t^{2} \\right)}\\,dt \\)",
      "\\( y = \\cos{\\left(x^{2} \\right)} - \\frac{3}{2} \\)",
      "\\( y = \\int_{0}^{x} \\cos{\\left(t^{2} \\right)}\\,dt \\)",
   ],
   "07011-03": [
      "\\( y = 3 + \\int_{2}^{x} \\sqrt{t^{4} + 1} \\)",
      "\\( y = 3 + \\int_{2}^{x} \\sqrt{t^{4} + 1}\\,dt \\)",
      "\\( y = \\int_{2}^{x} \\sqrt{t^{4} + 1}\\,dt \\)",
      "\\( y = \\sqrt{x^{4} + 1} - \\sqrt{17} + 3 \\)",
   ],
   "07011-04": [
      "\\( y = - \\frac{1}{x - 1} \\), for \\( x < 1 \\)",
      "\\( y = \\frac{1}{x + 1} \\), for \\( x < -1 \\)",
      "\\( y = \\frac{1}{x + 1} \\), for \\( x > -1 \\)",
      "\\( y = \\frac{1}{x + 1} \\), for all \\( x \\ne -1 \\)",
   ],
}

PARSE_TRANSFORMATIONS = standard_transformations + (implicit_multiplication, convert_xor)
PARSE_NAMES = {
   "x": x, "y": y, "t": t, "P": P, "C": C, "H": H, "T": T, "k": k,
   "e": E, "sqrt": sqrt, "sin": sin, "cos": cos, "oo": oo,
}
CONCAVITY_SAMPLE_COUNT = 9
REGION_SAMPLE_DEPTHS = [Rational(1, 100), Rational(1, 2), 1, 3, 10, 50]


def braced_argument(text, open_index):
   depth = 0

   for index in range(open_index, len(text)):
      if text[index] == "{":
         depth += 1
      elif text[index] == "}":
         depth -= 1

         if depth == 0:
            return text[open_index + 1:index], index + 1

   raise ValueError(f"unbalanced braces in {text}")


def rewrite_command(text, command, arity, template):
   while command in text:
      start = text.index(command)
      cursor = start + len(command)
      arguments = []

      for _ in range(arity):
         argument, cursor = braced_argument(text, cursor)
         arguments.append(argument)

      text = text[:start] + template.format(*arguments) + text[cursor:]

   return text


def latex_to_sympy(latex):
   text = latex.replace("\\left", "").replace("\\right", "").replace("\\,", " ")
   text = text.replace("\\cdot", "*").replace("\\infty", "oo")
   text = rewrite_command(text, "\\frac", 2, "(({0})/({1}))")
   text = rewrite_command(text, "\\sqrt", 1, "sqrt({0})")
   text = rewrite_command(text, "\\sin", 1, "sin({0})")
   text = rewrite_command(text, "\\cos", 1, "cos({0})")
   text = rewrite_command(text, "^", 1, "**({0})")

   return parse_expr(text, local_dict=PARSE_NAMES, transformations=PARSE_TRANSFORMATIONS)


def same_expression(left, right):
   return sympy.simplify(sympy.sympify(left) - sympy.sympify(right)) == 0


def only_choice(matching):
   if len(matching) == 1:
      return matching[0]

   return matching


def choices_of(suffix):
   return CHOICES_BY_SUFFIX[suffix]


def autonomous_solution_curve(suffix, rate, dependent, independent_name, start_value):
   """dD/d(independent) = rate(D), linear in D, through a point off the equilibrium: the curve
   moves monotonically toward the equilibrium as the input runs in the direction where it is
   attracting, and never reaches it by uniqueness."""
   equilibrium = sympy.solve(rate, dependent)[0]
   growth = sympy.diff(rate, dependent)
   start_value = sympy.nsimplify(start_value)
   rate_at_start = rate.subs(dependent, start_value)
   motion = "rises" if rate_at_start > 0 else "falls"
   side = "from above" if start_value > equilibrium else "from below"
   direction = f"as {independent_name} increases" if growth < 0 else f"as {independent_name} decreases"
   line_text = f"line \\( {dependent} = {equilibrium} \\)"
   wanted = [
      choice for choice in choices_of(suffix)
      if f"{motion} across the whole window" in choice
      and f"flattening toward the {line_text} {side} {direction}" in choice
      and "never touches" in choice
   ]

   return only_choice(wanted)


SLOPE_REGION = re.compile(
   r"horizontal exactly along the (line|parabola) \\\( (\w) = (.+?) \\\), have positive slope where \\\( (\w) ([<>]) (.+?) \\\), "
   r"and have negative slope where \\\( (\w) ([<>]) (.+?) \\\)"
)


def slope_field_regions(suffix, rate, dependent, independent):
   """Horizontal where the rate is 0; the rate is linear in the dependent variable, so its sign
   above that curve is the sign of the coefficient of the dependent variable."""
   zero_curve = sympy.solve(rate, dependent)[0]
   coefficient = sympy.diff(rate, dependent)
   positive_side = ">" if coefficient > 0 else "<"
   negative_side = "<" if coefficient > 0 else ">"
   curve_word = "parabola" if sympy.degree(zero_curve, independent) == 2 else "line"
   wanted = []

   for choice in choices_of(suffix):
      match = SLOPE_REGION.search(choice)

      if match is None:
         continue

      names_dependent = match.group(2) == str(dependent) and match.group(4) == str(dependent) and match.group(7) == str(dependent)
      curves_agree = all(same_expression(latex_to_sympy(match.group(index)), zero_curve) for index in (3, 6, 9))
      signs_agree = match.group(5) == positive_side and match.group(8) == negative_side
      word_agrees = match.group(1) == curve_word
      is_correct = names_dependent and curves_agree and signs_agree and word_agrees

      if is_correct:
         wanted.append(choice)

   return only_choice(wanted)


def separable_solution(rate, start_x, start_y):
   solutions = particular_solutions(rate, start_x, start_y)

   return only_choice(solutions)


def euler_two_steps(rate, start_x, start_y, target_x):
   step = (sympy.nsimplify(target_x) - sympy.nsimplify(start_x)) / 2

   return euler_approximation(rate, start_x, start_y, step, 2)


def concavity_sign_on(rate, start_x, end_x, bound, above):
   """The sign of y'' = f_x + f_y f over the x interval and the stated y region, sampled on a
   grid; raises if it is not one sign throughout."""
   second = second_derivative_along_solution(rate)
   signs = set()

   for step_index in range(CONCAVITY_SAMPLE_COUNT):
      at_x = sympy.nsimplify(start_x) + (sympy.nsimplify(end_x) - sympy.nsimplify(start_x)) * Rational(step_index, CONCAVITY_SAMPLE_COUNT - 1)

      for depth in REGION_SAMPLE_DEPTHS:
         at_y = bound + depth if above else bound - depth
         signs.add(sympy.sign(second.subs({x: at_x, y: at_y})))

   if len(signs) != 1 or 0 in signs:
      raise ValueError(f"y'' changes sign or vanishes: {signs}")

   return signs.pop()


def over_or_under(suffix, rate, start_x, start_y, end_x, bound, above):
   """Tangent lines and Euler steps lie above a concave down solution and below a concave up one;
   the reason must be the concavity over the whole interval, not only at the start."""
   is_in_region = start_y > bound if above else start_y < bound

   if not is_in_region:
      raise ValueError("the initial value is outside the stated region")

   sign = concavity_sign_on(rate, start_x, end_x, bound, above)
   verdict = "An overestimate" if sign < 0 else "An underestimate"
   concavity = "concave down" if sign < 0 else "concave up"
   wanted = [
      choice for choice in choices_of(suffix)
      if choice.startswith(verdict) and "for all x in the interval" in choice and concavity in choice
   ]

   return only_choice(wanted)


def proportional_to_difference(suffix, quantity, target, initial):
   """dQ/dt = k (target - Q) with k > 0, which moves Q toward the target from either side."""
   wanted_rate = k * (target - quantity)
   wanted_condition = f"\\( {quantity}(0) = {initial} \\)"
   wanted = []

   for choice in choices_of(suffix):
      rate_match = re.match(r"\\\( \\frac\{d\w\}\{dt\} = (.+?) \\\), with (.+)$", choice)

      if rate_match is None:
         continue

      stated_rate = latex_to_sympy(rate_match.group(1))
      rate_agrees = same_expression(stated_rate, wanted_rate)
      condition_agrees = rate_match.group(2) == wanted_condition

      if rate_agrees and condition_agrees:
         wanted.append(choice)

   return only_choice(wanted)


def candidate_check(suffix, candidate, rate, start_x, start_y):
   satisfies_equation = is_solution(candidate, rate)
   value_at_start = sympy.simplify(candidate.subs(x, start_x))
   meets_condition = value_at_start == start_y
   choices = choices_of(suffix)

   if satisfies_equation and meets_condition:
      wanted = [choice for choice in choices if choice.startswith("Yes.") and f"and \\( f(0) = {start_y} \\)" in choice]
   elif satisfies_equation:
      wanted = [
         choice for choice in choices
         if choice.startswith("No.") and "for every x, but" in choice and f"\\( f(0) = {value_at_start} \\), not {start_y}" in choice
      ]
   else:
      wanted = [choice for choice in choices if choice.startswith("No.") and "\\ne" in choice]

   return only_choice(wanted)


def exponential_model(start_value, later_time, later_value):
   growth_constant = log(Rational(later_value, start_value)) / later_time

   return start_value * exp(growth_constant * t)


def logistic_facts(suffix, rate, start_value):
   """Equilibria are the roots of the rate; from a start strictly between 0 and the carrying
   capacity the solution tends to the capacity, and the growth rate peaks where d(rate)/dP = 0."""
   roots = sorted(sympy.solve(rate, P))
   capacity = roots[-1]
   starts_inside = 0 < start_value < capacity

   if not starts_inside:
      raise ValueError("start is not between the equilibria")

   fastest = sympy.solve(sympy.diff(rate, P), P)[0]
   wanted = [
      choice for choice in choices_of(suffix)
      if f"approaches \\( {capacity} \\)" in choice and f"when \\( P = {fastest} \\)" in choice
   ]

   return only_choice(wanted)


def critical_point_type(suffix, input_factor_roots, output_factor, output_symbol, bound, above, input_name):
   """d(out)/d(in) = (in - a)(in + b) g(out) with g of one sign on the stated region: for in > 0
   the only zero is in = a, and the sign change there follows the sign of g."""
   positive_root, negative_root = input_factor_roots
   sample_output = bound + 1 if above else bound - 1
   factor_sign = sympy.sign(output_factor.subs(output_symbol, sample_output))
   is_minimum = factor_sign > 0
   kind = "relative minimum" if is_minimum else "relative maximum"
   change = "from negative to positive" if is_minimum else "from positive to negative"
   location = f"\\( {input_name} = {positive_root} \\)"
   wanted = [
      choice for choice in choices_of(suffix)
      if choice == f"The solution has a {kind} at {location}, because the derivative changes {change} at {location}."
   ]

   return only_choice(wanted)


def integral_form_solution(suffix, integrand_latex, start_x, start_value_latex):
   """y = y0 + the integral from x0 to x of the rate, with its differential."""
   wanted_text = f"\\( y = {start_value_latex} + \\int_{{{start_x}}}^{{x}} {integrand_latex}\\,dt \\)"

   return only_choice([choice for choice in choices_of(suffix) if choice == wanted_text])


def separable_with_interval(suffix, rate, start_x, start_y):
   """The solution through the point, kept on the one interval of its domain holding start_x."""
   solution = only_choice(particular_solutions(rate, start_x, start_y))
   singular = sympy.solve(sympy.denom(sympy.together(solution)), x)
   wanted = []

   for choice in choices_of(suffix):
      match = re.match(r"\\\( y = (.+?) \\\), for (.+)$", choice)
      stated = latex_to_sympy(match.group(1))

      if not same_expression(stated, solution):
         continue

      interval_ok = all(
         match.group(2) == (f"\\( x > {point} \\)" if start_x > point else f"\\( x < {point} \\)")
         for point in singular
      )

      if interval_ok:
         wanted.append(choice)

   return only_choice(wanted)


def curve(suffix, rate, dependent, name, start_value):
   return lambda: autonomous_solution_curve(suffix, rate, dependent, name, start_value)


def regions(suffix, rate, dependent, independent):
   return lambda: slope_field_regions(suffix, rate, dependent, independent)


def estimate(suffix, rate, start_x, start_y, end_x, bound, above):
   return lambda: over_or_under(suffix, rate, start_x, start_y, end_x, bound, above)


def approach(suffix, quantity, target, initial):
   return lambda: proportional_to_difference(suffix, quantity, target, initial)


def logistic(suffix, rate, start_value):
   return lambda: logistic_facts(suffix, rate, start_value)


def critical(suffix, roots, factor, symbol, bound, above, name):
   return lambda: critical_point_type(suffix, roots, factor, symbol, bound, above, name)


ABOVE = True
BELOW = False

BY_SUFFIX = {
   "07001-00": curve("07001-00", 2*P + 4, P, "t", 0),
   "07001-01": curve("07001-01", 6 - 2*y, y, "x", 1),
   "07001-02": curve("07001-02", 3 - y, y, "t", 5),
   "07001-03": curve("07001-03", P/2 - Rational(1, 2), P, "t", 0),
   "07001-04": curve("07001-04", -P - 1, P, "t", -2),
   "07001-05": curve("07001-05", -y, y, "x", -2),
   "07001-06": curve("07001-06", 1 - y, y, "x", 2),
   "07001-07": curve("07001-07", 2 - y, y, "t", 0),
   "07001-08": curve("07001-08", 2 - P/2, P, "t", 6),
   "07001-09": curve("07001-09", P/3 - Rational(2, 3), P, "t", 4),
   "07001-10": curve("07001-10", -2*y, y, "x", 2),
   "07001-11": curve("07001-11", 2*y - 8, y, "x", 6),
   "07001-12": curve("07001-12", y/3, y, "x", 1),
   "07001-13": curve("07001-13", -y, y, "x", 2),
   "07001-14": curve("07001-14", 1 - y/3, y, "x", 1),
   "07001-15": curve("07001-15", -y/2 - Rational(1, 2), y, "t", 0),
   "07001-16": curve("07001-16", 1 - P, P, "t", 3),
   "07001-17": curve("07001-17", -y/3 - Rational(1, 3), y, "t", 1),
   "07001-18": curve("07001-18", y/2 - 2, y, "t", 5),
   "07001-19": curve("07001-19", P/3 - 1, P, "t", 1),
   "07001-20": curve("07001-20", -P - 2, P, "t", -1),
   "07001-21": curve("07001-21", y/2 + 1, y, "x", -3),

   "07002-00": regions("07002-00", -2*P - 6*t + 8, P, t),
   "07002-01": regions("07002-01", -P + t + 2, P, t),
   "07002-02": regions("07002-02", 6*x**2 - 2*y - 2, y, x),
   "07002-03": regions("07002-03", 6*t**2 - 3*y - 12, y, t),
   "07002-04": regions("07002-04", 3*P + 3*t + 6, P, t),
   "07002-05": regions("07002-05", 2*t**2 - y + 1, y, t),
   "07002-06": regions("07002-06", -6*t + 2*y + 8, y, t),
   "07002-07": regions("07002-07", -3*P - 9*t**2 + 12, P, t),
   "07002-08": regions("07002-08", -t**2 + y - 5, y, t),
   "07002-09": regions("07002-09", -P + 3*t, P, t),
   "07002-10": regions("07002-10", 3*P - 6*t**2, P, t),
   "07002-11": regions("07002-11", -P + 2*t + 2, P, t),
   "07002-12": regions("07002-12", -6*x + 3*y, y, x),
   "07002-13": regions("07002-13", -6*t - 2*y + 4, y, t),
   "07002-14": regions("07002-14", 6*t + 3*y - 12, y, t),
   "07002-15": regions("07002-15", 2*P + 2*t**2 - 2, P, t),
   "07002-16": regions("07002-16", -2*t**2 + 2*y + 6, y, t),
   "07002-17": regions("07002-17", -4*x + 2*y + 6, y, x),
   "07002-18": regions("07002-18", -3*x**2 - y - 1, y, x),
   "07002-19": regions("07002-19", 2*x + 2*y - 2, y, x),
   "07002-20": regions("07002-20", -3*P + 9*t + 15, P, t),
   "07002-21": regions("07002-21", -2*t + y - 1, y, t),

   "07003-00": lambda: separable_solution(3*x / y, 3, 7),
   "07003-01": lambda: separable_solution(2*x*y, 0, 2),
   "07003-02": lambda: separable_solution(x**2 * y, -1, -4),
   "07003-03": lambda: separable_solution(4*x**4 * y, -1, -5),
   "07003-04": lambda: separable_solution(-2*x**4 * y, 0, 9),

   "07004-00": lambda: euler_two_steps(3 - x, 0, -2, 1),
   "07004-01": lambda: euler_two_steps(2 - 3*x, -1, 3, 0),
   "07004-02": lambda: euler_two_steps(-3*x + 2*y - 2, -1, 3, 0),
   "07004-03": lambda: euler_two_steps(3 - 3*x, 2, -3, 4),
   "07004-04": lambda: euler_two_steps(-x - 1, -1, 3, Rational(-1, 2)),

   "07005-00": estimate("07005-00", -3*y - 3, 2, -2, 3, -1, BELOW),
   "07005-01": estimate("07005-01", 9 - 3*y, 0, 0, 1, 3, BELOW),
   "07005-02": estimate("07005-02", 1 - y, 0, 0, Rational(1, 2), 1, BELOW),
   "07005-03": estimate("07005-03", x*(y - 1), 1, 2, Rational(3, 2), 1, ABOVE),
   "07005-04": estimate("07005-04", 2 - 2*y, 0, 2, Rational(1, 2), 1, ABOVE),
   "07005-05": estimate("07005-05", -2*y - 4, 1, 0, 2, -2, ABOVE),
   "07005-06": estimate("07005-06", 2 - 2*y, 2, 4, Rational(5, 2), 1, ABOVE),
   "07005-07": estimate("07005-07", 9 - 3*y, 2, 5, 3, 3, ABOVE),
   "07005-08": estimate("07005-08", 1 - y, 1, -2, Rational(3, 2), 1, BELOW),
   "07005-09": estimate("07005-09", 3*y + 3, 1, -3, Rational(3, 2), -1, BELOW),
   "07005-10": estimate("07005-10", x*(y - 1), 1, 2, 2, 1, ABOVE),
   "07005-11": estimate("07005-11", 2 - 2*y, 2, 3, 3, 1, ABOVE),
   "07005-12": estimate("07005-12", x*(y - 3), 1, 2, Rational(3, 2), 3, BELOW),
   "07005-13": estimate("07005-13", 2*x*(y + 2), 1, 0, Rational(3, 2), -2, ABOVE),
   "07005-14": estimate("07005-14", 3*x*(y - 1), 1, -1, Rational(3, 2), 1, BELOW),
   "07005-15": estimate("07005-15", 3*y + 6, 1, -1, Rational(3, 2), -2, ABOVE),
   "07005-16": estimate("07005-16", -y - 2, 1, -5, Rational(3, 2), -2, BELOW),
   "07005-17": estimate("07005-17", 2*x*y, 2, -2, Rational(5, 2), 0, BELOW),
   "07005-18": estimate("07005-18", 6 - 3*y, 0, -1, Rational(1, 2), 2, BELOW),
   "07005-19": estimate("07005-19", 3*y - 3, 0, 2, Rational(1, 2), 1, ABOVE),
   "07005-20": estimate("07005-20", x*(y - 1), 2, 2, Rational(5, 2), 1, ABOVE),
   "07005-21": estimate("07005-21", x*(y - 3), 2, 4, 3, 3, ABOVE),

   "07006-00": approach("07006-00", C, 45, 35),
   "07006-01": approach("07006-01", C, 65, 125),
   "07006-02": approach("07006-02", H, 55, 20),
   "07006-03": approach("07006-03", T, 55, 45),
   "07006-04": approach("07006-04", P, 40, 20),
   "07006-05": approach("07006-05", T, 60, 5),
   "07006-06": approach("07006-06", P, 55, 40),
   "07006-07": approach("07006-07", C, 90, 50),
   "07006-08": approach("07006-08", P, 60, 80),
   "07006-09": approach("07006-09", P, 25, 20),
   "07006-10": approach("07006-10", C, 75, 65),
   "07006-11": approach("07006-11", H, 95, 60),
   "07006-12": approach("07006-12", H, 25, 5),
   "07006-13": approach("07006-13", T, 95, 145),
   "07006-14": approach("07006-14", H, 55, 80),
   "07006-15": approach("07006-15", C, 70, 15),
   "07006-16": approach("07006-16", T, 95, 130),
   "07006-17": approach("07006-17", H, 90, 140),
   "07006-18": approach("07006-18", C, 80, 125),
   "07006-19": approach("07006-19", C, 95, 35),
   "07006-20": approach("07006-20", C, 90, 50),
   "07006-21": approach("07006-21", T, 75, 55),

   "07007-00": lambda: candidate_check("07007-00", 4*exp(2*x) - 2, 2*y + 4, 0, 3),
   "07007-01": lambda: candidate_check("07007-01", 2 - 3*exp(2*x), 2*y - 4, 0, -2),
   "07007-02": lambda: candidate_check("07007-02", -4 + 4*exp(-2*x), -2*y - 8, 0, 0),
   "07007-03": lambda: candidate_check("07007-03", -1 + exp(-x), -y - 1, 0, 0),

   "07008-00": lambda: exponential_model(100, 5, 200),
   "07008-01": lambda: exponential_model(580, 1, 145),
   "07008-02": lambda: exponential_model(120, 4, 300),
   "07008-03": lambda: exponential_model(80, 5, 240),
   "07008-04": lambda: exponential_model(420, 5, 1680),
   "07008-05": lambda: exponential_model(540, 1, 810),
   "07008-06": lambda: exponential_model(440, 3, 1760),
   "07008-07": lambda: exponential_model(480, 1, 192),
   "07008-08": lambda: exponential_model(60, 1, 120),
   "07008-09": lambda: exponential_model(360, 4, 144),
   "07008-10": lambda: exponential_model(320, 3, 128),
   "07008-11": lambda: exponential_model(360, 3, 1440),
   "07008-12": lambda: exponential_model(280, 1, 1120),
   "07008-13": lambda: exponential_model(340, 1, 510),
   "07008-14": lambda: exponential_model(420, 1, 1050),
   "07008-15": lambda: exponential_model(420, 2, 210),
   "07008-16": lambda: exponential_model(460, 2, 1150),
   "07008-17": lambda: exponential_model(560, 4, 2240),
   "07008-18": lambda: exponential_model(380, 5, 190),
   "07008-19": lambda: exponential_model(340, 2, 510),
   "07008-20": lambda: exponential_model(380, 1, 152),
   "07008-21": lambda: exponential_model(200, 6, 500),

   "07009-00": logistic("07009-00", Rational(2, 5) * P * (1 - P / 1300), 260),
   "07009-01": logistic("07009-01", P/3 - P**2 / 600, 40),
   "07009-02": logistic("07009-02", Rational(1, 3) * P * (1 - P / 1700), 170),
   "07009-03": logistic("07009-03", P/4 - P**2 / 7200, 360),
   "07009-04": logistic("07009-04", Rational(1, 2) * P * (1 - P / 200), 60),
   "07009-05": logistic("07009-05", Rational(1, 2) * P * (1 - P / 1800), 360),
   "07009-06": logistic("07009-06", Rational(1, 2) * P * (1 - P / 1100), 220),
   "07009-07": logistic("07009-07", Rational(1, 3) * P * (1 - P / 2000), 200),
   "07009-08": logistic("07009-08", Rational(1, 4) * P * (1 - P / 1400), 560),
   "07009-09": logistic("07009-09", P/5 - P**2 / 2500, 100),
   "07009-10": logistic("07009-10", P/5 - P**2 / 3500, 210),
   "07009-11": logistic("07009-11", 2*P/5 - P**2 / 1250, 200),
   "07009-12": logistic("07009-12", P/3 - P**2 / 2100, 280),
   "07009-13": logistic("07009-13", P/3 - P**2 / 5100, 340),
   "07009-14": logistic("07009-14", P/2 - P**2 / 1800, 270),
   "07009-15": logistic("07009-15", P/2 - P**2 / 1600, 80),
   "07009-16": logistic("07009-16", P/3 - P**2 / 3300, 220),
   "07009-17": logistic("07009-17", P/2 - P**2 / 1000, 100),
   "07009-18": logistic("07009-18", P/4 - P**2 / 1200, 75),
   "07009-19": logistic("07009-19", P/2 - P**2 / 2000, 300),
   "07009-20": logistic("07009-20", P/4 - P**2 / 7600, 475),
   "07009-21": logistic("07009-21", 2*P/5 - P**2 / 4000, 400),

   "07010-00": critical("07010-00", (1, -1), 2*y - 6, y, 3, BELOW, "x"),
   "07010-01": critical("07010-01", (3, -3), 3*y, y, 0, ABOVE, "x"),
   "07010-02": critical("07010-02", (2, -2), 2*y - 4, y, 2, ABOVE, "x"),
   "07010-03": critical("07010-03", (3, -2), -2*y - 6, y, -3, ABOVE, "x"),
   "07010-04": critical("07010-04", (5, -2), 3*y - 6, y, 2, BELOW, "t"),
   "07010-05": critical("07010-05", (2, -3), 2*y - 6, y, 3, BELOW, "t"),
   "07010-06": critical("07010-06", (1, -2), -2*P - 6, P, -3, BELOW, "t"),
   "07010-07": critical("07010-07", (4, -4), 3*y + 3, y, -1, ABOVE, "x"),
   "07010-08": critical("07010-08", (1, -3), 2*y + 2, y, -1, BELOW, "x"),
   "07010-09": critical("07010-09", (5, -3), -y - 1, y, -1, BELOW, "t"),
   "07010-10": critical("07010-10", (2, -2), -3*P - 6, P, -2, BELOW, "t"),
   "07010-11": critical("07010-11", (4, -1), 2*y, y, 0, ABOVE, "t"),
   "07010-12": critical("07010-12", (5, -3), y + 1, y, -1, ABOVE, "t"),
   "07010-13": critical("07010-13", (1, -2), y + 1, y, -1, ABOVE, "x"),
   "07010-14": critical("07010-14", (4, -4), 2*y + 2, y, -1, BELOW, "t"),
   "07010-15": critical("07010-15", (5, -3), 3*y + 3, y, -1, ABOVE, "t"),
   "07010-16": critical("07010-16", (4, -2), y + 3, y, -3, ABOVE, "t"),
   "07010-17": critical("07010-17", (1, -3), y + 3, y, -3, ABOVE, "t"),
   "07010-18": critical("07010-18", (1, -3), -3*y - 9, y, -3, ABOVE, "t"),
   "07010-19": critical("07010-19", (4, -1), y + 3, y, -3, BELOW, "t"),
   "07010-20": critical("07010-20", (1, -1), 2*y - 2, y, 1, BELOW, "x"),
   "07010-21": critical("07010-21", (2, -2), P - 1, P, 1, ABOVE, "t"),

   "07011-00": lambda: integral_form_solution("07011-00", r"\sqrt{t^{4} + 1}", 3, "-1"),
   "07011-01": lambda: integral_form_solution("07011-01", r"\sin{\left(t^{2} \right)}", 1, "-1"),
   "07011-02": lambda: integral_form_solution("07011-02", r"\cos{\left(t^{2} \right)}", 0, r"- \frac{1}{2}"),
   "07011-03": lambda: integral_form_solution("07011-03", r"\sqrt{t^{4} + 1}", 2, "3"),
   "07011-04": lambda: separable_with_interval("07011-04", -y**2, 0, 1),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
