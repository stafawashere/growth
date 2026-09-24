"""BC-QA-06009, an antiderivative or a definite integral found by integration by parts."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "multiplier", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4, 5]}},
      {"name": "variable", "type": "label", "role": "safe", "domain": {"values": ["x", "t", "s", "w"]}},
      {"name": "reach", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "partner", "type": "label", "role": "difficulty", "domain": {"values": ["exponential", "sine", "cosine"]}},
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["indefinite", "definite"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "partner", "difficulty_factor_id": "BC-DF-02", "settings": {"exponential": "off", "sine": "low", "cosine": "low"}},
      {"parameter": "form", "difficulty_factor_id": "BC-DF-06", "settings": {"indefinite": "off", "definite": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["multiplier", "rate", "partner", "form"]},
   ],
   "notes": (
      "The integrand is multiplier x times e^(rate x), sin(rate x) or cos(rate x), with u = multiplier x. The definite "
      "form runs from 0 to reach for the exponential and from 0 to reach pi / (3 rate) for the trigonometric "
      "partners, where the boundary term uv is not zero."
   ),
}

C = sympy.Symbol("C")


def _partner(kind, rate, x):
   if kind == "exponential":
      return sympy.exp(rate * x)

   if kind == "sine":
      return sympy.sin(rate * x)

   return sympy.cos(rate * x)


def build(names):
   kind = names["partner"]
   rate = names["rate"]
   multiplier = names["multiplier"]
   is_definite = names["form"] == "definite"
   x = sympy.Symbol(names["variable"])
   differential = r"\,d" + names["variable"]

   first = multiplier * x
   partner = _partner(kind, rate, x)
   integrand = first * partner
   v_value = sympy.integrate(partner, x)
   boundary = first * v_value
   remaining = sympy.integrate(v_value * multiplier, x)
   antiderivative = sympy.expand(boundary - remaining)
   separate = sympy.integrate(first, x) * v_value
   plus_sign = sympy.expand(boundary + remaining)

   u_text = math(f"u = {tex(first)}")
   dv_text = math(f"dv = {tex(partner)}" + differential)
   coefficient_text = {1: "", -1: "-"}.get(int(multiplier), str(multiplier))
   is_unit_coefficient = coefficient_text in ("", "-")
   du_differential = "d" + names["variable"] if is_unit_coefficient else differential
   du_text = math(f"du = {coefficient_text}" + du_differential)
   v_text = math(f"v = {tex(v_value)}")
   parts_text = math(f"{tex(boundary)} - " + r"\int " + tex(multiplier * v_value) + differential)
   steps = [
      Step(
         text=f"Let {u_text} and {dv_text}, so {du_text} and {v_text}.",
         point_type_id="BC-PT-99056",
         rule="choice of u and dv",
      ),
      Step(
         text=f"Integration by parts gives {parts_text}.",
         point_type_id="BC-PT-99057",
         rule="integration by parts",
      ),
   ]

   if is_definite:
      reach = names["reach"]
      upper = reach if kind == "exponential" else reach * sympy.pi / (3 * rate)
      integral_tex = rf"\int_{{0}}^{{{tex(upper)}}} {tex(integrand)}" + differential
      stem = f"Find the exact value of {math(integral_tex)}."

      def evaluate(expression):
         return sympy.simplify(expression.subs(x, upper) - expression.subs(x, 0))

      key_value = evaluate(antiderivative)
      bracket = r"\left[" + tex(antiderivative) + r"\right]_{0}^{" + tex(upper) + "}"
      steps.append(Step(
         text=f"So the integral is {math(bracket + ' = ' + tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="Fundamental Theorem of Calculus",
      ))
      distractors = [
         Distractor(
            error_path="BC-ERR-06023",
            derivation="the minus sign before the integral of v du dropped",
            value=evaluate(plus_sign),
            mechanism="sign_error",
         ),
         Distractor(
            error_path="BC-ERR-06022",
            derivation=f"the two factors antidifferentiated separately, {tex(sympy.integrate(first, x))} times {tex(v_value)}, and multiplied",
            value=evaluate(separate),
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99025",
            derivation="the boundary term uv left out, so only the remaining integral is evaluated between the limits",
            value=evaluate(-remaining),
            mechanism="wrong_limits",
         ),
      ]
      command = "evaluate"
   else:
      integral_tex = r"\int " + tex(integrand) + differential
      stem = f"Find {math(integral_tex)}."
      key_value = antiderivative + C
      steps.append(Step(
         text=f"The remaining integral is basic, so the antiderivative is {math(tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="basic antiderivative",
      ))
      distractors = [
         Distractor(
            error_path="BC-ERR-06023",
            derivation="the minus sign before the integral of v du dropped",
            value=plus_sign + C,
            mechanism="sign_error",
         ),
         Distractor(
            error_path="BC-ERR-06022",
            derivation=f"the two factors antidifferentiated separately, {tex(sympy.integrate(first, x))} times {tex(v_value)}, and multiplied",
            value=separate + C,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99025",
            derivation=f"the remaining integral of v du antidifferentiated without dividing by {rate} a second time",
            value=sympy.expand(boundary - remaining * rate) + C,
            mechanism="algebra_slip",
         ),
      ]
      command = "find"

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb=command,
   )
