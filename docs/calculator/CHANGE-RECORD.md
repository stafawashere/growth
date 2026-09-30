---
title: Desmos fluency, record of additions and changes
research_date: 2026-09-29
status: complete
purpose: Every file added or changed on branch calculator/desmos-fluency since its merge base with today/redesign, grouped by area, with line counts.
---

# Desmos fluency, record of additions and changes [verified]

Branch `calculator/desmos-fluency`, merge base `23cb026` with `today/redesign`. Counts come from `git diff --numstat` against that base. The cached web pages under cache/text are summarised at the end rather than listed one by one.

## Commits, oldest first [verified]

- bfa1769 2026-09-29 Carry pending key recheck helper edits and the history student seeder onto the calculator branch
- 22383d9 2026-09-29 Cache web pages as first-class corpus documents: Bluebook, calculator policy and Desmos documentation
- e9b56d9 2026-09-29 Desmos fluency: research, synthesis, design and architecture, with the library's Bluebook Desmos questions settled from cached pages
- bb6d30c 2026-09-29 Desmos fluency: build plan with the fixed API and template contracts, and dated amendments to plans 05, 08, 09, 11 and 12
- a7919ce 2026-09-29 Desmos fluency: nine procedure cards, their schema and checker
- 49174bb 2026-09-29 Desmos fluency: the Calculator destination, procedure cards, drill screen, measured view and links in the web client
- 41615e2 2026-09-29 Desmos fluency: the drill engine, twelve templates, the three-place value check and the setup equivalence check
- 795d243 2026-09-29 Desmos fluency: the calculator_drills table, the drill service, the five routes and the measured computation
- 47b7e37 2026-09-29 Read Compute Engine Pair and Triple heads as tuples in MathJSON conversion
- 2b06b69 2026-09-29 Read prime notation and implicit function application in typed setups
- 9f7533d 2026-09-29 Keep the drill screen's skip link hidden until it is focused
- bb40223 2026-09-29 Desmos fluency: build ledger entry and handoff
- be3cd43 2026-09-29 Desmos fluency: full-suite results appended to the ledger

## Research documents [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| docs/calculator/research/bluebook-desmos.md | added | 170 | 0 |
| docs/calculator/research/desmos-technique.md | added | 211 | 0 |
| docs/calculator/research/exam-calculator-work.md | added | 164 | 0 |
| docs/calculator/research/fluency-training.md | added | 112 | 0 |
| docs/calculator/research/synthesis.md | added | 47 | 0 |

## Design, architecture, build plan, handoff [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| docs/calculator/HANDOFF.md | added | 33 | 0 |
| docs/calculator/architecture.md | added | 154 | 0 |
| docs/calculator/build-plan.md | added | 78 | 0 |
| docs/calculator/design.md | added | 92 | 0 |

## Plan amendments [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| docs/plan/05-assessment-modes.md | changed | 14 | 0 |
| docs/plan/08-design-brief.md | changed | 8 | 0 |
| docs/plan/09-security-and-privacy.md | changed | 9 | 0 |
| docs/plan/11-phased-delivery.md | changed | 1 | 1 |
| docs/plan/12-open-questions.md | changed | 1 | 1 |

## Library and registry [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| data/ids.json | changed | 150 | 0 |
| data/sources.json | changed | 697 | 40 |
| qa/00_manifest.py | changed | 39 | 15 |
| qa/last_report.json | changed | 4 | 4 |
| research/PROGRESS.md | changed | 5 | 5 |
| research/evidence/claims-and-confidence.md | changed | 8 | 6 |
| research/evidence/unresolved-questions.md | changed | 2 | 1 |
| research/exam/calculator-policy.md | changed | 22 | 11 |

## Corpus pipeline and its tests [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| .gitignore | changed | 2 | 0 |
| cache/manifest.json | changed | 667 | 0 |
| cache/page_index.json | changed | 545 | 0 |
| cache/quarantine.json | changed | 40 | 1 |
| tests/tools/test_corpus_web.py | added | 209 | 0 |
| tools/build_sources.py | changed | 67 | 3 |
| tools/extract_text.py | changed | 95 | 1 |
| tools/fetch_corpus.py | changed | 198 | 1 |

