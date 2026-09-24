"""BC-QA-08003, total distance travelled by a particle on a line whose velocity changes sign twice."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "size", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["right_first", "left_first"]}},
      {"name": "first_zero", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "overrun", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "3/2", "2", "5/2"]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["particle", "bead", "cart"]}},
      {"name": "units", "type": "label", "role": "safe", "domain": {"values": ["meters", "feet", "centimeters"]}},
      {"name": "framing", "type": "label", "role": "safe", "domain": {"values": ["bare", "context"]}},
   ],
   "constraints": [
      "net_shape < 0 if direction == 'right_first' else net_shape > 0 and middle_shape > last_shape",
   ],
   "derived": [
      {"name": "second_zero", "expression": "first_zero + gap"},
      {"name": "end_time", "expression": "first_zero + gap + overrun"},
      {"name": "net_shape", "expression": "end_time**3 / 3 - (first_zero + second_zero) * end_time**2 / 2 + first_zero * second_zero * end_time"},
      {"name": "middle_shape", "expression": "gap**3 / 6"},
      {"name": "last_shape", "expression": "overrun**3 / 3 + gap * overrun**2 / 2"},
   ],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-12", "settings": {"right_first": "off", "left_first": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["size", "direction", "first_zero", "gap", "overrun"]},
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["size", "direction", "first_zero", "gap", "overrun", "context", "units"]},
   ],
   "notes": "The velocity is a multiple of (t - first_zero)(t - second_zero), so it changes sign at two interior times. The constraint makes the displacement negative in both directions (net_shape is the displacement of the monic shape), so its absolute value is a separate distractor; when the particle moves left first, the middle lobe also outweighs the last one, so splitting only at the first zero gives a value apart from the others.",
}

OBJECTS = {"particle": "A particle", "bead": "A bead on a wire", "cart": "A cart on a straight track"}

t = sympy.Symbol("t")


def build(names):
   size = names["size"]
   first_zero = names["first_zero"]
   second_zero = names["second_zero"]
   end_time = names["end_time"]
   is_left_first = names["direction"] == "left_first"
   is_context = names["framing"] == "context"
   leading = -size if is_left_first else size

   velocity = sympy.expand(leading * (t - first_zero) * (t - second_zero))
   antiderivative = sympy.integrate(velocity, t)

   def change(low, high):
      return antiderivative.subs(t, high) - antiderivative.subs(t, low)

   first_piece = change(0, first_zero)
   middle_piece = change(first_zero, second_zero)
   last_piece = change(second_zero, end_time)
   distance = abs(first_piece) + abs(middle_piece) + abs(last_piece)
   displacement = first_piece + middle_piece + last_piece
   split_once = abs(first_piece) + abs(middle_piece + last_piece)

   window = rf"0 \le t \le {tex_f(end_time)}"
   velocity_tex = tex_f(velocity)

   if is_context:
      units = names["units"]
      stem = (
         f"{OBJECTS[names['context']]} moves along a line so that its velocity at time t seconds is "
         f"{math('v(t) = ' + velocity_tex)} {units} per second. Find the exact total distance, in {units}, "
         f"that it travels over the time interval {math(window)}."
      )
      representation = "BC-REP-05"
      key_units = units
   else:
      stem = (
         f"A particle moves along the x-axis with velocity {math('v(t) = ' + velocity_tex)} for "
         f"{math(r't \ge 0')}. Find the exact total distance the particle travels over the time interval "
         f"{math(window)}."
      )
      representation = "BC-REP-01"
      key_units = None

   factored = tex_f(leading * sympy.Mul(t - first_zero, t - second_zero, evaluate=False))

   def piece_text(low, high, value):
      integral = rf"\int_{{{tex_f(low)}}}^{{{tex_f(high)}}} v(t)\,dt = {tex_f(value)}"

      return f"On {math(rf'[{tex_f(low)}, {tex_f(high)}]')}, {math(integral)}."

   steps = [
      Step(
         text=(
            f"Total distance is {math(rf'\int_{{0}}^{{{tex_f(end_time)}}} \left|v(t)\right|\,dt')}. Since "
            f"{math('v(t) = ' + factored)}, the velocity changes sign at {math('t = ' + tex_f(first_zero))} and "
            f"{math('t = ' + tex_f(second_zero))}, so the interval is split there."
         ),
         rule="total distance as the integral of speed",
      ),
      Step(text=piece_text(0, first_zero, first_piece), value=first_piece, rule="definite integral of a polynomial"),
      Step(text=piece_text(first_zero, second_zero, middle_piece), value=middle_piece, rule="definite integral of a polynomial"),
      Step(text=piece_text(second_zero, end_time, last_piece), value=last_piece, rule="definite integral of a polynomial"),
      Step(
         text=(
            f"Add the sizes of the three pieces: the total distance is "
            f"{math(f'{tex_f(abs(first_piece))} + {tex_f(abs(middle_piece))} + {tex_f(abs(last_piece))} = {tex_f(distance)}')}."
         ),
         value=distance,
         rule="sum of absolute changes",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-08009",
         derivation="the velocity itself integrated over the whole interval in place of its absolute value",
         value=displacement,
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-08010",
         derivation="the velocity integrated over the whole interval with one absolute value taken at the end",
         value=abs(displacement),
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-99010",
         derivation=f"the interval split only at t = {first_zero}, so the last two pieces net against each other",
         value=split_once,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=distance, units=key_units),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="no_calculator",
      command_verb="find",
   )
