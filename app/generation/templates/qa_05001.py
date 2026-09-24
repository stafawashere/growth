"""BC-QA-05001, whether the Mean Value Theorem guarantees an input with a stated derivative value, from a table."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-05001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inputs", "type": "integer", "role": "safe", "count": 5, "distinct": True, "order": "increasing", "domain": {"min": 0, "max": 12, "step": 1}},
      {"name": "outputs", "type": "integer", "role": "safe", "count": 5, "domain": {"min": -9, "max": 20, "step": 1}},
      {"name": "rows", "type": "label", "role": "safe", "domain": {"values": ["0-2", "1-3", "2-4", "0-3", "1-4", "0-4"]}},
      {"name": "context", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
      {"name": "hypothesis", "type": "label", "role": "difficulty", "domain": {"values": ["differentiable", "corner", "jump"]}},
   ],
   "constraints": [
      "average_rate != 0",
   ],
   "derived": [
      {"name": "low_row", "expression": "0 if rows in ['0-2', '0-3', '0-4'] else (1 if rows in ['1-3', '1-4'] else 2)"},
      {"name": "high_row", "expression": "2 if rows == '0-2' else (3 if rows in ['1-3', '0-3'] else 4)"},
      {"name": "average_rate", "expression": "(outputs[high_row] - outputs[low_row]) / (inputs[high_row] - inputs[low_row])"},
   ],
   "invariants": [
      "average_rate != 0",
      "low_row < high_row",
   ],
   "dial_bindings": [
      {"parameter": "context", "difficulty_factor_id": "BC-DF-14", "settings": {"bare": "off", "context": "low"}},
      {"parameter": "hypothesis", "difficulty_factor_id": "BC-DF-09", "settings": {"differentiable": "off", "corner": "low", "jump": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["inputs", "outputs", "rows", "context", "hypothesis"]},
   ],
   "notes": "The named value always equals the average rate of change over the named rows. When f is differentiable the verdict is yes; when f has a corner or a jump strictly inside the interval, a hypothesis of the Mean Value Theorem fails and the verdict is no, which happens on two thirds of draws.",
}

CONTEXT_OPENING = "The function f gives the height, in meters, of a drone above the ground at time x seconds. "


def build(names):
   inputs = [int(value) for value in names["inputs"]]
   outputs = [int(value) for value in names["outputs"]]
   low_row = int(names["low_row"])
   high_row = int(names["high_row"])
   low, high = inputs[low_row], inputs[high_row]
   low_value, high_value = outputs[low_row], outputs[high_row]
   rate = sympy.Rational(high_value - low_value, high - low)
   is_context = names["context"] == "context"

   table = table_figure(
      ["x", "f(x)"],
      [[str(value), str(output)] for value, output in zip(inputs, outputs)],
      alt="The table lists f(x) at five inputs, " + "; ".join(f"f({value}) = {output}" for value, output in zip(inputs, outputs)) + ".",
   )

   hypothesis = names["hypothesis"]
   break_point = sympy.Rational(low + high, 2)
   break_text = tex(break_point)

   if hypothesis == "differentiable":
      hypothesis_sentence = "The function f is differentiable for all real x. "
   elif hypothesis == "corner":
      hypothesis_sentence = (
         f"The function f is continuous for all real x and differentiable for all x except {math(f'x = {break_text}')}, "
         "where its graph has a corner. "
      )
   else:
      hypothesis_sentence = (
         f"The function f is differentiable for all x except {math(f'x = {break_text}')}, where it has a jump "
         "discontinuity. "
      )

   opening = (CONTEXT_OPENING if is_context else "") + hypothesis_sentence
   derivative_target = "f'(c) = " + tex(rate)
   stem = (
      f"{opening}Selected values of f are given in the table. Does the Mean Value Theorem guarantee a value c, with "
      f"{math(f'{low} < c < {high}')}, such that {math(derivative_target)}? Justify the answer."
   )

   subtracted = f"({low_value})" if low_value < 0 else str(low_value)
   quotient = rf"\frac{{f({high}) - f({low})}}{{{high} - {low}}} = \frac{{{high_value} - {subtracted}}}{{{high - low}}} = {tex(rate)}"
   reversed_quotient = rf"\frac{{f({low}) - f({high})}}{{{high} - {low}}} = {tex(-rate)}"
   closed = math(rf"\left[{low}, {high}\right]")
   open_interval = math(f"({low}, {high})")
   short_quotient = math(rf"\frac{{f({high}) - f({low})}}{{{high} - {low}}} = {tex(rate)}")
   break_at = math(f"x = {break_text}")

   average_step = Step(
      text=f"The average rate of change of f over {closed} is {math(quotient)}.",
      value=rate,
      point_type_id="BC-PT-99021",
      rule="average rate of change",
   )

   if hypothesis == "differentiable":
      steps = [
         average_step,
         Step(
            text=(
               f"f is differentiable, so it is continuous on {closed} and differentiable on {open_interval}. By the "
               f"Mean Value Theorem there is a c with {math(f'{low} < c < {high}')} and {math(derivative_target)}. The answer is yes."
            ),
            point_type_id="BC-PT-99017",
            rule="Mean Value Theorem",
         ),
      ]
      key_label = (
         f"Yes. Since f is differentiable, it is continuous on {closed}, and {short_quotient}, so the Mean Value Theorem "
         "guarantees such a c."
      )
      distractors = [
         Distractor(
            error_path="BC-ERR-05003",
            derivation="the average rate formed with the subtraction in the wrong order, which gives the opposite of the named value",
            label=(
               f"No. Since f is differentiable, it is continuous on {closed}, but {math(reversed_quotient)}, so the Mean Value "
               "Theorem does not give such a c."
            ),
            mechanism="sign_error",
         ),
         Distractor(
            error_path="BC-ERR-05006",
            derivation="the Intermediate Value Theorem cited for a claim about the derivative",
            label=(
               f"Yes. Since f is differentiable, it is continuous on {closed}, and {short_quotient}, so the Intermediate Value "
               "Theorem guarantees such a c."
            ),
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-05002",
            derivation="continuity on the closed interval never drawn from differentiability; the hypothesis offered is only that f is defined",
            label=(
               f"Yes. Since f is defined at every point of {closed}, and {short_quotient}, the Mean Value Theorem "
               "guarantees such a c."
            ),
            mechanism="theorem_condition_ignored",
         ),
      ]
   else:
      if hypothesis == "corner":
         failure = f"f is not differentiable at {break_at}, which lies in {open_interval}"
      else:
         failure = f"f is not continuous at {break_at}, which lies in {closed}"

      steps = [
         average_step,
         Step(
            text=(
               f"The Mean Value Theorem needs f continuous on {closed} and differentiable on {open_interval}, but {failure}. "
               f"The theorem does not apply, and no other fact given forces {math(derivative_target)} anywhere in the "
               "interval, so the answer is no."
            ),
            point_type_id="BC-PT-99017",
            rule="hypotheses of the Mean Value Theorem",
         ),
      ]
      key_label = (
         f"No. Although {short_quotient}, {failure}, so the Mean Value Theorem does not apply and such a c is not "
         "guaranteed."
      )
      distractors = [
         Distractor(
            error_path="BC-ERR-99008",
            derivation=f"the Mean Value Theorem applied without checking its hypotheses, which fail at x = {break_point}",
            label=(
               f"Yes. Since {short_quotient}, the Mean Value Theorem guarantees such a c, with f taken to be differentiable "
               f"on {open_interval}."
            ),
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-05006",
            derivation="the Intermediate Value Theorem cited for a claim about the derivative",
            label=(
               f"Yes. Since {short_quotient}, the Intermediate Value Theorem guarantees such a c, with f taken to be "
               f"continuous on {closed}."
            ),
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-05004",
            derivation="existence asserted from the arithmetic alone, with no theorem named and no check that one applies",
            label=(
               f"Yes. Since {short_quotient}, there is a c with {math(f'{low} < c < {high}')} and {math(derivative_target)}, "
               "because an average rate of change is always reached by the derivative."
            ),
            mechanism="theorem_condition_ignored",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="justify",
   )
