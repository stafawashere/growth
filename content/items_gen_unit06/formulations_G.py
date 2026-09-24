"""Answers to the batch G unit 6 generated items, computed from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The solver
read only stems_G.json, never a key, a worked solution or a template, so a match with the stored
key is independent evidence that the key answers the stem.
"""
import mpmath
import sympy

mpmath.mp.dps = 30


def as_sympy(value):
   return sympy.Float(mpmath.nstr(value, 30), 30)


def sine_square_rate(amplitude, divisor, offset):
   return lambda time: amplitude * mpmath.sin(time**2 / divisor) + offset


def amount_arriving(amplitude, divisor, offset, start, end):
   """Only the inflow R arrives; an outflow the stem mentions does not change what arrives."""
   inflow_rate = sine_square_rate(amplitude, divisor, offset)

   return as_sympy(mpmath.quad(inflow_rate, [start, end]))


CHOSEN_TEXT = {
   "99010-00": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 56 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 48.917 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} b(h)\\,dh = 7 \\).",
   "99010-01": "\\( T = \\int_{0}^{3} f(h)\\,dh + \\int_{3}^{D} g(h)\\,dh \\), and \\( T \\le 42 \\) because \\( \\int_{0}^{3} f(h)\\,dh \\approx 31.272 \\) and \\( \\int_{3}^{D} g(h)\\,dh \\le \\int_{3}^{\\infty} 10 e^{3 - h}\\,dh = 10 \\).",
   "99010-02": "\\( T = \\int_{0}^{4} f(h)\\,dh + \\int_{4}^{D} g(h)\\,dh \\), and \\( T \\le 40 \\) because \\( \\int_{0}^{4} f(h)\\,dh \\approx 32.898 \\) and \\( \\int_{4}^{D} g(h)\\,dh \\le \\int_{4}^{\\infty} b(h)\\,dh = 7 \\).",
   "99010-03": "\\( T = \\int_{0}^{2} f(h)\\,dh + \\int_{2}^{D} g(h)\\,dh \\), and \\( T \\le 23 \\) because \\( \\int_{0}^{2} f(h)\\,dh \\approx 14.998 \\) and \\( \\int_{2}^{D} g(h)\\,dh \\le \\int_{2}^{\\infty} 8 e^{2 - h}\\,dh = 8 \\).",
   "99010-04": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 50 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 37.583 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} 12 e^{5 - h}\\,dh = 12 \\).",
   "99010-05": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 40 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 27.612 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} 12 e^{5 - h}\\,dh = 12 \\).",
   "99010-06": "\\( T = \\int_{0}^{2} f(h)\\,dh + \\int_{2}^{D} g(h)\\,dh \\), and \\( T \\le 32 \\) because \\( \\int_{0}^{2} f(h)\\,dh \\approx 19.019 \\) and \\( \\int_{2}^{D} g(h)\\,dh \\le \\int_{2}^{\\infty} b(h)\\,dh = 12 \\).",
   "99010-07": "\\( T = \\int_{0}^{3} f(h)\\,dh + \\int_{3}^{D} g(h)\\,dh \\), and \\( T \\le 29 \\) because \\( \\int_{0}^{3} f(h)\\,dh \\approx 19.556 \\) and \\( \\int_{3}^{D} g(h)\\,dh \\le \\int_{3}^{\\infty} b(h)\\,dh = 9 \\).",
   "99010-08": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 29 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 21.722 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} b(h)\\,dh = 7 \\).",
   "99010-09": "\\( T = \\int_{0}^{2} f(h)\\,dh + \\int_{2}^{D} g(h)\\,dh \\), and \\( T \\le 29 \\) because \\( \\int_{0}^{2} f(h)\\,dh \\approx 20.993 \\) and \\( \\int_{2}^{D} g(h)\\,dh \\le \\int_{2}^{\\infty} 8 e^{2 - h}\\,dh = 8 \\).",
   "99010-10": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 31 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 21.722 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} 9 e^{5 - h}\\,dh = 9 \\).",
   "99010-11": "\\( T = \\int_{0}^{3} f(h)\\,dh + \\int_{3}^{D} g(h)\\,dh \\), and \\( T \\le 24 \\) because \\( \\int_{0}^{3} f(h)\\,dh \\approx 17.848 \\) and \\( \\int_{3}^{D} g(h)\\,dh \\le \\int_{3}^{\\infty} b(h)\\,dh = 6 \\).",
   "99010-12": "\\( T = \\int_{0}^{2} f(h)\\,dh + \\int_{2}^{D} g(h)\\,dh \\), and \\( T \\le 28 \\) because \\( \\int_{0}^{2} f(h)\\,dh \\approx 15.241 \\) and \\( \\int_{2}^{D} g(h)\\,dh \\le \\int_{2}^{\\infty} b(h)\\,dh = 12 \\).",
   "99010-13": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 60 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 48.622 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} 11 e^{5 - h}\\,dh = 11 \\).",
   "99010-14": "\\( T = \\int_{0}^{4} f(h)\\,dh + \\int_{4}^{D} g(h)\\,dh \\), and \\( T \\le 27 \\) because \\( \\int_{0}^{4} f(h)\\,dh \\approx 21.610 \\) and \\( \\int_{4}^{D} g(h)\\,dh \\le \\int_{4}^{\\infty} 5 e^{4 - h}\\,dh = 5 \\).",
   "99010-15": "\\( T = \\int_{0}^{4} f(h)\\,dh + \\int_{4}^{D} g(h)\\,dh \\), and \\( T \\le 50 \\) because \\( \\int_{0}^{4} f(h)\\,dh \\approx 39.219 \\) and \\( \\int_{4}^{D} g(h)\\,dh \\le \\int_{4}^{\\infty} b(h)\\,dh = 10 \\).",
   "99010-16": "\\( T = \\int_{0}^{3} f(h)\\,dh + \\int_{3}^{D} g(h)\\,dh \\), and \\( T \\le 21 \\) because \\( \\int_{0}^{3} f(h)\\,dh \\approx 17.959 \\) and \\( \\int_{3}^{D} g(h)\\,dh \\le \\int_{3}^{\\infty} 3 e^{3 - h}\\,dh = 3 \\).",
   "99010-17": "\\( T = \\int_{0}^{3} f(h)\\,dh + \\int_{3}^{D} g(h)\\,dh \\), and \\( T \\le 39 \\) because \\( \\int_{0}^{3} f(h)\\,dh \\approx 28.556 \\) and \\( \\int_{3}^{D} g(h)\\,dh \\le \\int_{3}^{\\infty} 10 e^{3 - h}\\,dh = 10 \\).",
   "99010-18": "\\( T = \\int_{0}^{2} f(h)\\,dh + \\int_{2}^{D} g(h)\\,dh \\), and \\( T \\le 23 \\) because \\( \\int_{0}^{2} f(h)\\,dh \\approx 12.998 \\) and \\( \\int_{2}^{D} g(h)\\,dh \\le \\int_{2}^{\\infty} 10 e^{2 - h}\\,dh = 10 \\).",
   "99010-19": "\\( T = \\int_{0}^{3} f(h)\\,dh + \\int_{3}^{D} g(h)\\,dh \\), and \\( T \\le 23 \\) because \\( \\int_{0}^{3} f(h)\\,dh \\approx 16.424 \\) and \\( \\int_{3}^{D} g(h)\\,dh \\le \\int_{3}^{\\infty} 6 e^{3 - h}\\,dh = 6 \\).",
   "99010-20": "\\( T = \\int_{0}^{5} f(h)\\,dh + \\int_{5}^{D} g(h)\\,dh \\), and \\( T \\le 47 \\) because \\( \\int_{0}^{5} f(h)\\,dh \\approx 42.414 \\) and \\( \\int_{5}^{D} g(h)\\,dh \\le \\int_{5}^{\\infty} b(h)\\,dh = 4 \\).",
   "99010-21": "\\( T = \\int_{0}^{4} f(h)\\,dh + \\int_{4}^{D} g(h)\\,dh \\), and \\( T \\le 35 \\) because \\( \\int_{0}^{4} f(h)\\,dh \\approx 30.000 \\) and \\( \\int_{4}^{D} g(h)\\,dh \\le \\int_{4}^{\\infty} 5 e^{4 - h}\\,dh = 5 \\).",
}


