# UltraResearch-N-Plan: AP Calculus BC Exam Intelligence Library

Date: 2026-09-19. Target administration: May 2027 (Monday, May 10, 2027, Session 1 [single-source]).
Working directory: /Users/mahfujm/Documents/growth (empty, greenfield, not a git repository).
Deliverable of this document: a build plan for research/ that a downstream agent fleet executes. Nothing below is the library itself.

## 1. Executive Summary

Build research/ as a two-layer system: a machine-readable core (JSON/CSV registries with stable opaque IDs and JSON Schemas) plus Markdown "views" generated or hand-written on top of it, with a mechanical QA suite that runs after every writing pass. Content is produced by Opus agents that read only from a local, hashed PDF cache built in Phase 0, never from the live web, and calibrated against one frozen gold unit before fan-out.

Four research findings change the plan compared with the request as written:

1. May 2027 is the first exam under a revised MCQ structure (42 MCQ: 29 no-calc in 62 min, 13 calc in 38 min). Every pre-2027 web source states the old 45/30/15 layout. Exam-format numbers must live in exactly one file.
2. AP Central publicly serves BC FRQ material for 2023 to 2026 only. 2018 to 2022 PDFs are recoverable from the Wayback Machine as real PDFs (verified for 2019 and 2022 FRQs). Pre-2018 files used a different legacy path and are unverified. "All available years" therefore means a tiered corpus: Tier A live (2023 to 2026), Tier B archived (2018 to 2022), Tier C legacy (pre-2018, best effort, and pre-2019 questions carry old LO codes needing a crosswalk).
3. Chief Reader reports are public for 2023 to 2025 only. Scoring commentary is not a separate document; it is inside each per-question "Student Samples and Commentaries" PDF. The official-material/ file list in the request must reflect this.
4. No public machine-readable CED exists. The CED PDF (cover "Effective Fall 2020", body silently updated, plus a Fall 2026 clarifications overlay) is the sole upstream. The transcription is original work and is on the critical path.

## 2. Task Understanding

Objective: a documentation library that lets a future AI diagnose, sequence, generate, and score AP Calculus BC at atomic-skill granularity, with every claim tagged and traceable.

Success criteria: the 25 completion questions in the request are answerable from the library; every CED topic, LO, and EK is represented; every indexed FRQ part has a metadata record; every ID resolves; every claim carries one of [verified] [single-source] [inferred] [uncertain]; QA suite passes.

Constraints: no study plan, no product code, no full reproduction of College Board questions or rubrics, no login-gated content, no numbers from model memory, primary College Board sources first, 3-space indentation for any new scripts, double quotes, no em dashes.

## 3. Repository Findings

The directory is empty. No incumbent conventions, no git. Decisions: initialise git locally (do not push; .claude/ and any generated agent artifacts gitignored per global rules), Python 3 for QA scripts and extraction, PyMuPDF primary extractor with pdftotext cross-check.

## 4. Research Findings

Finding: 2027 exam format. Section I: 42 MCQ, 100 min, 50%. Part A 29 q / 62 min / no calculator / 35%. Part B 13 q / 38 min / calculator / 15%. Section II: 6 FRQ, 90 min, 50%. Part A 2 q / 30 min / calculator. Part B 4 q / 60 min / no calculator. Total 3 h 10 min.
Evidence: CED PDF p.198 and https://apcentral.collegeboard.org/courses/ap-calculus-bc/exam, fetched 2026-09-19. Confidence: [verified].
Implication: exam/exam-structure.md is the only file permitted to state counts and timings; all others link to it.

Finding: hybrid digital delivery. MCQ answered and FRQ prompts viewed in Bluebook; FRQ answers handwritten in paper booklets. Built-in Desmos allowed in calculator parts only; up to two handheld graphing calculators.
Evidence: https://apstudents.collegeboard.org/courses/ap-calculus-bc/assessment and the calculator-policies page. Confidence: [verified].
Implication: scoring analysis of handwriting, notation, and "write the setup plus the result" for calculator work remains fully relevant.

