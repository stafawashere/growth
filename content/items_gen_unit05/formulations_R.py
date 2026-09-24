"""Blind answers for the unit 5 generated items in stems_R.json, one SymPy computation per stem.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, without seeing any key, worked solution or template. Each statement item is decided by
working the theorem hypotheses, the sign change of f', or the monotonic pieces of the graph of f'
the stem gives, then returning the one choice, copied below, that states that result with a valid
reason. A list means no choice or more than one choice fits. The Mean Value Theorem items also
check whether the table itself forces such a c through the mean value theorem on a smooth piece and
the intermediate value property of derivatives, in which case "not guaranteed" is false and no
choice is correct.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import sympy
from sympy import Rational, exp

from tools.key_recheck import x

CHOICES = {
   "05001-00": [
      "No. Although \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (1, 9) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[1, 9\\right] \\).",
      "Yes. Since \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 9) \\).",
      "Yes. Since \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), there is a c with \\( 1 < c < 9 \\) and \\( f'(c) = - \\frac{1}{4} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-01": [
      "No. Although \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), f is not differentiable at \\( x = 3 \\), which lies in \\( (0, 6) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 6) \\).",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), there is a c with \\( 0 < c < 6 \\) and \\( f'(c) = \\frac{3}{2} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-02": [
      "No. Although \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), f is not differentiable at \\( x = 7 \\), which lies in \\( (4, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[4, 10\\right] \\).",
      "Yes. Since \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 10) \\).",
      "Yes. Since \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), there is a c with \\( 4 < c < 10 \\) and \\( f'(c) = -3 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-03": [
      "No. Although \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), f is not differentiable at \\( x = \\frac{9}{2} \\), which lies in \\( (2, 7) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[2, 7\\right] \\).",
      "Yes. Since \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 7) \\).",
      "Yes. Since \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), there is a c with \\( 2 < c < 7 \\) and \\( f'(c) = \\frac{19}{5} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-04": [
      "No. Although \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), f is not continuous at \\( x = 8 \\), which lies in \\( \\left[7, 9\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[7, 9\\right] \\).",
      "Yes. Since \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (7, 9) \\).",
      "Yes. Since \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), there is a c with \\( 7 < c < 9 \\) and \\( f'(c) = -4 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-05": [
      "No. Although \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), f is not differentiable at \\( x = 8 \\), which lies in \\( (4, 12) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[4, 12\\right] \\).",
      "Yes. Since \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 12) \\).",
      "Yes. Since \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), there is a c with \\( 4 < c < 12 \\) and \\( f'(c) = - \\frac{19}{8} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-06": [
      "No. Although \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), f is not continuous at \\( x = \\frac{9}{2} \\), which lies in \\( \\left[0, 9\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 9\\right] \\).",
      "Yes. Since \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 9) \\).",
      "Yes. Since \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), there is a c with \\( 0 < c < 9 \\) and \\( f'(c) = - \\frac{2}{9} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-07": [
      "No. Although \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), f is not differentiable at \\( x = \\frac{11}{2} \\), which lies in \\( (3, 8) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 8\\right] \\).",
      "Yes. Since \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 8) \\).",
      "Yes. Since \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), there is a c with \\( 3 < c < 8 \\) and \\( f'(c) = \\frac{1}{5} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-08": [
      "No. Although \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (0, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 10\\right] \\).",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 10) \\).",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), there is a c with \\( 0 < c < 10 \\) and \\( f'(c) = \\frac{1}{5} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-09": [
      "No. Although \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), f is not continuous at \\( x = \\frac{13}{2} \\), which lies in \\( \\left[1, 12\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[1, 12\\right] \\).",
      "Yes. Since \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 12) \\).",
      "Yes. Since \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), there is a c with \\( 1 < c < 12 \\) and \\( f'(c) = \\frac{24}{11} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-10": [
      "No. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), but \\( \\frac{f(6) - f(12)}{12 - 6} = -1 \\), so the Mean Value Theorem does not give such a c.",
      "Yes. Since f is defined at every point of \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), the Mean Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), so the Intermediate Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), so the Mean Value Theorem guarantees such a c.",
   ],
   "05001-11": [
      "No. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), but \\( \\frac{f(2) - f(10)}{10 - 2} = - \\frac{5}{4} \\), so the Mean Value Theorem does not give such a c.",
      "Yes. Since f is defined at every point of \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), the Mean Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), so the Intermediate Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), so the Mean Value Theorem guarantees such a c.",
   ],
   "05001-12": [
      "No. Although \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), f is not continuous at \\( x = \\frac{9}{2} \\), which lies in \\( \\left[3, 6\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 6) \\).",
      "Yes. Since \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), there is a c with \\( 3 < c < 6 \\) and \\( f'(c) = 4 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-13": [
      "No. Although \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), f is not differentiable at \\( x = \\frac{15}{2} \\), which lies in \\( (3, 12) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 12\\right] \\).",
      "Yes. Since \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 12) \\).",
      "Yes. Since \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), there is a c with \\( 3 < c < 12 \\) and \\( f'(c) = - \\frac{1}{9} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-14": [
      "No. Although \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (2, 8) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[2, 8\\right] \\).",
      "Yes. Since \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 8) \\).",
      "Yes. Since \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), there is a c with \\( 2 < c < 8 \\) and \\( f'(c) = 1 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-15": [
      "No. Although \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), f is not continuous at \\( x = 4 \\), which lies in \\( \\left[1, 7\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[1, 7\\right] \\).",
      "Yes. Since \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 7) \\).",
      "Yes. Since \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), there is a c with \\( 1 < c < 7 \\) and \\( f'(c) = 4 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-16": [
      "No. Although \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (0, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 10\\right] \\).",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 10) \\).",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), there is a c with \\( 0 < c < 10 \\) and \\( f'(c) = -2 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-17": [
      "No. Although \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), f is not differentiable at \\( x = 3 \\), which lies in \\( (0, 6) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 6) \\).",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), there is a c with \\( 0 < c < 6 \\) and \\( f'(c) = 2 \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-18": [
      "No. Although \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), f is not differentiable at \\( x = \\frac{19}{2} \\), which lies in \\( (8, 11) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[8, 11\\right] \\).",
      "Yes. Since \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (8, 11) \\).",
      "Yes. Since \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), there is a c with \\( 8 < c < 11 \\) and \\( f'(c) = - \\frac{8}{3} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-19": [
      "No. Although \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), f is not differentiable at \\( x = 4 \\), which lies in \\( (3, 5) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 5\\right] \\).",
      "Yes. Since \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 5) \\).",
      "Yes. Since \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), there is a c with \\( 3 < c < 5 \\) and \\( f'(c) = \\frac{15}{2} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-20": [
      "No. Although \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), f is not continuous at \\( x = 4 \\), which lies in \\( \\left[2, 6\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[2, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 6) \\).",
      "Yes. Since \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), there is a c with \\( 2 < c < 6 \\) and \\( f'(c) = - \\frac{15}{4} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05001-21": [
      "No. Although \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), f is not continuous at \\( x = 6 \\), which lies in \\( \\left[4, 8\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[4, 8\\right] \\).",
      "Yes. Since \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 8) \\).",
      "Yes. Since \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), there is a c with \\( 4 < c < 8 \\) and \\( f'(c) = \\frac{3}{4} \\), because an average rate of change is always reached by the derivative.",
   ],
   "05003-00": [
      "f has a relative maximum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has a relative maximum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' stays close to 0 on both sides of x = 2.",
   ],
   "05003-01": [
      "f has a relative maximum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from negative to positive at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has neither a relative minimum nor a relative maximum at x = -3, because f' stays close to 0 on both sides of x = -3.",
   ],
   "05003-02": [
      "f has a relative maximum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative maximum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has neither a relative minimum nor a relative maximum at x = 0, because f' stays close to 0 on both sides of x = 0.",
   ],
   "05003-03": [
      "f has a relative maximum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' stays close to 0 on both sides of x = 2.",
   ],
   "05003-04": [
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from negative to positive at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has neither a relative minimum nor a relative maximum at x = 1, because f' stays close to 0 on both sides of x = 1.",
   ],
   "05003-05": [
      "f has a relative maximum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative maximum at x = -1, because f' changes from positive to negative at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' stays close to 0 on both sides of x = -1.",
   ],
   "05003-06": [
      "f has a relative maximum at x = 2, because f' is positive before and equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' takes its smallest nearby value at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
   ],
   "05003-07": [
      "f has a relative maximum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from negative to positive at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' stays close to 0 on both sides of x = -2.",
   ],
   "05003-08": [
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from negative to positive at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has neither a relative minimum nor a relative maximum at x = 1, because f' stays close to 0 on both sides of x = 1.",
   ],
   "05003-09": [
      "f has a relative maximum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has a relative maximum at x = 4, because f' changes from positive to negative at x = 4.",
      "f has a relative minimum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' stays close to 0 on both sides of x = 4.",
   ],
   "05003-10": [
      "f has a relative maximum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' stays close to 0 on both sides of x = 2.",
   ],
   "05003-11": [
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from negative to positive at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has neither a relative minimum nor a relative maximum at x = 1, because f' stays close to 0 on both sides of x = 1.",
   ],
   "05003-12": [
      "f has a relative maximum at x = 2, because f' is positive before and equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' takes its smallest nearby value at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
   ],
   "05003-13": [
      "f has a relative maximum at x = 2, because f' is positive before and equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' takes its smallest nearby value at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
   ],
   "05003-14": [
      "f has a relative maximum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has neither a relative minimum nor a relative maximum at x = 0, because f' stays close to 0 on both sides of x = 0.",
   ],
   "05003-15": [
      "f has a relative maximum at x = 4, because f' is positive before and equal to 0 at x = 4.",
      "f has a relative minimum at x = 4, because f' is equal to 0 at x = 4.",
      "f has a relative minimum at x = 4, because f' takes its smallest nearby value at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' does not change sign at x = 4.",
   ],
   "05003-16": [
      "f has a relative maximum at x = -3, because f' changes from negative to positive at x = -3.",
      "f has a relative maximum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from negative to positive at x = -3.",
      "f has neither a relative minimum nor a relative maximum at x = -3, because f' stays close to 0 on both sides of x = -3.",
   ],
   "05003-17": [
      "f has a relative maximum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative maximum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has neither a relative minimum nor a relative maximum at x = 0, because f' stays close to 0 on both sides of x = 0.",
   ],
   "05003-18": [
      "f has a relative maximum at x = -2, because f' is positive before and equal to 0 at x = -2.",
      "f has a relative minimum at x = -2, because f' is equal to 0 at x = -2.",
      "f has a relative minimum at x = -2, because f' takes its smallest nearby value at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' does not change sign at x = -2.",
   ],
   "05003-19": [
      "f has a relative maximum at x = 2, because f' is positive before and equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' takes its smallest nearby value at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
   ],
   "05003-20": [
      "f has a relative maximum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from negative to positive at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has neither a relative minimum nor a relative maximum at x = -3, because f' stays close to 0 on both sides of x = -3.",
   ],
   "05003-21": [
      "f has a relative maximum at x = 3, because f' changes from positive to negative at x = 3.",
      "f has a relative minimum at x = 3, because f' changes from negative to positive at x = 3.",
      "f has a relative minimum at x = 3, because f' changes from positive to negative at x = 3.",
      "f has neither a relative minimum nor a relative maximum at x = 3, because f' stays close to 0 on both sides of x = 3.",
   ],
   "05004-00": [
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(2, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(\\frac{7}{2}, \\frac{23}{4}\\right) \\), because f' is negative there.",
   ],
   "05004-01": [
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(1, \\frac{9}{4}\\right) \\) and \\( \\left(\\frac{22}{5}, \\frac{23}{4}\\right) \\), because f' is positive there.",
      "The graph of f is concave up exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
   ],
   "05004-02": [
      "The graph of f is concave down exactly on \\( \\left(0, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, \\frac{3}{4}\\right) \\), because f' is negative there.",
      "The graph of f is concave down exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(1, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
   ],
   "05004-03": [
      "The graph of f is concave up exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{22}{5}, \\frac{28}{5}\\right) \\), because f' is positive there.",
   ],
   "05004-04": [
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 3\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(\\frac{13}{5}, \\frac{17}{4}\\right) \\), because f' is negative there.",
   ],
   "05004-05": [
      "The graph of f is concave up exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, \\frac{1}{4}\\right) \\) and \\( \\left(\\frac{11}{2}, 6\\right) \\), because f' is positive there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
   ],
   "05004-06": [
      "The graph of f is concave down exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 2\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(\\frac{4}{3}, 3\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is negative there.",
   ],
   "05004-07": [
      "The graph of f is concave down exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(2, \\frac{7}{2}\\right) \\) and \\( \\left(\\frac{19}{4}, 6\\right) \\), because f' is negative there.",
   ],
   "05004-08": [
      "The graph of f is concave up exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, \\frac{1}{4}\\right) \\) and \\( \\left(2, \\frac{10}{3}\\right) \\), because f' is positive there.",
      "The graph of f is concave up exactly on \\( \\left(1, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 3\\right) \\), because f' is increasing there.",
   ],
   "05004-09": [
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(3, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(\\frac{27}{5}, 6\\right) \\), because f' is negative there.",
   ],
   "05004-10": [
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, \\frac{3}{5}\\right) \\) and \\( \\left(\\frac{11}{3}, 6\\right) \\), because f' is negative there.",
      "The graph of f is concave down exactly on \\( \\left(2, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
   ],
   "05004-11": [
      "The graph of f is concave down exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 2\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(\\frac{7}{5}, \\frac{7}{2}\\right) \\) and \\( \\left(\\frac{17}{3}, 6\\right) \\), because f' is negative there.",
   ],
   "05004-12": [
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 3\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{1}{4}, \\frac{3}{2}\\right) \\) and \\( \\left(\\frac{22}{5}, \\frac{11}{2}\\right) \\), because f' is positive there.",
   ],
   "05004-13": [
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, \\frac{7}{4}\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is positive there.",
   ],
   "05004-14": [
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{2}{5}, \\frac{18}{5}\\right) \\) and \\( \\left(\\frac{21}{4}, 6\\right) \\), because f' is positive there.",
   ],
   "05004-15": [
      "The graph of f is concave down exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, \\frac{1}{4}\\right) \\), \\( \\left(\\frac{9}{4}, \\frac{14}{3}\\right) \\) and \\( \\left(\\frac{11}{2}, 6\\right) \\), because f' is negative there.",
      "The graph of f is concave down exactly on \\( \\left(1, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(1, 3\\right) \\), because f' is decreasing there.",
   ],
   "05004-16": [
      "The graph of f is concave up exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{7}{2}, \\frac{11}{2}\\right) \\), because f' is positive there.",
   ],
   "05004-17": [
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{1}{2}, \\frac{8}{5}\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is positive there.",
   ],
   "05004-18": [
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, 3\\right) \\) and \\( \\left(3, \\frac{9}{2}\\right) \\), because f' is negative there.",
   ],
   "05004-19": [
      "The graph of f is concave up exactly on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{3}{2}, \\frac{9}{4}\\right) \\), because f' is positive there.",
   ],
   "05004-20": [
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(0, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up exactly on \\( \\left(\\frac{11}{3}, \\frac{13}{3}\\right) \\), because f' is positive there.",
   ],
   "05004-21": [
      "The graph of f is concave down exactly on \\( \\left(0, 1\\right) \\), \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(0, \\frac{2}{3}\\right) \\) and \\( \\left(3, \\frac{9}{2}\\right) \\), because f' is negative there.",
      "The graph of f is concave down exactly on \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down exactly on \\( \\left(2, 4\\right) \\), because f' is decreasing there.",
   ],
   "05005-00": [
      "The graph of f has exactly one point of inflection, at \\( x = 2 \\), because f' changes between increasing and decreasing there.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{10}{3} \\) and \\( x = \\frac{14}{3} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-01": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{3}{4} \\), \\( x = \\frac{8}{3} \\), \\( x = \\frac{7}{2} \\) and \\( x = \\frac{28}{5} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-02": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = \\frac{5}{2} \\), \\( x = \\frac{17}{4} \\) and \\( x = \\frac{23}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-03": [
      "The graph of f has exactly one point of inflection, at \\( x = 1 \\), because f' changes between increasing and decreasing there.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\) and \\( x = \\frac{14}{3} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-04": [
      "The graph of f has exactly one point of inflection, at \\( x = 1 \\), because f' changes between increasing and decreasing there.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 4 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{9}{4} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-05": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{1}{2} \\), \\( x = 2 \\) and \\( x = 4 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-06": [
      "The graph of f has exactly one point of inflection, at \\( x = 1 \\), because f' changes between increasing and decreasing there.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{1}{2} \\) and \\( x = \\frac{5}{2} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-07": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = \\frac{10}{3} \\), \\( x = \\frac{22}{5} \\) and \\( x = \\frac{23}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-08": [
      "The graph of f has exactly one point of inflection, at \\( x = 1 \\), because f' changes between increasing and decreasing there.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{3}{5} \\), \\( x = \\frac{5}{2} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-09": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{2}{5} \\), \\( x = 2 \\), \\( x = \\frac{11}{3} \\) and \\( x = \\frac{17}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-10": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{7}{5} \\), \\( x = \\frac{5}{2} \\) and \\( x = 4 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-11": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{2}{3} \\), \\( x = \\frac{9}{2} \\) and \\( x = \\frac{17}{3} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-12": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{2}{5} \\), \\( x = \\frac{3}{2} \\), \\( x = \\frac{13}{4} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-13": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{3}{4} \\), \\( x = \\frac{3}{2} \\), \\( x = 3 \\) and \\( x = \\frac{11}{2} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-14": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 2 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{2}{3} \\), \\( x = \\frac{3}{2} \\), \\( x = 3 \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-15": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{3}{4} \\), \\( x = \\frac{5}{2} \\), \\( x = \\frac{7}{2} \\) and \\( x = \\frac{19}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-16": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{10}{3} \\) and \\( x = \\frac{22}{5} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-17": [
      "The graph of f has exactly one point of inflection, at \\( x = 1 \\), because f' changes between increasing and decreasing there.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\) and \\( x = 2 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{7}{5} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-18": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{7}{5} \\), \\( x = \\frac{5}{2} \\) and \\( x = \\frac{15}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-19": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{1}{4} \\), \\( x = \\frac{12}{5} \\), \\( x = \\frac{7}{2} \\) and \\( x = \\frac{23}{5} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-20": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{1}{2} \\), \\( x = \\frac{8}{5} \\), \\( x = \\frac{12}{5} \\) and \\( x = \\frac{17}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-21": [
      "The graph of f has points of inflection exactly at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection exactly at \\( x = \\frac{13}{5} \\), \\( x = 4 \\) and \\( x = \\frac{11}{2} \\), because f' is equal to 0 at each of these values.",
   ],
}


SIGN_PROBE = Rational(1, 100)


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


def stated_points(text):
   return sorted(latex_number(value) for value in re.findall(r"x = (.+?) \\\)", text))


def secant_slopes(table, inputs):
   ordered = sorted(inputs)

   return [
      Rational(table[right] - table[left], right - left)
      for left, right in zip(ordered, ordered[1:])
   ]


def forced_on_piece(table, inputs, target):
   """On a closed piece where f is differentiable inside, each secant slope between consecutive
   table inputs is a value of f', and f' has the intermediate value property there."""
   slopes = secant_slopes(table, inputs)

   if not slopes:
      return False

   return min(slopes) <= target <= max(slopes)


def mvt_statement(suffix, table, left, right, target, defect, defect_at=None):
   """defect is None (differentiable everywhere), "corner" (continuous, not differentiable at
   defect_at) or "jump" (not continuous at defect_at)."""
   average = Rational(table[right] - table[left], right - left)
   shown_average = sympy.latex(average)
   is_corner_inside = defect == "corner" and left < defect_at < right
   is_jump_inside = defect == "jump" and left <= defect_at <= right
   hypotheses_hold = not (is_corner_inside or is_jump_inside)

   if average != target:
      return []

   if hypotheses_hold:
      def is_correct(text):
         says_yes = text.startswith("Yes. Since f is differentiable, it is continuous on")
         uses_mvt = text.endswith("so the Mean Value Theorem guarantees such a c.")
         states_average = f"= {shown_average} \\)" in text

         return says_yes and uses_mvt and states_average

      return pick(suffix, is_correct)

   if is_corner_inside:
      left_piece = [point for point in table if left <= point <= defect_at]
      right_piece = [point for point in table if defect_at <= point <= right]
      failure = f"f is not differentiable at \\( x = {sympy.latex(defect_at)} \\)"
   else:
      left_piece = [point for point in table if left <= point < defect_at]
      right_piece = [point for point in table if defect_at < point <= right]
      failure = f"f is not continuous at \\( x = {sympy.latex(defect_at)} \\)"

   is_forced = forced_on_piece(table, left_piece, target) or forced_on_piece(table, right_piece, target)

   if is_forced:
      return []

   def is_correct(text):
      says_no = text.startswith(f"No. Although \\( \\frac{{f({right}) - f({left})}}{{{right} - {left}}} = {shown_average} \\)")
      names_failure = failure in text
      concludes = text.endswith("so the Mean Value Theorem does not apply and such a c is not guaranteed.")

      return says_no and names_failure and concludes

   return pick(suffix, is_correct)


def extremum_statement(suffix, derivative_expression, at):
   before = sympy.sign(derivative_expression.subs(x, at - SIGN_PROBE))
   after = sympy.sign(derivative_expression.subs(x, at + SIGN_PROBE))
   is_zero_there = sympy.simplify(derivative_expression.subs(x, at)) == 0

   if not is_zero_there:
      raise ValueError(f"f' is not 0 at {at}")

   if before < 0 < after:
      expected = f"f has a relative minimum at x = {at}, because f' changes from negative to positive at x = {at}."
   elif before > 0 > after:
      expected = f"f has a relative maximum at x = {at}, because f' changes from positive to negative at x = {at}."
   else:
      expected = (
         f"f has neither a relative minimum nor a relative maximum at x = {at}, "
         f"because f' does not change sign at x = {at}."
      )

   return pick(suffix, lambda text: text == expected)


def segment_slopes(values):
   slopes = [right - left for left, right in zip(values, values[1:])]

   if 0 in slopes:
      raise ValueError("a flat segment needs its own reading")

   return slopes


def monotone_intervals(values, rising):
   """Maximal open intervals of 0 < x < 6 on which the piecewise linear f' through (k, values[k])
   is increasing (rising) or decreasing."""
   intervals = []

   for start, slope in enumerate(segment_slopes(values)):
      is_wanted = slope > 0 if rising else slope < 0

      if not is_wanted:
         continue

      continues_previous = intervals and intervals[-1][1] == start

      if continues_previous:
         intervals[-1] = (intervals[-1][0], start + 1)
      else:
         intervals.append((start, start + 1))

   return [(sympy.Integer(left), sympy.Integer(right)) for left, right in intervals]


def concavity_statement(suffix, values, way):
   rising = way == "up"
   intervals = monotone_intervals(values, rising)
   reason = "because f' is increasing there." if rising else "because f' is decreasing there."

   def is_correct(text):
      names_concavity = text.startswith(f"The graph of f is concave {way} exactly on")
      states_intervals = stated_intervals(text) == intervals
      gives_reason = text.endswith(reason)

      return names_concavity and states_intervals and gives_reason

   return pick(suffix, is_correct)


def inflection_statement(suffix, values):
   slopes = segment_slopes(values)
   points = [
      sympy.Integer(joint)
      for joint in range(1, len(slopes))
      if slopes[joint - 1] * slopes[joint] < 0
   ]

   def is_correct(text):
      states_points = stated_points(text) == points
      gives_reason = "because f' changes between increasing and decreasing" in text

      return states_points and gives_reason

   return pick(suffix, is_correct)


def mvt(suffix, table, left, right, target, defect=None, defect_at=None):
   return suffix, lambda: mvt_statement(suffix, table, left, right, target, defect, defect_at)


def extremum(suffix, derivative_expression, at):
   return suffix, lambda: extremum_statement(suffix, derivative_expression, at)


def concavity(suffix, values, way):
   return suffix, lambda: concavity_statement(suffix, values, way)


def inflection(suffix, values):
   return suffix, lambda: inflection_statement(suffix, values)


R = Rational

ITEMS = [
   mvt("05001-00", {1: 12, 2: -5, 4: 19, 9: 10, 10: -9}, 1, 9, -R(1, 4), "corner", 5),
   mvt("05001-01", {0: 9, 1: 0, 3: 14, 6: 18, 8: 18}, 0, 6, R(3, 2), "corner", 3),
   mvt("05001-02", {3: 17, 4: 20, 5: -1, 7: 3, 10: 2}, 4, 10, -3, "corner", 7),
   mvt("05001-03", {0: 20, 2: -1, 4: 20, 7: 18, 9: 18}, 2, 7, R(19, 5), "corner", R(9, 2)),
   mvt("05001-04", {2: -5, 6: -3, 7: 17, 8: 2, 9: 9}, 7, 9, -4, "jump", 8),
   mvt("05001-05", {3: 7, 4: 17, 5: 18, 7: 8, 12: -2}, 4, 12, -R(19, 8), "corner", 8),
   mvt("05001-06", {0: 15, 6: -8, 8: -9, 9: 13, 10: 17}, 0, 9, -R(2, 9), "jump", R(9, 2)),
   mvt("05001-07", {2: 6, 3: 2, 5: 5, 7: -1, 8: 3}, 3, 8, R(1, 5), "corner", R(11, 2)),
   mvt("05001-08", {0: 10, 1: 17, 3: 20, 10: 12, 11: -9}, 0, 10, R(1, 5), "corner", 5),
   mvt("05001-09", {1: -8, 5: -8, 10: 14, 11: 13, 12: 16}, 1, 12, R(24, 11), "jump", R(13, 2)),
   mvt("05001-10", {0: 13, 6: 10, 9: 1, 10: 13, 12: 16}, 6, 12, 1),
   mvt("05001-11", {1: 3, 2: 9, 3: -8, 5: 16, 10: 19}, 2, 10, R(5, 4)),
   mvt("05001-12", {3: -8, 4: 19, 6: 4, 7: 13, 10: 14}, 3, 6, 4, "jump", R(9, 2)),
   mvt("05001-13", {1: -8, 3: 7, 5: 5, 9: 17, 12: 6}, 3, 12, -R(1, 9), "corner", R(15, 2)),
   mvt("05001-14", {1: 12, 2: 6, 4: -7, 6: -7, 8: 12}, 2, 8, 1, "corner", 5),
   mvt("05001-15", {1: -4, 4: 7, 6: 16, 7: 20, 11: 0}, 1, 7, 4, "jump", 4),
   mvt("05001-16", {0: 20, 1: 6, 6: 18, 9: -3, 10: 0}, 0, 10, -2, "corner", 5),
   mvt("05001-17", {0: 7, 1: -7, 4: -8, 6: 19, 10: 4}, 0, 6, 2, "corner", 3),
   mvt("05001-18", {3: 5, 6: 12, 8: 5, 9: 9, 11: -3}, 8, 11, -R(8, 3), "corner", R(19, 2)),
   mvt("05001-19", {3: -8, 4: 2, 5: 7, 10: 9, 12: 7}, 3, 5, R(15, 2), "corner", 4),
   mvt("05001-20", {2: 14, 5: 6, 6: -1, 8: -3, 11: 7}, 2, 6, -R(15, 4), "jump", 4),
   mvt("05001-21", {0: -8, 2: 3, 4: 0, 7: -7, 8: 3}, 4, 8, R(3, 4), "jump", 6),

   extremum("05003-00", 4*(x - 2)*(x + 4)*(x**2 + 1), 2),
   extremum("05003-01", -2*(x + 3)*(x + 4)*exp(x), -3),
   extremum("05003-02", -3*x*(x - 2), 0),
   extremum("05003-03", -3*(x - 2)*(x + 2)*(x**2 + 1), 2),
   extremum("05003-04", -x*(x - 1)*exp(x), 1),
   extremum("05003-05", 4*(x + 1)*(x + 4)*(x**2 + 1), -1),
   extremum("05003-06", 4*(x - 2)**2*(x + 1)*exp(x), 2),
   extremum("05003-07", -4*(x + 2)*(x + 5)*(x**2 + 1), -2),
   extremum("05003-08", -(x - 1)*(x + 1)*(x**2 + 1), 1),
   extremum("05003-09", -4*(x - 4)*(x - 5)*(x**2 + 1), 4),
   extremum("05003-10", 2*(x - 2)*(x - 4)*exp(x), 2),
   extremum("05003-11", (x - 1)*(x - 6)*(x**2 + 1), 1),
   extremum("05003-12", (x - 2)**2*(x + 5)*exp(x), 2),
   extremum("05003-13", 4*x*(x - 2)**2, 2),
   extremum("05003-14", 2*x*(x - 3)*exp(x), 0),
   extremum("05003-15", 2*(x - 4)**2*(x - 3)*(x**2 + 1), 4),
   extremum("05003-16", 2*(x + 3)*(x + 4), -3),
   extremum("05003-17", 4*x*(x + 4)*(x**2 + 1), 0),
   extremum("05003-18", -(x + 2)**2*(x - 3)*(x**2 + 1), -2),
   extremum("05003-19", 4*(x - 2)**2*(x + 5)*exp(x), 2),
   extremum("05003-20", 2*(x + 3)*(x - 3), -3),
   extremum("05003-21", -(x - 3)*(x - 2)*exp(x), 3),

   concavity("05004-00", [1, 2, 3, 2, -2, -3, 1], "down"),
   concavity("05004-01", [2, 0, 1, -3, -2, 3, -1], "up"),
   concavity("05004-02", [-3, 1, 0, 3, 2, 3, 1], "down"),
   concavity("05004-03", [0, -3, -1, -3, -2, 3, -2], "up"),
   concavity("05004-04", [3, 1, 3, -2, -1, 3, 1], "down"),
   concavity("05004-05", [1, -3, -2, -3, -2, -1, 1], "up"),
   concavity("05004-06", [3, 1, -2, 0, -3, 0, 3], "down"),
   concavity("05004-07", [2, 1, 0, -3, 3, -1, -3], "down"),
   concavity("05004-08", [1, -3, 0, 1, -2, -3, -1], "up"),
   concavity("05004-09", [0, 1, 2, 3, 1, 2, -3], "down"),
   concavity("05004-10", [-3, 2, 3, 2, -1, -3, 0], "down"),
   concavity("05004-11", [3, 2, -3, -1, 1, 2, -1], "down"),
   concavity("05004-12", [-1, 3, -3, -1, -2, 3, -3], "up"),
   concavity("05004-13", [2, 3, -1, -3, -2, 0, 3], "up"),
   concavity("05004-14", [-2, 3, 1, 3, -2, -1, 3], "up"),
   concavity("05004-15", [-1, 3, 1, -3, -2, 1, -1], "down"),
   concavity("05004-16", [0, -2, -1, -3, 3, 2, -2], "up"),
   concavity("05004-17", [-3, 3, -2, -1, -3, 0, 1], "up"),
   concavity("05004-18", [-2, -3, -1, 0, -3, 3, 1], "down"),
   concavity("05004-19", [0, -1, 1, -3, -1, 0, -2], "up"),
   concavity("05004-20", [-1, 0, -3, -2, 1, -2, -1], "up"),
   concavity("05004-21", [-2, 1, 3, 0, -3, 3, 1], "down"),

   inflection("05005-00", [0, -1, -2, -1, 2, -1, -2]),
   inflection("05005-01", [-3, 1, 2, -1, 1, 3, -2]),
   inflection("05005-02", [-1, 0, -2, 2, 1, -3, 1]),
   inflection("05005-03", [0, 1, 0, -3, -2, 1, 2]),
   inflection("05005-04", [-2, -3, -1, 3, 1, 0, -1]),
   inflection("05005-05", [-1, 1, 0, -1, 0, 2, 1]),
   inflection("05005-06", [-2, 2, 1, -1, -2, -3, 0]),
   inflection("05005-07", [3, 0, 3, 1, -2, 3, -1]),
   inflection("05005-08", [3, -2, -1, 1, 3, 0, -1]),
   inflection("05005-09", [2, -3, 0, 2, -1, 3, 2]),
   inflection("05005-10", [1, 2, -3, 3, 0, -2, 0]),
   inflection("05005-11", [-2, 1, 2, 1, 2, -2, 1]),
   inflection("05005-12", [-2, 3, -3, -1, 3, 0, 1]),
   inflection("05005-13", [3, -1, 1, 0, 1, 3, -3]),
   inflection("05005-14", [-2, 1, -1, 0, 1, 0, -2]),
   inflection("05005-15", [3, -1, -3, 3, -3, 1, 2]),
   inflection("05005-16", [1, 3, 2, 1, -2, 3, 2]),
   inflection("05005-17", [1, 2, -3, -2, -1, 0, 2]),
   inflection("05005-18", [-1, -2, 3, -3, 1, 2, 1]),
   inflection("05005-19", [1, -3, -2, 3, -3, 2, 1]),
   inflection("05005-20", [3, -3, 2, -3, -1, 3, 0]),
   inflection("05005-21", [0, 1, 3, -2, 0, 2, -2]),
]

BY_SUFFIX = dict(ITEMS)

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
