---
title: Research Progress
research_date: 2026-09-19
status: in_progress
purpose: Tracks research completion so the project can resume across sessions. Not student progress.
---

# Research progress

Counters are regenerated from `qa/12_report.py`; narrative status is updated by hand at the end of every phase.

## Phase status

| Phase | Description | Status |
|---|---|---|
| 0 | cache, schemas, ID tool, QA suite, README | done 2026-09-19 |
| 1 | CED transcription into curriculum.json, exam/ files | done 2026-09-19 (111 topics, 81 LOs, 190 EKs, 23 practice skills) |
| 2 | gold unit (Unit 6) | done 2026-09-19 |
| 3 | unit fan-out | done 2026-09-19 (10 units, 541 skills, 134 archetypes) |
| 4 | official FRQ, scoring, sample indexing | done 2026-09-19 (249 FRQ part records over 2012 partial, 2013 to 2015, 2018, 2019, 2021 to 2026; 91 MCQ records; 69 point types; 38 Chief Reader errors) |
| 5 | archetypes, points, misconceptions, diagnostics synthesis | done 2026-09-19 (129 active archetypes in 72 families, 17 difficulty factors, 945 edges with 0 cycles, 57 duplicate records retired) |
| 6 | evidence files, skeptic pass, closure | skeptic pass done (fixes applied: inverted BC-ERR-99030 instance, skill tag policy, citation sync, adaptive metadata rewritten for all 541 skills); intra-unit edges for Units 8, 9, 10 authored; error causes enriched for all 390 active errors; diagnostic signals cover every active skill; independent-assessability flag added; mastery-state vocabulary unified |

## Counters (from qa/last_report.json, 2026-09-19)

| Registry | Records |
|---|---|
| curriculum.json:units | 10 |
| curriculum.json:topics | 111 |
| curriculum.json:learning_objectives | 81 |
| curriculum.json:essential_knowledge | 190 |
| curriculum.json:practices | 4 |
| curriculum.json:practice_skills | 23 |
| skills.json:concepts | 170 |
| skills.json:skills | 541 |
| skills.json:prerequisites | 77 |
| archetypes.json:archetypes | 134 |
| archetypes.json:variants | 394 |
| scoring_points.json:point_types | 69 |
| errors.json:errors | 424 |
| misconceptions.json:misconceptions | 236 |
| diagnostic_signals.json:signals | 711 |
| taxonomies.json:representations | 14 |
| taxonomies.json:difficulty_factors | 17 |
| taxonomies.json:command_verbs | 29 |
| frq_records.json:records | 249 |
| mcq_records.json:records | 91 |
| sources.json:sources | 108 |
| cache:documents_ok | 97 |
| cache:documents_missing | 60 |

QA: all 13 checks pass (00 to 10 plus 13_adaptive and 14_diagnosis); 11_freshness is network-only and run on demand.

## Sources and years

Sources discovered: 108 (97 cached College Board documents plus 11 web pages and one secondary index). Sources verified by fetch and hash: 97. Years indexed for FRQs: 2012 (Q6 only), 2013, 2014, 2015, 2018 (no rubric), 2019, 2021, 2022, 2023, 2024, 2025, 2026. Chief Reader reports analysed: 2022, 2023, 2024, 2025. Scoring guidelines analysed: 2019, 2021, 2022, 2023, 2024 (labels only), 2025, 2026, plus 2013 to 2015 rubrics inside sample documents.

## Resuming

Read CLAUDE.md, then run python3 qa/12_report.py. The staging files under data/staging are the authoritative edit history; a full python3 tools/merge_staging.py replay rebuilds every registry in phase order. Next candidates for work: author archetypes for the gaps listed in evidence/unresolved-questions.md; fill misconception causal_prerequisites; re-fetch 2026 samples, statistics, distributions, and Chief Reader report once College Board publishes them; retry OCR on sg-24 if a tool becomes available.

## Unresolved areas

See evidence/unresolved-questions.md and evidence/skeptic-review.md.
