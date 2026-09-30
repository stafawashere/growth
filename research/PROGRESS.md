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
| 6 | evidence files, skeptic pass, closure | skeptic pass done (fixes applied: inverted BC-ERR-99030 instance, skill tag policy, citation sync, adaptive metadata rewritten for all 541 skills); intra-unit edges for Units 8, 9, 10 authored; error causes enriched for all 390 active errors; diagnostic signals cover every active skill; independent-assessability flag added; mastery-state vocabulary unified; sg-24 and sample MCQ documents recovered by OCR (tools/ocr_pages.py) and their records re-derived; 10 gap archetypes, 7 new point types, misconception causal prerequisites filled; 2026-09-28 corrections: BC-CON-06001 and BC-CON-06007 skill lists matched to the skills' concept back-references (list total 544 to 541), and seven unloaded skills added to active archetypes whose solution paths exercise them (unloaded skills 19 to 12); confusable_with filled on 505 of 541 skills (1178 symmetric pairs, at most 6 per skill) by tools/derive_confusable.py; asked_to_produce, common_givens and wrong_approaches written for the 78 active archetypes that lacked them (78, 74 and 73 filled; the rest left absent where the cached pages give no support, listed in the staging file); 2026-09-28 stage 15: nine archetypes minted (BC-QA-03010, 05014, 06017, 06018, 06019, 07012 for skills no archetype isolated, and BC-QA-02014, 09014, 10021 as generation archetypes for the productive-failure openers of BC-CON-02002, 09015 and 10002), 148 active of 153 records; BC-ERR-02033 and BC-ERR-06033 minted (393 active of 427); BC-SKL-06046 retired into BC-SKL-06074 (541 records, 540 active), its edge to BC-SKL-06074 left in prereq_edges.csv; 2026-09-28 and 29 prerequisite gates: 149 inferred hard edges from data/staging/root-gates-*.edges.csv give every skill outside Unit 1 a parent in an earlier topic (1375 edges, 751 hard, 0 cycles), and tools/sync_dependents.py wrote the matching prerequisites and dependents onto 166 skills; 2026-09-29: web pages cached as corpus documents (tools/fetch_corpus.py web and --saved-dir), 40 documents cached, 30 new source records (10 hand-listed pages now carry cached text), Bluebook Desmos questions settled or narrowed (research/exam/calculator-policy.md) |

## Counters (from qa/last_report.json, 2026-09-29)

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
| archetypes.json:archetypes | 153 |
| archetypes.json:variants | 395 |
| scoring_points.json:point_types | 76 |
| errors.json:errors | 427 |
| misconceptions.json:misconceptions | 236 |
| diagnostic_signals.json:signals | 711 |
| taxonomies.json:representations | 14 |
| taxonomies.json:difficulty_factors | 17 |
| taxonomies.json:command_verbs | 29 |
| frq_records.json:records | 249 |
| mcq_records.json:records | 91 |
| sources.json:sources | 138 |
| cache:documents_ok | 136 |
| cache:documents_missing | 61 |

QA: all 14 checks pass (00 to 10 plus 13_adaptive, 14_diagnosis and 15_determinism_labels); 11_freshness is network-only and run on demand.

## Sources and years

Sources discovered: 108 (97 cached College Board documents plus 11 web pages and one secondary index). Sources verified by fetch and hash: 97. Years indexed for FRQs: 2012 (Q6 only), 2013, 2014, 2015, 2018 (no rubric), 2019, 2021, 2022, 2023, 2024, 2025, 2026. Chief Reader reports analysed: 2022, 2023, 2024, 2025. Scoring guidelines analysed: 2019, 2021, 2022, 2023, 2024 (labels only), 2025, 2026, plus 2013 to 2015 rubrics inside sample documents.

## Resuming

Read CLAUDE.md, then run python3 qa/12_report.py. The staging files under data/staging are the authoritative edit history; a full python3 tools/merge_staging.py replay rebuilds every registry in phase order. Next candidates for work: author archetypes for the gaps listed in evidence/unresolved-questions.md; fill misconception causal_prerequisites; re-fetch 2026 samples, statistics, distributions, and Chief Reader report once College Board publishes them; OCR (RapidOCR) is now available through tools/ocr_pages.py for any further image-only pages such as the handwritten sample responses.

## Unresolved areas

See evidence/unresolved-questions.md and evidence/skeptic-review.md.