## Procedure cards, schema, checker [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| content/calculator/cards/CCD-decimal-01.json | added | 82 | 0 |
| content/calculator/cards/CCD-derivative-01.json | added | 77 | 0 |
| content/calculator/cards/CCD-integral-01.json | added | 86 | 0 |
| content/calculator/cards/CCD-integral-02.json | added | 71 | 0 |
| content/calculator/cards/CCD-intersection-01.json | added | 86 | 0 |
| content/calculator/cards/CCD-mode-01.json | added | 79 | 0 |
| content/calculator/cards/CCD-plot-01.json | added | 85 | 0 |
| content/calculator/cards/CCD-value-01.json | added | 82 | 0 |
| content/calculator/cards/CCD-zero-01.json | added | 87 | 0 |
| content/calculator/templates.json | added | 257 | 0 |
| schemas/calculator/card.schema.json | added | 214 | 0 |
| tests/fixtures/calculator/clean.json | added | 77 | 0 |
| tests/fixtures/calculator/red_answer.json | added | 77 | 0 |
| tests/fixtures/calculator/red_citations.json | added | 82 | 0 |
| tests/fixtures/calculator/red_coverage.json | added | 77 | 0 |
| tests/fixtures/calculator/red_error_ids_retired.json | added | 78 | 0 |
| tests/fixtures/calculator/red_error_ids_unknown.json | added | 77 | 0 |
| tests/fixtures/calculator/red_habit_words.json | added | 77 | 0 |
| tests/fixtures/calculator/red_keys.json | added | 77 | 0 |
| tests/fixtures/calculator/red_quotes.json | added | 77 | 0 |
| tests/fixtures/calculator/red_quotes_partial.json | added | 77 | 0 |
| tests/fixtures/calculator/red_schema.json | added | 78 | 0 |
| tests/fixtures/calculator/red_student_text_advice.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_citation.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_dash.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_emoji.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_library_id.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_praise.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_prediction.json | added | 77 | 0 |
| tests/fixtures/calculator/red_student_text_tag.json | added | 77 | 0 |
| tests/fixtures/calculator/red_template_set.json | added | 78 | 0 |
| tests/tools/test_check_calculator.py | added | 227 | 0 |
| tools/check_calculator.py | added | 611 | 0 |

## Drill engine [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| app/calculator/__init__.py | added | 2 | 0 |
| app/calculator/check.py | added | 404 | 0 |
| app/calculator/kit.py | added | 254 | 0 |
| app/calculator/registry.py | added | 55 | 0 |
| app/calculator/templates/__init__.py | added | 0 | 0 |
| app/calculator/templates/cdt_derivative_01.py | added | 61 | 0 |
| app/calculator/templates/cdt_derivative_02.py | added | 63 | 0 |
| app/calculator/templates/cdt_integral_01.py | added | 71 | 0 |
| app/calculator/templates/cdt_integral_02.py | added | 75 | 0 |
| app/calculator/templates/cdt_intersection_01.py | added | 77 | 0 |
| app/calculator/templates/cdt_intersection_02.py | added | 67 | 0 |
| app/calculator/templates/cdt_plot_01.py | added | 62 | 0 |
| app/calculator/templates/cdt_plot_02.py | added | 61 | 0 |
| app/calculator/templates/cdt_value_01.py | added | 63 | 0 |
| app/calculator/templates/cdt_value_02.py | added | 72 | 0 |
| app/calculator/templates/cdt_zero_01.py | added | 65 | 0 |
| app/calculator/templates/cdt_zero_02.py | added | 60 | 0 |
| tests/calculator/__init__.py | added | 0 | 0 |
| tests/calculator/test_check.py | added | 351 | 0 |
| tests/calculator/test_invariants.py | added | 152 | 0 |
| tests/calculator/test_registry.py | added | 142 | 0 |
| tests/calculator/test_templates.py | added | 214 | 0 |

## Table, service, routes, measured, audit [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| app/api/app.py | changed | 2 | 2 |
| app/api/routes/calculator.py | added | 66 | 0 |
| app/api/routes/lessons.py | changed | 35 | 2 |
| app/audit/vocabulary.py | changed | 6 | 0 |
| app/calculator_drills/__init__.py | added | 2 | 0 |
| app/calculator_drills/service.py | added | 283 | 0 |
| app/db/models.py | changed | 30 | 0 |
| app/progress/calculator_fluency.py | added | 72 | 0 |
| tests/api/test_calculator_routes.py | added | 270 | 0 |
| tests/api/test_lesson_calculator_flag.py | added | 27 | 0 |
| tests/db/test_models.py | changed | 3 | 1 |
| tests/export/test_export.py | changed | 1 | 0 |
| tests/export/test_export_calculator.py | added | 25 | 0 |
| tests/session/test_purge_calculator.py | added | 34 | 0 |

## MathJSON reading [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| app/items/mathjson.py | changed | 2 | 2 |
| tests/items/test_mathjson_pair_triple.py | added | 30 | 0 |

