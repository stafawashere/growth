"""BC-QA-99010, an accumulation split at a change of model and bounded by a supplied improper integral, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-99010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "base_density", "type": "integer", "role": "safe", "domain": {"min": 4, "max": 9, "step": 1}},
      {"name": "swing", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "split", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "tail", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 12, "step": 1}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["salt", "iron"]}},
      {"name": "comparison", "type": "label", "role": "difficulty", "domain": {"values": ["named", "explicit"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "bound > first_piece + tail",
   ],
   "dial_bindings": [
      {"parameter": "comparison", "difficulty_factor_id": "BC-DF-14", "settings": {"explicit": "off", "named": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-04",
         "figure_kind": None,
         "requires": ["base_density", "swing", "stretch", "split", "tail", "context"],
      },
   ],
   "notes": "Above the split depth the density is base_density + swing sin(h^2 / stretch); below it the density g is unknown but satisfies 0 <= g(h) <= b(h), where the improper integral of b from the split depth to infinity is tail. The stated bound is the whole number just above the first piece plus tail.",
}

CONTEXTS = {
   "salt": ("dissolved salt", "grams"),
   "iron": ("iron ore", "kilograms"),
}

h = sympy.Symbol("h")


def _labelled(expression_tex, reason, bound):
   return f"{math('T = ' + expression_tex)}, and {math(rf'T \le {bound}')} because {reason}."


def build(names):
   base_density = names["base_density"]
   swing = names["swing"]
   stretch = names["stretch"]
   split = names["split"]
   tail = names["tail"]
   is_explicit = names["comparison"] == "explicit"
   substance, units = CONTEXTS[names["context"]]

   model = base_density + swing * sympy.sin(h**2 / stretch)
   first_piece = numeric_integral(model, h, 0, split)
   bound = int(sympy.floor(first_piece + tail)) + 1
   comparison_function = tail * sympy.exp(split - h)

   if is_explicit:
      comparison_text = (
         f"{math(r'0 \le g(h) \le ' + tex(comparison_function))} for {math(rf'h \ge {split}')}, and "
         f"{math(rf'\int_{{{split}}}^{{\infty}} ' + tex(comparison_function) + rf'\,dh = {tail}')}"
      )
   else:
      comparison_text = (
         f"{math(r'0 \le g(h) \le b(h)')} for {math(rf'h \ge {split}')}, where b is a function with "
         f"{math(rf'\int_{{{split}}}^{{\infty}} b(h)\,dh = {tail}')}"
      )

   stem = (
      f"A vertical shaft is drilled to an unknown depth D meters, where {math(f'D > {split}')}. The amount of {substance} "
      f"per meter of depth is {math('f(h) = ' + tex(model))} {units} per meter for {math(rf'0 \le h \le {split}')}, where h "
      f"is the depth in meters. Below depth {split} the amount per meter is an unknown continuous function g(h), and "
      f"{comparison_text}. Let T be the total amount of {substance}, in {units}, along the whole shaft. Write an expression "
      f"involving integrals for T, and explain why {math(rf'T \le {bound}')}. Use a calculator for any numerical work."
   )

   correct_expression = rf"\int_{{0}}^{{{split}}} f(h)\,dh + \int_{{{split}}}^{{D}} g(h)\,dh"
   bound_name = "b(h)" if not is_explicit else tex(comparison_function)
   reason = (
      rf"{math(rf'\int_{{0}}^{{{split}}} f(h)\,dh \approx ' + decimal_text(first_piece))} and "
      rf"{math(rf'\int_{{{split}}}^{{D}} g(h)\,dh \le \int_{{{split}}}^{{\infty}} ' + bound_name + rf'\,dh = {tail}')}"
   )

   steps = [
      Step(
         text=f"The model changes at depth {split}, so split the total there: {math('T = ' + correct_expression)}.",
         rule="additivity over adjacent intervals",
      ),
      Step(
         text=f"A calculator gives {math(rf'\int_{{0}}^{{{split}}} f(h)\,dh \approx ' + decimal_text(first_piece))}.",
         value=first_piece,
         rule="numerical integration",
      ),
      Step(
         text=(
            f"Since {math(r'0 \le g(h) \le ' + bound_name)} and the interval from {split} to D lies inside the interval from "
            f"{split} to infinity, {math(rf'\int_{{{split}}}^{{D}} g(h)\,dh \le {tail}')}. So "
            f"{math(rf'T \le {decimal_text(first_piece)} + {tail} < {bound}')}."
         ),
         rule="comparison of integrals",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-99012",
         derivation="the integral of g from the split depth to D written as g(D) - g(split), as though g were its own antiderivative",
         label=_labelled(rf"\int_{{0}}^{{{split}}} f(h)\,dh + g(D) - g({split})", reason, bound),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99032",
         derivation="a constant of integration attached to a sum of definite integrals",
         label=_labelled(correct_expression + " + C", reason, bound),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99032",
         derivation="the unknown function set equal to its own integral and substituted for the second piece",
         label=_labelled(rf"\int_{{0}}^{{{split}}} f(h)\,dh + g(h), \text{{ where }} g(h) = \int_{{{split}}}^{{D}} g(h)\,dh", reason, bound),
         mechanism="algebra_slip",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_labelled(correct_expression, reason, bound)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-04",
      calculator_status="calculator",
      setup_required=True,
      command_verb="explain",
      notes={"first_piece": first_piece, "bound": bound},
   )
