"""BC-QA-02007, a sum of sine, cosine, exponential, logarithm and constant terms differentiated by rule."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "sine", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "cosine", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "exponential", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "logarithm", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "evaluate", "type": "label", "role": "difficulty", "domain": {"values": ["expression", "point"]}},
      {"name": "angle", "type": "rational", "role": "safe", "domain": {"values": ["1/6", "1/4", "1/3", "1/2", "2/3"]}},
   ],
   "constraints": [
      "evaluate == 'expression' or constant != form('2*cosine*sin(pi*angle)')",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "evaluate", "difficulty_factor_id": "BC-DF-08", "settings": {"expression": "off", "point": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["sine", "cosine", "exponential", "logarithm", "constant", "evaluate"]},
   ],
   "notes": (
      "f(x) = sine sin x + cosine cos x + exponential e^x + logarithm ln x + constant on x > 0. The point form "
      "evaluates the derivative at angle times pi, where the sine is never 0, so the dropped cosine sign always "
      "moves the value."
   ),
}

x = sympy.Symbol("x")


def build(names):
   sine = int(names["sine"])
   cosine = int(names["cosine"])
   exponential = int(names["exponential"])
   logarithm = int(names["logarithm"])
   constant = int(names["constant"])
   at_point = names["evaluate"] == "point"
   point = sympy.pi * sympy.Rational(names["angle"])

   function = sine * sympy.sin(x) + cosine * sympy.cos(x) + exponential * sympy.exp(x) + logarithm * sympy.log(x) + constant
   derivative = sine * sympy.cos(x) - cosine * sympy.sin(x) + exponential * sympy.exp(x) + logarithm / x
   sign_dropped = sine * sympy.cos(x) + cosine * sympy.sin(x) + exponential * sympy.exp(x) + logarithm / x
   power_ruled = sine * sympy.cos(x) - cosine * sympy.sin(x) + exponential * x * sympy.exp(x - 1) + logarithm / x
   constant_kept = derivative + constant

   rules = (
      rf"\frac{{d}}{{dx}}\sin x = \cos x,\ \frac{{d}}{{dx}}\cos x = -\sin x,\ "
      rf"\frac{{d}}{{dx}}e^{{x}} = e^{{x}},\ \frac{{d}}{{dx}}\ln x = \frac{{1}}{{x}}"
   )
   steps = [
      Step(
         text=f"Each term has its own rule: {math(rules)}, and a constant has derivative 0.",
         rule="derivatives of the basic functions",
      ),
      Step(
         text=f"Term by term, {math("f'(x) = " + tex(derivative))}.",
         value=derivative,
         point_type_id="BC-PT-99004",
         rule="sum and constant multiple rules",
      ),
   ]

   if at_point:
      key_value = sympy.expand(derivative.subs(x, point))
      stem = f"Let {math('f(x) = ' + tex(function))} for {math('x > 0')}. Find the exact value of {math(f"f'\\left({tex(point)}\\right)")}."
      steps.append(Step(
         text=f"At {math('x = ' + tex(point))}, {math(f"f'\\left({tex(point)}\\right) = " + tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="evaluate",
      ))
      values = [
         sympy.expand(sign_dropped.subs(x, point)),
         sympy.expand(power_ruled.subs(x, point)),
         sympy.expand(constant_kept.subs(x, point)),
      ]
   else:
      key_value = derivative
      stem = f"Let {math('f(x) = ' + tex(function))} for {math('x > 0')}. Find {math("f'(x)")}."
      values = [sign_dropped, power_ruled, constant_kept]

   distractors = [
      Distractor(
         error_path="BC-ERR-02018",
         derivation="the derivative of cosine taken as sine, the negative sign dropped",
         value=values[0],
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-02019",
         derivation="e^x differentiated by the power rule, as x e^(x - 1)",
         value=values[1],
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-02016",
         derivation=f"the constant {constant} carried into the derivative unchanged",
         value=values[2],
         mechanism="algebra_slip",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