## Web client [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| app/web/src/App.test.tsx | changed | 2 | 2 |
| app/web/src/App.tsx | changed | 17 | 1 |
| app/web/src/api/client.ts | changed | 29 | 0 |
| app/web/src/api/types.ts | changed | 146 | 0 |
| app/web/src/assessment/SetupScreen.tsx | changed | 18 | 0 |
| app/web/src/calculator/CalculatorLink.test.tsx | added | 72 | 0 |
| app/web/src/calculator/CalculatorLink.tsx | added | 23 | 0 |
| app/web/src/calculator/CalculatorRoute.test.tsx | added | 79 | 0 |
| app/web/src/calculator/CalculatorRoute.tsx | added | 351 | 0 |
| app/web/src/calculator/CapabilityChooser.tsx | added | 46 | 0 |
| app/web/src/calculator/DrillClock.test.tsx | added | 42 | 0 |
| app/web/src/calculator/DrillClock.tsx | added | 88 | 0 |
| app/web/src/calculator/DrillScreen.test.tsx | added | 289 | 0 |
| app/web/src/calculator/DrillScreen.tsx | added | 323 | 0 |
| app/web/src/calculator/MeasuredView.test.tsx | added | 40 | 0 |
| app/web/src/calculator/MeasuredView.tsx | added | 112 | 0 |
| app/web/src/calculator/ProcedureCard.test.tsx | added | 61 | 0 |
| app/web/src/calculator/ProcedureCard.tsx | added | 131 | 0 |
| app/web/src/calculator/fixtures.ts | added | 88 | 0 |
| app/web/src/calculator/words.ts | added | 189 | 0 |
| app/web/src/input/DesmosPanel.test.tsx | changed | 35 | 1 |
| app/web/src/input/DesmosPanel.tsx | changed | 60 | 6 |
| app/web/src/lessons/LessonReader.tsx | changed | 3 | 0 |
| app/web/src/lessons/LessonRoute.tsx | changed | 1 | 0 |
| app/web/src/lessons/LessonSection.tsx | changed | 12 | 0 |
| app/web/src/progress/ProgressRoute.tsx | changed | 13 | 1 |
| app/web/src/routing.ts | changed | 56 | 0 |
| app/web/src/session/Item.tsx | changed | 2 | 1 |
| app/web/src/shell/TopBar.tsx | changed | 6 | 4 |
| app/web/src/styles/app.css | changed | 72 | 0 |
| app/web/vite.config.ts | changed | 1 | 0 |

## Ledger [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| BUILD-LEDGER.md | changed | 188 | 0 |

## Carried from the pending work of the earlier session (commit bfa1769) [verified]

| File | Status | Lines added | Lines removed |
|---|---|---|---|
| tests/items/test_key_recheck_helpers.py | changed | 46 | 0 |
| tests/tools/test_seed_history_student.py | added | 90 | 0 |
| tools/key_recheck.py | changed | 102 | 0 |
| tools/seed_history_student.py | added | 345 | 0 |

## Cached web pages [verified]

39 documents added under cache/text, 167 files (meta.json, page-001.txt and, where the raw text differs, page-001.raw.txt), all recorded in cache/manifest.json with status ok: 35 web pages carry kind web, and the four PDFs (desmos-cb-calculators-pdf, desmos-default-testing-pdf, desmos-user-guide-pdf, hybrid-booklets-2026) are ordinary PDF records without a kind field. The HTML copies live under cache/web and are gitignored.

- desmos-api-docs
- desmos-api-terms
- desmos-cb-calculators-pdf
- desmos-default-testing-pdf
- desmos-graphing-shortcuts
- desmos-help-api-plans
- desmos-help-assessment-faq
- desmos-help-derivatives
- desmos-help-faqs
- desmos-help-functions
- desmos-help-getting-started
- desmos-help-graph-settings
- desmos-help-in-class-assessments
- desmos-help-integrals
- desmos-help-keyboard-shortcuts
- desmos-help-regressions
- desmos-help-restrictions
- desmos-help-sliders
- desmos-help-supported-functions
- desmos-help-tables
- desmos-help-testing-calculators
- desmos-help-trigonometry
- desmos-help-user-guide
- desmos-help-whats-new
- desmos-terms
- desmos-testing
- desmos-user-guide-pdf
- hybrid-booklets-2026
- web-ab-subscore
- web-bc-course
- web-bc-exam
- web-bc-past
- web-bc-students
- web-bluebook-tools
- web-calc-policy
- web-calc-policy-central
- web-equating
- web-exam-dates
- web-score-setting

## Not on the branch [verified]

Local only: .claude/launch.json entries, var/calculator/driver.py and the 27 walk screenshots, and the agent briefs in the session scratchpad. Another chat's uncommitted files (tools/check_items.py, tools/seed_history_student.py, app/items/standards.py, tests/tools/test_item_standards.py) sit in the working tree and are not part of this record.
