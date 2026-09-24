"""Exact sign analysis and interval wording shared by the unit 4 and unit 5 templates of set C."""
import sympy


def pieces(breakpoints, low, high):
   """The open pieces of (low, high) cut at every breakpoint strictly inside it."""
   inside = sorted({sympy.nsimplify(point) for point in breakpoints if low < point < high})
   ends = [sympy.nsimplify(low)] + inside + [sympy.nsimplify(high)]

   return [(ends[index], ends[index + 1]) for index in range(len(ends) - 1)]


def midpoint(piece):
   return (piece[0] + piece[1]) / 2


def first_integer_inside(piece):
   candidate = sympy.floor(piece[0]) + 1
   is_inside = candidate < piece[1]

   return candidate if is_inside else midpoint(piece)


def where_sign(expression, variable, breakpoints, low, high, wanted_positive, sample=midpoint):
   """The pieces of (low, high), cut at the breakpoints, on which the expression has the wanted
   sign at the sample point of the piece."""
   chosen = []

   for piece in pieces(breakpoints, low, high):
      value = expression.subs(variable, sample(piece))
      has_wanted_sign = value > 0 if wanted_positive else value < 0

      if has_wanted_sign:
         chosen.append(piece)

   return chosen


def merge_touching(intervals):
   """Adjacent open intervals joined, for a property that also holds at the shared end."""
   merged = []

   for piece in intervals:
      touches = bool(merged) and merged[-1][1] == piece[0]

      if touches:
         merged[-1] = (merged[-1][0], piece[1])
      else:
         merged.append(piece)

   return merged


def interval_tex(piece):
   return rf"\left({sympy.latex(piece[0])}, {sympy.latex(piece[1])}\right)"


def intervals_text(intervals):
   """Open intervals written as a list a student would write, each in inline math."""
   parts = [rf"\( {interval_tex(piece)} \)" for piece in intervals]

   if len(parts) == 1:
      return parts[0]

   return ", ".join(parts[:-1]) + " and " + parts[-1]


def points_text(points):
   parts = [rf"\( x = {sympy.latex(point)} \)" for point in points]

   if len(parts) == 1:
      return parts[0]

   return ", ".join(parts[:-1]) + " and " + parts[-1]


def label_spot(heights):
   """A place for the curve's name on a graph of line segments through (index, heights[index]),
   at least one unit clear of the graph, trying the corners of a -4 to 4 window first."""
   candidates = [(0.2, 3.6), (0.2, -3.6), (4.6, 3.6), (4.6, -3.6), (2.4, 3.6), (2.4, -3.6)]
   last = len(heights) - 1

   for x_value, y_value in candidates:
      covered = [x_value + offset / 4 for offset in range(5)]
      clear = True

      for point in covered:
         index = min(int(point), last - 1)
         fraction = point - index
         height = heights[index] + (heights[index + 1] - heights[index]) * fraction
         too_close = abs(height - y_value) < 1

         if too_close:
            clear = False

      if clear:
         return x_value, y_value

   return candidates[0]