Finding: CED edition semantics. Cover reads "Effective Fall 2020"; a separate PDF "Clarifications and Corrections, Effective Fall 2026" rewords EK FUN-1.C.1 and FUN-7.B.2 and changes MCQ counts. Unit weightings for BC: U1 to U4 5-10%, U5 10-15%, U6 15-20%, U7 5-10%, U8 5-10%, U9 10-15%, U10 15-20%. Skills 1.A, 1.B, 3.A are marked "not assessed". The "Course at a Glance" PDF is stale.
Evidence: CED PDF pp.12, 198-201; clarifications PDF. Confidence: [verified].
Implication: store `ced_edition` as a pair (cover year, clarifications year). Never use CED codes as primary keys; store the EK sentence text verbatim so rewording is diffable.

Finding: public corpus depth. Live: 2023 to 2026 FRQ and SG; 2023 to 2025 samples, scoring statistics, distributions, Chief Reader reports. Withdrawn 2018 to 2022 files 301-redirect; Wayback serves them. 2020 has no BC file at the standard path. 2021 had multiple forms (a set-2 file once existed). 2012 full released BC practice exam is live. Official MCQ sources: CED sample questions, the standalone sample-questions PDF, the 2012 practice exam.
Evidence: inventory agent fetches plus my curl checks, 2026-09-19. Confidence: [verified] for live and for Wayback 2019/2022; [uncertain] for other archived years.
Implication: official-material/ needs a coverage matrix with explicit `status: not_published` and `status: archived_only` cells. Frequency analysis denominators must state which years were actually indexed.

Finding: scoring conventions. Current SGs state answers need not be simplified, decimals accurate to three places, at most one point per question lost to rounding. No "bald answer" phrase; the current equivalent is "with or without supporting work" stated per point. MC:FRQ raw weights and composite cuts are not published.
Evidence: ap25-sg-calculus-bc.pdf; score-setting page. Confidence: [verified] and [inferred] for the non-publication.
Implication: derive the point taxonomy from actual SG text; log unpublished raw-score structure in unresolved-questions.md, not as an estimate.

Finding: copyright terms. All AP content is College Board copyright; the only carve-out is limited classroom copying. No clause addresses metadata indexing.
Evidence: ap-services-terms-conditions.pdf. Confidence: [verified] on terms, not legal advice.
Implication: records store citation, paraphrase, and anchor quotes under 25 words; never stems, figures, or full rubric text. A QA script enforces the cap and an n-gram overlap limit.

Finding: prior art. Ted Gott's Exam Index (FRQ 1998 to 2017, MCQ 1998 to 2018, tagged to pre-2019 LO/EK, links only) is the closest model and a partial old-to-new crosswalk. Math Medic, CalcPrep, TI in Focus converge on facets {year, question, unit, topic, calculator, FRQ type}. Misconception literature is rich for limits, derivatives, FTC/accumulation (Tall and Vinner, Orton, Bezuidenhout, Thompson and Silverman) and thin for series and related rates. Junyi15 offers a dual-annotation edge protocol for prerequisite graphs.
Confidence: [single-source] each. Implication: adopt the converging facet vocabulary; type prerequisite edges (hard, supporting, co-requisite); flag Units 9 and 10 misconception records as literature-thin and lean on rubric and Chief Reader evidence there.

## 5. Alternatives Considered

| Dimension | A: Markdown only, hand-written | B: JSON core plus Markdown views (recommended) | C: Full graph database and generator |
|---|---|---|---|
| Correctness | Cross-links rot silently | Schemas and link checker catch rot | Same, higher setup |
| Complexity | Low | Medium | High |
| Machine usability | Poor | Good | Best |
| Token cost | High re-reading, duplicated facts | Facts stored once | Same as B plus tooling |
| Resumability | Weak | Strong (registries plus PROGRESS.md) | Strong |
| Fits "no production software" rule | Yes | Yes (scripts are QA, not product) | Borderline |

B wins: it satisfies the machine-usability requirement without building product software, and it makes the skeptic's QA checklist mechanical.

## 6. Recommended Approach

Phase 0 builds the cache, registries, schemas, ID minting, and QA scripts. Phase 1 transcribes the CED into the curriculum registry. Phase 2 writes one gold unit end to end and freezes it. Phase 3 fans out unit agents with the gold unit as the exemplar. Phase 4 indexes FRQs and scoring per year from cached text. Phase 5 derives cross-cutting taxonomies (archetypes, points, misconceptions, diagnostics) from the records produced in 3 and 4, not from memory. Phase 6 runs a skeptic pass and QA and writes evidence files. Each phase ends with QA green and PROGRESS.md updated.

