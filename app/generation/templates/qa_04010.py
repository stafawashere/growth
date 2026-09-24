"""BC-QA-04010, the position of a particle recovered from its velocity and one known position."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-04010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "cubic", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1, "exclude": [0]}},
      {"name": "quadratic", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "known_time", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "known_position", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["forward", "backward"]}},
   ],
   "constraints": [
      "target_time >= 0",
      "change != 0",
      "known_antiderivative != 0",
      "known_antiderivative != known_position",
      "known_position != 2 * change",
      "known_position != 2 * change + known_antiderivative",
      "known_position + change != 0",
   ],
   "derived": [
      {"name": "target_time", "expression": "known_time + gap if direction == 'forward' else known_time - gap"},
      {"name": "known_antiderivative", "expression": "cubic * known_time**3 + quadratic * known_time**2 + linear * known_time"},
      {"name": "target_antiderivative", "expression": "cubic * target_time**3 + quadratic * target_time**2 + linear * target_time"},
      {"name": "change", "expression": "target_antiderivative - known_antiderivative"},
   ],
   "invariants": [
      "exact(key)",
      "key == known_position + change",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-11", "settings": {"forward": "off", "backward": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["cubic", "quadratic", "linear", "known_time", "gap", "known_position", "direction"]},
   ],
   "notes": "The velocity is 3a t^2 + 2b t + c, so an antiderivative a t^3 + b t^2 + c t has integer values; the known time is never 0, so dropping the constant of integration gives a distinct wrong answer.",
}

t = sympy.Symbol("t")


def build(names):
   known_time = int(names["known_time"])
   target_time = int(names["target_time"])
   known_position = int(names["known_position"])
   antiderivative = names["cubic"] * t**3 + names["quadratic"] * t**2 + names["linear"] * t
   velocity = sympy.diff(antiderivative, t)
   change = antiderivative.subs(t, target_time) - antiderivative.subs(t, known_time)
   key_value = known_position + change

   stem = (
      f"A particle moves along the x-axis with velocity {math('v(t) = ' + tex(velocity))} meters per second, where t is "
      f"measured in seconds, for {math(r't \ge 0')}. At time t = {known_time} the position of the particle is "
      f"{math(f'x({known_time}) = {known_position}')} meters. Find the position of the particle at time t = {target_time}."
   )

   integral_tex = rf"\int_{{{known_time}}}^{{{target_time}}} v(t)\,dt"
   evaluation_tex = (
      rf"\left[{tex(antiderivative)}\right]_{{{known_time}}}^{{{target_time}}} = {tex(change)}"
   )
   position_tex = rf"x({target_time}) = x({known_time}) + {integral_tex} = {known_position} {'+' if change > 0 else '-'} {tex(abs(change))} = {tex(key_value)}"
   steps = [
      Step(
         text=f"Position changes by the integral of velocity, so {math(rf'x({target_time}) = x({known_time}) + {integral_tex}')}.",
         rule="position from velocity by accumulation",
      ),
      Step(
         text=f"An antiderivative of v is {math(tex(antiderivative))}, so {math(integral_tex + ' = ' + evaluation_tex)}.",
         value=change,
         rule="fundamental theorem of calculus",
      ),
      Step(
         text=f"Add the known position: {math(position_tex)} meters.",
         value=key_value,
         rule="add the initial position",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-08011",
         derivation=f"the integral of v from {known_time} to {target_time} reported as the position, with x({known_time}) never added",
         value=change,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-07026",
         derivation=f"x(t) written as the antiderivative {tex(antiderivative)} with no constant and evaluated at t = {target_time}",
         value=antiderivative.subs(t, target_time),
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-09021",
         derivation=f"the accumulation run the wrong way in time, x({known_time}) plus the integral from {target_time} to {known_time}",
         value=known_position - change,
         mechanism="wrong_limits",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value, units="meters"),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
