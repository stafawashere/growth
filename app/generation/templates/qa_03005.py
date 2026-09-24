"""BC-QA-03005, horizontal tangent lines on an implicitly defined cubic with a singular point."""
from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-03005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "spread", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "opening", "type": "label", "role": "difficulty", "domain": {"values": ["left", "right"]}},
      {"name": "h", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "v", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
   ],
   "constraints": [],
   "derived": [
      {"name": "shift", "expression": "3 * stretch * spread**2 if opening == 'left' else -3 * stretch * spread**2"},
   ],
   "invariants": [
      "len(key) > 0",
      "has_points == (opening == 'left')",
   ],
   "dial_bindings": [
      {"parameter": "opening", "difficulty_factor_id": "BC-DF-09", "settings": {"left": "off", "right": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["stretch", "spread", "opening", "h", "v"]},
   ],
   "notes": (
      "The curve stretch (y - v)^2 = (x - h)^2 (x - h + shift) has a singular point at (h, v), where both parts of "
      "dy/dx vanish. With shift = 3 stretch spread^2 the numerator's other root gives two points with horizontal "
      "tangents; with the opposite sign that root gives a negative square and there are none. The two cases are "
      "drawn equally often."
   ),
}


def _shifted(variable, amount):
   if amount == 0:
      return variable

   if amount > 0:
      return f"{variable} - {amount}"

   return f"{variable} + {-amount}"


def _point(x_value, y_value):
   return math(f"({x_value}, {y_value})")


def _points_sentence(points):
   if len(points) == 1:
      return f"The tangent line is horizontal only at {_point(*points[0])}."

   listed = [_point(*point) for point in points]
   joined = ", ".join(listed[:-1]) + f" and {listed[-1]}"

   return f"The tangent line is horizontal at {joined}."


NONE_SENTENCE = "No point of the curve has a horizontal tangent line."


def build(names):
   stretch = int(names["stretch"])
   spread = int(names["spread"])
   opens_left = names["opening"] == "left"
   h = int(names["h"])
   v = int(names["v"])
   shift = 3 * stretch * spread**2 if opens_left else -3 * stretch * spread**2

   critical_x = h - 2 * shift // 3
   height = 2 * stretch * spread**3
   denominator_x = h - shift

   stretch_text = "" if stretch == 1 else str(stretch)
   x_part = _shifted("x", h)
   curve = rf"{stretch_text}\left({_shifted('y', v)}\right)^{{2}} = \left({x_part}\right)^{{2}}\left({_shifted('x', h - shift)}\right)"
   numerator = rf"\left({x_part}\right)\left({_shifted('3x', 3 * h - 2 * shift)}\right)"
   derivative = rf"\frac{{dy}}{{dx}} = \frac{{{numerator}}}{{{2 * stretch}\left({_shifted('y', v)}\right)}}"

   stem = (
      f"A curve is defined by {math(curve)}, and its derivative is {math(derivative)}. Find every point of the "
      "curve at which the tangent line is horizontal, or show that there is none."
   )

   square_value = f"{4 * stretch**2 * spread**6}" if opens_left else f"-{4 * stretch**2 * spread**6}"
   steps = [
      Step(
         text=(
            "A horizontal tangent needs the numerator of dy/dx to be 0 and the denominator to be nonzero. "
            f"The numerator is 0 when {math(f'x = {h}')} or {math(f'x = {critical_x}')}."
         ),
         rule="numerator of dy/dx equal to zero",
      ),
      Step(
         text=(
            f"On the curve, {math(f'x = {h}')} forces {math(f'y = {v}')}, where the denominator is also 0, so "
            f"{_point(h, v)} is not a point with a horizontal tangent."
         ),
         rule="check the denominator",
      ),
   ]

   if opens_left:
      key_points = [(critical_x, v + height), (critical_x, v - height)]
      key_label = _points_sentence(key_points)
      steps.append(Step(
         text=(
            f"Substituting {math(f'x = {critical_x}')} into the curve gives {math(rf'\left({_shifted("y", v)}\right)^{{2}} = {square_value}')}, "
            f"so {math(f'y = {v + height}')} or {math(f'y = {v - height}')}, and the denominator is nonzero at both points."
         ),
         rule="substitute into the curve",
      ))
      extra_label = _points_sentence([(h, v)] + key_points)
   else:
      key_points = []
      key_label = NONE_SENTENCE
      steps.append(Step(
         text=(
            f"Substituting {math(f'x = {critical_x}')} into the curve gives {math(rf'\left({_shifted("y", v)}\right)^{{2}} = {square_value}')}, "
            "which no real y satisfies. There is no point of the curve with a horizontal tangent line."
         ),
         rule="substitute into the curve",
      ))
      extra_label = _points_sentence([(h, v)])

   distractors = [
      Distractor(
         error_path="BC-ERR-05057",
         derivation=f"the point ({h}, {v}), where the numerator is 0, kept without checking that the denominator is also 0 there",
         label=extra_label,
      ),
      Distractor(
         error_path="BC-ERR-03012",
         derivation="the denominator set to 0 instead of the numerator, which finds the points where y = v",
         label=_points_sentence([(h, v), (denominator_x, v)]),
      ),
      Distractor(
         error_path="BC-ERR-03013",
         derivation=f"the numerator's roots paired with y = {v} and reported without substituting into the curve",
         label=_points_sentence([(h, v), (critical_x, v)]),
      ),
   ]

   distractors[0].mechanism = "theorem_condition_ignored"
   distractors[1].mechanism = "reversed_quantities"
   distractors[2].mechanism = "theorem_condition_ignored"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"has_points": opens_left},
   )
