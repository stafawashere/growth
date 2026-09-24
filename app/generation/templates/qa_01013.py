"""BC-QA-01013, a limit statement in notation translated into a description of the function and its graph."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "number", "type": "rational", "role": "safe", "domain": {"min": -10, "max": 10, "step": 0.5}},
      {"name": "side", "type": "label", "role": "safe", "domain": {"values": ["left", "right"]}},
      {"name": "growth", "type": "label", "role": "safe", "domain": {"values": ["up", "down"]}},
      {"name": "direction", "type": "label", "role": "safe", "domain": {"values": ["positive", "negative"]}},
      {"name": "letter", "type": "label", "role": "safe", "domain": {"values": ["f", "g", "h", "k"]}},
      {"name": "statement", "type": "label", "role": "difficulty", "domain": {"values": ["infinite_limit", "limit_at_infinity"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "'asymptote' in key",
   ],
   "dial_bindings": [
      {"parameter": "statement", "difficulty_factor_id": "BC-DF-03", "settings": {"limit_at_infinity": "off", "infinite_limit": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["number", "side", "growth", "direction", "letter", "statement"]},
   ],
   "notes": "An infinite limit statement is a one sided limit at number that is plus or minus infinity; a limit at infinity statement is the limit of the function at one end equal to number. The options are verbal descriptions, each ending with what the statement says about the graph.",
}


def build(names):
   number = sympy.nsimplify(names["number"])
   letter = names["letter"]
   side = names["side"]
   grows_up = names["growth"] == "up"
   is_positive_end = names["direction"] == "positive"
   is_infinite_limit = names["statement"] == "infinite_limit"

   number_tex = tex(number)
   number_text = math(number_tex)
   value = f"{letter}(x)"

   if is_infinite_limit:
      superscript = "-" if side == "left" else "+"
      infinity_tex = r"\infty" if grows_up else r"-\infty"
      statement_tex = rf"\lim_{{x \to {number_tex}^{{{superscript}}}}} {letter}(x) = {infinity_tex}"
      unbounded = "increases without bound" if grows_up else "decreases without bound"
      vertical = math(f"x = {number_tex}")
      key_label = f"As x approaches {number_text} from the {side}, {value} {unbounded}, so the line {vertical} is a vertical asymptote."
      steps = [
         Step(text=f"The input approaches {number_text} from the {side} only, and the output is not approaching any number.", rule="read the input side and the output behaviour"),
         Step(text=f"The values {value} {unbounded}, which is what an infinite limit means, so the graph has the vertical asymptote {vertical}.", rule="infinite limit and vertical asymptote"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-01033",
            derivation="the infinite limit at an input read as a limit at infinity, with the roles of input and output exchanged",
            label=(
               f"As x {unbounded}, {value} approaches {number_text}, so the line {math(f'y = {number_tex}')} is a "
               "horizontal asymptote."
            ),
            mechanism="reversed_quantities",
         ),
         Distractor(
            error_path="BC-ERR-01002",
            derivation="the one sided statement read as describing the behaviour on both sides of the input",
            label=f"As x approaches {number_text} from either side, {value} {unbounded}, so the line {vertical} is a vertical asymptote.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01020",
            derivation="the statement that the limit equals infinity read as a statement that the limit exists",
            label=f"As x approaches {number_text} from the {side}, the limit of {value} exists and equals {math(infinity_tex)}, so there is no asymptote at {vertical}.",
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      end_tex = r"\infty" if is_positive_end else r"-\infty"
      statement_tex = rf"\lim_{{x \to {end_tex}}} {letter}(x) = {number_tex}"
      travel = "increases without bound" if is_positive_end else "decreases without bound"
      horizontal = math(f"y = {number_tex}")
      key_label = f"As x {travel}, {value} approaches {number_text}, so the line {horizontal} is a horizontal asymptote."
      steps = [
         Step(text=f"The input {travel}, so the statement is about the {'right' if is_positive_end else 'left'} end of the graph only.", rule="read the input behaviour"),
         Step(text=f"The outputs approach the number {number_text} there, so the graph has the horizontal asymptote {horizontal} at that end.", rule="limit at infinity and horizontal asymptote"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-01033",
            derivation="the limit at infinity read as an infinite limit at an input, with the roles of input and output exchanged",
            label=(
               f"As x approaches {number_text}, {value} {travel}, so the line {math(f'x = {number_tex}')} is a "
               "vertical asymptote."
            ),
            mechanism="reversed_quantities",
         ),
         Distractor(
            error_path="BC-ERR-01002",
            derivation="the statement about one end read as describing both ends of the graph",
            label=f"As x increases or decreases without bound, {value} approaches {number_text}, so the line {horizontal} is a horizontal asymptote at both ends.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01021",
            derivation="infinity treated as an input at which the function takes the value",
            label=f"The value of {letter} at the input {math(end_tex)} is {number_text}, so the graph of {letter} contains the point {math(rf'({end_tex}, {number_tex})')}.",
            mechanism="conceptual_confusion",
         ),
      ]

   stem = (
      f"A function {letter} satisfies {math(statement_tex)}. Describe in words what this statement says about "
      f"{letter} and about its graph."
   )

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="interpret",
   )