## 7. Architecture and Data Flow

```
College Board URLs + Wayback URLs
→ cache/pdf/{sha256}.pdf + cache/text/{doc_id}/page-NN.txt + cache/manifest.json
→ agents read cache paths only
→ registries: data/ids.json, data/curriculum.json, data/skills.json, data/prereq_edges.csv,
   data/archetypes.json, data/frq_records.json, data/scoring_points.json,
   data/misconceptions.json, data/errors.json, data/diagnostic_signals.json, data/sources.json
→ Markdown views in research/ (units/, question-analysis/, scoring/, misconceptions/, official-material/, exam/, curriculum/, evidence/)
→ qa/*.py validates schemas, IDs, links, tags, coverage, scope, quotes, prediction language, granularity
→ PROGRESS.md counters regenerated by qa/12_report.py
```

ID scheme (opaque, append-only, documented in README.md):
- BC-UNIT-01 .. BC-UNIT-10; BC-TOP-0101 (unit 01, topic 01); BC-LO-LIM-1A and BC-EK-LIM-1A1 mirror CED codes as attributes, not keys
- BC-CON-0001 concept, BC-SKL-0001 atomic skill, BC-PRQ-0001 non-calculus prerequisite (algebra, trig, function, notation)
- BC-QA-0001 archetype, BC-QV-0001-01 variant
- BC-PT-0001 scoring point type; BC-ERR-0001 observed error; BC-MIS-0001 misconception; BC-SIG-0001 diagnostic signal
- BC-FRQ-2025-Q3-C official question part; BC-MCQ-CED-0012 sample MCQ; BC-SRC-0001 source
- Every record: id, name, scope (AB_only | shared | BC_only), ced_edition, evidence_tag, sources[], created, updated. Retired IDs get a tombstone with superseded_by.

## 8. Implementation Blueprint

