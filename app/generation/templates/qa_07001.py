"""BC-QA-07001, the solution curve through a point on a supplied slope field, described across the window."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark, slope_segments, tex

ARCHETYPE_ID = "BC-QA-07001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "stability", "type": "label", "role": "difficulty", "domain": {"values": ["stable", "unstable"]}},
      {"name": "offset", "type": "integer", "role": "difficulty", "domain": {"values": [-2, -1, 1, 2]}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 4, "step": 1}},
      {"name": "start_x", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "rate", "type": "rational", "role": "safe", "domain": {"values": ["1/3", "1/2", "1", "2"]}},
      {"name": "letters", "type": "label", "role": "safe", "domain": {"values": ["xy", "ty", "tP"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "start_y", "expression": "level + offset"},
   ],
   "invariants": [
      "start_y != level",
      "abs(start_y - level) <= 2",
   ],
   "dial_bindings": [
      {"parameter": "stability", "difficulty_factor_id": "BC-DF-01", "settings": {"stable": "off", "unstable": "low"}},
      {"parameter": "offset", "difficulty_factor_id": "BC-DF-01", "settings": {"-2": "off", "-1": "low", "1": "low", "2": "off"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-07", "figure_kind": "slope_field", "requires": ["stability", "offset", "level", "start_x", "rate", "letters"]},
   ],
   "notes": "The equation is dy/dx = r(L - y) (stable) or r(y - L) (unstable), with a row of horizontal segments at y = L inside the window. The initial point is one or two units off that row, so its curve never meets it; an offset of one unit sits closer to the level and was bound as the harder read.",
}

LETTERS = {"xy": ("x", "y"), "ty": ("t", "y"), "tP": ("t", "P")}


def _describe(point_text, trend, approach, ending):
   return f"The solution curve through {point_text} {trend} across the whole window, {approach}, {ending}."


def build(names):
   stable = names["stability"] == "stable"
   level = int(names["level"])
   offset = int(names["offset"])
   start_x = int(names["start_x"])
   start_y = int(names["start_y"])
   rate = sympy.Rational(names["rate"])
   input_letter, output_letter = LETTERS[names["letters"]]
   x_symbol = sympy.Symbol(input_letter)
   y_symbol = sympy.Symbol(output_letter)

   right_side = rate * (level - y_symbol) if stable else rate * (y_symbol - level)
   slope_at_start = right_side.subs(y_symbol, start_y)
   rising = slope_at_start > 0
   side = "above" if offset > 0 else "below"
   trend = "rises" if rising else "falls"
   opposite_trend = "falls" if rising else "rises"
   level_text = math(f"{output_letter} = {level}")
   point_text = math(f"({start_x}, {start_y})")

   if stable:
      approach = f"flattening toward the line {level_text} from {side} as {input_letter} increases"
      reversed_approach = f"flattening toward the line {level_text} from {side} as {input_letter} decreases"
      reaches = f"reaching the line {level_text} at a finite value of {input_letter} and then running along it"
   else:
      approach = f"flattening toward the line {level_text} from {side} as {input_letter} decreases"
      reversed_approach = f"flattening toward the line {level_text} from {side} as {input_letter} increases"
      reaches = f"leaving the line {level_text} at a finite value of {input_letter} after running along it"

   key_label = _describe(point_text, trend, approach, f"and never touches the line {level_text}")

   equation = rf"\frac{{d{output_letter}}}{{d{input_letter}}} = {tex(right_side)}"
   stem = (
      f"The slope field for the differential equation {math(equation)} is shown. Describe the solution curve through "
      f"the point {point_text} across the whole window of the slope field."
   )

   difference_text = f"{level} - {output_letter}" if stable else f"{output_letter} - {level}"
   alt_right_side = f"{names['rate']} times ({difference_text})"
   xs = range(-3, 4)
   ys = range(level - 3, level + 4)
   field = figure(
      "slope_field",
      domain=(-3.5, 3.5),
      range_=(level - 3.5, level + 3.5),
      marks=slope_segments(right_side, x_symbol, y_symbol, xs, ys, half_length=0.3) + [point_mark(start_x, start_y)],
      labels=[label(f"({start_x}, {start_y})", start_x + 0.15, start_y + 0.3)],
      axis_titles=(input_letter, output_letter),
      alt=(
         f"Slope field for d{output_letter}/d{input_letter} = {alt_right_side} at every lattice point with {input_letter} "
         f"from -3 to 3 and {output_letter} from {level - 3} to {level + 3}. The segments are horizontal along "
         f"{output_letter} = {level}; the point ({start_x}, {start_y}) is marked."
      ),
   )

   sign_word = "positive" if rising else "negative"
   steps = [
      Step(
         text=(
            f"At {point_text} the slope is {math(tex(slope_at_start))}, which is {sign_word}, and every segment "
            f"{side} the line {level_text} has that sign, so the curve {trend} through the point."
         ),
         rule="slope from the right side of the equation",
      ),
      Step(
         text=(
            f"The segments along {level_text} are horizontal, so that line is itself a solution and the curve cannot cross "
            f"or reach it; the segments get flatter near it, so the curve bends toward it on one side and away on the other."
         ),
         rule="equilibrium solution",
      ),
      Step(
         text=f"Following the segments in both directions to the edges of the window, the curve {trend}, {approach}.",
         point_type_id="BC-PT-99065",
         rule="solution curve follows the field",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07015",
         derivation=f"the curve kept moving in its starting direction straight through the row of horizontal segments at {output_letter} = {level}",
         label=_describe(point_text, trend, f"passing through the line {level_text}", "and continuing on its other side"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07014",
         derivation="the curve drawn against the segments near the point, with the wrong direction of change",
         label=_describe(point_text, opposite_trend, reversed_approach, f"and never touches the line {level_text}"),
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-99024",
         derivation=f"the curve drawn onto the equilibrium row, sitting on {output_letter} = {level} instead of approaching it",
         label=_describe(point_text, trend, reaches, "so it meets the line in a corner"),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-07",
      calculator_status="no_calculator",
      figure=field,
      command_verb="describe",
   )
