"""docs/plan/13-ai-engineering.md quotes cost figures, and every one of them has to come out of
tools/cost_model.py rather than out of a hand edit. Two ways that can go wrong: the arithmetic in
the calculator drifts from the formula the document states, and a figure is patched in the prose
without the calculator changing. One test for each.
"""
from pathlib import Path

import pytest

from tools import cost_model

REPO = Path(__file__).resolve().parents[2]
DOCUMENTS = (
   REPO / "docs" / "plan" / "13-ai-engineering.md",
   REPO / "docs" / "operator" / "ai-operating-costs.md",
   REPO / "docs" / "plan" / "14-token-economy.md",
)


def test_tutor_cycle_matches_the_formula_the_document_states():
   """13 states the prefix term as writes x prefix x write_rate + (calls - writes) x prefix x
   read_rate. A regression that charged every call as a write, or none, changes this number."""
   figures = cost_model.figures()
   sonnet = cost_model.PRICES["claude-sonnet-5"]
   tutor = cost_model.ROLES["tutor"]
   calls = cost_model.TUTOR_CALLS_PER_SESSION * cost_model.SESSIONS
   writes = cost_model.SESSIONS

   prefix = writes * tutor["prefix"] * sonnet["write_1h"] + (calls - writes) * tutor["prefix"] * sonnet["read"]
   uncached = calls * tutor["uncached"] * sonnet["input"]
   output = calls * tutor["visible"] * sonnet["output"]
   by_hand = (prefix + uncached + output) / 1e6

   assert figures["tutor.cycle"] == pytest.approx(by_hand)
   assert round(by_hand, 2) == 5.01


def test_the_effort_lever_is_the_high_minus_medium_thinking_output():
   """The generator's effort lever is exactly the extra thinking tokens at the batch output
   rate; a change to how thinking enters output_cost would silently move the largest lever."""
   figures = cost_model.figures()
   extra_thinking = cost_model.GENERATOR_THINKING_HIGH - cost_model.GENERATOR_THINKING_MEDIUM
   batch_output = cost_model.PRICES["claude-opus-5"]["output"] * cost_model.BATCH_DISCOUNT
   expected = figures["generator.calls"] * extra_thinking * batch_output / 1e6

   assert figures["generator.lever.effort"] == pytest.approx(expected)


def test_claude_only_tier_grader_line_reads_the_labelling_pass():
   """docs/plan/14-token-economy.md open question 2 closed on the operator's labelling pass in
   data/bc_pt_determinism_labels.json, 48 deterministic and 28 model_required of 76 active BC-PT
   records. A regression that reverted the grader line to the 1,200-point worst case, or to the
   17-of-76 field bound, would silently reopen an overrun this test pins shut."""
   figures = cost_model.figures()

   assert cost_model.MEASURED_MODEL_JUDGED_POINT_RECORDS == 28
   assert round(figures["grader.measured_model_share_cycle"], 2) == 12.44
   assert round(figures["tier.hundred_claude_only.grader_line"], 2) == 12.44
   assert round(figures["tier.hundred_claude_only.pre_cadence_ruling_evals_line"], 2) == 38.00


def test_claude_only_tier_reads_the_2026_09_23_eval_cadence_ruling():
   """Ruled 2026-09-23: the labelling pass alone left an $8.07 overrun with no further sourced
   lever (docs/plan/14-token-economy.md), so the operator cut the golden set 2 canary cadence from
   monthly (9) to 2 runs a cycle, keeping golden set 3 at its full monthly cadence of 9 since it is
   the cheaper line and cutting it alone cannot close the gap. This test pins the new total and the
   at-least-$5.00 headroom the ruling requires; a regression to the old MONTHLY_RUNS canary cadence
   would silently reopen the overrun this ruling closed."""
   figures = cost_model.figures()

   assert cost_model.CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE == 2
   assert round(figures["tier.hundred_claude_only.evals_canary_cadence"], 2) == 2
   assert round(figures["tier.hundred_claude_only.evals_golden_set_3_cadence"], 2) == cost_model.MONTHLY_RUNS
   assert round(figures["tier.hundred_claude_only.evals_line"], 2) == 22.88
   assert round(figures["tier.hundred_claude_only.cycle"], 2) == 92.95
   assert round(figures["tier.hundred_claude_only.headroom"], 2) == 7.05
   assert figures["tier.hundred_claude_only.headroom"] >= 5.00
   assert round(figures["tier.hundred_claude_only.worst_case_cycle"], 2) == 113.83
   assert round(figures["tier.hundred.cycle"], 2) == 95.03, (
      "the Gemini-verifier tier's already-quoted total must not move with the Claude-only tier's cadence"
   )


@pytest.mark.parametrize("document", DOCUMENTS, ids=lambda path: path.name)
def test_every_dollar_figure_in_the_document_is_emitted_by_the_calculator(document):
   """A figure patched by hand in one section while the model moves in another is how the last
   two review rounds were generated. Positive control first: the checker must flag a figure the
   calculator does not emit, or a clean result over the document proves nothing."""
   figures = cost_model.figures()
   control = document.parent / "cost_model_control.md"
   control_text = "A stray figure of $999,999.99 that no model emits.\n"

   try:
      control.write_text(control_text)
      flagged = cost_model.check(control, figures)
   finally:
      control.unlink()

   assert flagged == [(1, "999,999.99")]

   unknown = cost_model.check(document, figures)

   assert unknown == [], f"{document.name} prints dollar figures the calculator does not emit: {unknown}"