Phase 0: infrastructure (one agent, then QA)
1. git init; .gitignore with .claude/, cache/pdf/, scratch.
2. tools/fetch_corpus.py: download from URL templates (live: B/ap{YY}-frq|sg|apc-q{N}|calculus-bc-scoring-statistics|score-distributions|ab-subscore-score-distributions|cr-report-calculus[-ab-bc].pdf for YY 23-26; archived: web.archive.org/web/{ts}id_/{same URL} for YY 18-22; legacy secure-media pattern for 2012-2017 best effort; 2012 practice exam; CED; clarifications; sample-questions PDF). Record URL, fetch date, HTTP status, sha256, byte length, tier in cache/manifest.json. Respect Wayback rate limits (sleep 3 s, retry on 429).
3. tools/extract_text.py: PyMuPDF get_text("dict") to per-page text with sub/superscript reconstruction, pdftotext -raw cross-check, min-char and math-density assertions, quarantine list for image-only pages.
4. schemas/*.schema.json for every registry; tools/mint_id.py; data/ids.json.
5. qa/00_manifest.py through qa/12_report.py per the skeptic checklist (manifest, schema, ids, links, tags, coverage, scope, quotes, prediction phrasing, granularity, crosswalk, freshness, report).
6. research/README.md (schema, ID rules, evidence-tag rules, file map) and PROGRESS.md skeleton.

Phase 1: curriculum transcription (one agent, CED pages only)
7. data/curriculum.json: 10 units, all topics 1.1 to 10.15, every LO and EK with verbatim EK text, BC-only markers derived from CED marking, unit weightings, MP skills 1.A to 4.E with "not assessed" flags, clarifications diff applied and recorded.
8. data/ced_crosswalk.csv: (internal id, ced_edition, ced_code); seed pre-2019 column from CED comparison and from Ted Gott index vocabulary (re-derived, not copied).
9. research/curriculum/curriculum-map.md, exam/mathematical-practices.md, exam/exam-structure.md, exam/exam-blueprint.md, exam/calculator-policy.md, exam/historical-changes.md, exam/scoring-system.md, exam/exam-construction.md from the verified ledger in this plan plus CED pages. qa/05 must pass topic set equality here.

Phase 2: gold unit (one agent, high effort)
10. Unit 6 (integration and accumulation) as the gold reference: full topic mapping, concept and subskill decomposition with target 4-8 skills per topic, prerequisites as typed edges, representations, assessment forms, archetypes, adaptive metadata block (MASTERED IF / PARTIALLY / PREREQ GAP IF / CONFUSIONS / NEXT DEPENDENT / DIAGNOSTIC TYPES / REMEDIATION TARGET). Freeze after skeptic review. Record the per-topic skill count distribution as the granularity baseline.

Phase 3: unit fan-out (up to 5 parallel agents, 2 units each, Unit 6 file as exemplar in each brief; Unit 9 and 10 briefs flag literature thinness)
11. units/unit-01 .. unit-10 (except 06), plus appends to skills.json, prereq_edges.csv, archetypes.json. Each agent returns only counts and open questions, not content, to the orchestrator.
12. curriculum/prerequisite-map.md, concept-dependency-graph.md, skill-taxonomy.md, notation-language-conventions.md generated from registries plus hand-written narrative on hidden prerequisites.

Phase 4: official material indexing (one agent per year tier, reading cache/text only)
13. data/frq_records.json: one record per part for every cached year; fields per request (calculator status, URLs, units, topics, LOs, skills, MPs, archetype and variant, representation, point allocation, scoring behaviors, notation and justification requirements, difficulty factors, diagnostic distinctions). Anchor quote under 25 words, checked by qa/07 against cached text.
14. data/scoring_points.json populated from SG text per point; data/errors.json from sample commentaries and Chief Reader reports (2023 to 2025 only; tag `chief_reader` forbidden elsewhere).
15. official-material/official-question-index.md, frq-question-bank.md, official-sample-question-index.md (CED samples, sample-questions PDF, 2012 practice exam, distractor notes tagged [inferred]), scoring-guideline-index.md, student-response-index.md, chief-reader-index.md, plus the coverage matrix with explicit not_published and archived_only cells.

Phase 5: cross-cutting synthesis (2 to 3 agents reading registries, not PDFs)
16. question-analysis/: question-archetypes.md, archetype-variants.md, mcq-analysis.md, frq-analysis.md, distractor-taxonomy.md, calculator-vs-noncalculator.md, representation-types.md, difficulty-factors.md; frequency tables live in question-analysis/historical-frequency.md with fixed disclaimer and stated denominators, 2020 and 2021 flagged as anomalous.
17. scoring/: scoring-patterns.md, point-taxonomy.md (each type cites at least 3 real rubric instances), justification-requirements.md, notation-requirements.md, partial-credit-patterns.md, common-point-losses.md, chief-reader-findings.md, command-verb catalog inside justification-requirements.md or its own file.
18. misconceptions/: misconception-taxonomy.md, diagnostic-signals.md, prerequisite-failures.md, error-to-concept-map.md. Every error-to-misconception edge is many-to-many with a confidence and a discriminating probe.

Phase 6: evidence, skeptic pass, closure
19. evidence/source-registry.md (from sources.json), claims-and-confidence.md, unresolved-questions.md seeded with the open items in section 12.
20. Skeptic agent reads a random sample of 10 percent of records against cached text and reports fabrications; fix and rerun qa. PROGRESS.md regenerated.

## 9. Testing Strategy

The QA scripts are the tests. Expected outcomes: qa/00 all manifest hashes match; qa/02 zero duplicate or malformed IDs; qa/03 zero dangling references and an orphan list reviewed; qa/04 zero unresolvable evidence tags; qa/05 exact set equality between CED topic list and library topics, and every LO and EK present; qa/06 zero scope contradictions; qa/07 zero records over the quote cap; qa/08 zero predictive phrases outside historical-frequency.md; qa/09 no unit outside 2x median skills per topic without a written justification; qa/10 crosswalk diff empty against the current CED. Before trusting any QA script, break it deliberately (insert one dangling ID, one over-long quote, one predictive phrase), watch it fail, then restore.

## 10. Verification Strategy

After every phase: run `python3 qa/12_report.py`, paste its output into PROGRESS.md, and spot-check three random FRQ records by opening the cited cache page. After Phase 1: a human-readable diff of EK text against the clarifications PDF for FUN-1.C.1 and FUN-7.B.2. After Phase 3: compare per-unit skill counts. At closure: answer the 25 completion questions from the library alone in a scratch file and log any that fail as unresolved.

## 11. Risks and Failure Modes

Fabricated FRQ content: mitigated by cache-only reads and anchor-quote grep. Stale 2027 format: single-file rule. CED code churn: opaque IDs plus crosswalk plus verbatim EK text. Copyright over-reproduction: quote cap and n-gram check. Overdiagnosis: many-to-many edges with probes. Prediction drift: forbidden-phrase grep. Granularity drift: gold unit plus qa/09. AB/BC conflation: scope field derived from CED markers. Missing Chief Reader years: coverage matrix and tag ban. Token blow-up: extract once, hand agents chunk paths, agents return counts not content. Wayback gaps or rate limits: tiered corpus with explicit archived_only status; never infer a year that was not fetched. Link rot: registry stores hash and fetch date; qa/11 revalidates.

## 12. Assumptions Requiring Verification

- Wayback holds all of 2018 to 2022 BC FRQ, SG, and sample files (verified only for 2019 and 2022 FRQ).
- Pre-2018 files exist under the legacy secure-media path in Wayback (unverified).
- The key-changes page (403 to fetch) says nothing beyond the clarifications PDF.
- Q2 to Q6 sample files exist for 2023 and 2024 (page listing only).
- The 2027 exam date and 8 a.m. start (single source).
- Whether a standalone scoring-commentary document ever existed for older years.
- Whether series and related-rates misconception literature exists beyond what the scan found.

## 13. Adversarial Review

Requirement attack: the request asks for "all available years" and a chief-reader-index for many years; the evidence shows four live years and three Chief Reader years. The plan delivers the tiered corpus and records the gap instead of padding. Scope attack: QA scripts could grow into a product; they stay under qa/ and tools/, are not shipped, and touch no student data. Architecture attack: JSON core could duplicate Markdown content; rule is facts in registries, narrative in Markdown, qa/01 checks front matter equals the record. Dependency attack: PyMuPDF sub/superscript recovery is imperfect; records store metadata, so extraction only has to be good enough to tag and to grep anchor quotes. Failure attack: Wayback rate-limits (observed 429 during this session); fetcher sleeps and retries and logs misses as archived_missing. Maintenance attack: College Board revises URLs; hashes are primary references. Simpler solution: plain Markdown only would be faster to start and slower to trust; rejected.

## 14. Final Execution Checklist

```
[x] architecture confirmed (JSON core plus Markdown views)
[x] versions confirmed (CED cover 2020 plus Fall 2026 clarifications; 2027 format 29/13)
[x] critical claims verified (format, delivery, weightings, corpus depth, scoring conventions)
[x] alternatives evaluated
[x] failure modes investigated (18 listed by skeptic track)
[x] implementation files identified
[x] tests defined (qa/00 to qa/12)
[x] verification defined
[x] risks documented
[x] assumptions documented
```

## 15. Handoff to Implementation Agent

OBJECTIVE
Produce research/ as specified, in six phases, with QA green after each.

IMPLEMENTATION STRATEGY
Cache first, transcribe CED second, gold Unit 6 third, fan out fourth, index official material fifth, synthesise sixth. Agents read cache paths only and return counts plus open questions to the orchestrator.

FILES
tools/fetch_corpus.py, tools/extract_text.py, tools/mint_id.py, schemas/*.schema.json, qa/00..12, data/*.json|csv, research/ tree as listed in the request with these corrections: add question-analysis/historical-frequency.md and data/ced_crosswalk.csv; official-material/ files carry a coverage matrix; no study-plan file.

ORDER
Phase 0 → 1 → 2 → 3 (parallel, 5 agents) → 4 (parallel by tier) → 5 (2-3 agents) → 6.

TESTS
qa suite; break-then-restore each script once before relying on it.

VERIFICATION
qa/12 report into PROGRESS.md per phase; random record spot-checks against cache; final 25-question self-test.

DO NOT
State exam counts or timings outside exam/exam-structure.md. Quote more than 25 words per record. Use CED codes as primary keys. Tag chief_reader evidence for years without a report. Write predictive language. Fetch PDFs inside content agents. Create any study plan or schedule. Commit .claude/ or push anything.

CRITICAL ASSUMPTIONS
Wayback coverage for 2018 to 2022; legacy-path availability pre-2018; no CED renumbering in the 2026 clarifications beyond the two EK rewordings.

## Confidence

Overall: High on exam facts and corpus shape, Medium on pre-2018 recoverability and on misconception-literature depth for Units 9 and 10.
