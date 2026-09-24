"""BC-QA-06008, an antiderivative or a definite integral found by substitution."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inner_power", "type": "integer", "role": "safe", "domain": {"values": [2, 3]}},
      {"name": "inner_scale", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "inner_shift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "multiplier", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "outer_power", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "upper", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "outer", "type": "label", "role": "difficulty", "domain": {"values": ["power", "exponential", "cosine"]}},
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["indefinite", "definite"]}},
   ],
   "constraints": [
      "multiplier != inner_scale * inner_power",
      "outer != 'power' or upper == 1 or inner_power == 2",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "outer", "difficulty_factor_id": "BC-DF-02", "settings": {"power": "off", "exponential": "low", "cosine": "low"}},
      {"parameter": "form", "difficulty_factor_id": "BC-DF-06", "settings": {"indefinite": "off", "definite": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["inner_power", "inner_scale", "inner_shift", "multiplier", "outer", "form"]},
   ],
   "notes": (
      "The integrand is multiplier x^(inner_power - 1) times the outer function of u = inner_scale x^inner_power + "
      "inner_shift, so du = inner_scale inner_power x^(inner_power - 1) dx and the constant multiplier / "
      "(inner_scale inner_power) is never 1. The definite form runs from 0 to upper."
   ),
}

x, u = sympy.symbols("x u")
C = sympy.Symbol("C")


def _outer(kind, argument, power):
   if kind == "exponential":
      return sympy.exp(argument)

   if kind == "cosine":
      return sympy.cos(argument)

   return argument**power


def _antiderivative(kind, argument, power):
   if kind == "exponential":
      return sympy.exp(argument)

   if kind == "cosine":
      return sympy.sin(argument)

   return argument ** (power + 1) / (power + 1)


def build(names):
   kind = names["outer"]
   degree = names["inner_power"]
   scale = names["inner_scale"]
   shift = names["inner_shift"]
   multiplier = names["multiplier"]
   power = names["outer_power"]
   is_definite = names["form"] == "definite"

   inner = scale * x**degree + shift
   differential_factor = scale * degree
   ratio = sympy.Rational(multiplier, differential_factor)
   integrand = multiplier * x ** (degree - 1) * _outer(kind, inner, power)
   outer_in_u = _outer(kind, u, power)
   antiderivative_in_u = _antiderivative(kind, u, power)

   u_text = math(f"u = {tex(inner)}")
   du_text = math(f"du = {tex(differential_factor * x ** (degree - 1))}" + r"\,dx")
   rewritten = math(rf"{tex(ratio)}\int {tex(outer_in_u)}\,du")
   steps = [
      Step(
         text=f"Let {u_text}. Then {du_text}, so the integrand is {math(tex(ratio))} times {math(tex(outer_in_u))} du: {rewritten}.",
         point_type_id="BC-PT-99002",
         rule="substitution",
      ),
   ]

   if is_definite:
      upper = names["upper"]
      low_u = inner.subs(x, 0)
      high_u = inner.subs(x, upper)
      integral_tex = rf"\int_{{0}}^{{{upper}}} {tex(integrand)}\,dx"
      stem = f"Find the exact value of {math(integral_tex)}."

      def evaluate(constant, top, bottom):
         return constant * (antiderivative_in_u.subs(u, top) - antiderivative_in_u.subs(u, bottom))

      key_value = evaluate(ratio, high_u, low_u)
      bracket = r"\left[" + tex(antiderivative_in_u) + r"\right]_{" + str(low_u) + "}^{" + str(high_u) + "}"
      steps += [
         Step(
            text=(
               f"The limits change with the variable: x = 0 gives u = {low_u} and x = {upper} gives u = {high_u}, so the "
               f"integral is {math(tex(ratio) + bracket)}."
            ),
            point_type_id="BC-PT-99003",
            rule="limits converted to u",
         ),
         Step(
            text=f"Evaluating gives {math(tex(key_value))}.",
            value=key_value,
            point_type_id="BC-PT-99004",
            rule="Fundamental Theorem of Calculus",
         ),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-06018",
            derivation=f"the antiderivative in u evaluated at the original limits 0 and {upper}",
            value=evaluate(ratio, upper, 0),
            mechanism="wrong_limits",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the reciprocal constant 1/{differential_factor} from du dropped, keeping only the multiplier {multiplier}",
            value=evaluate(multiplier, high_u, low_u),
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the constant {differential_factor} from du multiplied in instead of its reciprocal",
            value=evaluate(multiplier * differential_factor, high_u, low_u),
            mechanism="algebra_slip",
         ),
      ]
      command = "evaluate"
   else:
      integral_tex = rf"\int {tex(integrand)}\,dx"
      stem = f"Find {math(integral_tex)}."

      def antiderivative(constant):
         return constant * antiderivative_in_u.subs(u, inner)

      key_value = antiderivative(ratio) + C
      steps += [
         Step(
            text=f"Antidifferentiating in u gives {math(tex(ratio * antiderivative_in_u) + ' + C')}.",
            point_type_id="BC-PT-99003",
            rule="basic antiderivative",
         ),
         Step(
            text=f"Replacing u by {math(tex(inner))} gives {math(tex(key_value))}.",
            value=key_value,
            point_type_id="BC-PT-99004",
            rule="back substitution",
         ),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-06020",
            derivation=f"the factor {tex(x ** (degree - 1))} treated as a constant and left outside, so the substitution runs as if du held no power of x",
            value=x ** (degree - 1) * antiderivative(ratio) + C,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the reciprocal constant 1/{differential_factor} from du dropped, keeping only the multiplier {multiplier}",
            value=antiderivative(multiplier) + C,
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the constant {differential_factor} from du multiplied in instead of its reciprocal",
            value=antiderivative(multiplier * differential_factor) + C,
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
