"""BC-QA-10008, the alternating series error bound for a partial sum of a Maclaurin series at a point."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import x

ARCHETYPE_ID = "BC-QA-10008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "function", "type": "label", "role": "difficulty", "domain": {"values": ["exp", "sin", "cos", "atan"]}},
      {"name": "last", "type": "integer", "role": "difficulty", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "point", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1/3", "2/3", "1/4", "3/4", "1/5", "2/5", "3/5", "4/5", "1/6", "5/6", "3/7", "4/7", "5/7", "6/7", "5/8", "7/8", "7/9", "8/9"]}},
      {"name": "multiple", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 12, "step": 1}},
   ],
   "constraints": [
      "point ** order / divisor > 1 / 100000",
      "function != 'exp' or last >= 2",
   ],
   "derived": [
      {"name": "omitted", "expression": "last + 1"},
      {"name": "order", "expression": "omitted if function == 'exp' else (2 * omitted if function == 'cos' else 2 * omitted + 1)"},
      {"name": "divisor", "expression": "2 * omitted + 1 if function == 'atan' else [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800, 479001600, 6227020800, 87178291200, 1307674368000, 20922789888000][order]"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "function", "difficulty_factor_id": "BC-DF-08", "settings": {"exp": "low", "sin": "medium", "cos": "medium", "atan": "medium"}},
      {"parameter": "last", "difficulty_factor_id": "BC-DF-08", "settings": {"1": "low", "2": "low", "3": "low", "4": "low", "5": "low", "6": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["function", "last", "point", "multiple"]},
   ],
   "notes": "The Maclaurin series of e^(-x), sin x, cos x or arctan x times a whole-number multiple, evaluated at a rational point between 0 and 1, alternates with terms decreasing to 0, so the error of the partial sum through n = last is at most the size of the n = last + 1 term. That term is kept above 1/100000 so every option is a readable fraction.",
}

SERIES = {
   "exp": ("e^{-x}", lambda index: (-1) ** index * x**index / sympy.factorial(index), r"\frac{(-1)^n x^n}{n!}"),
   "sin": (r"\sin x", lambda index: (-1) ** index * x ** (2 * index + 1) / sympy.factorial(2 * index + 1), r"\frac{(-1)^n x^{2n+1}}{(2n+1)!}"),
   "cos": (r"\cos x", lambda index: (-1) ** index * x ** (2 * index) / sympy.factorial(2 * index), r"\frac{(-1)^n x^{2n}}{(2n)!}"),
   "atan": (r"\arctan x", lambda index: (-1) ** index * x ** (2 * index + 1) / (2 * index + 1), r"\frac{(-1)^n x^{2n+1}}{2n+1}"),
}


def build(names):
   function, term_at, general_tex = SERIES[names["function"]]
   last = int(names["last"])
   point = names["point"]
   multiple = names["multiple"]
   function_tex = function if multiple == 1 else f"{multiple} {function}"
   base_term_at = term_at

   def term_at(index):
      return multiple * base_term_at(index)

   lead = "" if multiple == 1 else f"{multiple} "
   general_tex = rf"{lead}{general_tex}"

   def size(index, at=point):
      return sympy.Abs(term_at(index).subs(x, at))

   bound = size(last + 1)
   positive_x = sympy.Symbol("x", positive=True)
   omitted_general = sympy.Abs(term_at(last + 1).subs(x, positive_x))
   series = rf"\sum_{{n=0}}^{{\infty}} {general_tex}"
   partial = rf"S_{{{last}}} = \sum_{{n=0}}^{{{last}}} {general_tex}"

   stem = (
      f"The Maclaurin series for {math('f(x) = ' + function_tex)} is {math(series)}. Let {math(partial)} evaluated at "
      f"{math(f'x = {tex(point)}')} approximate {math(f'f({tex(point)})')}. Use the alternating series error bound to find the "
      f"exact value of an upper bound for {math(rf'\left|f({tex(point)}) - S_{{{last}}}\right|')}."
   )
   steps = [
      Step(text=f"At {math(f'x = {tex(point)}')} the series alternates, and since {math(f'0 < x < 1')} the sizes of its terms decrease to 0, so the alternating series error bound applies.", rule="conditions of the alternating series error bound"),
      Step(text=f"The partial sum stops at {math(f'n = {last}')}, so the first omitted term is the {math(f'n = {last + 1}')} term, of size {math(tex(omitted_general))} for {math('x > 0')}.", point_type_id="BC-PT-99040", rule="first omitted term"),
      Step(text=f"At {math(f'x = {tex(point)}')} that size is {math(tex(bound))}, so {math(rf'\left|f({tex(point)}) - S_{{{last}}}\right| \le {tex(bound)}')}.", value=bound, point_type_id="BC-PT-99041", rule="error bound inequality"),
   ]
   distractors = [
      Distractor("BC-ERR-10024", f"the n = {last} term, already inside the partial sum, used as the bound", value=size(last), mechanism="wrong_limits"),
      Distractor("BC-ERR-10024", f"the n = {last + 2} term, one past the first omitted term, used as the bound", value=size(last + 2), mechanism="wrong_limits"),
      Distractor("BC-ERR-10025", "the first omitted term evaluated at x = 1 instead of at the given input", value=size(last + 1, sympy.Integer(1)), mechanism="algebra_slip"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=bound),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
   )
