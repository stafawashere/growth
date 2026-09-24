"""Helpers shared by the templates written in the stage 5 run F."""
import sympy


def three_place(value):
   return round(float(sympy.N(value, 30)), 3)


def differs_at_three_places(value, taken):
   rounded = three_place(value)

   return all(rounded != three_place(other) for other in taken)


def first_distinct(candidates, taken, wanted=1):
   """The first candidates, in order, whose values differ at three places from everything taken
   and from each other. A candidate is (value, description); a value of None is skipped."""
   chosen = []
   seen = list(taken)

   for value, description in candidates:
      if value is None:
         continue

      if not differs_at_three_places(value, seen):
         continue

      chosen.append((value, description))
      seen.append(value)

      if len(chosen) == wanted:
         break

   return chosen


def rounded(value, places):
   return sympy.Rational(round(float(sympy.N(value, 30)), places)).limit_denominator(10**places)


def distinct_exact(values):
   """True when no two exact values are equal."""
   for index, left in enumerate(values):
      for right in values[index + 1:]:
         difference = sympy.simplify(sympy.sympify(left) - sympy.sympify(right))

         if difference == 0:
            return False

   return True


def truncated(value, places):
   scale = 10**places

   return sympy.Rational(int(float(sympy.N(value, 30)) * scale), scale)


def tex_f(expression):
   """LaTeX as the course prints it: ln for the logarithm and arctan for the inverse tangent."""
   return sympy.latex(sympy.sympify(expression), ln_notation=True, inv_trig_style="full")


def tidy(expression):
   """A sum with each term brought over one denominator, so a derivative prints the way it is
   written by hand."""
   expression = sympy.sympify(expression)
   terms = [sympy.cancel(term) for term in sympy.Add.make_args(sympy.expand(expression))]

   return sympy.Add(*terms)
