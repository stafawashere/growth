---
title: Author one lesson for one concept
version: v1
role: generator
model: offline Claude Code session, claude-opus-5-5
purpose: The instruction an offline Claude Code session follows to author one concept lesson from the authoring bundle, which tools/check_lessons.py then verifies and a blind re-solve and a blind sign-off review then confirm.
---

# Author one lesson for one concept

You write one JSON file, `content/lessons/LSN-CON-<digits>.json`, for the concept you are given,
in the schema at `schemas/lessons/lesson.schema.json`. The file is a body of sections with bands,
sources and evidence tags. It is not a script for a student and it is not tuned to any one
student, because the app assembles what a student reads from your sections at serve time
(`app/lessons/plan.py`). You never write a per-band or per-error variant.

## Read first

1. The authoring bundle, which is everything you may use:
   `.venv/bin/python -c "import json; from pathlib import Path; from app.content.loader import load_snapshot; from app.lessons.source import authoring_bundle; print(json.dumps(authoring_bundle('<concept id>', load_snapshot(Path('data'))), indent=1))"`
   It holds the concept and its skills, the topic section of research/units without its Official
   mapping subsection, the linked errors (already in the order the lesson shows them),
   misconceptions, signals and point types, the archetypes that load the concept's skills, the
   BC-PRQ parents, the cached text of each cited CED page, and the `source_digest` you copy into
   the file.
2. The exemplar `content/lessons/LSN-CON-02013.json`, for the shape of every section type.
3. `docs/plan/15-lessons.md`, the content model and the band table.

Never open, quote or imitate an AP question, a released exam, a scoring guideline or anything
else under `cache/` except the CED pages in the bundle. Facts come from the bundle and never from
memory. A mathematical claim in a worked example is computed with SymPy before you write it down.

## The file

- `id`, `version` 1, `kind` `concept`, `target_id`, `status` `draft`, `snapshot_digest` from the
  snapshot you loaded, `source_digest` from the bundle, `refresher` (the ids of the core key ideas,
  every error block and worked example 1), and `provenance` with `author` set to your model id,
  `prompt_version` `generator/lesson_v1`, `signed_off_by` and `signed_off_at` null and `not_human`
  true.
- `sections`, in this fixed order: one `orientation` (at most 60 words, what a response must
  show, built from `description_plain` and the topic's Assessment behaviour paragraph); one
  `key_ideas` block per BC-EK the concept's skills map (at most 120 words, `depth` `core` or
  `extended`, at most 2 core, paraphrasing the topic's Required mathematical knowledge paragraph
  and citing the BC-EK and the CED page); one `strategy` block per archetype family that loads a
  skill of the concept (at most 3, at most 80 words); one or two `worked_example` sections drawn
  from an archetype that loads a skill of the concept; one `what_a_reader_scores` per worked
  example; one `common_error` per error in the bundle's order, at most 4; at most one
  `representations`; one `prerequisite_bridge` per BC-PRQ parent in the bundle.
- `checks`: two or three item-shaped records. Check 1 is the completion form of worked example 1
  on its draw. Check 2 is a short-answer isomorph from the same archetype on another draw. Check 3
  is a 4-option multiple choice whose distractors each carry the `error_path` of an error block
  above, derived by making that error on this draw.
- `read_minutes` and `word_count`, `full` and `brief`. Word counts are the words of the low-band
  and mid-band plans, which `app.lessons.plan.band_words(lesson, band)` returns. A minutes
  figure is never below the words at 150 per minute and never above 6 and 3.

## Section rules

- Every section names its `skills`, `sources` (each one present in the bundle) and an
  `evidence_tag`. Use `inferred` where you built the sentence from records tagged inferred.
- A `strategy` block reads in this order and holds nothing else: the cue in the archetype's own
  words from `asked_to_produce` and `common_givens` (or `typical_wording` with tag `inferred` when
  the archetype has neither), the method as the first entry of `expected_solution_path`, the rival
  from `wrong_approaches` or `prohibited_shortcuts`, and the one feature of the stem that
  separates them.
- Every worked step carries a `cue` of at most 20 words naming what in the stem or the previous
  line selects the step, a `why` of at most 25 words, an `expression` in MathJSON where the step
  has a value, and a `point_type_id` only from the archetype's `point_types`. Consecutive valued
  steps must be equivalent and must differ as expressions. A step that would restate the one
  before it carries no expression.
- A `what_a_reader_scores` section is never written by you. Its `lines` are
  `reader_checks(<the point types the example's steps tag>, snapshot)`, copied exactly. An
  example on an archetype with no `point_types` has no such section and no tagged step.
- A `common_error` block copies `observed_behavior` and `scoring_consequence` from the record,
  shows a wrong step beside a right step with a `relation` of `distinct` or `equivalent` that the
  checker recomputes, and may add a `possible_reason` only as words taken from the linked BC-MIS
  `description`. The error is never said to be what the student believes.
- One `quote` at most per section, at most 25 words, found on the cited CED page. Quotation
  marks never appear inside prose.
- Calculator boundary: a `no_calculator` example or check has an exact answer and no decimal
  anywhere on its path. A `calculator` one states its answer to three decimals.
- Draws: no example or check draw equals the `parameter_draw` of a published item on the same
  archetype. Inline mathematics sits between `\(` and `\)`.

## Rules the checker cannot enforce

- One idea per screen. A step that needs two sentences is two steps.
- Stems read as a question to a student: "Find", "Write", "Name". Never "Which of the following".
- No study advice, no schedules, no praise, no mention of the exam's frequency or of what it will
  hold, no sentence about what the student believes or feels, no em dash, no en dash, no emoji.
- Do not stretch an error to fit a distractor. If the concept's skills hold fewer honest errors
  than check 3 needs, use the ones that fit and report the gap in the run notes.

## Done

`.venv/bin/python tools/check_lessons.py content/lessons` exits 0, and you have read the rendered
low and mid plans (`app.lessons.plan.plan_lesson(lesson, "low", "first_contact")`) as a student
would and found nothing wrong. The lesson stays `draft`. The blind re-solve and the sign-off
review move it on, and neither is yours to do.
