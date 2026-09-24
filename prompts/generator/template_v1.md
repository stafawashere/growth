---
title: Author one item template for one archetype
version: v1
role: generator
model: offline Claude Code session, claude-opus-5-5
purpose: The instruction an offline Claude Code session follows to author one parameterised item template per archetype, which the backend instantiates into items.
---

# Author one item template for one archetype

You write one Python module, `app/generation/templates/qa_<digits>.py`, for the archetype you are
given. The module is a mould: the backend draws parameters from its spec, calls `build`, and turns
the result into item records. You never write items one at a time and you never pick parameter
values yourself.

## Read first

1. `python3 tools/template_gate.py --context <archetype id>` prints the archetype record, the
   BC-ERR errors its skills hold, its BC-PT point types and its BC-DF dials. That is everything
   you may use. The archetype's `typical_wording` is a paraphrase written for the library and may
   guide phrasing; it is never copied.
2. The exemplars: `qa_08001.py` (a calculator item with a three-decimal key), `qa_06004.py` (a
   graph figure with an exact key), `qa_10007.py` (a statement key chosen among labelled options).
3. `app/generation/kit.py` for the parts `build` returns and the figure helpers, and
   `prompts/generator/figure_spec_v1.md` and `prompts/generator/calculator_v1.md` when the item
   carries a figure or is calculator active.

Never open, quote or imitate an AP question, a released exam, a scoring guideline or anything under
`cache/`. Stems are written from the archetype's structure alone.

## The module

- `ARCHETYPE_ID`, `TEMPLATE_VERSION = "1"`, `AUTHORED_BY` naming the model and the run.
- `SPEC`, the archetype's parameter spec in the schema at `schemas/archetypes.schema.json`
  `$defs/parameter_spec`: every parameter with a `type`, a `role` (`safe` for a number or a context
  that changes nothing about the solution path, `difficulty` for anything that changes what the
  student has to do), an explicit `domain`, `constraints` and `invariants` written as expressions
  the checker evaluates, `dial_bindings` mapping each difficulty parameter's values to settings of
  a BC-DF dial the archetype carries (a two-state dial uses `off` and `low`), a `calculator_guard`
  on every `no_calculator` or `either` archetype (`"exact(key)"` for an exact answer, `"True"` for a
  statement), and one `representation_bindings` entry per representation the template emits.
- `build(names)`, returning a `kit.Instance`: the stem, the key, the worked solution steps, exactly
  three distractors, the representation, the item's calculator status, and a figure when the
  representation needs one.

## Rules the gate enforces

The gate (`python3 tools/template_gate.py <archetype id>`) draws 300 parameter sets and fails the
template on a single bad draw. It checks:

- Every distractor names a BC-ERR id held by the archetype's skills, and a mechanism from the
  distractor taxonomy. Derive each distractor's value by actually making that error on this draw,
  and say how in `derivation`. A distractor that does not follow from its named error is a defect
  the gate cannot see; the reviewer will.
- The key and every distractor are pairwise different, symbolically and numerically; numeric
  options differ at three decimals.
- A `symbolic` key is exact and round-trips through MathJSON; the last step that carries a value
  equals the key; no valued step restates the one before it (leave `value` off a step that only
  restates).
- A `numeric` key is on a calculator item only, has `decimals=3` and is not a whole number at three
  places; a calculator item sets `setup_required=True` and its stem asks for the setup.
- A `statement` key has a label, each distractor a different label; use it for verdicts,
  classifications, intervals, sets of points and interpretations, which no MathJSON value holds.
- A no-calculator template calls no numeric method (`evalf`, `N`, `Float`, `nsolve`, the kit's
  `numeric_integral` or `three_decimals`); its path is closed form.
- Every step's `point_type_id` is one of the archetype's point types.
- A representation in the spec's bindings; a figure of the bound kind when the representation is
  graphical, tabular, a slope field or a geometric diagram; every figure label inside the window;
  a stem that says "shown", "figure" or "the table" carries a figure.
- LaTeX between `\(` and `\)` is balanced and has no doubled signs such as `+ -`.
- The spec's constraints hold on every draw and its invariants hold on every built item.
- At least 2,000 parameter tuples satisfy the constraints, at least 40 distinct stems and figures
  appear in 300 draws, and varying a `safe` parameter alone never changes the solution path.

## Rules the gate cannot enforce

- One stem, one answer. State every domain, quadrant, branch and requested form the answer depends
  on. Say "exact value" when the key is exact.
- Stems read as a question to a student: "Find", "What is", "Classify". Never "Which of the
  following", because the item is also served as a short answer.
- Numbers stay small and clean on no-calculator items; a no-calculator answer never needs a
  decimal approximation.
- Units appear in context items and in the answer when the quantity has them.
- Worked steps are short, correct and in the order the archetype's `expected_solution_path` gives.
- No study advice, no schedules, no mention of the exam.

## Done

`python3 tools/template_gate.py <archetype id>` prints `PASS`, and you have read three records from
`python3 tools/template_gate.py --show 3 <archetype id>` as a student would and found nothing
wrong. If the archetype's skills hold fewer than three errors that honestly produce distractors,
do not stretch an error to fit. Write `var/p4/error_links/<archetype id>.json` naming the existing
BC-ERR ids whose `skills` should gain this archetype's skills and why, and report it.
