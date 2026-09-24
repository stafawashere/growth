"""BC-QA-01005, a limit of a bounded oscillating product found with the squeeze theorem."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "wave", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "naming", "type": "label", "role": "difficulty", "domain": {"values": ["open", "named"]}},
   ],
   "constraints": [
      "power % 2 == 1 or coefficient < 0",
   ],
   "derived": [],
   "invariants": [
      "'The limit is' in key",
   ],
   "dial_bindings": [
      {"parameter": "naming", "difficulty_factor_id": "BC-DF-09", "settings": {"named": "off", "open": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["target", "shift", "coefficient", "power", "wave"]},
   ],
   "notes": "f(x) = shift + coefficient (x - target)^power times sin or cos of 1/(x - target). The vanishing factor is negative on one side of the target (odd power) or everywhere (even power with a negative coefficient), so multiplying the bounds of the oscillating factor by it without reversal gives a false inequality.",
}

x = sympy.Symbol("x")


def _plus_constant(term_tex, constant):
   if constant == 0:
      return term_tex

   sign = "+" if constant > 0 else "-"

   return f"{term_tex} {sign} {abs(constant)}"


def _minus_term(constant, term_tex):
   if constant == 0:
      return f"-{term_tex}"

   return f"{constant} - {term_tex}"


def _scaled(coefficient, power_term):
   """coefficient times the power, held unevaluated so the factor stays whole, except that a unit
   coefficient is printed as a sign rather than as 1."""
   is_unit = abs(coefficient) == 1

   if is_unit:
      return coefficient * power_term

   return sympy.Mul(coefficient, power_term, evaluate=False)


def build(names):
   target = names["target"]
   shift = names["shift"]
   coefficient = names["coefficient"]
   power = int(names["power"])
   wave = sympy.sin if names["wave"] == "sin" else sympy.cos
   is_named = names["naming"] == "named"

   offset = x - target
   vanishing = _scaled(coefficient, offset**power)
   oscillating = wave(1 / offset)
   magnitude = offset**power if power % 2 == 0 else sympy.Abs(offset) ** power
   size = sympy.Mul(abs(coefficient), magnitude, evaluate=False)
   size_tex = tex(magnitude) if abs(coefficient) == 1 else tex(size)
   vanishing_tex = tex(vanishing)
   function_tex = _plus_constant(f"{vanishing_tex} {tex(oscillating)}", shift)
   lower_tex = _minus_term(shift, size_tex)
   upper_tex = _plus_constant(size_tex, shift)
   wrong_lower_tex = _plus_constant(tex(_scaled(-coefficient, offset**power)), shift)
   wrong_upper_tex = _plus_constant(vanishing_tex, shift)

   limit_tex = rf"\lim_{{x \to {target}}} f(x)"
   request = "Use the squeeze theorem to find" if is_named else "Find"
   stem = (
      f"Let {math('f(x) = ' + function_tex)} for {math(rf'x \ne {target}')}. {request} {math(limit_tex)}, "
      "and justify your answer."
   )

   bounds_tex = rf"{lower_tex} \le f(x) \le {upper_tex}"
   wrong_bounds_tex = rf"{wrong_lower_tex} \le f(x) \le {wrong_upper_tex}"
   condition = f"for {math(rf'x \ne {target}')}"
   key_label = f"The limit is {shift}, because {math(bounds_tex)} {condition} and both bounds approach {shift} as x approaches {target}."

   adding = "" if shift == 0 else f" and adding {shift}"
   steps = [
      Step(
         text=f"For {math(rf'x \ne {target}')}, {math(rf'-1 \le {tex(oscillating)} \le 1')}.",
         rule="bounded oscillating factor",
      ),
      Step(
         text=(
            f"Multiplying by the nonnegative quantity {math(size_tex)}{adding} gives {math(bounds_tex)}. "
            f"The factor {math(vanishing_tex)} can be negative, so its absolute value is used to keep the inequality true."
         ),
         rule="bounding inequality",
      ),
      Step(
         text=f"Both bounds are continuous, so their limits as x approaches {target} are both {shift}.",
         rule="limits of the bounds",
      ),
      Step(
         text=f"By the squeeze theorem, {math(limit_tex + f' = {shift}')}.",
         rule="squeeze theorem",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-01012",
         derivation="the bounds of the oscillating factor multiplied by the sign changing factor without reversing the inequality where it is negative",
         label=f"The limit is {shift}, because {math(wrong_bounds_tex)} {condition} and both bounds approach {shift} as x approaches {target}.",
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-01013",
         derivation="the bounding functions evaluated at the target instead of their limits being taken",
         label=f"The limit is {shift}, because {math(bounds_tex)} {condition}, and bounds that are equal at x = {target} force that limit, whatever their limits.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99008",
         derivation="the product limit theorem used although its hypothesis fails, since the oscillating factor has no limit",
         label=f"The limit is {shift}, because {math(vanishing_tex)} approaches 0 and {math(tex(oscillating))} approaches a limit as x approaches {target}, so the product theorem applies.",
         mechanism="theorem_condition_ignored",
      ),
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
