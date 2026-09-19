---
title: AP Calculus BC Exam Intelligence Library
research_date: 2026-09-19
status: in_progress
purpose: Index of every file, the ID scheme, the evidence-tag rules, and how the registries and Markdown views relate.
---

# AP Calculus BC Exam Intelligence Library

Target administration: May 2027. This library dissects the AP Calculus BC course and exam into structured knowledge for a future adaptive AI system. It is not a study plan and contains no schedule.

## How the library is organised

Two layers. The machine-readable core lives in `../data/` as JSON and CSV registries validated by `../schemas/`. The Markdown files under `research/` are views written over those registries. Facts live once, in a registry; narrative and reasoning live in Markdown and cite registry IDs. Every check in `../qa/` enforces that relationship.

```
data/curriculum.json        units, topics, learning objectives, essential knowledge, practices, practice skills
data/skills.json            concepts, atomic skills, non-calculus prerequisites
data/prereq_edges.csv       typed prerequisite graph edges (from,to,type,evidence_tag,note)
data/archetypes.json        question archetypes and their variants
data/scoring_points.json    scoring point types derived from official scoring guidelines
data/errors.json            observed error behaviours
data/misconceptions.json    possible internal misconceptions
data/diagnostic_signals.json  what a specific wrong answer is consistent with
data/taxonomies.json        representations, difficulty factors, command verbs
data/frq_records.json       one record per official FRQ part
data/mcq_records.json       one record per public official sample MCQ
data/sources.json           source registry, generated from cache/manifest.json by tools/build_sources.py
data/ids.json               append-only registry of every ID ever minted
```

## ID scheme

IDs are opaque and append-only. Retired IDs get a tombstone with `superseded_by` in `ids.json`. CED codes are attributes on records, never keys, because College Board revises the CED (clarifications effective Fall 2026 reworded two EK statements).

| Prefix | Form | Meaning | Derivation |
|---|---|---|---|
| BC-UNIT | BC-UNIT-06 | CED unit | unit number |
| BC-TOP | BC-TOP-0603 | CED topic | unit two digits + topic two digits (topic 6.3) |
| BC-LO | BC-LO-FUN-6A | learning objective | CED code FUN-6.A with dots removed |
| BC-EK | BC-EK-FUN-6A1 | essential knowledge | CED code FUN-6.A.1 with dots removed |
| BC-MP | BC-MP-3 | mathematical practice | practice number |
| BC-MPS | BC-MPS-3D | practice skill | skill code 3.D |
| BC-CON | BC-CON-06042 | concept | two-digit block (unit number; 00 cross-cutting; 99 synthesis) plus three-digit sequence |
| BC-SKL | BC-SKL-06017 | atomic skill | block plus sequence, as for BC-CON |
| BC-PRQ | BC-PRQ-00012 | non-calculus prerequisite (algebra, trig, function, notation) | block plus sequence |
| BC-QA | BC-QA-06031 | question archetype | block plus sequence |
| BC-QV | BC-QV-06031-02 | variant of an archetype | archetype number plus sequence |
| BC-PT | BC-PT-99007 | scoring point type | block plus sequence |
| BC-ERR | BC-ERR-06090 | observed error | block plus sequence |
| BC-MIS | BC-MIS-06044 | misconception | block plus sequence |
| BC-SIG | BC-SIG-06120 | diagnostic signal | block plus sequence |
| BC-REP | BC-REP-03 | representation type | minted |
| BC-DF | BC-DF-05 | difficulty factor | minted |
| BC-CV | BC-CV-04 | command verb | minted |
| BC-FRQ | BC-FRQ-2025-Q3-C | official FRQ part | year, question, part |
| BC-MCQ | BC-MCQ-CED-012 | official sample MCQ | source document key + number |
| BC-SRC | BC-SRC-sg-25 | source | cache document id or web page key |

Mint sequential IDs with `python3 tools/mint_id.py BC-SKL "name" [count] [block]`. Unit agents write staging files under `data/staging/` and `tools/merge_staging.py` merges them into the registries and registers the IDs; agents never edit the main registries or ids.json directly. Deterministic IDs (UNIT, TOP, LO, EK, MP, MPS, FRQ, MCQ, SRC) are registered with `register()` from the same tool.

## Evidence tags

