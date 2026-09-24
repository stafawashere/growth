"""BC-QA-04008, a tangent line approximation, with an over or under estimate judgement from concavity."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-04008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "curvature", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "anchor", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "height", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "step", "type": "rational", "role": "safe", "domain": {"values": ["-1/2", "-1/5", "-1/10", "1/10", "1/5", "1/2"]}},
      {"name": "judgement", "type": "label", "role": "difficulty", "domain": {"values": ["off", "on"]}},
   ],
   "constraints": [
      "slope != 0",
      "estimate != 0",
      "slope != estimate",
      "distinct([estimate, height, far_slope_estimate, exchanged_estimate])",
      "judgement == 'off' or curvature * slope < 0",
   ],
   "derived": [
      {"name": "slope", "expression": "curvature * anchor**2 + offset"},
      {"name": "estimate", "expression": "height + (curvature * anchor**2 + offset) * step"},
      {"name": "far_slope_estimate", "expression": "height + (curvature * (anchor + step)**2 + offset) * step"},
      {"name": "exchanged_estimate", "expression": "(curvature * anchor**2 + offset) + height * step"},
   ],
   "invariants": [
      "anchor + step > 0",
      "judgement == 'off' or exact(estimate)",
   ],
   "dial_bindings": [
      {"parameter": "judgement", "difficulty_factor_id": "BC-DF-10", "settings": {"off": "off", "on": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["curvature", "offset", "anchor", "height", "step", "judgement"]},
   ],
   "notes": "f'(x) = c x^2 + m, so f''(x) = 2 c x keeps the sign of c for x > 0, which holds on the whole interval between the anchor and the nearby input. With a judgement, the slope at the anchor has the sign opposite to c, so a verdict read from the sign of f' is wrong.",
}

x = sympy.Symbol("x")


def _decimal(value):
   """A rational whose denominator divides a power of ten, written out exactly as a decimal."""
   value = sympy.Rational(value)

   if value.q == 1:
      return str(value.p)

   places = 0

   while (value * 10**places).q != 1:
      places += 1

   scaled = abs(value.p * 10**places // value.q)
   digits = str(scaled).rjust(places + 1, "0")
   sign = "-" if value < 0 else ""

   return f"{sign}{digits[:-places]}.{digits[-places:]}"


def _verdict_label(estimate, verdict, reason):
   return f"The approximation is {math(_decimal(estimate))}, and it is an {verdict}, because {reason}."


def _line_tex(height, slope, anchor):
   size = abs(slope)
   coefficient = "" if size == 1 else tex(size)
   joiner = "+" if slope > 0 else "-"

   return f"y = {height} {joiner} {coefficient}(x - {anchor})"


def build(names):
   curvature = int(names["curvature"])
   anchor = int(names["anchor"])
   height = int(names["height"])
   step = sympy.Rational(names["step"])
   nearby = anchor + step
   nearby_text = _decimal(nearby)
   derivative = curvature * x**2 + names["offset"]
   slope = derivative.subs(x, anchor)
   far_slope = derivative.subs(x, nearby)
   estimate = height + slope * step
   second_derivative = sympy.diff(derivative, x)
   with_judgement = names["judgement"] == "on"

   derivative_statement = "f'(x) = " + tex(derivative)
   stem = (
      f"Let f be a twice-differentiable function with {math(f'f({anchor}) = {height}')} and {math(derivative_statement)} "
      f"for all x. Use the line tangent to the graph of f at x = {anchor} to approximate {math(f'f({nearby_text})')}."
   )

   if with_judgement:
      stem += (
         f" Is this approximation an overestimate or an underestimate of {math(f'f({nearby_text})')}? Give a reason "
         "for the answer."
      )
   else:
      stem += " Give the exact value."

   slope_statement = f"f'({anchor}) = " + tex(slope)
   second_statement = "f''(x) = " + tex(second_derivative)
   line_tex = _line_tex(height, slope, anchor)
   steps = [
      Step(
         text=f"The slope of the tangent line is {math(slope_statement)}.",
         value=slope,
         point_type_id="BC-PT-99025",
         rule="slope of the tangent line from the derivative",
      ),
      Step(
         text=f"The tangent line at x = {anchor} is {math(line_tex)}.",
         point_type_id="BC-PT-99025",
         rule="point-slope form",
      ),
      Step(
         text=f"At x = {nearby_text}, {math(f'y = {height} + ({tex(slope)})({tex(step)}) = ' + tex(estimate))}.",
         value=estimate,
         point_type_id="BC-PT-99004",
         rule="evaluate the tangent line at the nearby input",
      ),
   ]

   concave_up = curvature > 0
   verdict = "underestimate" if concave_up else "overestimate"
   concavity_reason = (
      f"{math(second_statement)} is {'positive' if concave_up else 'negative'} for x > 0, "
      f"so the graph of f is concave {'up' if concave_up else 'down'} and lies {'above' if concave_up else 'below'} its tangent line there"
   )

   if with_judgement:
      steps.append(Step(
         text=(
            f"{math(second_statement)}, which is {'positive' if concave_up else 'negative'} "
            f"for every x between {anchor} and {nearby_text}. The graph is concave {'up' if concave_up else 'down'} there, so it "
            f"lies {'above' if concave_up else 'below'} the tangent line and the approximation is an {verdict}."
         ),
         point_type_id="BC-PT-99005",
         rule="concavity decides the direction of the error",
      ))
      increasing = slope > 0
      slope_verdict = "underestimate" if increasing else "overestimate"
      slope_reason = (
         f"{math(slope_statement)} is {'positive' if increasing else 'negative'}, "
         f"so f is {'increasing' if increasing else 'decreasing'} and its values {'rise above' if increasing else 'fall below'} the starting value f({anchor})"
      )
      distractors = [
         Distractor(
            error_path="BC-ERR-99020",
            derivation="the verdict decided from the sign of the first derivative, not from concavity",
            label=_verdict_label(estimate, slope_verdict, slope_reason),
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-04024",
            derivation=f"the tangent line evaluated at the point of tangency x = {anchor}, which returns f({anchor})",
            label=_verdict_label(sympy.Integer(height), verdict, concavity_reason),
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-04027",
            derivation=f"the slope taken as f'({nearby_text}) at the nearby input instead of f'({anchor})",
            label=_verdict_label(height + far_slope * step, verdict, concavity_reason),
            mechanism="algebra_slip",
         ),
      ]
      key = Key(form="statement", label=_verdict_label(estimate, verdict, concavity_reason))
   else:
      distractors = [
         Distractor(
            error_path="BC-ERR-04024",
            derivation=f"the tangent line evaluated at the point of tangency x = {anchor}, which returns f({anchor})",
            value=sympy.Integer(height),
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-04027",
            derivation=f"the slope taken as f'({nearby_text}) at the nearby input instead of f'({anchor})",
            value=height + far_slope * step,
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-04023",
            derivation=f"the point and the slope exchanged, {_line_tex(slope, height, anchor)}",
            value=slope + height * step,
            mechanism="reversed_quantities",
         ),
      ]
      key = Key(form="symbolic", value=estimate)

   return Instance(
      stem=stem,
      key=key,
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="approximate",
   )
