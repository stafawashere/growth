"""BC-QA-10016, the first nonzero terms and the general term of a Maclaurin series for c x^m f(kx)."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_h import polynomial_tex

ARCHETYPE_ID = "BC-QA-10016"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "base", "type": "label", "role": "difficulty", "domain": {"values": ["exp", "sin", "cos", "geometric"]}},
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "negative"]}},
      {"name": "count", "type": "integer", "role": "difficulty", "domain": {"values": [3, 4]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 7, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"values": [0, 1, 2, 3]}},
   ],
   "constraints": [
      "sign == 'positive' or base == 'exp' or base == 'geometric'",
   ],
   "derived": [],
   "invariants": [
      "base in ['exp', 'sin', 'cos', 'geometric']",
   ],
   "dial_bindings": [
      {"parameter": "base", "difficulty_factor_id": "BC-DF-06", "settings": {"exp": "low", "sin": "medium", "cos": "medium", "geometric": "low"}},
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-06", "settings": {"positive": "low", "negative": "medium"}},
      {"parameter": "count", "difficulty_factor_id": "BC-DF-02", "settings": {"3": "low", "4": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["base", "sign", "count", "scale", "coefficient", "power"]},
   ],
   "notes": "The function is c x^m f(kx) or c x^m f(-kx) with f one of e^x, sin x, cos x, 1/(1 - x); a negative argument is used only where it produces a new alternating factor. The general term starts at n = 0.",
}

# Each shape: the order of the kth term in terms of n, whether it alternates, whether it has a factorial.
SHAPES = {
   "exp": (1, 0, False, True),
   "sin": (2, 1, True, True),
   "cos": (2, 0, True, True),
   "geometric": (1, 0, False, False),
}

FUNCTION_TEX = {
   "exp": lambda argument: f"e^{{{argument}}}",
   "sin": lambda argument: rf"\sin\left({argument}\right)",
   "cos": lambda argument: rf"\cos\left({argument}\right)",
   "geometric": None,
}


def _linear(multiple, offset, shift=0):
   """The text of multiple (n + shift) + offset, simplified."""
   constant = multiple * shift + offset
   head = "n" if multiple == 1 else f"{multiple}n"

   if constant == 0:
      return head

   return f"{head}+{constant}"


def _general_tex(coefficient, scale, alternates, multiple, offset, power, has_factorial, raise_scale=True, shift=0):
   order = _linear(multiple, offset, shift)
   x_power = _linear(multiple, offset + power, shift)
   sign = f"(-1)^{{{_linear(1, 0, shift)}}}" if alternates else ""
   scale_part = f"{scale}^{{{order}}}" if raise_scale else str(scale)
   lead = "" if coefficient == 1 else f"{coefficient} \\cdot "
   numerator = " ".join(part for part in (f"{lead}{sign}".strip(), scale_part, f"x^{{{x_power}}}") if part)

   if has_factorial:
      factorial = f"{order}!" if order == "n" else f"({order})!"

      return rf"\frac{{{numerator}}}{{{factorial}}}"

   return numerator


def _coefficients(coefficient, scale, alternates, multiple, offset, power, has_factorial, count, raise_scale=True):
   """The first count nonzero terms as a coefficient list indexed by the power of x."""
   degree = multiple * (count - 1) + offset + power
   values = [sympy.Integer(0)] * (degree + 1)

   for index in range(count):
      order = multiple * index + offset
      sign = (-1) ** index if alternates else 1
      scale_factor = sympy.Integer(scale) ** order if raise_scale or order == 0 else scale
      factorial = sympy.factorial(order) if has_factorial else 1
      values[order + power] = sympy.Rational(coefficient * sign * scale_factor, factorial)

   return values


def _option(terms, general):
   return math(rf"{polynomial_tex(terms, 0)} + \cdots + {general} + \cdots")


def build(names):
   base = names["base"]
   count = int(names["count"])
   scale = int(names["scale"])
   coefficient = int(names["coefficient"])
   power = int(names["power"])
   is_negative = names["sign"] == "negative"
   multiple, offset, alternates, has_factorial = SHAPES[base]
   alternates = alternates or is_negative

   argument = f"{'-' if is_negative else ''}{scale}x"
   lead = "" if coefficient == 1 else str(coefficient)
   power_part = "" if power == 0 else ("x" if power == 1 else f"x^{{{power}}}")

   if base == "geometric":
      sign = "+" if is_negative else "-"
      function_tex = rf"\frac{{{lead}{power_part or ('' if lead else '1')}}}{{1 {sign} {scale}x}}"
      known = r"\frac{1}{1 - x}"
   else:
      function_tex = f"{lead}{' ' if lead and power_part else ''}{power_part} {FUNCTION_TEX[base](argument)}".strip()
      known = {"exp": "e^{x}", "sin": r"\sin x", "cos": r"\cos x"}[base]

   stem = (
      f"Let {math('f(x) = ' + function_tex)}. Find the first {count} nonzero terms and the general term of the Maclaurin "
      "series for f."
   )

   key_terms = _coefficients(coefficient, scale, alternates, multiple, offset, power, has_factorial, count)
   key_general = _general_tex(coefficient, scale, alternates, multiple, offset, power, has_factorial)
   key = _option(key_terms, key_general)

   steps = [
      Step(text=f"Start from the Maclaurin series for {math(known)} and replace x by {math(argument)}, raising the whole of {math(argument)} to each power.", rule="substitution into a known series"),
      Step(text=f"Multiply every term by {math((lead + ' ' + power_part).strip() or '1')}; the first {count} nonzero terms are {math(polynomial_tex(key_terms, 0))}.", rule="first nonzero terms"),
      Step(text=f"The general term is {math(key_general)}; putting n = 0, 1, 2 reproduces the terms above.", rule="general term"),
   ]

   if base == "exp":
      wrong = (alternates, False)
      wrong_how = "the series for e^x recalled without its factorials"
   elif base == "geometric":
      wrong = (not alternates, False)
      wrong_how = "the series for 1/(1 - x) recalled with alternating signs, as for 1/(1 + x)" if not is_negative else "the alternating factor from the negative argument lost"
   else:
      wrong = (False, True)
      wrong_how = f"the series for {'sin' if base == 'sin' else 'cos'} x recalled without its alternating signs"

   wrong_alternates, wrong_factorial = wrong
   distractors = [
      Distractor("BC-ERR-10040", wrong_how, label=_option(
         _coefficients(coefficient, scale, wrong_alternates, multiple, offset, power, wrong_factorial, count),
         _general_tex(coefficient, scale, wrong_alternates, multiple, offset, power, wrong_factorial),
      )),
      Distractor("BC-ERR-10041", f"x replaced by {argument} but {scale} not raised to the power of each term", label=_option(
         _coefficients(coefficient, scale, alternates, multiple, offset, power, has_factorial, count, raise_scale=False),
         _general_tex(coefficient, scale, alternates, multiple, offset, power, has_factorial, raise_scale=False),
      )),
      Distractor("BC-ERR-99018", "the general term written with n + 1 where n belongs, so at n = 0 it gives the second term rather than the first", label=_option(
         key_terms,
         _general_tex(coefficient, scale, alternates, multiple, offset, power, has_factorial, shift=1),
      )),
   ]

   for distractor in distractors:
      distractor.mechanism = "conceptual_confusion"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"base": base},
   )
