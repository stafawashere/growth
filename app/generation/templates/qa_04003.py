"""BC-QA-04003, the speed of a particle at an instant and whether that speed is increasing."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-04003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "cubic", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1, "exclude": [0]}},
      {"name": "quadratic", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "free", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "speed_value", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "instant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["position", "velocity"]}},
      {"name": "heading", "type": "label", "role": "safe", "domain": {"values": ["left", "right"]}},
   ],
   "constraints": [
      "heading == 'left' or given == 'position'",
      "acceleration_at != 0",
      "misread_velocity != 0",
      "misread_acceleration != 0",
      "abs(misread_velocity) != abs(velocity_at)",
      "heading == 'left' or (abs(second_at) != abs(velocity_at) and abs(second_at) != abs(misread_velocity))",
   ],
   "derived": [
      {"name": "velocity_at", "expression": "speed_value if heading == 'right' else -speed_value"},
      {"name": "linear", "expression": "velocity_at - 3*cubic*instant**2 - 2*quadratic*instant if given == 'position' else free"},
      {"name": "constant", "expression": "free if given == 'position' else velocity_at - cubic*instant**3 - quadratic*instant**2 - free*instant"},
      {"name": "given_at", "expression": "cubic*instant**3 + quadratic*instant**2 + linear*instant + constant"},
      {"name": "first_at", "expression": "3*cubic*instant**2 + 2*quadratic*instant + linear"},
      {"name": "second_at", "expression": "6*cubic*instant + 2*quadratic"},
      {"name": "acceleration_at", "expression": "second_at if given == 'position' else first_at"},
      {"name": "misread_velocity", "expression": "given_at if given == 'position' else first_at"},
      {"name": "misread_acceleration", "expression": "first_at if given == 'position' else second_at"},
   ],
   "invariants": [
      "velocity_at != 0",
      "acceleration_at != 0",
      "velocity_at == (first_at if given == 'position' else given_at)",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-12", "settings": {"velocity": "off", "position": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["cubic", "quadratic", "free", "speed_value", "heading", "instant", "given"]},
   ],
   "notes": "The given function is a cubic in position or in velocity. When the particle moves left, deciding the speed from the sign of the acceleration alone gives the wrong verdict and a signed speed is negative; when it moves right (position given), those errors change nothing visible, so the distractors are that acceleration-only reason with the right verdict and both wrong counts of differentiation.",
}

t = sympy.Symbol("t")


def _trend(velocity_value, acceleration_value):
   same_sign = velocity_value * acceleration_value > 0

   return "increasing" if same_sign else "decreasing"


def _sign_word(velocity_value, acceleration_value):
   same_sign = velocity_value * acceleration_value > 0

   return "the same sign" if same_sign else "opposite signs"


def _label(speed, trend, reason):
   return f"The speed is {tex(speed)} meters per second, and it is {trend} at that time, because {reason}."


def build(names):
   instant = int(names["instant"])
   given_function = names["cubic"] * t**3 + names["quadratic"] * t**2 + names["linear"] * t + names["constant"]
   is_position = names["given"] == "position"

   if is_position:
      velocity = sympy.diff(given_function, t)
      function_text = f"Its position at time t seconds is {math('x(t) = ' + tex(given_function))} meters"
   else:
      velocity = given_function
      function_text = f"Its velocity at time t seconds is {math('v(t) = ' + tex(given_function))} meters per second"

   acceleration = sympy.diff(velocity, t)
   velocity_value = velocity.subs(t, instant)
   acceleration_value = acceleration.subs(t, instant)
   speed = abs(velocity_value)
   trend = _trend(velocity_value, acceleration_value)

   misread_velocity = names["misread_velocity"]
   misread_acceleration = names["misread_acceleration"]
   misread_trend = _trend(misread_velocity, misread_acceleration)
   acceleration_only_trend = "increasing" if acceleration_value > 0 else "decreasing"

   stem = (
      f"A particle moves along the x-axis. {function_text}, for {math(r't \ge 0')}. Find the speed of the particle at "
      f"time t = {instant}, and determine whether the speed is increasing or decreasing at that time. Give a reason "
      "for the answer."
   )

   velocity_statement = f"v({instant}) = {tex(velocity_value)}"
   acceleration_statement = f"a({instant}) = {tex(acceleration_value)}"
   key_reason = f"{math(velocity_statement)} and {math(acceleration_statement)} have {_sign_word(velocity_value, acceleration_value)}"

   steps = []

   if is_position:
      steps.append(Step(
         text=f"Velocity is the derivative of position, {math('v(t) = ' + tex(velocity))}, so {math(velocity_statement)}.",
         value=velocity_value,
         point_type_id="BC-PT-99027",
         rule="velocity is the derivative of position",
      ))
   else:
      steps.append(Step(
         text=f"At t = {instant}, {math(velocity_statement)}.",
         value=velocity_value,
         point_type_id="BC-PT-99027",
         rule="evaluate the velocity",
      ))

   steps.extend([
      Step(
         text=f"Acceleration is the derivative of velocity, {math('a(t) = ' + tex(acceleration))}, so {math(acceleration_statement)}.",
         value=acceleration_value,
         point_type_id="BC-PT-99027",
         rule="acceleration is the derivative of velocity",
      ),
      Step(
         text=f"The speed is {math(rf'\left|v({instant})\right| = {tex(speed)}')} meters per second.",
         value=speed,
         point_type_id="BC-PT-99004",
         rule="speed is the absolute value of velocity",
      ),
      Step(
         text=(
            f"Because {key_reason}, the speed of the particle is {trend} at t = {instant}."
         ),
         point_type_id="BC-PT-99004",
         rule="speed increases when velocity and acceleration share a sign",
      ),
   ])

   if is_position:
      misread_how = "the position read as the velocity and the velocity as the acceleration, one differentiation too few"
   else:
      misread_how = "the velocity differentiated once too often, so its derivative is read as the velocity and the next as the acceleration"

   misread_reason = (
      f"{math(f'v({instant}) = {tex(misread_velocity)}')} and {math(f'a({instant}) = {tex(misread_acceleration)}')} "
      f"have {_sign_word(misread_velocity, misread_acceleration)}"
   )

   acceleration_only = Distractor(
      error_path="BC-ERR-99003",
      derivation="the change in speed decided from the sign of the acceleration alone, without the sign of the velocity",
      label=_label(speed, acceleration_only_trend, f"{math(acceleration_statement)} is {'positive, so the particle is speeding up' if acceleration_value > 0 else 'negative, so the particle is slowing down'}"),
      mechanism="theorem_condition_ignored",
   )
   too_few = Distractor(
      error_path="BC-ERR-04006",
      derivation=misread_how,
      label=_label(abs(misread_velocity), misread_trend, misread_reason),
      mechanism="conceptual_confusion",
   )

   if velocity_value < 0:
      distractors = [
         Distractor(
            error_path="BC-ERR-04007",
            derivation="the speed reported as the signed velocity",
            label=_label(velocity_value, trend, key_reason),
            mechanism="sign_error",
         ),
         acceleration_only,
         too_few,
      ]
   else:
      overshoot_velocity = acceleration_value
      overshoot_acceleration = sympy.diff(acceleration, t).subs(t, instant)
      overshoot_reason = (
         f"{math(f'v({instant}) = {tex(overshoot_velocity)}')} and {math(f'a({instant}) = {tex(overshoot_acceleration)}')} "
         f"have {_sign_word(overshoot_velocity, overshoot_acceleration)}"
      )
      overshoot = Distractor(
         error_path="BC-ERR-04006",
         derivation="the position differentiated once too often, so the acceleration is read as the velocity and its derivative as the acceleration",
         label=_label(abs(overshoot_velocity), _trend(overshoot_velocity, overshoot_acceleration), overshoot_reason),
         mechanism="conceptual_confusion",
      )
      key_label = _label(speed, trend, key_reason)
      taken = {key_label, too_few.label, overshoot.label}
      third = None

      for read_velocity, read_acceleration, how in (
         (velocity_value, overshoot_acceleration, "the velocity found correctly but differentiated twice more for the acceleration"),
         (names["given_at"], acceleration_value, "the position itself read as the velocity, with the acceleration found correctly"),
      ):
         reason = (
            f"{math(f'v({instant}) = {tex(read_velocity)}')} and {math(f'a({instant}) = {tex(read_acceleration)}')} "
            f"have {_sign_word(read_velocity, read_acceleration)}"
         )
         candidate = _label(abs(read_velocity), _trend(read_velocity, read_acceleration), reason)
         is_new = candidate not in taken and read_velocity != 0 and read_acceleration != 0

         if is_new:
            third = Distractor(error_path="BC-ERR-04006", derivation=how, label=candidate, mechanism="conceptual_confusion")
            break

      distractors = [too_few, overshoot, third]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_label(speed, trend, key_reason)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
