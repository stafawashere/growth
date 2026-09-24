"""BC-QA-02010, tangent, secant, cotangent and cosecant differentiated by rewriting over sine and cosine."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "first", "type": "label", "role": "difficulty", "domain": {"values": ["tan", "sec"]}},
      {"name": "second", "type": "label", "role": "difficulty", "domain": {"values": ["cot", "csc"]}},
      {"name": "first_coefficient", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "second_coefficient", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "evaluate", "type": "label", "role": "difficulty", "domain": {"values": ["expression", "point"]}},
      {"name": "angle", "type": "rational", "role": "safe", "domain": {"values": ["1/6", "1/4", "1/3", "2/3", "3/4", "5/6"]}},
   ],
   "constraints": [
      "evaluate == 'expression' or options[0] != 0",
      "evaluate == 'expression' or (options[3] != options[0] and options[3] != options[1] and options[3] != options[2])",
   ],
   "derived": [
      {"name": "first_slope", "expression": "form('sec(pi*angle)^2') if first == 'tan' else form('sec(pi*angle)*tan(pi*angle)')"},
      {"name": "second_slope", "expression": "form('-csc(pi*angle)^2') if second == 'cot' else form('-csc(pi*angle)*cot(pi*angle)')"},
      {"name": "first_quotient", "expression": "form('-cot(pi*angle)') if first == 'tan' else 0"},
      {"name": "second_quotient", "expression": "form('-tan(pi*angle)') if second == 'cot' else 0"},
      {
         "name": "options",
         "expression": (
            "[first_coefficient * first_slope + second_coefficient * second_slope, "
            "-first_coefficient * first_slope - second_coefficient * second_slope, "
            "first_coefficient * first_slope - second_coefficient * second_slope, "
            "first_coefficient * first_quotient + second_coefficient * second_quotient]"
         ),
      },
   ],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "first", "difficulty_factor_id": "BC-DF-06", "settings": {"tan": "off", "sec": "low"}},
      {"parameter": "second", "difficulty_factor_id": "BC-DF-06", "settings": {"cot": "off", "csc": "low"}},
      {"parameter": "evaluate", "difficulty_factor_id": "BC-DF-08", "settings": {"expression": "off", "point": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["first", "second", "first_coefficient", "second_coefficient", "evaluate"]},
   ],
   "notes": (
      "h(x) = a F(x) + b G(x) with F the tangent or secant and G the cotangent or cosecant, so every item has "
      "one cofunction term whose derivative carries a negative sign. The point form uses a multiple of pi/6 or "
      "pi/4 where all four functions are defined and none of their derivatives is 0; the constraints drop the "
      "few points where the two terms cancel or the term-by-term value meets another option."
   ),
}

x = sympy.Symbol("x")

FUNCTIONS = {
   "tan": {
      "function": sympy.tan(x),
      "numerator": sympy.sin(x),
      "denominator": sympy.cos(x),
      "derivative": sympy.sec(x) ** 2,
      "term_by_term": -sympy.cot(x),
   },
   "sec": {
      "function": sympy.sec(x),
      "numerator": sympy.Integer(1),
      "denominator": sympy.cos(x),
      "derivative": sympy.sec(x) * sympy.tan(x),
      "term_by_term": sympy.Integer(0),
   },
   "cot": {
      "function": sympy.cot(x),
      "numerator": sympy.cos(x),
      "denominator": sympy.sin(x),
      "derivative": -sympy.csc(x) ** 2,
      "term_by_term": -sympy.tan(x),
   },
   "csc": {
      "function": sympy.csc(x),
      "numerator": sympy.Integer(1),
      "denominator": sympy.sin(x),
      "derivative": -sympy.csc(x) * sympy.cot(x),
      "term_by_term": sympy.Integer(0),
   },
}


def _at(expression, point):
   return sympy.radsimp(sympy.expand(expression.subs(x, point)))


def build(names):
   first = FUNCTIONS[names["first"]]
   second = FUNCTIONS[names["second"]]
   first_coefficient = int(names["first_coefficient"])
   second_coefficient = int(names["second_coefficient"])
   at_point = names["evaluate"] == "point"
   point = sympy.pi * sympy.Rational(names["angle"])

   function = first_coefficient * first["function"] + second_coefficient * second["function"]
   key_expression = first_coefficient * first["derivative"] + second_coefficient * second["derivative"]
   reversed_expression = -key_expression
   sign_dropped_expression = first_coefficient * first["derivative"] - second_coefficient * second["derivative"]
   term_by_term_expression = first_coefficient * first["term_by_term"] + second_coefficient * second["term_by_term"]

   steps = [
      Step(
         text=(
            f"Rewrite with sine and cosine: {math(rf'{tex(first["function"])} = \frac{{{tex(first["numerator"])}}}{{{tex(first["denominator"])}}}')} "
            f"and {math(rf'{tex(second["function"])} = \frac{{{tex(second["numerator"])}}}{{{tex(second["denominator"])}}}')}."
         ),
         rule="rewrite over sine and cosine",
      ),
      Step(
         text=(
            "Apply the quotient rule to each piece and simplify the numerators with "
            f"{math(r'\sin^{2} x + \cos^{2} x = 1')}: the derivatives are {math(tex(first["derivative"]))} and "
            f"{math(tex(second["derivative"]))}."
         ),
         rule="quotient rule and a Pythagorean identity",
      ),
      Step(
         text=f"So {math("h'(x) = " + tex(key_expression))}.",
         value=key_expression,
         rule="constant multiple and sum rules",
      ),
   ]

   if at_point:
      key_value = _at(key_expression, point)
      values = [_at(reversed_expression, point), _at(sign_dropped_expression, point), _at(term_by_term_expression, point)]
      stem = (
         f"Let {math('h(x) = ' + tex(function))}. Find the exact value of {math(f"h'\\left({tex(point)}\\right)")}."
      )
      steps.append(Step(
         text=f"At {math('x = ' + tex(point))}, {math(f"h'\\left({tex(point)}\\right) = {tex(key_value)}")}.",
         value=key_value,
         rule="evaluate at a standard angle",
      ))
   else:
      key_value = key_expression
      values = [reversed_expression, sign_dropped_expression, term_by_term_expression]
      stem = f"Let {math('h(x) = ' + tex(function))}. Find {math("h'(x)")}."

   distractors = [
      Distractor(
         error_path="BC-ERR-02021",
         derivation="the numerator terms of each quotient rule taken in reverse order, which flips every sign",
         value=values[0],
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-02025",
         derivation=f"the derivative of {names['second']} given without its negative sign",
         value=values[1],
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-02026",
         derivation="each quotient differentiated as the derivative of its numerator over the derivative of its denominator",
         value=values[2],
         mechanism="conceptual_confusion",
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
