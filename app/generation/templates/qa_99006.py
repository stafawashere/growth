"""BC-QA-99006, the rate of change with respect to theta of the gap between two polar curves, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-99006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "outer_constant", "type": "integer", "role": "safe", "domain": {"min": 4, "max": 12, "step": 1}},
      {"name": "outer_sign", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "outer_coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "inner_constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "inner_coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "inner_trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "angle", "type": "real", "role": "safe", "domain": {"values": [0.3, 0.5, 0.7, 0.9, 1.1, 1.2, 1.4]}},
      {"name": "outer_named", "type": "label", "role": "difficulty", "domain": {"values": ["stated", "argued"]}},
   ],
   "constraints": [
      "outer_constant > inner_constant + inner_coefficient",
      "outer_sign == 1 or outer_constant > inner_constant + inner_coefficient + 2 * outer_coefficient",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "outer_named", "difficulty_factor_id": "BC-DF-12", "settings": {"stated": "off", "argued": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-13",
         "figure_kind": None,
         "requires": ["outer_constant", "outer_coefficient", "inner_constant", "inner_coefficient", "inner_trig", "angle"],
      },
   ],
   "notes": "The outer curve is r = A + s B theta sin(theta) with s = 1 or -1; on 0 <= theta <= pi/2 the term theta sin(theta) lies between 0 and pi/2 < 2, so the outer radius is at least A when s = 1 and more than A - 2B when s = -1. The inner curve r = C + D sin or cos(theta) is at most C + D, below either bound, so the curves never meet on the interval and the gap is outer minus inner. The sign s lets the rate of the gap take both signs.",
}

theta = sympy.Symbol("theta")


def build(names):
   outer_coefficient = names["outer_coefficient"]
   inner_trig = sympy.sin if names["inner_trig"] == "sin" else sympy.cos
   angle = sympy.nsimplify(names["angle"])
   is_stated = names["outer_named"] == "stated"

   outer_sign = names["outer_sign"]
   outer = names["outer_constant"] + outer_sign * outer_coefficient * theta * sympy.sin(theta)
   inner = names["inner_constant"] + names["inner_coefficient"] * inner_trig(theta)
   gap = outer - inner
   gap_rate = sympy.diff(gap, theta)
   key_value = sympy.N(gap_rate.subs(theta, angle), 30)

   inner_rate = sympy.diff(inner, theta)
   outer_rate_value = sympy.N(sympy.diff(outer, theta).subs(theta, angle), 30)
   no_product_rule = sympy.N((outer_sign * outer_coefficient * sympy.cos(theta) - inner_rate).subs(theta, angle), 30)

   angle_text = f"{float(angle):g}"
   window = r"0 \le \theta \le \frac{\pi}{2}"
   outer_sentence = " On this interval the first curve lies outside the second." if is_stated else ""
   stem = (
      f"Two polar curves are given by {math('r = ' + tex(outer))} and {math('r = ' + tex(inner))} for {math(window)}, "
      f"and they do not meet on this interval.{outer_sentence} Let D be the distance between the two curves measured "
      f"along the ray at angle {math(r'\theta')}. Using a calculator, find the rate at which D changes with respect to "
      f"{math(r'\theta')} at {math(r'\theta = ' + angle_text)}. Show the setup, and give the value correct to three "
      "decimal places."
   )

   if is_stated:
      outer_step = "The first curve is outside the second on the interval"
   elif outer_sign == 1:
      outer_step = (
         f"On the interval {math(r'\theta\sin\theta \ge 0')}, so the first radius is at least "
         f"{names['outer_constant']}, while the second is at most "
         f"{names['inner_constant'] + names['inner_coefficient']}. The first curve is outside"
      )
   else:
      outer_step = (
         f"On the interval {math(r'0 \le \theta\sin\theta \le \frac{\pi}{2} < 2')}, so the first radius is more than "
         f"{names['outer_constant'] - 2 * outer_coefficient}, while the second is at most "
         f"{names['inner_constant'] + names['inner_coefficient']}. The first curve is outside"
      )

   steps = [
      Step(
         text=f"{outer_step}, so {math('D(\\theta) = ' + tex(outer) + ' - \\left(' + tex(inner) + '\\right)')}.",
         point_type_id="BC-PT-99005",
         rule="distance along a ray",
      ),
      Step(
         text=(
            f"Differentiate, using the product rule on {math(r'\theta\sin\theta')}: "
            f"{math(r"D'(\theta) = " + tex(gap_rate))}."
         ),
         point_type_id="BC-PT-99005",
         rule="product rule",
      ),
      Step(
         text=f"At {math(r'\theta = ' + angle_text)}, a calculator in radian mode gives {math(r"D' \approx " + decimal_text(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="evaluation at the stated angle",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09039",
         derivation="the inner curve taken as the outer one, so the gap is written inner minus outer and its derivative has the wrong sign",
         value=-key_value,
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="the outer radius differentiated without the product rule, theta sin(theta) giving cos(theta)",
         value=no_product_rule,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="only the outer radius differentiated, so dr/dtheta of the first curve is reported as the rate of the gap",
         value=outer_rate_value,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-13",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
