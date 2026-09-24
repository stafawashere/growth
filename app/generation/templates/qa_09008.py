"""BC-QA-09008, the times at which a particle in the plane moves toward a coordinate axis."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_roots, tex

ARCHETYPE_ID = "BC-QA-09008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 8, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "divisor", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "end_time", "type": "rational", "role": "safe", "domain": {"values": ["2", "5/2", "3"]}},
      {"name": "other_turn", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "shape", "type": "label", "role": "safe", "domain": {"values": ["rising", "falling"]}},
      {"name": "axis", "type": "label", "role": "safe", "domain": {"values": ["y-axis", "x-axis"]}},
      {"name": "sign_given", "type": "label", "role": "difficulty", "domain": {"values": ["stated", "argued"]}},
      {"name": "side", "type": "label", "role": "difficulty", "domain": {"values": ["negative", "positive"]}},
   ],
   "constraints": [
      "offset > amplitude",
      "shape == 'rising' or offset > end_time**2 / divisor",
   ],
   "derived": [],
   "invariants": [
      "0 < turning_time < end_time",
      "turning_time**2 != other_turn",
   ],
   "dial_bindings": [
      {"parameter": "sign_given", "difficulty_factor_id": "BC-DF-14", "settings": {"stated": "off", "argued": "low"}},
      {"parameter": "side", "difficulty_factor_id": "BC-DF-12", "settings": {"positive": "off", "negative": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-14",
         "figure_kind": None,
         "requires": ["offset", "amplitude", "divisor", "end_time", "other_turn", "shape", "axis"],
      },
   ],
   "notes": "The base coordinate is negative on the whole interval (offset exceeds the sine term, and on the falling shape also exceeds end_time squared over divisor), and its rate changes sign exactly once, at a root of amplitude cos t = 2t / divisor below pi / 2. On the positive side the named coordinate is the negative of the base, so it keeps one sign either way and both signs occur.",
}

t = sympy.Symbol("t")


def _interval(low, high):
   return math(rf"{low} < t < {high}")


def _sign_step(named, axis, is_stated, is_rising, is_negative, amplitude, offset, divisor, end_time):
   sign_symbol = "<" if is_negative else ">"
   side_word = "negative" if is_negative else "positive"

   if is_stated:
      text = f"The stem gives {math(named + '(t) ' + sign_symbol + ' 0')} on the whole interval, so the particle stays on one side of the {axis}."
   elif is_rising:
      bound = amplitude - offset
      comparison = r" \le " + tex(bound) if is_negative else r" \ge " + tex(-bound)
      text = (
         f"Since {math(r'\sin t \le 1')}, {math(named + '(t)' + comparison)} for every t, so {math(named + '(t)')} is "
         f"{side_word} and the particle stays on one side of the {axis}."
      )
   else:
      bound = end_time**2 / divisor - offset
      comparison = r" \le " + tex(bound) if is_negative else r" \ge " + tex(-bound)
      text = (
         f"On the interval, {math(r'\sin t \ge 0')} and {math('t^2 \\le ' + tex(end_time**2))}, so "
         f"{math(named + '(t)' + comparison)}, and {math(named + '(t)')} is {side_word}, so the particle stays on one side "
         f"of the {axis}."
      )

   return Step(text=text, point_type_id="BC-PT-99014", rule="sign of the coordinate")


def build(names):
   offset = names["offset"]
   amplitude = names["amplitude"]
   divisor = names["divisor"]
   end_time = names["end_time"]
   other_turn = names["other_turn"]
   is_rising = names["shape"] == "rising"
   axis = names["axis"]
   is_stated = names["sign_given"] == "stated"
   is_negative = names["side"] == "negative"
   side_sign = 1 if is_negative else -1

   if is_rising:
      base_coordinate = amplitude * sympy.sin(t) - t**2 / divisor - offset
   else:
      base_coordinate = t**2 / divisor - amplitude * sympy.sin(t) - offset

   named_coordinate = sympy.expand(side_sign * base_coordinate)
   other_coordinate = other_turn * t - t**3 / 3
   named_rate = sympy.diff(named_coordinate, t)
   turning_time = numeric_roots(named_rate, t, 0, end_time)[0]
   other_turning_time = sympy.sqrt(other_turn)

   if axis == "y-axis":
      named, other = "x", "y"
      position_pair = (named_coordinate, other_coordinate)
   else:
      named, other = "y", "x"
      position_pair = (other_coordinate, named_coordinate)

   turning_text = decimal_text(turning_time)
   end_text = tex(end_time)
   other_turning_text = tex(other_turning_time)
   position_tex = rf"\left( {tex(position_pair[0])},\ {tex(position_pair[1])} \right)"
   window = rf"0 \le t \le {end_text}"
   sign_symbol = "<" if is_negative else ">"
   side_word = "negative" if is_negative else "positive"
   rate_word = "positive" if is_negative else "negative"
   rate_symbol = ">" if is_negative else "<"

   sign_sentence = f" For {math(window)}, {math(named + '(t) ' + sign_symbol + ' 0')}." if is_stated else ""
   stem = (
      f"A particle moves in the xy-plane so that its position at time t is {math('\\left(x(t), y(t)\\right) = ' + position_tex)} "
      f"for {math(window)}.{sign_sentence} Using a calculator where needed, find all times t in the open interval "
      f"{math(rf'0 < t < {end_text}')} at which the particle is moving toward the {axis}. Give a reason for your answer, "
      "and give any decimal endpoint correct to three decimal places."
   )

   if is_rising:
      approach_interval = _interval(0, turning_text)
      away_interval = _interval(turning_text, end_text)
   else:
      approach_interval = _interval(turning_text, end_text)
      away_interval = _interval(0, turning_text)

   whole_interval = _interval(0, end_text)
   named_rate_tex = math(named + "'(t)")
   named_tex = math(named + "(t)")
   before_sign = rate_word if is_rising else ("negative" if is_negative else "positive")

   steps = [
      _sign_step(named, axis, is_stated, is_rising, is_negative, amplitude, offset, divisor, end_time),
      Step(
         text=(
            f"The particle moves toward the {axis} when {named_tex} and {named_rate_tex} have opposite signs, "
            f"that is, when {math(named + "'(t) = " + tex(named_rate) + ' ' + rate_symbol + ' 0')}. A calculator gives "
            f"{math(named + "'(t) = 0")} at {math('t \\approx ' + turning_text)}, with {named_rate_tex} {before_sign} "
            "before that time and the opposite sign after it."
         ),
         value=turning_time,
         point_type_id="BC-PT-99014",
         rule="zero of the velocity component",
      ),
      Step(
         text=(
            f"So the particle moves toward the {axis} for {approach_interval}, because there {math(named + '(t) ' + sign_symbol + ' 0')} "
            f"and {math(named + "'(t) " + rate_symbol + ' 0')}, so its distance from the {axis}, {math('|' + named + '(t)|')}, "
            "is decreasing."
         ),
         point_type_id="BC-PT-99010",
         rule="sign analysis of the velocity component",
      ),
   ]

   key_label = f"The particle moves toward the {axis} for {approach_interval}, because {named_tex} and {named_rate_tex} have opposite signs there."

   if is_negative:
      other_interval = _interval(0, other_turning_text)
      distractors = [
         Distractor(
            error_path="BC-ERR-09025",
            derivation=f"the sign of the coordinate read as the direction of motion, so every time with {named}(t) < 0 counted as approaching",
            label=f"The particle moves toward the {axis} for {whole_interval}, because {named_tex} is negative there.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-09025",
            derivation=f"approaching read as a negative rate, so the times with {named}'(t) < 0 taken without the sign of {named}(t)",
            label=f"The particle moves toward the {axis} for {away_interval}, because {named_rate_tex} is negative there.",
            mechanism="sign_error",
         ),
         Distractor(
            error_path="BC-ERR-99029",
            derivation=f"the other velocity component used, so the times with {other}'(t) > 0 reported",
            label=f"The particle moves toward the {axis} for {other_interval}, because {math(other + "'(t)")} is positive there.",
            mechanism="reversed_quantities",
         ),
      ]
   else:
      other_interval = _interval(other_turning_text, end_text)
      distractors = [
         Distractor(
            error_path="BC-ERR-09025",
            derivation=f"the sign of the coordinate read as the direction of motion, so a positive {named}(t) taken to mean the particle never approaches",
            label=f"The particle moves toward the {axis} for no t with {math(rf'0 < t < {end_text}')}, because {named_tex} is positive there.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-09025",
            derivation=f"the right times given but justified by the sign of {named}(t) instead of the sign of its rate",
            label=f"The particle moves toward the {axis} for {approach_interval}, because {named_tex} is positive there.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99029",
            derivation=f"the other velocity component used, so the times with {other}'(t) < 0 reported",
            label=f"The particle moves toward the {axis} for {other_interval}, because {math(other + "'(t)")} is negative there.",
            mechanism="reversed_quantities",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-14",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
      notes={"turning_time": turning_time},
   )