def bounded_total_statement(item_id, amplitude, divisor, offset, split_depth, tail_integrand, tail_value, claimed_bound):
   """T is the integral of f over [0, split] plus the integral of g over [split, D], with no
   constant and no antiderivative of g. The justification holds only when the stated
   approximation is the integral rounded to three places and that value plus the tail bound
   stays at or below the claimed bound."""
   density = sine_square_rate(amplitude, divisor, offset)
   top_amount = mpmath.quad(density, [0, split_depth])
   rounded_text = f"{float(top_amount):.3f}"
   bound_holds = top_amount + tail_value <= claimed_bound

   correct_text = (
      f"\\( T = \\int_{{0}}^{{{split_depth}}} f(h)\\,dh + \\int_{{{split_depth}}}^{{D}} g(h)\\,dh \\), "
      f"and \\( T \\le {claimed_bound} \\) because \\( \\int_{{0}}^{{{split_depth}}} f(h)\\,dh \\approx {rounded_text} \\) "
      f"and \\( \\int_{{{split_depth}}}^{{D}} g(h)\\,dh \\le \\int_{{{split_depth}}}^{{\\infty}} {tail_integrand}\\,dh = {tail_value} \\)."
   )

   if not bound_holds:
      return []

   suffix = item_id.removeprefix("ITM-GEN-")
   inlined_text = CHOSEN_TEXT[suffix]

   if inlined_text != correct_text:
      raise ValueError(f"inlined choice for {suffix} differs from the computed one")

   return inlined_text


