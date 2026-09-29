"""BC-QA-05014, every critical point of a function, including an input where the derivative fails to exist."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-05014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "shape", "type": "label", "role": "difficulty", "domain": {"values": ["cusp", "vertical", "corner"]}},
      {"name": "root", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "pole", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "multiplier", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
   ],
   "constraints": [
      "root != pole",
      "shape != 'vertical' or (3 * root - pole) % 2 == 0",
   ],
   "derived": [
      {"name": "cusp_zero", "expression": "3 * root - 2 * pole"},
      {"name": "vertical_zero", "expression": "(3 * root - pole) / 2"},
   ],
   "invariants": [
      "cusp_zero != root and cusp_zero != pole",
      "vertical_zero != root and vertical_zero != pole",
   ],
   "dial_bindings": [
      {"parameter": "shape", "difficulty_factor_id": "BC-DF-06", "settings": {"cusp": "medium", "vertical": "medium", "corner": "low"}},
      {"parameter": "shape", "difficulty_factor_id": "BC-DF-17", "settings": {"cusp": "off", "vertical": "off", "corner": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["shape", "root", "pole", "multiplier"]},
   ],
   "notes": "f(x) = k (x - r)^(2/3)/(x - d), k (x - r)^(1/3)/(x - d) or k |x - r|/(x - d), defined for x != d. The derivative is zero at 3r - 2d, at (3r - d)/2, or nowhere; it fails to exist at x = r (cusp, vertical tangent or corner) where f is defined, and at x = d, which is outside the domain and so is not a critical point.",
}

x = sympy.Symbol("x")
THIRD = sympy.Rational(1, 3)
PRIME = "f'(x)"


def _points(values):
   ordered = sorted(int(value) for value in values)

   if len(ordered) == 1:
      return f"The only critical point of f is x = {ordered[0]}."

   if len(ordered) == 2:
      return f"The critical points of f are x = {ordered[0]} and x = {ordered[1]}."

   listed = ", ".join(f"x = {value}" for value in ordered[:-1])

   return f"The critical points of f are {listed} and x = {ordered[-1]}."


def _function(shape, multiplier, root, pole):
   if shape == "cusp":
      return multiplier * (x - root) ** (2 * THIRD) / (x - pole)

   if shape == "vertical":
      return multiplier * (x - root) ** THIRD / (x - pole)

   return multiplier * sympy.Abs(x - root) / (x - pole)


def _derivative_text(shape, multiplier, root, pole, zero):
   if shape == "cusp":
      derivative = multiplier * (zero - x) / (3 * (x - root) ** THIRD * (x - pole) ** 2)
      failure = "the factor in the denominator is 0 while the numerator is not, so the graph of f has a cusp there"
   elif shape == "vertical":
      derivative = 2 * multiplier * (zero - x) / (3 * (x - root) ** (2 * THIRD) * (x - pole) ** 2)
      failure = "the factor in the denominator is 0 while the numerator is not, so the graph of f has a vertical tangent there"
   else:
      right = multiplier * (root - pole) / (x - pole) ** 2
      pieces = rf"f'(x) = {tex(right)} \text{{ for }} x > {root} \text{{ and }} f'(x) = {tex(-right)} \text{{ for }} x < {root}"
      opening = f"For x other than {root} and {pole}, {math(pieces)}. The derivative is never 0."
      failure = "the one-sided derivatives there have opposite signs, so the graph of f has a corner there"

      return opening, failure

   opening = f"For x other than {root} and {pole}, the quotient and chain rules give {math(PRIME + ' = ' + tex(derivative))}."

   return opening, failure


def build(names):
   shape = names["shape"]
   root = int(names["root"])
   pole = int(names["pole"])
   multiplier = int(names["multiplier"])
   has_zero = shape != "corner"
   zero = int(names["cusp_zero"]) if shape == "cusp" else int(names["vertical_zero"]) if shape == "vertical" else None

   function = _function(shape, multiplier, root, pole)
   power_note = ""

   if shape == "cusp":
      power_note = f", where {math(tex((x - root) ** (2 * THIRD)))} is the square of the real cube root"
   elif shape == "vertical":
      power_note = f", where {math(tex((x - root) ** THIRD))} is the real cube root"

   excluded = rf"x \ne {pole}"
   stem = f"Let {math('f(x) = ' + tex(function))} for {math(excluded)}{power_note}. Find all critical points of f."

   opening, failure = _derivative_text(shape, multiplier, root, pole, zero)
   steps = [Step(text=opening, rule="quotient and chain rules")]

   if has_zero:
      steps.append(Step(
         text=f"Setting {math(PRIME + ' = 0')} gives x = {zero}, and f is defined there, so x = {zero} is a critical point.",
         point_type_id="BC-PT-99013",
         rule="critical point where the derivative is zero",
      ))
   else:
      steps.append(Step(
         text=f"The numerator {multiplier * (root - pole)} is never 0, so {math(PRIME + ' = 0')} has no solution.",
         point_type_id="BC-PT-99013",
         rule="critical point where the derivative is zero",
      ))

   steps.append(Step(
      text=(
         f"At x = {root} the function is defined, {math(f'f({root}) = 0')}, and {failure}; so the derivative fails to exist at an "
         f"input in the domain and x = {root} is a critical point. At x = {pole} the derivative also fails to exist, but f is not "
         f"defined there, so x = {pole} is not a critical point."
      ),
      rule="critical point where the derivative fails to exist",
   ))

   if has_zero:
      key_label = _points([zero, root])
      distractors = [
         Distractor("BC-ERR-05011", f"only the zero of f' kept, and the input {root} where f' fails to exist skipped", label=_points([zero]), mechanism="conceptual_confusion"),
         Distractor("BC-ERR-05010", f"the excluded input {pole}, where f' fails to exist but f is undefined, kept as a critical point", label=_points([zero, root, pole]), mechanism="theorem_condition_ignored"),
         Distractor("BC-ERR-05010", f"the excluded input {pole} taken as the place where f' fails to exist, and the cusp or tangent at {root} missed", label=_points([zero, pole]), mechanism="compound"),
      ]
   else:
      key_label = _points([root])
      distractors = [
         Distractor("BC-ERR-05011", "f' is never 0, so no critical point was reported, with the corner skipped", label="f has no critical points.", mechanism="conceptual_confusion"),
         Distractor("BC-ERR-05010", f"the excluded input {pole} kept beside the corner", label=_points([root, pole]), mechanism="theorem_condition_ignored"),
         Distractor("BC-ERR-05010", f"the excluded input {pole} reported as the only place where f' fails to exist, with the corner missed", label=_points([pole]), mechanism="compound"),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
