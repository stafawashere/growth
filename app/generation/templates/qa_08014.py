"""BC-QA-08014, the arc length of the graph of a function: the integral written out, or evaluated with a calculator."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "safe", "domain": {"values": ["log", "exponential", "radical"]}},
      {"name": "scale", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "3/2", "2", "5/2", "3"]}},
      {"name": "left", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "units", "type": "label", "role": "safe", "domain": {"values": ["feet", "meters", "inches"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
      {"name": "task", "type": "label", "role": "difficulty", "domain": {"values": ["setup", "evaluate"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "right", "expression": "left + width"},
   ],
   "invariants": [
      "task == 'setup' or nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-05", "settings": {"bare": "off", "context": "low"}},
      {"parameter": "task", "difficulty_factor_id": "BC-DF-09", "settings": {"setup": "off", "evaluate": "off"}},
   ],
   "calculator_guard": "True if task == 'setup' else exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["form", "scale", "left", "width", "task"]},
      {"representation": "BC-REP-09", "figure_kind": None, "requires": ["form", "scale", "left", "width", "task"]},
   ],
   "notes": "Each function is a product, so its derivative needs the product rule, and the derivative is positive for x at least 1, which keeps the square root of 1 + f'(x) real for the unsquared-derivative distractor. The setup task asks for the integral itself as a statement key; the evaluate task asks for its value with a calculator. Neither task is a named dial setting, so the task binding leaves BC-DF-09 off.",
}

CONTEXTS = ("A wire is bent into the shape of the graph of", "with x and y measured in")

x = sympy.Symbol("x")


def _function(form, scale):
   if form == "log":
      return scale * x * sympy.log(x)

   if form == "exponential":
      return scale * x * sympy.exp(x / 4)

   return scale * x * sympy.sqrt(x + 1)


def _integral_tex(low, high, integrand):
   return rf"\int_{{{low}}}^{{{high}}} {integrand}\,dx"


def build(names):
   form = names["form"]
   scale = names["scale"]
   left = names["left"]
   right = names["right"]
   units = names["units"]
   is_context = names["framing"] == "context"
   is_setup = names["task"] == "setup"

   function = _function(form, scale)
   derivative = sympy.simplify(sympy.diff(function, x))
   derivative_tex = tex_f(derivative)

   radical = rf"\sqrt{{1 + \left({derivative_tex}\right)^{{2}}}}"
   no_radical = rf"\left(1 + \left({derivative_tex}\right)^{{2}}\right)"
   unsquared = rf"\sqrt{{1 + {derivative_tex}}}"

   key_tex = _integral_tex(left, right, radical)
   no_radical_tex = _integral_tex(left, right, no_radical)
   unsquared_tex = _integral_tex(left, right, unsquared)
   wrong_limits_tex = _integral_tex(0, right, radical)

   if is_context:
      opening = f"{CONTEXTS[0]} {math('f(x) = ' + tex_f(function))} for {math(rf'{left} \le x \le {right}')}, {CONTEXTS[1]} {units}."
      subject = "the length of the wire"
   else:
      opening = f"Let {math('f(x) = ' + tex_f(function))}."
      subject = f"the length of the graph of f from {math(f'x = {left}')} to {math(f'x = {right}')}"

   if is_setup:
      stem = f"{opening} Write, but do not evaluate, an integral expression in terms of x that gives {subject}."
   else:
      stem = (
         f"{opening} Using a calculator, find {subject}. Show the setup for the calculation, and give the value "
         "correct to three decimal places."
      )

   steps = [
      Step(
         text=f"By the product rule, {math(r"f'(x) = " + derivative_tex)}.",
         point_type_id="BC-PT-99022",
         rule="product rule",
      ),
      Step(
         text=f"The length is the integral of {math(r"\sqrt{1 + \left(f'(x)\right)^{2}}")} over the interval: {math(key_tex)}.",
         point_type_id="BC-PT-99051",
         rule="arc length",
      ),
   ]

   if is_setup:
      distractors = [
         Distractor("BC-ERR-08041", "the square root left off the arc length integrand", label=math(no_radical_tex), mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08042", "the derivative left unsquared inside the radical", label=math(unsquared_tex), mechanism="algebra_slip"),
         Distractor("BC-ERR-08019", "the lower limit taken as 0, the start of the axis, instead of the left end of the stated interval", label=math(wrong_limits_tex), mechanism="wrong_limits"),
      ]

      return Instance(
         stem=stem,
         key=Key(form="statement", label=math(key_tex)),
         steps=steps,
         distractors=distractors,
         representation="BC-REP-01",
         calculator_status="no_calculator",
         command_verb="write",
      )

   length = numeric_integral(sympy.sqrt(1 + derivative**2), x, left, right)
   steps.append(
      Step(
         text=f"A calculator gives the value {decimal_text(length)}" + (f" {units}." if is_context else "."),
         value=length,
         point_type_id="BC-PT-99004",
         rule="numerical integration",
      )
   )
   distractors = [
      Distractor("BC-ERR-08041", "the square root left off, the integral of 1 + f'(x)^2", numeric_integral(1 + derivative**2, x, left, right), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-08042", "the derivative left unsquared, the integral of the square root of 1 + f'(x)", numeric_integral(sympy.sqrt(1 + derivative), x, left, right), mechanism="algebra_slip"),
      Distractor("BC-ERR-08019", "the arc length integrand integrated from 0 instead of from the left end of the stated interval", numeric_integral(sympy.sqrt(1 + derivative**2), x, 0, right), mechanism="wrong_limits"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=length, decimals=3, units=units if is_context else None),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-09",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
