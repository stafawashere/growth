"""Blind answers to the unit 5 Mean Value Theorem items in stems_R2.json.

Written from the stems and their tables alone by a blind solver, claude-opus-5-5, on the operator's
delegation of 2026-09-24. Each stem asks whether the Mean Value Theorem guarantees a c with
f'(c) equal to a given value, so the verdict turns on whether the theorem's hypotheses hold on
the closed interval: continuity on [a, b] and differentiability on (a, b). A corner inside (a, b)
or a jump inside [a, b] breaks them, and then nothing is guaranteed even when the secant slope
matches. The file never reads a stems file at run time.
"""
from sympy import Rational


def mvt_verdict(table, left, right, target, break_point, break_kind, no_choice, yes_choice):
   secant_slope = Rational(table[right] - table[left], right - left)
   slope_matches = secant_slope == target

   if not slope_matches:
      raise ValueError(f"secant slope {secant_slope} does not equal {target}")

   has_break = break_point is not None
   corner_inside_open = has_break and break_kind == "corner" and left < break_point < right
   jump_inside_closed = has_break and break_kind == "jump" and left <= break_point <= right
   hypotheses_fail = corner_inside_open or jump_inside_closed

   if hypotheses_fail:
      return no_choice

   return yes_choice


BY_SUFFIX = {
   "05001-00": lambda: mvt_verdict(
      table={1: 12, 2: -5, 4: 19, 9: 10, 10: -9},
      left=1, right=9, target=-Rational(1,4), break_point=5, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (1, 9) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 9) \\).",
   ),
   "05001-01": lambda: mvt_verdict(
      table={0: 9, 1: 0, 3: 14, 6: 18, 8: 18},
      left=0, right=6, target=Rational(3,2), break_point=3, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), f is not differentiable at \\( x = 3 \\), which lies in \\( (0, 6) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 6) \\).",
   ),
   "05001-02": lambda: mvt_verdict(
      table={3: 17, 4: 20, 5: -1, 7: 3, 10: 2},
      left=4, right=10, target=-3, break_point=7, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), f is not differentiable at \\( x = 7 \\), which lies in \\( (4, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 10) \\).",
   ),
   "05001-03": lambda: mvt_verdict(
      table={0: 20, 2: -1, 4: 20, 7: 18, 9: 18},
      left=2, right=7, target=Rational(19,5), break_point=Rational(9, 2), break_kind="corner",
      no_choice="No. Although \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), f is not differentiable at \\( x = \\frac{9}{2} \\), which lies in \\( (2, 7) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 7) \\).",
   ),
   "05001-04": lambda: mvt_verdict(
      table={2: -5, 6: -3, 7: 17, 8: 2, 9: 9},
      left=7, right=9, target=-4, break_point=8, break_kind="jump",
      no_choice="No. Although \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), f is not continuous at \\( x = 8 \\), which lies in \\( \\left[7, 9\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (7, 9) \\).",
   ),
   "05001-05": lambda: mvt_verdict(
      table={3: 7, 4: 17, 5: 18, 7: 8, 12: -2},
      left=4, right=12, target=-Rational(19,8), break_point=8, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), f is not differentiable at \\( x = 8 \\), which lies in \\( (4, 12) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 12) \\).",
   ),
   "05001-06": lambda: mvt_verdict(
      table={0: 15, 6: -8, 8: -9, 9: 13, 10: 17},
      left=0, right=9, target=-Rational(2,9), break_point=Rational(9, 2), break_kind="jump",
      no_choice="No. Although \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), f is not continuous at \\( x = \\frac{9}{2} \\), which lies in \\( \\left[0, 9\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 9) \\).",
   ),
   "05001-07": lambda: mvt_verdict(
      table={2: 6, 3: 2, 5: 5, 7: -1, 8: 3},
      left=3, right=8, target=Rational(1,5), break_point=Rational(11, 2), break_kind="corner",
      no_choice="No. Although \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), f is not differentiable at \\( x = \\frac{11}{2} \\), which lies in \\( (3, 8) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 8) \\).",
   ),
   "05001-08": lambda: mvt_verdict(
      table={0: 10, 1: 17, 3: 20, 10: 12, 11: -9},
      left=0, right=10, target=Rational(1,5), break_point=5, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (0, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 10) \\).",
   ),
   "05001-09": lambda: mvt_verdict(
      table={1: -8, 5: -8, 10: 14, 11: 13, 12: 16},
      left=1, right=12, target=Rational(24,11), break_point=Rational(13, 2), break_kind="jump",
      no_choice="No. Although \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), f is not continuous at \\( x = \\frac{13}{2} \\), which lies in \\( \\left[1, 12\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 12) \\).",
   ),
   "05001-10": lambda: mvt_verdict(
      table={0: 13, 6: 10, 9: 1, 10: 13, 12: 16},
      left=6, right=12, target=1, break_point=None, break_kind="none",
      no_choice="No. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), but \\( \\frac{f(6) - f(12)}{12 - 6} = -1 \\), so the Mean Value Theorem does not give such a c.",
      yes_choice="Yes. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), so the Mean Value Theorem guarantees such a c.",
   ),
   "05001-11": lambda: mvt_verdict(
      table={1: 3, 2: 9, 3: -8, 5: 16, 10: 19},
      left=2, right=10, target=Rational(5,4), break_point=None, break_kind="none",
      no_choice="No. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), but \\( \\frac{f(2) - f(10)}{10 - 2} = - \\frac{5}{4} \\), so the Mean Value Theorem does not give such a c.",
      yes_choice="Yes. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), so the Mean Value Theorem guarantees such a c.",
   ),
   "05001-12": lambda: mvt_verdict(
      table={3: -8, 4: 19, 6: 4, 7: 13, 10: 14},
      left=3, right=6, target=4, break_point=Rational(9, 2), break_kind="jump",
      no_choice="No. Although \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), f is not continuous at \\( x = \\frac{9}{2} \\), which lies in \\( \\left[3, 6\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 6) \\).",
   ),
   "05001-13": lambda: mvt_verdict(
      table={1: -8, 3: 7, 5: 5, 9: 17, 12: 6},
      left=3, right=12, target=-Rational(1,9), break_point=Rational(15, 2), break_kind="corner",
      no_choice="No. Although \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), f is not differentiable at \\( x = \\frac{15}{2} \\), which lies in \\( (3, 12) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 12) \\).",
   ),
   "05001-14": lambda: mvt_verdict(
      table={1: 12, 2: 6, 4: -7, 6: -7, 8: 12},
      left=2, right=8, target=1, break_point=5, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (2, 8) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 8) \\).",
   ),
   "05001-15": lambda: mvt_verdict(
      table={1: -4, 4: 7, 6: 16, 7: 20, 11: 0},
      left=1, right=7, target=4, break_point=4, break_kind="jump",
      no_choice="No. Although \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), f is not continuous at \\( x = 4 \\), which lies in \\( \\left[1, 7\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 7) \\).",
   ),
   "05001-16": lambda: mvt_verdict(
      table={0: 20, 1: 6, 6: 18, 9: -3, 10: 0},
      left=0, right=10, target=-2, break_point=5, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (0, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 10) \\).",
   ),
   "05001-17": lambda: mvt_verdict(
      table={0: 7, 1: -7, 4: -8, 6: 19, 10: 4},
      left=0, right=6, target=2, break_point=3, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), f is not differentiable at \\( x = 3 \\), which lies in \\( (0, 6) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 6) \\).",
   ),
   "05001-18": lambda: mvt_verdict(
      table={3: 5, 6: 12, 8: 5, 9: 9, 11: -3},
      left=8, right=11, target=-Rational(8,3), break_point=Rational(19, 2), break_kind="corner",
      no_choice="No. Although \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), f is not differentiable at \\( x = \\frac{19}{2} \\), which lies in \\( (8, 11) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (8, 11) \\).",
   ),
   "05001-19": lambda: mvt_verdict(
      table={3: -8, 4: 2, 5: 7, 10: 9, 12: 7},
      left=3, right=5, target=Rational(15,2), break_point=4, break_kind="corner",
      no_choice="No. Although \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), f is not differentiable at \\( x = 4 \\), which lies in \\( (3, 5) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 5) \\).",
   ),
   "05001-20": lambda: mvt_verdict(
      table={2: 14, 5: 6, 6: -1, 8: -3, 11: 7},
      left=2, right=6, target=-Rational(15,4), break_point=4, break_kind="jump",
      no_choice="No. Although \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), f is not continuous at \\( x = 4 \\), which lies in \\( \\left[2, 6\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 6) \\).",
   ),
   "05001-21": lambda: mvt_verdict(
      table={0: -8, 2: 3, 4: 0, 7: -7, 8: 3},
      left=4, right=8, target=Rational(3,4), break_point=6, break_kind="jump",
      no_choice="No. Although \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), f is not continuous at \\( x = 6 \\), which lies in \\( \\left[4, 8\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      yes_choice="Yes. Since \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 8) \\).",
   ),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
