"""Blind re-solve of generated unit 10 items, batch X, each answer computed from its stem alone.

Written from var/p4/resolve/items_gen_unit10/stems_X.json and nothing else about these items by a blind
solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The file is self-contained: each
item's choices are copied into it from the stems. The classification is worked out from the general
term, and the choice stating that classification with its valid reason is returned; when no choice or
more than one does, the list of matches comes back so the recheck reports the item.
"""
import sympy
from sympy import oo

n = sympy.Symbol("n", positive=True, integer=True)
ALTERNATION_CHECKS = 6

DIVERGES = "The series diverges, because its terms do not approach 0."
CONVERGES_ABSOLUTELY = (
   "The series converges absolutely, because the series of absolute values converges by comparison "
   "with a p-series."
)
CONVERGES_CONDITIONALLY = (
   "The series converges conditionally, because it passes the alternating series test while the "
   "series of absolute values diverges."
)


def expression(text):
   return sympy.sympify(text, locals={"n": n})


def choice_stating(suffix, wanted):
   matches = [choice for choice in CHOICES[suffix] if choice == wanted]

   return matches[0] if len(matches) == 1 else matches


def classification(term, first):
   size = sympy.simplify(sympy.Abs(term))
   limit_of_size = sympy.limit(size, n, oo)

   if limit_of_size != 0:
      return DIVERGES

   decay_power = sympy.limit(-sympy.log(size) / sympy.log(n), n, oo)

   if decay_power > 1:
      return CONVERGES_ABSOLUTELY

   signs = [sympy.sign(term.subs(n, first + offset)) for offset in range(ALTERNATION_CHECKS)]
   alternates = all(earlier == -later for earlier, later in zip(signs, signs[1:]))
   continuous_size = size.subs(n, sympy.Symbol("u", positive=True))
   size_decreases = sympy.is_decreasing(continuous_size, sympy.Interval(first, oo))
   passes_alternating_test = alternates and size_decreases

   if not passes_alternating_test:
      return None

   return CONVERGES_CONDITIONALLY


def series_classification_choice(suffix, term, first):
   verdict = classification(term, first)

   if verdict is None:
      return []

   return choice_stating(suffix, verdict)


CHOICES = {
   "10007-00": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-01": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-02": [
      "The series converges absolutely, because it passes the alternating series test while the series of absolute values diverges.",
      "The series converges absolutely, because it passes the alternating series test, its terms decreasing in size to 0.",
      "The series converges conditionally, because it passes the alternating series test while the series of absolute values diverges.",
      "The series diverges, because the series of absolute values diverges by comparison with a p-series.",
   ],
   "10007-03": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-04": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-05": [
      "The series converges absolutely, because it passes the alternating series test while the series of absolute values diverges.",
      "The series converges absolutely, because it passes the alternating series test, its terms decreasing in size to 0.",
      "The series converges conditionally, because it passes the alternating series test while the series of absolute values diverges.",
      "The series diverges, because the series of absolute values diverges by comparison with a p-series.",
   ],
   "10007-06": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-07": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-08": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-09": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-10": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-11": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-12": [
      "The series converges absolutely, because it passes the alternating series test while the series of absolute values diverges.",
      "The series converges absolutely, because it passes the alternating series test, its terms decreasing in size to 0.",
      "The series converges conditionally, because it passes the alternating series test while the series of absolute values diverges.",
      "The series diverges, because the series of absolute values diverges by comparison with a p-series.",
   ],
   "10007-13": [
      "The series converges absolutely, because it passes the alternating series test while the series of absolute values diverges.",
      "The series converges absolutely, because it passes the alternating series test, its terms decreasing in size to 0.",
      "The series converges conditionally, because it passes the alternating series test while the series of absolute values diverges.",
      "The series diverges, because the series of absolute values diverges by comparison with a p-series.",
   ],
   "10007-14": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-15": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-16": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-17": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
   "10007-18": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-19": [
      "The series converges absolutely, because its terms alternate in sign.",
      "The series converges conditionally, because its terms alternate in sign while their sizes do not shrink.",
      "The series converges, because it is an alternating series.",
      "The series diverges, because its terms do not approach 0.",
   ],
   "10007-20": [
      "The series converges absolutely, because it passes the alternating series test while the series of absolute values diverges.",
      "The series converges absolutely, because it passes the alternating series test, its terms decreasing in size to 0.",
      "The series converges conditionally, because it passes the alternating series test while the series of absolute values diverges.",
      "The series diverges, because the series of absolute values diverges by comparison with a p-series.",
   ],
   "10007-21": [
      "The series converges absolutely, because the series of absolute values converges by comparison with a p-series.",
      "The series converges conditionally, because it passes the alternating series test.",
      "The series converges conditionally, because the series of absolute values converges by comparison with a p-series.",
      "The series diverges, because the series of absolute values is compared with a p-series.",
   ],
}


