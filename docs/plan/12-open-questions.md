---
title: Open Questions and Library Dependencies
research_date: 2026-09-19
status: draft
purpose: Every unresolved decision in the plan with the evidence that would resolve it, every tunable parameter that has no source, and every research-library dependency the plan needs but the library does not yet satisfy, so that research and implementation work can be prioritised.
---

# Open questions and library dependencies

Each entry names the question, the plan document that depends on it, what was tried or what the ledgers found, and the evidence that would settle it. Entries are tagged [uncertain] unless partial evidence exists. Tunables with a current value are listed in the register at the end; they are working values, not findings.

## Exam and administration facts [uncertain]

- Whether AP Calculus BC receives a Bluebook reference sheet. The Bluebook tools page says a reference sheet with commonly used formulas appears on all tests with math questions (https://bluebook.collegeboard.org/students/tools [verified, the sentence]); no Calculus-specific College Board source confirms or denies it, and the CED and scoring guidelines do not mention one. Affects [04-item-generation.md](04-item-generation.md) (what an item may assume the student can look up) and [05-assessment-modes.md](05-assessment-modes.md). The plan builds the bank as if no sheet exists. Settled by: a College Board page or a 2027 sample booklet naming the Calculus reference sheet, or a screenshot from a Bluebook practice test for AP Calculus.
- Which Desmos variant Bluebook ships for Calculus and whether it satisfies all four CED calculator capabilities. The policy page says Bluebook may include graphing, scientific or four-function calculators depending on the exam (https://apstudents.collegeboard.org/exam-policies-guidelines/calculator-policies [verified]). Affects the calculator-part simulator in 05. Settled by: the Bluebook practice app for Calculus, or a College Board statement.
- The 2027 booklet layout under the revised 42-question Section I. The booklet overview is effective January 2026 and full-length 2027 sample booklets were promised for early 2027 (https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf [verified]). Affects the printable booklet page in 05 and 08. Settled by: the 2027 sample booklet.
- Whether multiple-choice numbering is continuous 1 through 42 across the calculator boundary in the Bluebook interface. Carried from research/exam/exam-structure.md. Affects wireframe copy in 08 only.
- The number of answer options on 2027 multiple-choice items. research/question-analysis/mcq-analysis.md records four options on both current-framework sample sets and five on the 2012 practice exam. The plan assumes four (guessing floor 0.25, credit 0.75, diagnostic raw target 0.625) and stores the option count per item so the constant can follow the item ([02-adaptive-engine.md](02-adaptive-engine.md)). Settled by: 2027 sample questions.
- The exam date Monday 10 May 2027 rests on one web page (research/exam/exam-structure.md [single-source]). Settled by: the printed 2027 exam calendar PDF.
- Hybrid delivery for 2027 is [single-source] in the library although track 3 found three corroborating College Board pages; the library record should be promoted before the plan's tag changes.

## Learning-science parameters with no source

These are the parameters the ledgers could not source. All are [inferred] and listed as tunables below.

- Optimal spacing gap for calculus. Cepeda et al 2008 gives 5 to 20 percent of the retention interval for trivia facts up to a year (https://journals.sagepub.com/doi/abs/10.1111/j.1467-9280.2008.02209.x [verified]); Rohrer and Taylor 2006 is one small mathematics study [single-source]. The plan uses FSRS-7 defaults with a desired retention of 0.90 then 0.95 from 15 March 2027. Settled by: this student's own retention curve on due reviews (metric in [10-quality-and-evaluation.md](10-quality-and-evaluation.md)).
- Whether FSRS, SM-2 or half-life regression is valid for procedural mathematics. No benchmark was found (track 2 [inferred from absence]). Settled by: the arm 6 ablation in 10 (lambda = 0 versus lambda = 2.0) and the retention metrics.
- Session length. Only Baddeley and Longman 1978 on typing exists (https://www.tandfonline.com/doi/abs/10.1080/00140137808931764 [single-source]); no meta-analysis for mathematics. The 45-minute forecast is a queue forecast, not evidence. Settled by: accuracy by minute within session (10).
- The interleaving constants (2 consecutive, 4 skills per 10, 2 units), the 20 percent translation floor, the 70/30 attempted-versus-worked split, the 60 to 85 percent target band, the fading ladder thresholds (2 and 2), the mastery corroboration rule (3 successes, 2 archetypes, 3 days, 7-day span), the 1-day hypercorrection gap, the 3-point confidence scale, and the 10 to 15 minute productive-failure cap. All named as inferred in [01-learning-model.md](01-learning-model.md). Settled by: the within-student A/B designs in 10 where a single student can power them (elaborated versus verification feedback; RETRIEVAL_ENTRY 1 versus 3), and otherwise by the offline simulation.
- Calculus-specific effect sizes. None exist beyond the contested Calculus Concept Inventory gain comparison (https://www.ams.org/notices/201308/rnoti-p1018.pdf [verified, the numbers], psychometric critique [single-source]). The plan does not use the CCI as a criterion.
- Deci, Koestner and Ryan 1999 effect sizes came from a search summary, not the loaded paper (track 4 [single-source]). Settled by: reading the paper.

## Engine questions

- The conjunctive-over-hard-edges, compensatory-over-supporting split in item prediction has no published model behind it (track 2 [inferred]). The plan logs the pure compensatory counterfactual on every observation (invariant in 02) and gates its retention on calibration. Settled by: head-to-head calibration after the first few hundred items, and by the offline simulation.
- The five-term selection score (learning target, due coverage, coverage tie-break, exam weight, representation gap) is deferred. Settled by: the P7 simulation showing it beats the two-term score on mastery per item, not merely random ([10-quality-and-evaluation.md](10-quality-and-evaluation.md)).
- Cold-start distribution of predicted item probabilities. Gate: before P1 merges, compute p_A_knowledge for all 139 archetypes under the centred beta prior; if the 90th percentile is below 0.3, recalibrate the 0.35 coefficient and TARGET_LEARN together ([11-phased-delivery.md](11-phased-delivery.md)). Pre-computed from `data/` on 2026-09-19 under the split rule: p50 0.456, p90 0.587, so the prior passes on paper; a pure conjunctive product over all loaded skills gives p90 0.207 and would fail (details in [02-adaptive-engine.md](02-adaptive-engine.md), Calibration plan).
- The 85 percent rule is derived for a binary classifier under Gaussian noise and its authors state it does not yet generalise to multi-choice tasks (https://www.nature.com/articles/s41467-019-12552-4 [verified]); Math Academy's 80 percent is vendor-published [single-source]. The plan uses 0.8 as a fading-stage filter, not a score term.
- Whether the co_requisite edge type (2 edges) should ever gate. Treated as inert (02 invariant 21).
- Precedence when a diagnosis, a hypercorrection flag and a pending probe all want the next slot. Order fixed in 02 Session assembly (probe, then hypercorrection, then due reviews) [inferred].

## Grading, generation and verification questions

- At what per-point agreement the app should stop showing scores at all. The ledger ceiling is kappa 0.56 and exact agreement at most 0.22 on N = 28 (https://arxiv.org/pdf/2603.00451 and https://arxiv.org/html/2607.01247 [single-source]); no published figure exists for agreement with AP Readers on the nine-point scale. Every point stays provisional; the threshold is unset. Settled by: the operator golden set in 10 (exact match and kappa per point type).
- The acceptable key error rate for items. No source gives one. Gate: measured on a 100-item audited sample in P1, then P4 may not regress against it ([11-phased-delivery.md](11-phased-delivery.md)).
- The fraction of BC-relevant expressions SymPy can settle. Unknown until measured; P1 measures it on the 40-pair equivalence fixture, and unanimity as the P4 publication rule is conditional on it ([04-item-generation.md](04-item-generation.md)).
- How LLM graders handle eligibility-after-error rules, which no cited study covers. Settled by: golden responses in 10 written specifically with earlier-step errors.
- Whether transcription and rubric evaluation should be one call or two. The literature has both designs and does not settle it (track 3 [single-source]). The plan separates them so the read-back can be confirmed.
- Duplicate-detection thresholds (MinHash 5-gram Jaccard 0.8, embedding cosine 0.85) are practitioner rules of thumb, not validated on mathematics item text (track 3 [single-source]). Settled by: a labelled sample of near-duplicates against the official corpus.
- Whether College Board treats a structural description of a question type, as opposed to its text, as protected. No cited page answers it. The plan serves no official text and logs provenance per item. Settled by: counsel, not research.
- Whether P4 (generation for all archetypes) may run in parallel with P3 (grading). The dependency graph allows it; the plan keeps phases serial as a working rule ([11-phased-delivery.md](11-phased-delivery.md)).

## Assessment and score-estimate questions

- Section weighting from raw points to composite and the composite-to-score cut points are unpublished (https://apstudents.collegeboard.org/help-center/how-are-ap-exams-scored [verified]; research/exam/scoring-system.md). The plan shows a band with stated assumptions and no centre. Settled by: nothing public; the position stands.
- Evidence-based standard setting is described in a 2025 College Board post ([single-source]); whether it moves cut points year to year is unknown.
- Mock-exam cadence. No source gives an evidence-based frequency for a three-hour exam. The plan uses part drills every 2 to 3 weeks and mocks every 4 to 6 weeks, more often in the final 8 weeks [inferred].
- Whether timed practice on AP-format sections improves AP scores. No study found; speededness transfer is narrow (track 3 [single-source]). Timed sessions update pacing metrics only.

## Provider and tooling unknowns

- Gemini free-tier numeric limits (shown only in AI Studio) and Gemini's data-retention policy (not loaded). Gemini stays second tier until the policy is read ([07-ai-provider-layer.md](07-ai-provider-layer.md)).
- OpenRouter's tool-calling page returned 404; tool_choice semantics are unknown.
- MathLive's licence and current feature list: track 3 loaded the npm page (MathJSON export, 800+ commands [verified]) while track 4 got an empty site. Re-fetch before the input decision is final.
- KaTeX font family names and their Computer Modern lineage, Inter's optical-size tracking table, Material 3 duration and easing tokens, the WCAG 1.4.11 non-text contrast ratio, and Latin Modern, STIX Two and Libertinus metrics were not loaded (track 4). [08-design-brief.md](08-design-brief.md) states them as unknown.
- Per-quantisation VRAM for DeepSeek-R1-Distill-Qwen-14B on Ollama is not published on the GPU page; measure before relying on the offline fallback.
- Consumer subscription weekly limits are not published as hours; claudebox remains single-operator and off by default regardless ([07-ai-provider-layer.md](07-ai-provider-layer.md)).
- Whether the FRQ image size and the requests per session assumed in [06-architecture.md](06-architecture.md) hold; both are unmeasured.

## Security and privacy questions

- Parental access to a minor learner's data: what a parent may see, how consent is recorded, and the applicable law in the operator's jurisdiction. Written as open questions in [09-security-and-privacy.md](09-security-and-privacy.md); the design position is mastery and effort views, not per-item transcripts.
- Retention default of 30 days after the exam date with export first is a plan choice, not a legal finding.

## Research-library dependencies not yet satisfied

All computed from `data/` on 2026-09-19. Each names the plan document blocked and the library work that closes it.

| Gap | Count or IDs | Blocks | Library work |
|---|---|---|---|
| Active archetypes with no `point_types` | 56 (list in the P1 section of [11-phased-delivery.md](11-phased-delivery.md) for Units 1 to 3; full list from `python3 -c` over data/archetypes.json) | Per-point grading of their free-response variants (03, 05); they are served as MCQ or short answer only | Fill `point_types` from the scoring guidelines via a staging file and `tools/merge_staging.py` |
| Archetypes with no `official_examples` | 36 | Difficulty priors rest on BC-DF counts only (02, 04) | Link official evidence or record why none exists |
| `safe_variables` and `difficulty_variables` are prose | all 139 archetypes | Machine generation in P4 needs a structured parameter spec per archetype: parameter names, domains, exclusions, and the invariants to assert under Monte Carlo (04) | New archetype field, schema change, staging merge |
| BC-DF factors carry no numeric weights | 17 | `beta_k` prior and the difficulty dials are [inferred] (02, 04) | Either author weights from FRQ score means per factor or leave to product calibration |
| Prerequisite edges to topic nodes | 48 edges (31 from BC-TOP, 17 to BC-TOP), all tagged inferred and noted "unmapped" | Loaded inert; they neither gate nor propagate (02 R13) | Remap each edge to the BC-SKL ids it stands for, or retire it |
| Skill with no archetype | BC-SKL-02001 | Cannot be assessed or fringe-selected | Author or map an archetype |
| Block-99 misconceptions linked to no skill or archetype | 10 | Never proposed by the diagnostician (03) | Link or retire |
| 2018 FRQ records carry no points | 22 parts | Excluded from golden-set derivation (10) | 2018 scoring guidelines were not recoverable (research/evidence/unresolved-questions.md) |
| sg-24 records rest on OCR | 2024 point and FRQ records [single-source] | Golden responses for 2024 archetypes carry the tag | Nothing further unless a text-layer PDF is found |
| 2026 samples, statistics, distributions and Chief Reader report | not yet published | Score positioning uses 2023 to 2025 only (05) | Re-fetch with `python3 tools/fetch_corpus.py live` when published, then the CLAUDE.md workflow |
| Misconception literature citations | [single-source] Tall and Vinner frame; Units 9 and 10 causes [inferred] | Diagnostician priors (03) | Verify citations from primary sources |
| Only 5 of 711 signals carry `mastered` | 5 | The `mastered` state is assigned by rule, rarely by signal match (03) | Author mastered-state signals or accept the rule |
| exam-structure.md is silent on the Bluebook tool set | none recorded | 05 cites track 3 directly | Add the tool set with its source to the library file |
| calculator-policy.md omits the stem-level "show the setup" wording and the radian-mode note | none recorded | 05 cites the 2025 scoring guidelines directly | Add both with page citations |
| scoring-system.md omits evidence-based standard setting | none recorded | 05 | Add with the College Board post as [single-source] |

## Tunables register

Every parameter below is [inferred] unless noted. The authoritative per-engine list with the metric that watches each one is the tunables table at the end of [02-adaptive-engine.md](02-adaptive-engine.md); this register collects the ones that cross documents.

| Parameter | Current | Owner | What would settle it |
|---|---|---|---|
| gamma, rho | 1.0, -0.5 (were 0.4, -0.2 until 2026-09-19) | 02 | per-skill fit after 20 observations |
| lambda | 0 (was 2.0) | 02 | arm 6 ablation in 10 |
| beta coefficient on centred BC-DF count | -0.35 per factor above the median of 2 | 02, 04 | first-attempt accuracy regressed on factor count |
| Credit weights per mastery_state | mastered 1.0 to c; partial 0 to c and 0.5 to f; notation_only 0.25 to c; not_mastered 1.0 to f | 02, 03 | sensitivity sweep in simulation |
| MCQ guessing floor and credit | 0.25, 0.75 (four options) | 02, 10 | 2027 option count; MCQ versus free-response calibration split |
| Propagation weights | 0.3 at 1 hop, 0.09 at 2, 0.1 supporting, 0.3 forward failure | 02 | simulation ablation |
| FSRS grade mapping | 4/3 mastered, 2 partial and notation_only, 1 not_mastered and prerequisite_gap (departs from track 2's 3 for partial) | 02 | retention at 7 and 30 days |
| Mastery and un-mastery thresholds | 0.9, 0.75 | 02 | un-mastery rate after declaration |
| RETRIEVAL_ENTRY | 1 unaided success | 02, 10 | within-student A/B, 1 versus 3 |
| Desired retention schedule | 0.90, then 0.95 from 2027-03-15 | 02, 05 | review volume against retention |
| Diagnostic cap and stop | 30 items, entropy 0.02 bits over 3 items, floor 10 | 02 | held-out agreement at several stopping points |
| Interleaving constants and translation floor | 2 consecutive, 4 skills per 10, 2 units, 0.20 | 01, 02 | method-selection versus execution accuracy; representation matrix |
| Session blocks and forecast | 5 review, 25 minute learning, 10 to 15 mixed, 3 minutes per unknown archetype | 02 | accuracy by minute; queue completion |
| Probe queue | 3 entries, 7-day expiry | 02, 03 | probe resolution rate |
| Diagnostician priors and multipliers | 0.5 / 0.25 / 0.1; 2.0 and 0.5 signal match; 1.5 confidence; 0.3 to 0.5 non-conceptual mass | 03 | error-type recurrence after diagnosis |
| Grader sampling | 2 at temperature 0 plus 1 strictness-varied | 03 | agreement on the golden set |
| Monte Carlo family gate | 0 failures on 300 draws (P1), threshold unset for P4 | 04 | measured family failure rate |
| Duplicate thresholds | Jaccard 0.8 on 5-grams; cosine 0.85 | 04 | labelled near-duplicate sample |
| Difficulty dial cost | 0.35 logits per step | 04 | same regression as beta |
| Timed cadence | drills every 2 to 3 weeks, mocks every 4 to 6, more in the final 8 | 05 | mock trajectory |
| Score band | at least one point either side, no centre shown | 05 | nothing public; policy |
| Rapid-guessing threshold | per-archetype latency distribution, factor-count fallback | 05 | latency data |
| Job retry ladder and cooldown | 1, 5, 25 minutes, 4 attempts; 2 fails, 60 s | 06, 07 | provider error logs |
| Role temperatures | tutor 0.3, generator 0.7, diagnostician 0.2, grader and verifier and transcriber 0.0 | 07 | golden tests |
| Item bank size | 30 to 60 verified items per archetype | 06 | repeat-exposure rate |
| Key error rate threshold | unset; measured in P1 | 10, 11 | 100-item audit |
| Simulation acceptance | 5 percent false-mastery declarations; slip sweeps 0.05, 0.10, 0.20 | 10 | first simulation run |
| Golden set size | 5 responses on each of at least 30 BC-PT ids | 10 | operator capacity |
| Diagnostician exit floor | two ranked hypotheses on at least 80 percent of diagnosed errors | 11 | P3 trial |
| Retention and purge | 30 days after exam date, export first | 09 | operator policy |
| Tutor daily cap | $1.00 per day, token cap unset | 07 | a week of real sessions against the measured cost per feedback screen |
| Client token estimate divisor | 4 characters per token | 07 | the first `raw_usage` block from a real key, since 07 records the Claude 4.7 tokenizer producing about 30 percent more tokens for the same text, and an under-estimate is the unsafe direction for a cap |
