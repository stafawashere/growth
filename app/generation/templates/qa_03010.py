"""BC-QA-03010, an inverse trigonometric derivative derived by differentiating the identity f(g(x)) = x."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-03010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inverse", "type": "label", "role": "difficulty", "domain": {"values": ["arctan", "arcsin", "arccos"]}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "slope_sign", "type": "integer", "role": "safe", "domain": {"values": [-1, 1]}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": -10, "max": 10, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 11, "step": 1}},
   ],
   "constraints": [
      "slope != scale",
      "gcd(slope, scale) == 1",
   ],
   "derived": [
      {"name": "inner_rate", "expression": "slope * slope_sign"},
   ],
   "invariants": [
      "exact(key)",
      "inner_rate != 0",
   ],
   "dial_bindings": [
      {"parameter": "inverse", "difficulty_factor_id": "BC-DF-06", "settings": {"arctan": "low", "arcsin": "medium", "arccos": "medium"}},
      {"parameter": "inverse", "difficulty_factor_id": "BC-DF-04", "settings": {"arctan": "high", "arcsin": "high", "arccos": "high"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["inverse", "slope", "slope_sign", "offset", "scale"]},
   ],
   "notes": "g(x) is the inverse tangent, sine or cosine of u = (p x + q)/a, stated with the identity tan(g(x)) = u, sin(g(x)) = u or cos(g(x)) = u. Differentiating the identity by the chain rule and replacing sec^2 g, cos g or sin g through the Pythagorean identity on the principal branch gives p a/(a^2 + (p x + q)^2), p/sqrt(a^2 - (p x + q)^2) or -p/sqrt(a^2 - (p x + q)^2). The slope and the scale differ and are coprime, so dropping the inner factor p/a always changes the answer.",
}

x = sympy.Symbol("x")

DERIVATIVE = "g'(x)"

TRIG_NAMES = {"arctan": r"\tan", "arcsin": r"\sin", "arccos": r"\cos"}
INVERSE_NAMES = {"arctan": r"\arctan", "arcsin": r"\arcsin", "arccos": r"\arccos"}
BRANCHES = {
   "arctan": r"-\frac{\pi}{2} < g(x) < \frac{\pi}{2}",
   "arcsin": r"-\frac{\pi}{2} \le g(x) \le \frac{\pi}{2}",
   "arccos": r"0 \le g(x) \le \pi",
}


def _answers(inverse, rate, inner, scale):
   tangent_form = rate * scale / (scale**2 + inner**2)
   radical = sympy.sqrt(scale**2 - inner**2)

   if inverse == "arctan":
      return {
         "key": tangent_form,
         "inner_dropped": scale**2 / (scale**2 + inner**2),
         "wrong_formula": rate / radical,
         "wrong_sign": rate * scale / (scale**2 - inner**2),
      }

   sign = 1 if inverse == "arcsin" else -1

   return {
      "key": sign * rate / radical,
      "inner_dropped": sign * scale / radical,
      "wrong_formula": sign * tangent_form,
      "wrong_sign": -sign * rate / radical,
   }


def _derivation_steps(inverse, inner, scale, rate, ratio_text):
   ratio = inner / scale
   trig = TRIG_NAMES[inverse]
   rate_ratio = tex(sympy.Rational(rate, scale))

   if inverse == "arctan":
      chain = rf"\sec^{{2}}\left(g(x)\right) \cdot g'(x) = {rate_ratio}"
      identity = rf"\sec^{{2}}\left(g(x)\right) = 1 + \tan^{{2}}\left(g(x)\right) = {tex(1 + ratio**2)}"
      reason = "the Pythagorean identity for tangent and secant"
   elif inverse == "arcsin":
      chain = rf"\cos\left(g(x)\right) \cdot g'(x) = {rate_ratio}"
      identity = rf"\cos\left(g(x)\right) = \sqrt{{1 - \sin^{{2}}\left(g(x)\right)}} = {tex(sympy.sqrt(1 - ratio**2))}"
      reason = "the Pythagorean identity, with the positive root because the cosine is not negative on this branch"
   else:
      chain = rf"-\sin\left(g(x)\right) \cdot g'(x) = {rate_ratio}"
      identity = rf"\sin\left(g(x)\right) = \sqrt{{1 - \cos^{{2}}\left(g(x)\right)}} = {tex(sympy.sqrt(1 - ratio**2))}"
      reason = "the Pythagorean identity, with the positive root because the sine is not negative on this branch"

   return [
      Step(
         text=(
            f"Differentiate both sides of {math(trig + r'\left(g(x)\right) = ' + ratio_text)} with respect to x. "
            f"The chain rule on the left gives {math(chain)}."
         ),
         rule="chain rule on the identity f(g(x)) = x",
      ),
      Step(
         text=f"Express the trigonometric factor in x by {reason}: {math(identity)}.",
         rule="Pythagorean identity on the principal branch",
      ),
   ]


def build(names):
   inverse = names["inverse"]
   rate = int(names["inner_rate"])
   offset = int(names["offset"])
   scale = int(names["scale"])
   inner = rate * x + offset
   ratio_text = rf"\frac{{{tex(inner)}}}{{{scale}}}"
   answers = _answers(inverse, rate, inner, scale)

   definition = f"g(x) = {INVERSE_NAMES[inverse]}\\left({ratio_text}\\right)"
   identity = f"{TRIG_NAMES[inverse]}\\left(g(x)\\right) = {ratio_text}"
   domain_note = "" if inverse == "arctan" else f" for {math('-1 < ' + ratio_text + ' < 1')}"
   stem = (
      f"Let {math(definition)}{domain_note}, so that {math(BRANCHES[inverse])} and {math(identity)}. "
      f"Differentiate both sides of this identity with respect to x to find {math(DERIVATIVE)}."
   )

   steps = _derivation_steps(inverse, inner, scale, rate, ratio_text)
   steps.append(Step(
      text=f"Solve for the derivative: {math(DERIVATIVE + ' = ' + tex(answers['key']))}.",
      value=answers["key"],
      rule="solve the differentiated identity",
   ))

   if inverse == "arctan":
      wrong_formula = "the inverse sine pattern, one over a square root, used in place of the inverse tangent pattern"
      wrong_sign = "the secant squared replaced by 1 minus the tangent squared, a sign misplaced in the identity"
   else:
      wrong_formula = "the inverse tangent pattern, one over 1 plus the square, used in place of the radical pattern"
      wrong_sign = "the sign of the derivative of the cosine lost, so the inverse sine and inverse cosine results are exchanged"

   distractors = [
      Distractor(
         error_path="BC-ERR-03018",
         derivation=f"the factor {rate}/{scale} from differentiating the inner expression omitted",
         value=answers["inner_dropped"],
         mechanism="chain_rule_omitted",
      ),
      Distractor(error_path="BC-ERR-03017", derivation=wrong_formula, value=answers["wrong_formula"], mechanism="conceptual_confusion"),
      Distractor(error_path="BC-ERR-03017", derivation=wrong_sign, value=answers["wrong_sign"], mechanism="sign_error"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=answers["key"]),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