Every registry record and every Markdown H2 section carries one of `[verified]` (fetched from a primary College Board source in this project's cache, with the document and page named), `[single-source]` (one source, not independently confirmed, or a secondary source), `[inferred]` (a research conclusion drawn from official material, stated as inference), `[uncertain]` (could not be established; also logged in evidence/unresolved-questions.md). `sources` on a record lists `BC-SRC` IDs or cache doc ids with an optional `:page` suffix.

## Tag policy for atomic skills

Every BC-SKL record carries `evidence_tag: inferred` because the atomic decomposition is a research decision the CED does not itself state, and `mapping_tag` (verified or single-source) for its topic, LO, and EK mapping, which is read from the CED. Prerequisite edges and archetype variants are likewise inferred unless a rubric instance is cited.

## Mastery-state vocabulary

Diagnostic signals use one controlled `mastery_state` vocabulary, enforced by the schema: mastered, partial_procedural, partial_conceptual, partial_unspecified (older records that did not distinguish the two partial states), prerequisite_gap, notation_only, not_mastered, not_attempted.

## Independent assessability

Each BC-SKL record carries `independently_assessable` (true when an active archetype requires at most two skills including this one) and `assessability_basis` naming those archetypes. Skills flagged false are assessed only inside multi-skill question parts in the indexed material.

## Scope field

Every record carries `scope`: `AB_only`, `shared` (in both AB and BC), `BC_only`, or `n/a`. Scope for topics is derived from the CED's BC-only markers.

## Corpus tiers

Tier A live: documents currently served by AP Central (2023 to 2026 FRQ and scoring guidelines; 2023 to 2025 samples, statistics, distributions, Chief Reader reports). Tier B archived: withdrawn 2018 to 2022 documents recovered from the Wayback Machine at their original College Board URLs. Tier C legacy: pre-2018 documents at the retired secure-media path, best effort. `official-material/official-question-index.md` holds the coverage matrix; cells state `ok`, `archived_only`, or `not_obtained`.

## Copyright rule

Records store metadata, paraphrase, and an anchor quote of at most 25 words that `qa/07_quotes.py` verifies against the cached text. No question stems, figures, or full rubric text are reproduced.

## File index

exam/: exam-structure.md (the only file allowed to state question counts and timings), exam-blueprint.md (unit and practice weightings), calculator-policy.md, scoring-system.md, exam-construction.md, mathematical-practices.md, historical-changes.md.
curriculum/: curriculum-map.md, prerequisite-map.md, skill-taxonomy.md, concept-dependency-graph.md, notation-language-conventions.md.
units/: unit-01 through unit-10, one file per CED unit, every topic, LO, and EK represented.
question-analysis/: question-archetypes.md, archetype-variants.md, mcq-analysis.md, frq-analysis.md, distractor-taxonomy.md, calculator-vs-noncalculator.md, representation-types.md, difficulty-factors.md, historical-frequency.md (the only file permitted to hold frequency tables).
scoring/: scoring-patterns.md, point-taxonomy.md, justification-requirements.md, notation-requirements.md, partial-credit-patterns.md, common-point-losses.md, chief-reader-findings.md, command-verbs.md.
misconceptions/: misconception-taxonomy.md, diagnostic-signals.md, prerequisite-failures.md, error-to-concept-map.md.
official-material/: official-question-index.md, frq-question-bank.md, official-sample-question-index.md, scoring-guideline-index.md, student-response-index.md, chief-reader-index.md.
evidence/: source-registry.md (generated), claims-and-confidence.md, unresolved-questions.md, skeptic-review.md.

## Tooling

Merge order matters: `tools/merge_staging.py` replays staging files by phase (unit files, taxonomies, scoring points, Chief Reader, MCQ, FRQ, difficulty factors, representation map, consolidations, signal remap, dependents sync, link-evidence) so consolidation and linking edits always win over the original unit records. `tools/retire_ids.py` writes tombstones from registry status fields. `tools/link_official_evidence.py` propagates FRQ and MCQ ids into skills, archetypes, variants, errors, point types, and difficulty factors. `tools/frequency_tables.py` writes count tables to cache/frequency/ for historical-frequency.md. `tools/unit_evidence_sections.py` regenerates the official-evidence section at the end of every unit file. `tools/graph_check.py` reports cycles, roots, leaves, and unit dependencies. `tools/find_duplicates.py` and `tools/find_duplicate_archetypes.py` surface consolidation candidates.

`tools/fetch_corpus.py` builds the cache. `tools/extract_text.py` writes per-page text. `tools/build_sources.py` regenerates sources.json. `qa/12_report.py` runs every check and prints the counters used in PROGRESS.md. All QA scripts exit non-zero on failure.