def statement(suffix, amplitude, divisor, offset, split_depth, tail_integrand, tail_value, claimed_bound):
   item_id = f"ITM-GEN-{suffix}"

   return lambda: bounded_total_statement(
      item_id, amplitude, divisor, offset, split_depth, tail_integrand, tail_value, claimed_bound
   )


BY_SUFFIX = {
   "99008-00": lambda: amount_arriving(3, 5, 13, 1, 4),
   "99008-01": lambda: amount_arriving(5, 2, 9, 1, 4),
   "99008-02": lambda: amount_arriving(2, 4, 10, 1, 4),
   "99008-03": lambda: amount_arriving(4, 6, 13, 0, 3),
   "99008-04": lambda: amount_arriving(2, 2, 13, 2, 7),
   "99008-05": lambda: amount_arriving(4, 4, 10, 1, 4),
   "99008-06": lambda: amount_arriving(2, 5, 13, 2, 7),
   "99008-07": lambda: amount_arriving(2, 5, 15, 0, 5),
   "99008-08": lambda: amount_arriving(3, 2, 11, 0, 4),
   "99008-09": lambda: amount_arriving(2, 6, 11, 0, 4),
   "99008-10": lambda: amount_arriving(3, 6, 7, 0, 4),
   "99008-11": lambda: amount_arriving(2, 3, 14, 0, 5),
   "99008-12": lambda: amount_arriving(5, 2, 10, 0, 4),
   "99008-13": lambda: amount_arriving(5, 2, 15, 0, 4),
   "99008-14": lambda: amount_arriving(2, 5, 12, 0, 5),
   "99008-15": lambda: amount_arriving(4, 2, 12, 0, 5),
   "99008-16": lambda: amount_arriving(5, 6, 6, 2, 5),
   "99008-17": lambda: amount_arriving(4, 6, 11, 0, 4),
   "99008-18": lambda: amount_arriving(2, 5, 13, 2, 5),
   "99008-19": lambda: amount_arriving(4, 2, 14, 0, 3),
   "99008-20": lambda: amount_arriving(3, 6, 14, 2, 6),
   "99008-21": lambda: amount_arriving(3, 3, 10, 0, 3),

   "99010-00": statement("99010-00", 3, 5, 9, 5, "b(h)", 7, 56),
   "99010-01": statement("99010-01", 3, 5, 9, 3, "10 e^{3 - h}", 10, 42),
   "99010-02": statement("99010-02", 1, 3, 8, 4, "b(h)", 7, 40),
   "99010-03": statement("99010-03", 1, 2, 7, 2, "8 e^{2 - h}", 8, 23),
   "99010-04": statement("99010-04", 3, 4, 7, 5, "12 e^{5 - h}", 12, 50),
   "99010-05": statement("99010-05", 2, 5, 5, 5, "12 e^{5 - h}", 12, 40),
   "99010-06": statement("99010-06", 2, 5, 9, 2, "b(h)", 12, 32),
   "99010-07": statement("99010-07", 1, 4, 6, 3, "b(h)", 9, 29),
   "99010-08": statement("99010-08", 2, 4, 4, 5, "b(h)", 7, 29),
   "99010-09": statement("99010-09", 3, 2, 9, 2, "8 e^{2 - h}", 8, 29),
   "99010-10": statement("99010-10", 2, 4, 4, 5, "9 e^{5 - h}", 9, 31),
   "99010-11": statement("99010-11", 2, 5, 5, 3, "b(h)", 6, 24),
   "99010-12": statement("99010-12", 2, 4, 7, 2, "b(h)", 12, 28),
   "99010-13": statement("99010-13", 3, 3, 9, 5, "11 e^{5 - h}", 11, 60),
   "99010-14": statement("99010-14", 1, 4, 5, 4, "5 e^{4 - h}", 5, 27),
   "99010-15": statement("99010-15", 2, 4, 9, 4, "b(h)", 10, 50),
   "99010-16": statement("99010-16", 3, 2, 5, 3, "3 e^{3 - h}", 3, 21),
   "99010-17": statement("99010-17", 1, 4, 9, 3, "10 e^{3 - h}", 10, 39),
   "99010-18": statement("99010-18", 1, 2, 6, 2, "10 e^{2 - h}", 10, 23),
   "99010-19": statement("99010-19", 1, 5, 5, 3, "6 e^{3 - h}", 6, 23),
   "99010-20": statement("99010-20", 2, 3, 8, 5, "b(h)", 4, 47),
   "99010-21": statement("99010-21", 3, 5, 6, 4, "5 e^{4 - h}", 5, 35),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
