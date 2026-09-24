"""Interval and sign-chart helpers shared by the templates written in the stage 5 run D."""
import sympy

from app.generation.kit import math, tex


def product_tex(variable, roots):
   """(x - a)(x - b) as LaTeX, with a zero root written as a bare x in front."""
   zero_roots = [root for root in roots if root == 0]
   other_roots = [root for root in roots if root != 0]
   bare = tex(variable) * len(zero_roots) if len(zero_roots) < 2 else tex(variable) + "^{" + str(len(zero_roots)) + "}"
   factors = "".join(r"\left(" + tex(variable - root) + r"\right)" for root in other_roots)

   return bare + factors


def interval_tex(low, high):
   """An open interval, with None standing for an infinite end."""
   left = r"-\infty" if low is None else tex(low)
   right = r"\infty" if high is None else tex(high)

   return f"({left}, {right})"


def interval_list_text(intervals):
   """Several open intervals as a sentence fragment: one interval, or a list joined with and."""
   pieces = [math(interval_tex(low, high)) for low, high in intervals]

   if len(pieces) == 1:
      return f"the interval {pieces[0]}"

   if len(pieces) == 2:
      return f"the intervals {pieces[0]} and {pieces[1]}"

   return "the intervals " + ", ".join(pieces[:-1]) + f" and {pieces[-1]}"


def pieces_between(points):
   """The open pieces of the real line cut at the sorted points."""
   ordered = sorted(points)
   ends = [None] + ordered + [None]

   return [(ends[index], ends[index + 1]) for index in range(len(ends) - 1)]


def sample_point(low, high):
   if low is None and high is None:
      return sympy.Integer(0)

   if low is None:
      return high - 1

   if high is None:
      return low + 1

   return sympy.Rational(low + high, 2)


def sign_on(expression, variable, low, high):
   value = expression.subs(variable, sample_point(low, high))

   return 1 if value > 0 else -1


def merge_touching(intervals, removed_points=()):
   """Join neighbouring intervals that share an endpoint, unless that endpoint is a removed point."""
   merged = []

   for low, high in intervals:
      has_previous = bool(merged)
      touches = has_previous and merged[-1][1] is not None and merged[-1][1] == low
      is_gap = touches and low in removed_points

      if touches and not is_gap:
         merged[-1] = (merged[-1][0], high)
         continue

      merged.append((low, high))

   return merged
