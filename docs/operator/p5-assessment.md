---
title: P5 assessment modes, what was built and how it was checked
research_date: 2026-09-24
status: measured
purpose: The canonical record of stage 6 (docs/plan/11 P5): the unit check, the timed part drills, the full mock, pacing, the score band, and the checks behind each, built by Claude on the operator's delegation.
---

# P5 assessment modes [verified]

Built on 2026-09-24 by claude-opus-5-5 on the operator's delegation. Every number below was
measured in this repository on that day; where a number is a model's measurement rather than a
person's, the row says so.

## What the student can do

- **Full mock** (`POST /mocks`): the four parts in order at the documented shape, read at run time
  from research/exam/exam-structure.md through app/checkpoint/published.py and never restated in
  code. Multiple choice is answered in the app; free response is written on the printed booklet
  page during the part and captured after it (photo or typed), read back, confirmed and graded
  per point. Parts open only in order, a closed part never reopens, and the server's deadline
  closes a part as the student left it. The result is a band with its assumptions, raw points,
  per-question points against the published 2023 to 2025 means, and pacing per part.
- **Part drill** (`POST /drills`): any one of the four parts alone, the same machinery.
- **Unit check** (`POST /unit-checks`): untimed, 8 to 12 items chosen by a greedy set cover over the
  unit's skills among the archetypes the fringe gate allows, feedback withheld until the whole
  check is submitted, then every observation applied with the student's own ratings, a per-item
  breakdown and a per-skill list of what moved. Skills the cover cannot reach are recorded with the
  reason (gated, no published item, or over the cap).

## Where the rules live

| Rule | Where | Checked by |
| --- | --- | --- |
| Part counts, minutes, calculator status, weights read from exam-structure.md | `app/assessment/shape.py`, `app/checkpoint/published.py` | `test_part_shapes` (parses the table independently) |
| Form order, labels, booklet wording as data | `content/assessment/form_2027.json` | `test_calculator_lockout`, the booklet route |
| Timed work never touches skills_state | `app/assessment/service.py` (sessions written with updates_mastery 0, no engine update), `app/grading/service.py` `MASTERY_MODES` | `test_timed_does_not_update_mastery`, `test_full_mock_run`, docs/operator/p5-timed-runs.md |
| Hard part boundaries | `service.start_part`, `service.open_part_or_refuse`, `service.expire_if_due` | `test_part_boundary_closed` |
| Tool set, graphing panel on calculator parts only | `shape.tools_for`, the client's part runner | `test_tool_set_present`, `test_calculator_lockout` and their client halves |
| Pacing only, rapid guesses flagged and left out of means and diagnosis | `app/assessment/pacing.py` | `test_a_fast_answer_in_the_final_minutes_is_flagged_and_left_out_of_diagnosis`, `eval_pacing_metrics` |
| Band, never a single number or a centre | `app/assessment/band.py` | `test_score_band_never_single_number`, `test_band_is_never_narrower_than_two_points_anywhere` |
| Radian-mode note on calculator trigonometry | `assemble.radian_note_applies` | `test_the_radian_note_rides_on_calculator_trigonometry_only` |
| Reference sheet treated as absent | `form_2027.json` `reference_sheet` | shown on the setup screen |
| Rollback | `GROWTH_TIMED_ASSESSMENTS=off` switches the mock and drills off; the unit check stays | `app/main.py` |

## The score band

The composite is the two sections' shares weighted by their published weights. Cut points are
unpublished, so the composite is placed against past cohorts: the national composite is taken to
spread like the free-response section, the only section with published per-question means and
standard deviations, as a normal curve with the summed means and summed standard deviations; the
student's position on it is read against each published year's score distribution; that internal
score is widened one score point either side (sliding, not narrowing, at 1 and 5), and the band is
the union over 2023, 2024 and 2025 and over every way the provisional free-response points could
fall. The internal score is never returned, stored or shown. The seven assumptions travel with the
band on the result screen. This method is [inferred] and is carried into docs/plan/12.

## Free-response questions for the mock

The mock needs questions at the exam's per-question total, 9 points, and 2 calculator questions
for Section II Part A; the P3 bank had none of either. Sixteen were written for this stage by
three authoring agents (6 calculator, 10 no-calculator, units 4 to 10), each on one archetype with
only that archetype's point types. A separate agent given only the stems and part prompts wrote
blind SymPy formulations of every deterministic point: 71 of 71 matched the keys with the control
holding (`tools/frq_key_recheck.py`), and the whole bank reads 137 of 137. Every stem and prompt was
read for ambiguity and checked against the cached official pages (longest shared run 18 words
against the 25-word cap; `test_no_official_text_in_free_response_questions` now gates the whole
free-response bank). Two integrand checks that would have failed correct work written as two
separate integrals were narrowed to their limits. Each record is signed off by claude-opus-5-5 on
the operator's delegation; this is a model review, not the operator's.

## Measurements

See docs/operator/p5-timed-runs.md (20 timed runs, 0 skills_state rows changed) and
docs/operator/p5-full-mock.md (the full mock driven through the running app in the browser).
