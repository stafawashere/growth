"""BC-QA-07007, whether a candidate function is the particular solution of a differential equation with an initial condition."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "case", "type": "label", "role": "difficulty", "domain": {"values": ["solution", "wrong_initial_value"]}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"values": [-3, -2, -1, 1, 2, 3]}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 5, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
   ],
   "constraints": [
      "initial != level",
      "case == 'solution' or initial + shift != level",
      "rate != 1 or level != 0",
   ],
   "derived": [
      {"name": "candidate_start", "expression": "initial if case == 'solution' else initial + shift"},
   ],
   "invariants": [
      "len(key) > 30",
   ],
   "dial_bindings": [
      {"parameter": "case", "difficulty_factor_id": "BC-DF-14", "settings": {"solution": "off", "wrong_initial_value": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["case", "rate", "level", "initial", "shift"]},
   ],
   "notes": "The equation is dy/dx = k(y - L) with f(0) = y0 required. The candidate L + (c - L) e^(kx) always satisfies the equation; c equals y0 on half the draws and misses it by a nonzero shift on the other half, so the verdict is yes or no in equal shares.",
}

x = sympy.Symbol("x")
y = sympy.Symbol("y")


def _times_gap(rate, inner, level):
   factor = {1: "", -1: "-"}.get(rate, str(rate))

   if level == 0:
      return f"{factor}{inner}"

   sign = "-" if level > 0 else "+"

   return rf"{factor}\left({inner} {sign} {abs(level)}\right)"


def build(names):
   rate = int(names["rate"])
   level = int(names["level"])
   initial = int(names["initial"])
   candidate_start = int(names["candidate_start"])
   is_solution = names["case"] == "solution"

   coefficient = candidate_start - level
   exponential = sympy.exp(rate * x)
   candidate = level + coefficient * exponential
   derivative = sympy.diff(candidate, x)
   right_side = rate * (y - level)
   right_on_candidate = sympy.expand(rate * (candidate - level))

   equation_text = math(rf"\frac{{dy}}{{dx}} = {tex(right_side)}")
   holds_text = math(rf"f^{{\prime}}(x) = {_times_gap(rate, 'f(x)', level)}")
   fails_text = math(rf"f^{{\prime}}(x) \ne {_times_gap(rate, 'f(x)', level)}")

   stem = (
      f"Determine whether {math('f(x) = ' + tex(candidate))} is the particular solution to the differential equation "
      f"{equation_text} with the initial condition {math(f'f(0) = {initial}')}. Justify your answer."
   )

   steps = [
      Step(
         text=f"Differentiate the candidate: {math(rf'f^{{\prime}}(x) = {tex(derivative)}')}.",
         point_type_id="BC-PT-99005",
         rule="differentiate the candidate",
      ),
      Step(
         text=(
            f"Substitute into the right side: {math(_times_gap(rate, 'f(x)', level) + ' = ' + tex(right_on_candidate))}, "
            f"which equals {math(r'f^{\prime}(x)')} for every x, so f satisfies the differential equation."
         ),
         point_type_id="BC-PT-99068",
         rule="verification of the equation",
      ),
      Step(
         text=(
            f"Check the initial condition: {math(f'f(0) = {tex(candidate.subs(x, 0))}')}, "
            + ("which matches, so f is the particular solution." if is_solution else f"which is not {initial}, so f is not the particular solution.")
         ),
         point_type_id="BC-PT-99004",
         rule="initial condition",
      ),
   ]

   substitution_label = (
      f"No. Substituting f(x) for y on both sides gives {math(tex(candidate))} on the left and "
      f"{math(tex(right_on_candidate))} on the right, which are not equal."
   )
   unshown_failure_label = f"No. {fails_text} for the candidate, so f is not a solution of the equation."

   if is_solution:
      key_label = f"Yes. {holds_text} for every x, and {math(f'f(0) = {initial}')}."
      distractors = [
         Distractor(
            error_path="BC-ERR-07006",
            derivation="f substituted for y and for dy/dx alike, never differentiated",
            label=substitution_label,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-07008",
            derivation="failure asserted with no input at which the two sides disagree",
            label=unshown_failure_label,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-07009",
            derivation="the check of the equation read as making f the only solution of the equation, with the initial condition never used",
            label=f"Yes. {holds_text} for every x, so f is the only solution of the equation.",
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      key_label = f"No. {holds_text} for every x, but {math(f'f(0) = {candidate_start}')}, not {initial}."
      distractors = [
         Distractor(
            error_path="BC-ERR-07007",
            derivation="the equation verified and the candidate declared the particular solution without testing f(0)",
            label=f"Yes. {holds_text} for every x, so f is the particular solution.",
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-07006",
            derivation="f substituted for y and for dy/dx alike, never differentiated",
            label=substitution_label,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-07008",
            derivation="failure of the equation asserted with no input exhibited, when the equation in fact holds",
            label=unshown_failure_label,
            mechanism="conceptual_confusion",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="determine",
      notes={"verdict": "yes" if is_solution else "no"},
   )
