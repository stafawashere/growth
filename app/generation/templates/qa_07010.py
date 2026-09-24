"""BC-QA-07010, a critical point of a solution located and classified from the differential equation alone."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "bound_side", "type": "label", "role": "difficulty", "domain": {"values": ["above", "below"]}},
      {"name": "outside_root", "type": "integer", "role": "safe", "domain": {"min": -4, "max": -1, "step": 1}},
      {"name": "inside_root", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "sign", "type": "integer", "role": "safe", "domain": {"values": [-1, 1]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "letters", "type": "label", "role": "safe", "domain": {"values": ["xy", "ty", "tP"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "outside_root < 0",
      "inside_root > 0",
      "len(key) > 40",
   ],
   "dial_bindings": [
      {"parameter": "bound_side", "difficulty_factor_id": "BC-DF-12", "settings": {"above": "off", "below": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["bound_side", "outside_root", "inside_root", "level", "sign", "scale", "letters"]},
   ],
   "notes": "The right side is s k (y - L)(x - p)(x - q) with p < 0 < q. The stated range x > 0 removes p, and the stated bound on y fixes the sign of (y - L), so the only critical input is q and the sign change of (x - q) classifies it.",
}

LETTERS = {"xy": ("x", "y"), "ty": ("t", "y"), "tP": ("t", "P")}


def _claim(kind_text, reason):
   return f"The solution has {kind_text}, because {reason}."


def build(names):
   input_letter, output_letter = LETTERS[names["letters"]]
   x_symbol = sympy.Symbol(input_letter)
   y_symbol = sympy.Symbol(output_letter)
   outside_root = int(names["outside_root"])
   inside_root = int(names["inside_root"])
   level = int(names["level"])
   multiplier = int(names["sign"]) * int(names["scale"])
   is_above = names["bound_side"] == "above"

   right_side = multiplier * (y_symbol - level) * (x_symbol - outside_root) * (x_symbol - inside_root)
   derivative = rf"\frac{{d{output_letter}}}{{d{input_letter}}}"
   bound_text = math(f"{output_letter} {'>' if is_above else '<'} {level}")
   inside_text = math(f"{input_letter} = {inside_root}")
   outside_text = math(f"{input_letter} = {outside_root}")

   stem = (
      f"The function {math(f'{output_letter} = f({input_letter})')} is a solution to the differential equation "
      f"{math(f'{derivative} = {tex(right_side)}')}, and {bound_text} for all {input_letter}. For "
      f"{math(f'{input_letter} > 0')}, find the input at which f has a critical point and determine whether it is the "
      "location of a relative minimum, a relative maximum, or neither."
   )

   fixed_sign = multiplier * (1 if is_above else -1)
   rises_after = fixed_sign > 0
   kind = "minimum" if rises_after else "maximum"
   other_kind = "maximum" if rises_after else "minimum"
   before, after = ("negative", "positive") if rises_after else ("positive", "negative")
   change_reason = f"the derivative changes from {before} to {after} at {inside_text}"

   sign_prefix = {1: "", -1: "-"}.get(fixed_sign, str(fixed_sign))
   sign_factor_text = sign_prefix + rf"\left({tex(x_symbol - inside_root)}\right)"

   key_label = _claim(f"a relative {kind} at {inside_text}", change_reason)

   steps = [
      Step(
         text=(
            f"A critical point needs {math(f'{derivative} = 0')}. Because {bound_text}, the factor "
            f"{math(tex(y_symbol - level))} is never 0, and for {math(f'{input_letter} > 0')} the factor "
            f"{math(tex(x_symbol - outside_root))} is positive, so the only zero in the range is {inside_text}."
         ),
         point_type_id="BC-PT-99005",
         rule="zeros of the right side within the stated range",
      ),
      Step(
         text=(
            f"On the range, the sign of {math(derivative)} is the sign of "
            f"{math(sign_factor_text)}"
            f" times a positive quantity, so it is {before} just before {inside_text} and {after} just after."
         ),
         point_type_id="BC-PT-99010",
         rule="sign analysis of the derivative",
      ),
      Step(
         text=f"Because {change_reason}, f has a relative {kind} there.",
         point_type_id="BC-PT-99063",
         rule="first derivative test",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05021",
         derivation="the sign change found correctly and then read the wrong way round",
         label=_claim(f"a relative {other_kind} at {inside_text}", change_reason),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-05025",
         derivation=f"the zero at {input_letter} = {outside_root}, outside the stated range, kept as a second critical point",
         label=_claim(
            f"a relative {kind} at {inside_text} and a relative {other_kind} at {outside_text}",
            "the derivative changes sign at both inputs",
         ),
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-07012",
         derivation=f"the right side never set equal to 0 in {input_letter}; only the factor in {output_letter} was examined",
         label=_claim(
            f"no critical point for {math(f'{input_letter} > 0')}",
            f"the factor {math(tex(y_symbol - level))} is never 0 when {bound_text}",
         ),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="determine",
   )
