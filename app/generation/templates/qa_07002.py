"""BC-QA-07002, the pattern of a slope field read from its differential equation: zero slope locus and slope signs."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "locus", "type": "label", "role": "difficulty", "domain": {"values": ["line", "parabola"]}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "intercept", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "orientation", "type": "integer", "role": "safe", "domain": {"values": [-1, 1]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "letters", "type": "label", "role": "safe", "domain": {"values": ["xy", "ty", "tP"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "power", "expression": "1 if locus == 'line' else 2"},
   ],
   "invariants": [
      "slope != 0",
      "len(key) > 60",
   ],
   "dial_bindings": [
      {"parameter": "locus", "difficulty_factor_id": "BC-DF-01", "settings": {"line": "off", "parabola": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["locus", "slope", "intercept", "orientation", "scale", "letters"]},
   ],
   "notes": "The right side is s q (y - m x^p - b) with p = 1 or 2, so the zero slope locus is y = m x^p + b and the sign of the slope is the sign of s on each side. The slope m is never 0, so the locus always depends on x and differs from the horizontal line y = b.",
}

LETTERS = {"xy": ("x", "y"), "ty": ("t", "y"), "tP": ("t", "P")}


def _pattern(locus_text, positive_text, negative_text):
   return (
      f"The segments are horizontal exactly along {locus_text}, have positive slope where {positive_text}, and have "
      f"negative slope where {negative_text}."
   )


def _regions(dependent, boundary, orientation):
   above = math(f"{tex(dependent)} > {tex(boundary)}")
   below = math(f"{tex(dependent)} < {tex(boundary)}")

   return (above, below) if orientation > 0 else (below, above)


def build(names):
   input_letter, output_letter = LETTERS[names["letters"]]
   x_symbol = sympy.Symbol(input_letter)
   y_symbol = sympy.Symbol(output_letter)
   power = int(names["power"])
   slope = int(names["slope"])
   intercept = int(names["intercept"])
   orientation = int(names["orientation"])
   scale = int(names["scale"])

   boundary = slope * x_symbol**power + intercept
   right_side = sympy.expand(orientation * scale * (y_symbol - boundary))
   equation = rf"\frac{{d{output_letter}}}{{d{input_letter}}} = {tex(right_side)}"
   shape = "line" if power == 1 else "parabola"
   locus_text = f"the {shape} {math(f'{output_letter} = {tex(boundary)}')}"
   positive_text, negative_text = _regions(y_symbol, boundary, orientation)

   stem = (
      f"Consider the differential equation {math(equation)}. Without drawing it, describe the field of slope segments "
      "for this equation: where the segments are horizontal, where they have positive slope, and where they have "
      "negative slope."
   )

   key_label = _pattern(locus_text, positive_text, negative_text)
   factor = orientation * scale
   factor_text = {1: "", -1: "-"}.get(factor, str(factor))

   steps = [
      Step(
         text=(
            f"A segment is horizontal where the right side is 0: {math(tex(right_side) + ' = 0')} exactly when "
            f"{math(f'{output_letter} = {tex(boundary)}')}, which is {locus_text}."
         ),
         point_type_id="BC-PT-99083",
         rule="zero slope locus",
      ),
      Step(
         text=(
            f"The right side equals {math(factor_text + rf'\left({tex(y_symbol - boundary)}\right)')}, so its "
            f"sign is positive where {positive_text} and negative where {negative_text}."
         ),
         point_type_id="BC-PT-99066",
         rule="sign of the slope on each side of the locus",
      ),
   ]

   x_dropped = sympy.Integer(intercept)
   x_dropped_positive, x_dropped_negative = _regions(y_symbol, x_dropped, orientation)
   swapped_boundary = slope * y_symbol**power + intercept
   swapped_positive, swapped_negative = _regions(x_symbol, swapped_boundary, orientation)

   distractors = [
      Distractor(
         error_path="BC-ERR-07013",
         derivation=f"the slope read as depending on {output_letter} alone, the {input_letter} term ignored, so the segments would match along horizontal lines",
         label=_pattern(f"the line {math(f'{output_letter} = {intercept}')}", x_dropped_positive, x_dropped_negative),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07010",
         derivation=f"each lattice point read with its coordinates exchanged, so {input_letter} and {output_letter} trade places",
         label=_pattern(
            f"the {shape} {math(f'{input_letter} = {tex(swapped_boundary)}')}", swapped_positive, swapped_negative,
         ),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-07016",
         derivation="the horizontal row located but the tilt on each side taken from the look of a familiar field instead of from a computed slope",
         label=_pattern(locus_text, negative_text, positive_text),
         mechanism="sign_error",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="describe",
   )
