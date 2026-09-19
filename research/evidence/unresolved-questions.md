---
title: Unresolved Questions
research_date: 2026-09-19
status: in_progress
purpose: Every question the research could not settle with confidence, with what was tried, so that nothing in the library is a guess. Agents append here instead of guessing.
---

# Unresolved questions

Each entry states the question, what was attempted, and what would resolve it. Entries are tagged [uncertain] unless partial evidence exists.

## Corpus availability [verified attempts, uncertain existence]

- 2012 to 2017 free-response questions and scoring guidelines: not obtained. Live AP Central 404s at the ap{YY}-frq-calculus-bc pattern; the retired secure-media legacy path and seven filename variants were probed in the Wayback Machine (2019 to 2023 snapshots) and returned 404 (see cache/manifest.json attempts and BC-SRC-web-bc-past). Partial substitute: the 2013 to 2015 per-question Student Samples documents (BC-SRC-samples-14-q2 and siblings) bundle the question text and its scoring guideline, so those years can be indexed from samples alone. 2016 and 2017 have nothing.
- 2018 scoring guidelines: not obtained (frq-18 was recovered, sg-18 was not, under five name variants). 2018 records can be tagged to topics but not to scoring points.
- Chief Reader reports before 2022: not obtained at ap{YY}-cr-report-calculus.pdf for 2018, 2019, 2021 in any snapshot. cr-23 page 17 refers to a 2021 report, so at least one earlier report existed [single-source]. Whether the older "Student Performance Q&A" series covered Calculus BC is unknown.
- 2020: no BC file exists at the standard pattern. The 2020 administration was abnormal; nothing in the cache describes it, so the library states nothing about 2020 beyond its absence.
- 2021: frq-21, sg-21, and six sample files were recovered. A set-2 FRQ file once existed at the College Board URL (301 observed), consistent with multiple 2021 forms; only one form is cached and its form label is not verified.
- 2026 samples, statistics, distributions, and Chief Reader report: not yet published as of 2026-09-19 (404 live).

## Extraction quality [verified]

- sg-24 (2024 scoring guidelines): the prose of the scoring-note bullets is absent from the PDF text layer in both PyMuPDF and pdftotext output (page 4 has 50 vector drawings, no images, 919 characters). Only point labels, point values, and model-solution fragments survive. No OCR tool is available on this machine. Consequence: 2024 point types carry labels but not rubric wording; scoring-point records cite sg-24 for structure only.
- Sample documents 2019 to 2025: handwritten response pages have no text layer and are quarantined (cache/quarantine.json). Commentary pages extract normally.
- Mathematical notation in every document is imperfectly linearised; anchor quotes are taken from prose, not from formulas.

## CED edition [verified]

- The cached CED cover says "Effective Fall 2020" but its body already contains the Fall 2026 clarified wording of EK FUN-1.C.1 and FUN-7.B.2 and the 29/13 multiple-choice counts. The pre-2026 wording of those two EK statements is not recoverable from the cache, so `previous_text` is empty on those records (BC-EK-FUN-1C1, BC-EK-FUN-7B2).
- Whether the May 2026 exam used the old or the new multiple-choice counts is not established from cached material.
- The College Board key-changes page returned HTTP 403 to fetch (BC-SRC-web-key-changes); its content is known only through search-index extracts.

## Scoring process [inferred]

- Raw multiple-choice to free-response point weights, composite scale, and cut scores for any year are not published in any cached document.
- Per-point score means are available only in the 2025 Chief Reader report (crabbc-25) as prose, not as numbers; 2023 and 2024 reports give one mean per question.
- Linkage rule change: sg-22 and sg-23 deduct for an integral equated to a divided value, sg-25 and sg-26 treat it as scratch work. Whether this is a policy change or question-specific is not stated.

## Exam logistics [single-source]

- May 10, 2027 exam date and 8 a.m. start rest on one College Board page (BC-SRC-web-exam-dates).
- Whether Bluebook's built-in Desmos satisfies all four CED calculator capabilities, and how it counts against the two-handheld limit, is not stated in cached material.

## Findings from the skeptic pass and indexing agents [verified]

- 2018 free-response records (22 parts) carry points 0 and no point types because no 2018 scoring guideline is in the corpus; corpus point totals in research/question-analysis/frq-analysis.md exclude them.
- 2021 form: the cached frq-21 and sg-21 never name a form, and a set-2 file once existed at the College Board URL; all 2021 records carry that caveat.
- 161 of 541 atomic skills have no linked official FRQ evidence (list in research/question-analysis/historical-frequency.md). This is a coverage fact about the indexed years, not evidence that those skills are untested.
- Sample MCQ material: the standalone sample-questions document loses all mathematics in its text layer, so 18 of its 24 items have no recoverable options; CED sample items 13, 15, 17, 18, 19 lost stems or options; 2012 practice exam item 82 could not be reconciled with its key. BC-MCQ-CED-004 and BC-MCQ-CED-006 are tagged uncertain because the printed key is displaced across columns on ced:221. No public College Board rationale exists for any distractor; every distractor mechanism in data/mcq_records.json is [inferred] or [uncertain].
- Archetype gaps recorded in FRQ record notes (candidates for new archetypes): polar tangent-slope solved for dx/dtheta (2026 Q2b); average value of a radial function along a polar curve (2019 Q2b); time at which a Cartesian coordinate on a polar path reaches a value, and position plus velocity vectors on a polar path (2013 Q2); rate of change of the gap between two polar curves (2014 Q2c); average rate of change reported alone (2014 Q1a); density accumulated over depth, and bounding an accumulation by a comparison function (2018 Q2). Point-type gaps: convergence conclusion supported by a named test, quotient rule, partial-fraction decomposition, slope-plus-equation, slope-field drawing.
- Scoring-point records for 2024 rest on point labels only (sg-24 text-layer loss).
- Linkage rule divergence: sg-22 and sg-23 deduct for an integral equated to a divided value; sg-25 and sg-26 treat it as scratch work. Candidates-test justification wording differs between 2023 and 2025; the Euler demonstration point differs between 2024 and 2025. Recorded as year-to-year observations, not reconciled.
- Misconception literature: no author-attributed citation could be verified from the cache, so literature claims in research/misconceptions/misconception-taxonomy.md are [single-source] (Tall and Vinner 1981 frame) and Units 9 and 10 causes are [inferred] from scoring guidelines only.
- Misconception records carry empty causal_prerequisites; prerequisite linkage lives on skills and edges instead.
- Intra-unit skill-to-skill edges for Units 8, 9, and 10 were absent after the unit fan-out and were authored in a separate pass tagged [inferred].