BY_SUFFIX = {
   "10007-00": lambda: series_classification_choice("10007-00", expression("4*(-1)**(n + 1)*n/(n + 3)"), 2),
   "10007-01": lambda: series_classification_choice("10007-01", expression("6*(-1)**(n + 1)*n/(n + 8)"), 1),
   "10007-02": lambda: series_classification_choice("10007-02", expression("(-1)**n/sqrt(n + 7)"), 2),
   "10007-03": lambda: series_classification_choice("10007-03", expression("8*(-1)**(n + 1)*n/(n + 6)"), 2),
   "10007-04": lambda: series_classification_choice("10007-04", expression("2*(-1)**n*n/(n + 3)"), 2),
   "10007-05": lambda: series_classification_choice("10007-05", expression("5*(-1)**(n + 1)/(n + 3)**(1/3)"), 1),
   "10007-06": lambda: series_classification_choice("10007-06", expression("6*(-1)**(n + 1)/(n + 5)**3"), 2),
   "10007-07": lambda: series_classification_choice("10007-07", expression("6*(-1)**(n + 1)/(n + 8)**(4/3)"), 2),
   "10007-08": lambda: series_classification_choice("10007-08", expression("(-1)**(n + 1)/(n + 1)**2"), 1),
   "10007-09": lambda: series_classification_choice("10007-09", expression("2*(-1)**n*n/(n + 1)"), 2),
   "10007-10": lambda: series_classification_choice("10007-10", expression("2*(-1)**n/(n + 9)**(4/3)"), 1),
   "10007-11": lambda: series_classification_choice("10007-11", expression("9*(-1)**(n + 1)/(n + 3)**(3/2)"), 1),
   "10007-12": lambda: series_classification_choice("10007-12", expression("7*(-1)**(n + 1)/(n + 5)**(1/3)"), 1),
   "10007-13": lambda: series_classification_choice("10007-13", expression("4*(-1)**n/sqrt(n + 9)"), 1),
   "10007-14": lambda: series_classification_choice("10007-14", expression("9*(-1)**(n + 1)*n/(n + 4)"), 2),
   "10007-15": lambda: series_classification_choice("10007-15", expression("9*(-1)**n/(n + 6)**(4/3)"), 1),
   "10007-16": lambda: series_classification_choice("10007-16", expression("8*(-1)**n/(n + 1)**3"), 2),
   "10007-17": lambda: series_classification_choice("10007-17", expression("5*(-1)**(n + 1)/(n + 8)**(4/3)"), 2),
   "10007-18": lambda: series_classification_choice("10007-18", expression("9*(-1)**n*n/(n + 9)"), 2),
   "10007-19": lambda: series_classification_choice("10007-19", expression("3*(-1)**n*n/(n + 8)"), 2),
   "10007-20": lambda: series_classification_choice("10007-20", expression("8*(-1)**n/(n + 4)"), 2),
   "10007-21": lambda: series_classification_choice("10007-21", expression("(-1)**(n + 1)/(n + 3)**3"), 1),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
