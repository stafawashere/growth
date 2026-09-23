---
title: Adaptive Engine
research_date: 2026-09-19
status: draft
purpose: The mastery model, evidence model, update rules, decay, prerequisite gating, item selection, cold-start diagnostic, difficulty calibration and testable invariants for the AP Calculus BC tutor, with every parameter carrying a source and an evidence tag.
---

# Adaptive Engine

This document specifies the engine that decides what the student sees next and what the app believes about the student afterwards. It implements the teaching thesis in [01-learning-model.md](01-learning-model.md), consumes the research library registries by ID, and hands its unresolved parameters to [12-open-questions.md](12-open-questions.md). The feedback and diagnosis contract it depends on is in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md); item generation is in [04-item-generation.md](04-item-generation.md); assessment modes that do or do not write to this engine are in [05-assessment-modes.md](05-assessment-modes.md); the process boundaries are in [06-architecture.md](06-architecture.md); the tests that hold this engine honest are in [10-quality-and-evaluation.md](10-quality-and-evaluation.md).

Evidence tags follow the convention in `research/README.md` and in the track ledgers. [verified] means a primary source was read with the number attached. [single-source] means one source only, uncorroborated. [inferred] means reasoning from cited facts that no source states. Every [inferred] parameter in this document is repeated in the final section as a tunable.

The design constraint that shapes everything below: there is one learner and no response history at launch. Nothing in this engine may require fitting. Every parameter is either declared from the authored library, taken from a published default, or set by hand and flagged tunable.

## Scope and inputs

The engine reads the research library at startup through the content loader described in [06-architecture.md](06-architecture.md) and holds it as an immutable in-memory graph. It never writes to `data/`.

Registries consumed, with the counts as computed from the repository on 2026-09-19:

| Registry file | Records consumed | Fields the engine reads |
|---|---|---|
| `data/skills.json` | 541 active BC-SKL, 170 BC-CON, 77 BC-PRQ | `id`, `unit`, `concept`, `prerequisites`, `dependents`, `archetypes`, `diagnostic_signals`, `misconceptions`, `common_errors`, `representations`, `calculator_relevance`, `independently_assessable`, `scope`, `adaptive.mastered_if`, `adaptive.partially_mastered_if`, `adaptive.prerequisite_gap_if`, `adaptive.remediation_target`, `adaptive.common_confusions`, `adaptive.diagnostic_archetypes`, `adaptive.next_dependent_skills` |
| `data/prereq_edges.csv` | 1226 edges: 602 `hard_prerequisite`, 622 `supporting`, 2 `co_requisite`, 0 cycles. 48 of those edges touch a BC-TOP id (31 as `from`, 17 as `to`) and are loaded inert, per the BC-TOP rule below | `from`, `to`, `type`, `evidence_tag` |
| `data/archetypes.json` | 139 active BC-QA in 77 families, 395 BC-QV variants | `id`, `family`, `primary_unit`, `skills`, `prerequisites`, `difficulty_factors`, `difficulty_variables`, `safe_variables`, `invariant_structure`, `expected_solution_path`, `point_types`, `representations`, `calculator_status`, `scoring_pattern`, `common_distractors`, `misconceptions`, `official_examples`, `status`; on variants `archetype`, `dimension`, `difficulty_effect` |
| `data/diagnostic_signals.json` | 711 BC-SIG | `skill`, `archetype`, `observation`, `mastery_state`, `consistent_with`, `distinguish_by` |
| `data/errors.json` | 390 active BC-ERR | `skills`, `archetypes`, `possible_misconceptions`, `non_conceptual_causes`, `discriminating_probe`, `scoring_consequence` |
| `data/misconceptions.json` | 213 active BC-MIS | `observable_errors`, `rival_misconceptions`, `discriminating_probe`, `causal_prerequisites`, `exposing_archetypes`, `severity`, `skills` |
| `data/scoring_points.json` | 76 BC-PT | `id`, point definition text used by the grader contract in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md) |
| `data/taxonomies.json` | 14 BC-REP, 17 BC-DF, 29 BC-CV | `id`, `name` for representation-gap scoring and for the declared difficulty prior |
| `data/curriculum.json` | 10 units, 111 topics | unit membership for exam-weight priors |

The engine also reads two research files as data, not as prose: `research/exam/exam-blueprint.md` for the published multiple-choice unit weighting bands [verified, BC-SRC-ced p.199], and `research/exam/exam-structure.md` for the exam date used as the terminal retention target [single-source]. No selection prior in this engine reads a frequency table, so `research/question-analysis/historical-frequency.md` is not an input here (C16).

**BC-TOP nodes (R13).** `data/prereq_edges.csv` carries 48 edges whose `from` or `to` is a BC-TOP id, all tagged inferred in the file and noted as unmapped, and four of them reach the P1 subgraph. The content loader accepts these edges, validates every BC-TOP id against `data/curriculum.json`, and holds the nodes inert: they do not gate, they neither send nor receive propagated credit, they never enter the outer fringe, and they are never selection targets. The remapping of those edges onto BC-SKL ids is carried as a library gap in [12-open-questions.md](12-open-questions.md).

Two structural facts about the library drive most of the modelling decisions. First, only 31 of 541 skills are `independently_assessable`, and the distribution of skills per archetype is 4 skills on 34 archetypes, 6 on 33, 5 on 31, 3 on 22, 2 on 15 and 1 on 4. Every observation is therefore joint evidence about several skills, which rules out any model whose likelihood is written over a single skill per opportunity. Second, the prerequisite graph is authored and acyclic, so structural information about 541 skills exists before the first response, which is the only asset that compensates for having no response data.

`BC-SKL-02001` has no archetype and cannot be observed directly at all. The engine holds state for it and updates it only through prerequisite propagation, and the invariant suite asserts that it never enters the outer fringe as a selectable target.

## Mastery state schema per atomic skill

One row per user per BC-SKL, table `skills_state` in [06-architecture.md](06-architecture.md). This is exactly the D2 state.

| Field | Type | Initial value | Update trigger |
|---|---|---|---|
| `skill_id` | text, BC-SKL foreign key | from `data/skills.json` at first load | never |
| `beta_k` | float, logit | computed declared prior, see Calibration below [inferred] | content snapshot change only; never moved by responses |
| `c_k` | float, credited successes | 0.0 | any credited observation whose mastery_state contributes success credit, and any propagated success from a descendant |
| `f_k` | float, credited failures | 0.0 | any credited observation contributing failure credit, and any propagated failure from a diagnosed prerequisite gap |
| `S_k` | float, FSRS stability in days | null until first credited observation, then `S0(G) = w0 + (G - 1) * w1` from the FSRS-7 defaults [verified] | every credited observation, scaled by the credit weight |
| `D_k` | float, FSRS difficulty on the 1 to 10 scale | null until first credited observation, then `D0(G)` from the FSRS-7 defaults [verified] | every credited observation |
| `last_practised_at` | timestamp | null | every credited observation, direct or propagated |
| `fading_stage` | enum `example`, `completion`, `unsupported` | `example`, or `unsupported` when the skip condition below fires | 2 consecutive credited successes advance, 2 consecutive credited failures drop [inferred] |
| `observation_count` | integer | 0 | every direct observation on an archetype loading this skill, including uncredited ones |
| `distinct_archetypes_succeeded` | set of BC-QA ids | empty | on a credited success at stage `unsupported`, add the archetype |
| `success_days` | set of calendar dates in the user's timezone | empty | on a credited success at stage `unsupported`, add the date; same-day repeats do not add a second entry |
| `mastered` | boolean | false | evaluated after every update to this skill against the mastery declaration rule |
| `mastered_at` | timestamp | null | set when `mastered` flips true, cleared on un-mastery |
| `hypercorrection_due` | date | null | set to tomorrow on a high-confidence error naming this skill; cleared when the requeued item is attempted |
| `consecutive_successes` | integer | 0 | incremented on credited success, reset to 0 on credited failure |
| `consecutive_failures` | integer | 0 | incremented on credited failure, reset to 0 on credited success |
| `concept_opener_done` | integer, 0 or 1 | 0 | stored on the first skill of each BC-CON; set to 1 once the productive-failure opener for that concept has been served by session assembly |

`m_k` and `R_k` are derived, not stored, because both depend on the current clock and a stored copy would go stale between sessions. They are recomputed on read.

**Cold-start values (R1).** For a skill with no credited observation, `S_k` and `D_k` are null, `c_k = f_k = 0`, and `R_k` is defined as 1 rather than undefined, which is the only definition consistent with "no memory has yet decayed". With `lambda = 0` (R3) the decay term is inert in any case, so `m_k = beta_k` for every unobserved skill and `beta_k` alone decides every cold-start prediction. That makes the centring of `beta_k` in the calibration section load-bearing.

**Queue state on the user, not the skill (R6).** One further field lives on the user row rather than in `skills_state`: `pending_probes`, an ordered queue of discriminating-probe requests written by the diagnostician in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md). It holds at most 3 entries and expires entries older than 7 days [inferred]. Every selection function drains it before its own scoring.

Two fields deserve a note. `observation_count` counts every direct exposure, including items where the diagnosis returned `not_attempted` for this skill, because the coverage tie-break in the selection algorithm needs to know how much the engine has looked at a skill, not how much credit it gave. `success_days` is deliberately restricted to stage `unsupported`, because a success on a faded completion problem is not an unaided demonstration and the mastery rule in D2 asks for unaided ones.

## Evidence model

An observation is the complete record of one student encounter with one generated item, written to `attempts` and its child tables. It carries:

1. The item, resolved to its archetype BC-QA, its variant BC-QV when one was chosen, its parameter draw, and the skill list from `archetypes.skills`.
2. The response, which is either a selected option for a multiple-choice item or the student's work for a free-response item, captured as typed MathLive with MathJSON export or as a photographed page that has passed the transcription read-back gate in [05-assessment-modes.md](05-assessment-modes.md).
3. The graded point vector: one decision per BC-PT in `archetypes.point_types`, each earned or not earned, produced by the grader contract in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md). Mechanical points are decided by deterministic pre-checks; only justification, interpretation and notation points are model-decided.
4. The diagnosis: a list of observed errors, each a BC-ERR id or a new candidate, each with a probability-weighted list of BC-MIS candidates and non-conceptual causes, plus one `mastery_state` per skill the item loads, drawn from the enum and ideally matched to a BC-SIG record.
5. The confidence rating, collected on a 3-point scale (guess, unsure, confident) before any feedback is shown [verified that calibration correlates with retention, Dunlosky and Rawson 2012, https://www.sciencedirect.com/science/article/pii/S0959475211000685; the 3-point scale is inferred].
6. Timing: time to first keystroke, total time on item, and the archetype's running median time, used only for the FSRS grade mapping and for the pacing metrics in [05-assessment-modes.md](05-assessment-modes.md).
7. The mode in which the item was served, because rehearsal mode items never write mastery state.

The `mastery_state` enum is the unit of evidence, not binary correctness. The library ships 711 BC-SIG records distributed as `partial_procedural` 204, `partial_conceptual` 189, `partial_unspecified` 174, `not_mastered` 53, `notation_only` 50, `prerequisite_gap` 34, `mastered` 5, `not_attempted` 2. Feeding a eight-valued signal into a binary emission model throws away most of the evidence, which is the concrete reason classic BKT is rejected below [inferred, track 2].

### How MCQ and FRQ evidence differ

Multiple-choice evidence is thin in three ways and the engine treats it as such.

A correct multiple-choice answer is contaminated by guessing. Standard 3PL practice sets a lower asymptote near the reciprocal of the option count. research/question-analysis/mcq-analysis.md records that both current-framework sample sets use four options and only the 2012 practice exam used five [verified], and no source states the 2027 option count, so the engine assumes four options and a floor of 0.25 [inferred] and stores the option count on every item so the floor can follow the item. ALEKS's own design note is the reason this matters: their 0.5 informative target and their claim that lucky guesses are negligible both rest on open-response items [verified, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf]. Move to multiple choice and the premise fails. The engine therefore credits a correct multiple-choice response at 0.75 of a success rather than 1.0 [inferred], and applies no discount to an incorrect one, because a wrong answer on a four-option item is not contaminated by guessing in the same direction.

Multiple-choice evidence also carries no point vector. `data/mcq_records.json` holds 91 official items with `distractor_analysis`, and generated multiple-choice items carry a named BC-ERR path per distractor from the generation contract in [04-item-generation.md](04-item-generation.md), so a chosen distractor is itself a diagnosis. That is the only per-skill resolution multiple choice gives: the selected distractor's error path names the skills it implicates. Where the distractor analysis does not resolve a skill, that skill's `mastery_state` is `not_attempted` and it receives no credit.

Free-response evidence is per-point. An FRQ-shaped item carries between two and nine BC-PT decisions, and the 76 point types separate mechanical from justification and notation demands. This is what makes the eight-valued mastery_state recoverable: a response with the right integral and the wrong units is `notation_only` or `partial_procedural` on distinct skills, and the point vector says which. Free-response evidence is credited at full weight.

The engine records the format on every observation and the invariant suite asserts that no multiple-choice observation ever produces a credit greater than 1 minus the item's guessing floor (0.75 at four options) for a single skill.

### Guessing correction

Guessing correction applies at two places and they must not be confused.

At credit time, a correct multiple-choice response credits `0.75` to `c_k` for each skill the diagnosis marks `mastered`, before any other weighting [inferred].

At selection time, the predicted probability used for difficulty targeting is guessing-corrected in the other direction. For a four-option multiple-choice archetype, a raw success probability of `p_raw` corresponds to a knowledge probability of `p_know = (p_raw - 0.25) / 0.75`, and conversely a knowledge target of 0.5 corresponds to a raw target of `0.5 * 0.75 + 0.25 = 0.625` [inferred, track 2 derived the same form for five options]. Targeting raw accuracy on multiple choice silently drifts the real difficulty upward, which is the failure mode track 2 names for naive ZPD targeting.

## Update rules

### The strength formula

Per skill `k`:

```
phi(x)  = log(1 + x)
m_k     = beta_k + gamma * phi(c_k) + rho * phi(f_k)
P(skill k demonstrated) = sigmoid(m_k)
```

**The decay term is off (R3).** The formula above is the full expression `beta_k + gamma * phi(c_k) + rho * phi(f_k) - lambda * (1 - R_k)` evaluated at `lambda = 0`, which is where it stays until the arm 6 ablation in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) reports. The reason is that the decay quantity would otherwise be used twice from one unvalidated model, once to schedule reviews and once to penalise the mastery estimate, and no source fixes the second use. FSRS-7 retrievability `R_k` therefore enters the engine only in two places: the due test that schedules reviews, and mastery condition 6 (`R_k >= desired retention` at declaration time). The `lambda` row stays in the tunables table at current value 0 so that turning it back on is a parameter change with a named gate rather than a rewrite.

The first three terms are Performance Factors Analysis with the log-rescaled counts that Gervet et al found in Best-LR, formally `sigma(alpha_s - delta_q + phi(c_s) + phi(f_s) + sum_k [beta_k + gamma_k phi(c_sk) + rho_k phi(f_sk)])` [verified, https://files.eric.ed.gov/fulltext/EJ1273917.pdf]. The per-student ability term `alpha_s` is dropped, which is PFA's own construction and costs nothing here because with one learner `alpha` is unidentifiable anyway [verified, the construction, https://files.eric.ed.gov/fulltext/ED506305.pdf; inferred for the consequence].

The fourth term, currently at weight zero, is the decay that no classical model carries. Khajah, Lindsey and Mozer found forgetting to be the single most valuable BKT extension, recovering 50.6 percent of the gap that DKT had been credited with [verified, https://arxiv.org/pdf/1604.02416]. That result is what keeps the term in the formula; it is not a result about a decay penalty applied on top of a decay-driven scheduler, which is why the weight starts at 0.

Parameter values:

| Parameter | Value | Source | Tag |
|---|---|---|---|
| `gamma` | 1.0 | PFA's own construction carries `phi(c)` at unit weight; corrected 2026-09-19 from 0.4, under which `sigmoid(gamma * phi(c))` from `beta = 0` needed 242 credited successes to reach 0.9 and no skill was ever declared in simulation; at 1.0 it takes 9. Sign and asymmetry follow https://files.eric.ed.gov/fulltext/ED506305.pdf | [inferred] |
| `rho` | -0.5 | same, keeping the 2 to 1 asymmetry against `gamma`; corrected 2026-09-19 from -0.2 | [inferred] |
| `lambda` | 0 (R3) | off until the arm 6 ablation in 10 reports. The value it would take if turned on is 2.0 logits, chosen so that full decay to `R = 0` costs about what two failed attempts cost | [inferred] |
| `beta_k` | declared, see Calibration | Pelanek's at-least-100-students floor forbids learning it, https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf | [verified, the floor, inferred for the prior formula] |

`gamma` and `rho` are pooled across all 541 skills and stay pooled. Unpooling needs at least 20 observations per skill, which one learner over one school year will reach for perhaps a few dozen skills, so unpooling is deferred to [12-open-questions.md](12-open-questions.md) rather than built.

### Credit assignment by mastery_state

Each skill the item loads receives one `mastery_state` from the diagnostician. The credit table is D2 verbatim and every weight in it is [inferred, track 2].

| `mastery_state` | Credit to `c_k` | Credit to `f_k` | Elsewhere |
|---|---|---|---|
| `mastered` | 1.0 | 0.0 | adds archetype to `distinct_archetypes_succeeded` and date to `success_days` when `fading_stage` is `unsupported` |
| `partial_procedural` | 0.0 | 0.5 | no mastery-day credit |
| `partial_conceptual` | 0.0 | 0.5 | no mastery-day credit; routes the remediation target from `adaptive.remediation_target` |
| `partial_unspecified` | 0.0 | 0.5 | no mastery-day credit; flagged for the review queue because the diagnosis did not resolve |
| `notation_only` | 0.25 | 0.0 | no mastery-day credit |
| `prerequisite_gap` | 0.0 | 0.0 to the target | 1.0 to `f` of the named prerequisite, plus forward propagation below |
| `not_mastered` | 0.0 | 1.0 | resets `consecutive_successes` |
| `not_attempted` | 0.0 | 0.0 | increments `observation_count` only |

**Why the partials credit 0 to `c_k` (R2).** The earlier split of 0.5 and 0.5 was a ratchet. With `gamma = 0.4` and `rho = -0.2` the asymmetry makes a partial worth `0.4 * log(1.5) - 0.2 * log(1.5) = +0.081` logits, so a student who half-solves every item climbs monotonically toward mastery without ever solving one. The three `partial_*` states therefore credit 0.0 to `c_k` and 0.5 to `f_k`, and a new invariant asserts that no `partial_*` observation may increase `m_k`. `notation_only` keeps its 0.25 to `c_k` and 0.0 to `f_k`, because there the mathematics was demonstrated and only the writing failed. The FSRS grade mapping is unchanged by this decision.

`partial_unspecified` is the largest partial bucket in the library at 174 of 711 signals, so its handling matters. It is credited like the other partials but it is also the single strongest signal that the diagnostician failed to discriminate, and D4's rule applies: when the top two misconception hypotheses sit within 0.2 of each other, the leading misconception's `discriminating_probe` is scheduled as the next item. That scheduling is concrete rather than notional (C18, R6): the probe is pushed onto `pending_probes` and every one of the three selection functions drains that queue before its own scoring, so the probe reaches the student whichever mode the next item comes from.

Multiple-choice credits are multiplied by 0.75 before being applied, as above.

### FSRS-7 grade mapping and stability update

FSRS is used as a decay layer only, never as the mastery model. The rejection of FSRS-as-mastery-model is argued in the comparison section.

Grade mapping, all [inferred]:

| `mastery_state` | FSRS grade `G` |
|---|---|
| `mastered`, confidence `confident`, time below the archetype median | 4 (Easy) |
| `mastered`, otherwise | 3 (Good) |
| `partial_procedural`, `partial_conceptual`, `partial_unspecified` | 2 (Hard) |
| `notation_only` | 2 (Hard) |
| `not_mastered` | 1 (Again) |
| `prerequisite_gap` | 1 (Again) for the named prerequisite; the target skill gets no grade |
| `not_attempted` | no grade |

This table departs from the mapping in the track 2 ledger, and the departure is deliberate rather than an oversight (C15). Track 2 records `mastered = 4, partial_* = 3, notation_only = 2, not_mastered = 1`. This engine maps `mastered` to 4 only when confidence is `confident` and time is below the archetype median, and pushes all three `partial_*` states down to 2, so a partial schedules a shorter interval than the ledger would. The reason is that a partial on a multi-skill calculus item is weaker evidence of a formed memory than a "Hard" recall of a flashcard, and the credit rule now treats it as failure evidence (R2). Both mappings are [inferred] and the row in the tunables table covers the whole table, so the ledger's mapping is the first alternative to test.

The update uses the FSRS-7 default parameter vector, all 34 entries, taken verbatim from the reference implementation, `src/inference_v7.rs` in https://github.com/open-spaced-repetition/fsrs-rs, whose `model_v7.rs` fixes the count at 34 [verified, that repository at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae, 2026-09-19]. The srs-benchmark README, which earlier drafts of this document named as the source, still prints a 35-value block under "Default Parameters" that belongs to a superseded March 2026 draft of the model and begins 0.041, 2.4175, 4.1283, 11.9709; that block is not the vector the benchmark's "FSRS-7" row runs [verified, srs-benchmark models/fsrs_v7.py at commit bd9110f791e5b37282c55a9aa8db35f68f0c4aa2]. **R28.** No entry of the vector is written here, because a number recalled rather than copied would be worse than a gap. The implementer copies the full 34-entry vector out of the source file into a versioned constants file at implementation time, commits that source file as a fixture with the commit hash and digest recorded beside it, and `test_retrievability_monotone` asserts that the constants file still matches the fixture. The choice of defaults over per-user optimization is forced and cheap: on 9,999 Anki collections and 349,923,850 reviews, FSRS-7 with default parameters scores log loss 0.3620 against 0.3401 optimized, so per-user optimization buys about 0.02 log loss, and the default configuration still beats every pre-FSRS-5 version, HLR at 0.4694 and DASH at 0.3682 [verified, same source].

The update forms come from the reference implementation and no other source: `src/model_v7.rs` in https://github.com/open-spaced-repetition/fsrs-rs, committed as a test fixture with its commit hash and digest (R28) [verified, that file at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae on 2026-09-19]. The awesome-fsrs wiki page named in earlier drafts documents only v0 to v6. The block below is the earlier draft's transcription and is superseded: its parameter indices do not match the shipped model (under the shipped vector the exponent it puts on `S` makes stability grow about 500-fold per review, and its difficulty step has the sign inverted), and the shipped model carries a second, fast stability and a two-component forgetting curve that the block does not show. It is kept only so the correction is legible; the implemented forms are the source's [verified, computed 2026-09-19, `app/engine/fsrs.py`]:

```
first observation:   S_k = S0(G) = w0 + (G - 1) * w1
                     D_k = D0(G)

successful recall:   S_k' = S_k * (exp(w6) * (11 - D_k) * S_k^w7
                                   * (exp(w8 * (1 - R_k)) - 1) + 1)
lapse:               S_k' = w9 * D_k^w10 * S_k^w11 * exp(w12 * (1 - R_k))
difficulty:          D_k' = w5 * D0(3) + (1 - w5) * (D_k + w4 * (G - 3))
```

The stability gain is larger when `R_k` was low at review time, which is the spacing effect written into the model and the reason review scheduling and mastery estimation can share one state.

Two departures from stock FSRS, both [inferred]. First, the unit is a skill, not a card, so one archetype attempt updates three to six stabilities at once; the benchmark covers nothing like this. Second, a propagated fractional credit performs a stability update scaled by its credit weight: a 0.3-weight propagated success applies the successful-recall form and then interpolates, `S_k_new = S_k + 0.3 * (S_k' - S_k)`. Neither has a source and both are listed as tunables.

### Prerequisite propagation

Propagation is Math Academy's Fractional Implicit Repetition applied to the authored graph [single-source, vendor-published, https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/ and https://www.mathacademy.com/how-our-ai-works]. Their interpretation of the weight is roughly the probability that a random problem on the advanced topic exercises the simpler one.

The independent warrant is the ALEKS retention result, which is the strongest evidence in the whole ledger for the idea that downstream practice is upstream review: over 6,701,233 students and 8,352,006 extra problems, retention curves conditioned on the inner layer of a learned item rise monotonically with layer depth, with layer 1 flattening near 0.6, layer 2 near 0.67, and layers 5 and above near 0.8 [verified, https://jmatayoshi.github.io/publications/JMP2021_KST_ALEKS_preprint.pdf]. Their own explanation is that deeper items are supported by later material that builds on them, which acts as retrieval practice.

Weights and hops, all [inferred]:

| Event | Target | Weight | Hops |
|---|---|---|---|
| Credited success on `k` | each `hard_prerequisite` ancestor | 0.3 of a success | 1 hop |
| Credited success on `k` | each `hard_prerequisite` ancestor | 0.09 of a success | 2 hops, then stop |
| Credited success on `k` | each `supporting` parent | 0.1 of a success | 1 hop only |
| Diagnosed `prerequisite_gap` naming `p` | `p` | 1.0 failure | direct |
| Diagnosed `prerequisite_gap` naming `p` | each `hard_prerequisite` dependant of `p` | 0.3 failure | 1 hop |

`co_requisite` edges, of which there are exactly 2 in the graph, propagate nothing and gate nothing. Two edges is too thin a basis for a rule, and the safe behaviour is to treat them as advisory metadata surfaced to the student rather than as engine input.

Propagated credit updates `c_k` or `f_k`, updates `S_k` and `D_k` by the scaled rule above, and sets `last_practised_at`. It does not touch `distinct_archetypes_succeeded`, `success_days`, `consecutive_successes` or `fading_stage`, because a fractional implicit repetition is not an unaided demonstration and must never on its own carry a skill to mastery. This is an invariant.

### Hypercorrection flag

A credited failure on an item where the student rated confidence `confident` sets `hypercorrection_due` to tomorrow for every skill the diagnosis marked worse than `mastered`, and the requeue overrides the FSRS due date. High-confidence errors are the most persistent and the most correctable once corrected [single-source, https://www.columbia.edu/cu/psychology/metcalfe/PDFs/ButterfieldMetcalfe2001.pdf; no effect size retrieved]. The 1 day gap is [inferred] and rests on Cepeda et al's lower bound rather than on hypercorrection research [verified, the spacing floor, https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf].

### Mastery declaration and un-mastery

Skill `k` is declared mastered when all of the following hold [inferred; combines the 3-on-3-days rule from track 1 with the distinct-archetype rule from track 2]:

1. `sigmoid(m_k) >= 0.9` at the current retrievability.
2. At least 3 credited unaided successes, meaning successes recorded at `fading_stage` equal to `unsupported`.
3. Those successes span at least 2 distinct archetypes, or every archetype that lists the skill when the active snapshot lists fewer than 2. Corrected 2026-09-19: 440 of the 522 skills that any active archetype lists sit in exactly one archetype, so the unconditional form made 84 percent of skills unmasterable, and gate 31 in [11-phased-delivery.md](11-phased-delivery.md) read 0 in both arms [verified, `data/archetypes.json`].
4. Those successes span at least 3 distinct calendar days.
5. The span between the first and last of those days is at least 7 days.
6. `R_k >= desired_retention(today)` at the moment of declaration, so a skill is never declared mastered while it is already due for review.

No same-day repeat counts toward conditions 4 or 5.

### Retrieval eligibility is not mastery (R8, fix 12)

Two quantities have used nearly the same words and they are different (fix 12). Retrieval eligibility is the point at which a skill joins the interleaved mixed-review pool in block 3 of session assembly: it enters after its **first** credited success at `fading_stage` equal to `unsupported`, which is the constant `RETRIEVAL_ENTRY = 1`. Mastery is the six-condition declaration above and still needs 3 credited unaided successes. The A/B in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) varies `RETRIEVAL_ENTRY` between 1 and 3 and does not touch the mastery rule; the tunables table below names the row `RETRIEVAL_ENTRY` accordingly, and the mastery corroboration rule keeps its own separate row.

Condition 1 uses 0.9 rather than the 0.95 that Corbett and Anderson's Cognitive Tutors use and that PFA's authors describe as current practice [verified, https://files.eric.ed.gov/fulltext/ED506305.pdf]. The 0.95 convention is tied to a binary latent state with an explicit guess parameter, which this model does not have, so importing the number without the model behind it would be false precision. The corroboration requirements in conditions 2 through 6 do the work that a higher threshold would do, and they do it in a way the student can be shown.

Conditions 4 and 5 come from the mastery-gating mechanic in [01-learning-model.md](01-learning-model.md), where mastery gating carries d = 0.4 to 0.6 in Kulik, Kulik and Bangert-Drowns 1990 [single-source, https://journals.sagepub.com/doi/10.3102/00346543060002265] and a median 0.66 for intelligent tutors that shrinks on standardized tests in Kulik and Fletcher 2016 [verified, https://journals.sagepub.com/doi/abs/10.3102/0034654315581420]. The shrinkage on standardized tests is why the measurement cadence in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) is against released AP material and not against internal scores.

Condition 3 exists because of the library's structure. With 510 of 541 skills never isolated by an archetype, a skill's estimate is identified only through variation in which archetypes are served, so demanding two archetypes is demanding that the estimate be identified at all [inferred].

Un-mastery fires when either `sigmoid(m_k)` falls below 0.75, or a credited failure occurs at `fading_stage` equal to `unsupported`. `mastered` flips false, `mastered_at` clears, and the skill re-enters the fringe. Un-mastery does **not** itself move `fading_stage` (R7); only the counter pair in the fading ladder below does, and a credited failure at `unsupported` is already one of the two failures that ladder counts. Nothing is erased: `c_k`, `f_k`, `distinct_archetypes_succeeded` and `success_days` persist, so re-mastery is faster than first mastery, which is the behaviour the forgetting curve implies.

### Fading ladder

`fading_stage` advances `example` to `completion` to `unsupported` on 2 consecutive credited successes and drops one level on 2 consecutive credited failures [inferred; the adaptive rather than fixed trigger is from Salden et al, http://www.cee.uma.pt/ron/Salden%20et%20al.%20-%20The%20Expertise%20Reversal%20Effect%20and%20Worked%20Examples.pdf, and backward fading is Renkl and Atkinson, https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6].

**Precedence: one counter pair, and only one (R7).** Three rules have been written in three documents as if each could move `fading_stage`: un-mastery dropping a level, "after two failed mastery attempts the ladder drops" in [01-learning-model.md](01-learning-model.md), and the two-consecutive-failures trigger here. They are not three rules. `consecutive_successes` and `consecutive_failures` are the only writers of `fading_stage`: 2 consecutive credited successes advance a stage, 2 consecutive credited failures drop one, and nothing else touches it. Un-mastery flips `mastered` and leaves the stage to the counters. The sentence in 01 is a restatement of the same counter and is reworded there to say so.

**`serve_stage` does not compete with the counters (R32).** `serve_stage` chooses the initial stage only, for a skill that has no credited observation yet, and it chooses it from the `p_A_knowledge` bands. Once one observation exists, `fading_stage` is whatever the counter pair last wrote, and `serve_stage` returns it unchanged. The band reading of "below `STAGE_LOW` is served at example or completion" therefore applies at first service only: below `STAGE_LOW` the initial stage is `example`, between the bands it is `completion`, above `STAGE_HIGH` it is `unsupported`. The earlier `min(stage_of(A, state), "completion")` form is withdrawn, because it could never return `example` and it overrode the counters after the first observation.

**The `example` skip condition, stated once (R32).** Stage `example` is skipped entirely, and the skill starts at `completion`, when every `hard_prerequisite` parent of the skill is mastered and the student's first attempt succeeds with confidence not rated `guess` [inferred]. This sentence is the only statement of the rule; 11-phased-delivery.md points here rather than restating it, and the phrase "confidence-corrected" is not part of it. This is the expertise reversal guard: instructional support that helps novices becomes redundant and then harmful as expertise grows, and a student who already holds every prerequisite is not a novice on this skill.

**Format and stage (R29).** The two dimensions do not interact freely. Stages `example` and `completion` are always short answer, because a worked example with a self-explanation prompt and a completion problem with a blanked step have no four-option form. Alternation between MCQ and MathLive short answer therefore applies only at stage `unsupported`, it alternates per attempt on one archetype for one user, and the first `unsupported` attempt on an archetype is short answer. Attempts at the other two stages neither consume nor advance the alternation.

## Decay

Retrievability `R_k` is the FSRS-7 forgetting curve evaluated at the elapsed time since `last_practised_at`. In FSRS 4.5 the curve is `R = (1 + (19/81) * t / S)^(-0.5)`; v6 makes the decay exponent trainable and v7 gives the curve 8 optimizable parameters and supports fractional intervals [verified, the version history, https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm]. The implementation uses the v7 curve with the default parameter vector.

`R_k` enters the engine in three places, and the decay term in `m_k` is not one of them while `lambda = 0` (R3): the review-due test that schedules block 1, mastery condition 6, and the displayed progress representation in [08-design-brief.md](08-design-brief.md), where progress is shown as a fading map rather than a completion bar precisely because the underlying quantity decays.

A skill is due for review when `R_k` falls below the desired retention. Desired retention is scheduled, not constant:

| Window | Desired retention | Source | Tag |
|---|---|---|---|
| Launch to 2027-03-15 | 0.90 | FSRS's own review-volume against retention trade-off, https://github.com/open-spaced-repetition/srs-benchmark | [verified, the trade-off direction, inferred for the value] |
| 2027-03-15 to exam day 2027-05-10 | 0.95 | same | [inferred, both the date and the value] |

Raising desired retention shortens intervals and raises review volume. Raising it eight weeks out concentrates review effort where it is worth most and accepts the volume cost when the terminal date is close. No source gives an optimal retention target for a fixed-deadline exam goal, so both the value and the switch date are tunables.

The exam date, Monday 10 May 2027, is [single-source] from `research/exam/exam-structure.md` and is the only date the schedule is anchored to. If that date is corrected, the switch date moves with it.

After a long gap the engine does not simply let `R_k` collapse and serve everything as due. Two behaviours fire. A gap over 21 days since the last session puts the next session into diagnostic mode rather than review mode [inferred], because after three weeks the model's per-skill estimates are extrapolations from a decay curve that was never validated on procedural mathematics and the cheaper fix is to re-measure. Within diagnostic mode the state is not reset; the diagnostic updates it. Separately, a skill whose `R_k` has fallen below 0.5 has its `fading_stage` capped at `completion` on its next encounter, so a long-decayed skill is re-entered with support rather than cold.

The honest caveat, repeated here because it is load-bearing and easily forgotten: every validated result behind FSRS is on declarative recall, vocabulary and flashcards. No benchmark validating FSRS, SM-2 or HLR on mathematical problem solving or procedural skills was found in this session [inferred from absence, not a claim that none exists]. The transfer is unvalidated and the offline simulation in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) is the only planned check on it.

## Prerequisite gating and the outer fringe

The outer fringe `F` is every active skill that is not mastered and whose `hard_prerequisite` parents are all mastered. This is knowledge space theory's rule, and it is free here because the graph is already authored and acyclic [verified, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf; inferred for the availability]. In a learning space the outer and inner fringes together determine the state, and for realistic school-mathematics structures the two fringes average about 11 items, with 9 items specifying a state of 80 in the worked example [verified, same source].

Edge semantics, and the behaviour each type buys:

**`hard_prerequisite`** (602 edges). Gating and conjunctive. An archetype whose primary skill has an unmastered hard prerequisite is never served outside diagnostic mode. Hard edges carry propagation at 0.3 and 0.09 per hop and they define the fringe. This is what the 602 edges are for.

**`supporting`** (622 edges). Neither gating nor conjunctive. A supporting edge means an observation on the child is weak evidence about the parent, nothing more. Supporting edges carry propagation at 0.1 for 1 hop and they enter item prediction compensatorily. Treating all 1226 edges alike would propagate false evidence across 622 edges whose semantics are explicitly weaker, which is the failure mode track 2 names for naive KST application [inferred].

**`co_requisite`** (2 edges). Inert in the engine, as described above.

**BC-PRQ handling.** The 77 non-calculus prerequisites are assumed mastered until a diagnosis says otherwise. They begin with `mastered` true, `mastered_at` set to the account creation timestamp, and `beta_k` set to a neutral 0.0 [inferred]. A diagnosed `prerequisite_gap` naming a BC-PRQ flips it to unmastered, which immediately removes from the fringe every skill that depends on it, and the fringe recomputation puts the BC-PRQ itself at the front of the queue. This is the only route by which a non-calculus prerequisite enters instruction, and it is the right one: spending diagnostic items probing algebra the student already has is a poor use of a 30-item budget, while a single diagnosed gap is strong evidence. The cold-start diagnostic probes BC-PRQ skills only indirectly, as described below.

**Seeded assumed-mastered parents outside a loaded subgraph (R15).** The same treatment extends to any parent that sits outside the subgraph a phase loads, which in P1 means 19 BC-PRQ and 6 BC-SKL (BC-SKL-01018, 01039, 01044, 02001, 02002, 03001), plus 4 BC-TOP parents that are inert per R13 and get no state at all. Each seeded row starts `beta_k = 0.0`, `c_k = f_k = 0`, `S_k` and `D_k` null, `fading_stage` `unsupported`, `mastered` true with `mastered_at` at account creation [inferred]. Those six BC-SKL are real skills that will be taught later, so the seed is flipped by a diagnosed gap or a credited failure exactly as a BC-PRQ seed is, and from that moment the skill is an ordinary skill with an ordinary history.

**`primary_skill(A)` (R25).** The primary skill of an archetype is the first entry of its `skills` array in `data/archetypes.json`. Nothing else defines it, no field is added to the library, and every use of the phrase "primary skill" in this document and in the phase plan means that first entry. Fringe membership, candidate selection, the interleaving window, invariants 3 and 12 and the P1 gating tests all read it this way.

Separately, and this is the point the earlier wording ran together (R25), the set of archetypes that a skill `k` contributes its difficulty prior from is **the archetypes that list `k` in their `skills` array**, not only those whose first entry is `k`. The `beta_k` formula in the Calibration plan below uses that wider set, which is the set the recorded pre-computation was run over.

### The conjunctive and compensatory split

Item-level prediction for archetype `A` loading skill set `K`:

```
K_hard  = { k in K : k is reachable from A's primary skill by hard_prerequisite edges }
K_soft  = K \ K_hard

p_hard  = product over k in K_hard of sigmoid(m_k)
p_soft  = sigmoid( sum over k in K_soft of m_k / |K_soft| )     when K_soft is non-empty
                 = 1                                            when K_soft is empty

p_A_knowledge = p_hard * p_soft
p_A_raw       = p_A_knowledge                       for free response
              = 0.25 + 0.75 * p_A_knowledge        for 4-option multiple choice (floor = 1 / option_count)
```

This split is the one place the design departs from every published model, and it is the plan's main modelling risk. It must be stated plainly.

Pavlik, Cen and Koedinger's published PFA handles multi-skill steps compensatorily, summing beta, gamma and rho contributions over all knowledge components, which lets strength in one component offset weakness in another [verified, https://files.eric.ed.gov/fulltext/ED506305.pdf]. They also name the alternative and its status: the knowledge-tracing workaround of multiplying per-skill probabilities has been explored but was not used for domain-model search [verified, same source]. So the conjunctive product is not new, and it is not validated either.

The domain argument for the split is that calculus items are frequently conjunctive in fact. A chain-rule item that also needs algebraic simplification fails if either sub-skill fails, and strength in one does not rescue the other. Pure compensation would predict that a student with a very strong chain rule and a weak algebraic manipulation still succeeds, which is not what happens.

The risk is threefold. First, nothing validates the mapping from edge type to functional form; the edge types were authored to describe curriculum structure, not to parameterise a likelihood. Second, 602 of 1226 edges are `hard_prerequisite` and the tags on those edges are themselves largely `inferred` in `data/prereq_edges.csv`, so an authoring judgement is being promoted to a modelling assumption. Third, a product over five or six sigmoids is aggressively pessimistic: five skills at 0.9 each predict 0.59, which will push the difficulty-targeting rule toward easier items than intended and may make the fringe feel stuck. The `|K_soft|` division in `p_soft` is a partial guard against the same problem on the soft side and is itself [inferred].

The mitigation is instrumentation, not cleverness. Every observation logs `p_A_raw`, the realised outcome, and the counterfactual prediction from a pure compensatory model over the whole skill set. Calibration of both is reported in the metrics dashboard in [10-quality-and-evaluation.md](10-quality-and-evaluation.md). If the pure compensatory model calibrates better over the first few hundred items, the split is dropped. Gervet et al's warning applies directly: models with similar predictive accuracy can make vastly different recommendations, citing Rollinson and Brunskill 2015 [verified, https://files.eric.ed.gov/fulltext/EJ1273917.pdf], so this is a decision to measure rather than to argue about.

## Item selection algorithm

Selection runs in four modes. Learning, review and diagnostic are specified here. Rehearsal, the timed mode, is specified in [05-assessment-modes.md](05-assessment-modes.md) and writes pacing metrics only, never mastery state, because speededness contaminates ability estimates [single-source]. Its graded errors still feed the diagnostician so the student gets feedback.

The learning-mode score is two terms, not five (R4). The argument is in the adversarial review and it is short: at cold start a conjunctive product over four to six sigmoids puts `p_A_knowledge` far below any plausible target for every candidate, so `1 - |p_A - TARGET_LEARN|` is nearly flat across the fringe, and half the score by weight carries no information. A flat term plus three small inferred terms is a round-robin with arithmetic on top. P1 and P2 therefore select on due coverage inside the fringe and break ties at random, which is a policy whose behaviour can be stated in one sentence and whose failure would be visible. The five-term score is not deleted; it is deferred, with a named gate, in the subsection after the pseudocode.

```
# ---------------------------------------------------------------------------
# Constants. Every value is [inferred] and listed as a tunable.
# ---------------------------------------------------------------------------
TARGET_LEARN       = 0.80     # knowledge-scale success target; in P1 and P2 this
                              # is a fading-stage filter, not a score term (R4)
STAGE_LOW          = 0.50     # p_A_knowledge below this: serve at example or
                              # completion stage
STAGE_HIGH         = 0.90     # p_A_knowledge above this: serve at unsupported
TARGET_DIAG_FR     = 0.50     # knowledge-scale informative target, free response
TARGET_DIAG_MCQ    = 0.625    # RAW target for 4-option MCQ = 0.5*0.75 + 0.25
RETRIEVAL_ENTRY    = 1        # credited unsupported successes before a skill
                              # joins the block 3 mixed-review pool (R8)
MAX_CONSECUTIVE    = 2        # items sharing a primary skill
MIN_SKILLS_PER_10  = 4
MIN_UNITS_PER_10   = 2        # applies once 2 units are open
MIN_TRANSLATION    = 0.20     # share of items that are BC-REP translation variants
PROBE_QUEUE_MAX    = 3        # pending_probes depth (R6)
PROBE_TTL_DAYS     = 7        # pending_probes expiry (R6)
DIAG_CAP           = 30
DIAG_MIN           = 10
GAP_DAYS_DIAGNOSTIC = 21

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
function outer_fringe(state):
    F = []
    for k in active_skills:                       # 541 BC-SKL
        if state[k].mastered: continue
        if k has no archetype: continue           # excludes BC-SKL-02001
        if k is a BC-TOP node: continue           # inert, R13
        parents = hard_prerequisite_parents(k)
        if every p in parents is mastered(state):  # BC-PRQ default true
            F.append(k)
    return F

function candidates(F):
    # primary_skill(A) is A.skills[0], the first entry of the archetype's
    # skills array (R25). An archetype is a candidate when its primary skill
    # is in F, every hard
    # prerequisite of that primary skill is mastered, and at least one
    # published item exists for it. An archetype with no published item is
    # excluded and logged as a coverage gap.
    out = []
    for A in active_archetypes:                   # 139 BC-QA
        if primary_skill(A) in F and has_published_item(A):
            out.append(A)
    return out

function drain_probe_queue(state, session_history):
    # R6, C18. The diagnostician writes recommended_probe here whenever its
    # top two misconception hypotheses sit within 0.2 of each other. Every
    # selection function calls this before its own scoring.
    expire_entries_older_than(state.pending_probes, PROBE_TTL_DAYS)
    if state.pending_probes is empty: return null
    probe = pop_front(state.pending_probes)
    A = archetype_for_probe(probe)
    if A is null or not has_published_item(A): return null
    return pick_variant(A, state, session_history)

function due_coverage(A, state):
    n = 0
    for k in A.skills:
        if state[k].mastered and R(state[k]) < desired_retention(today): n += 1
        for anc in hard_ancestors(k, hops = 1):
            if state[anc].mastered and R(state[anc]) < desired_retention(today): n += 1
    return n

function min_observations(A, state):
    return min(state[k].observation_count for k in A.skills)

function serve_stage(A, state):
    # TARGET_LEARN as a fading-stage filter rather than a score term (R4).
    # R32: the bands pick the INITIAL stage only. Once the skill has a
    # credited observation, fading_stage belongs to the R7 counter pair and
    # this function never overrides it.
    k = primary_skill(A)
    if state[k].observation_count > 0: return state[k].fading_stage
    p = p_A_knowledge(A, state)
    if p < STAGE_LOW:  return "example"
    if p > STAGE_HIGH: return "unsupported"
    return "completion"

# ---------------------------------------------------------------------------
# Learning mode, two-term score
# ---------------------------------------------------------------------------
function next_item_learning(state, session_history):
    probe = drain_probe_queue(state, session_history)
    if probe is not null: return probe            # R6: probes jump the queue

    F = outer_fringe(state)
    C = candidates(F)                             # term 1: fringe membership
    C = filter_interleaving(C, session_history)
    C = filter_calculator_policy(C, session_mode)
    if C is empty: return escalate_to_review_or_unblock(state)

    best_cover = max over A in C of due_coverage(A, state)   # term 2

    if best_cover == 0:
        # Nothing due anywhere in the fringe: choose uniformly at random.
        best = uniform_random_choice(C)
    else:
        ties = [A in C where due_coverage(A, state) == best_cover]
        best = uniform_random_choice(ties)        # uniform random on ties

    return pick_variant(best, state, session_history)

function pick_variant(A, state, session_history):
    # 395 BC-QV variants carry dimension and difficulty_effect. With no score
    # term to move p_A toward, the variant choice serves the translation floor
    # first and is otherwise uniform.
    V = variants_of(A)
    if translation_share(session_history) < MIN_TRANSLATION:
        V = prefer(V, dimension = "representation")
    return uniform_random_choice(V)

function filter_interleaving(C, session_history):
    # Rohrer et al 2020: no more than 2 consecutive same-skill items;
    # each block of 10 draws from at least 4 skills spanning at least 2 units.
    last2 = primary_skills(session_history[-2:])
    if len(last2) == 2 and last2[0] == last2[1]:
        C = [A in C where primary_skill(A) != last2[0]]

    block = session_history[-9:]
    if distinct_skills(block) < MIN_SKILLS_PER_10 - 1:
        C = [A in C where primary_skill(A) not in primary_skills(block)]
    if open_units(state) >= 2 and distinct_units(block) < MIN_UNITS_PER_10:
        C = [A in C where A.primary_unit not in units(block)]

    # Repetition compression guard: no archetype family may supply more than
    # 3 of any 10 consecutive items.
    C = [A in C where family_count(A.family, block) < 3]
    return C

# ---------------------------------------------------------------------------
# Review mode
# ---------------------------------------------------------------------------
function next_item_review(state, session_history):
    probe = drain_probe_queue(state, session_history)
    if probe is not null: return probe            # R6

    due = [k in active_skills where state[k].mastered
                               and R(state[k]) < desired_retention(today)]
    hyper = [k where state[k].hypercorrection_due <= today]
    if hyper is non-empty:
        # Hypercorrection overrides the FSRS order.
        return best_archetype_covering(hyper, state, session_history)
    if due is empty: return null                  # queue ends; session ends

    # Repetition compression: prefer the archetype covering the most due
    # skills, counting 1-hop hard ancestors that receive fractional credit.
    best = null; best_cover = -1
    C = filter_interleaving(archetypes_touching(due), session_history)
    # Do not serve an item the student is very likely to fail: a review
    # is a retrieval opportunity, not a fringe probe.
    eligible = [A in C where p_A_knowledge(A, state) >= 0.5]
    for A in eligible:
        cover = due_coverage(A, state)
        if cover > best_cover: best_cover = cover; best = A

    ties = [A in eligible where due_coverage(A, state) == best_cover]
    best = uniform_random_choice(ties)
    return pick_variant(best, state, session_history)

# ---------------------------------------------------------------------------
# Diagnostic mode
# ---------------------------------------------------------------------------
function next_item_diagnostic(state, asked, unit_posterior):
    probe = drain_probe_queue(state, asked)
    if probe is not null: return probe            # R6

    if len(asked) >= DIAG_CAP: return null
    if len(asked) >= DIAG_MIN and entropy_stalled(unit_posterior): return null

    # Whole graph, not the fringe. Gating is suspended here by design.
    C = [A in active_archetypes where A not in asked_families(asked)]
    C = pool_by_unit(C, unit_posterior)           # at most 4 per unit before
                                                  # every unit has been probed

    best = null; best_dist = infinity
    for A in C:
        if A.calculator_status == "calculator" and not calculator_available:
            continue
        p_raw = raw_probability(A, state)
        target = TARGET_DIAG_MCQ if is_mcq(A) else TARGET_DIAG_FR
        d = abs(p_raw - target)
        if d < best_dist: best_dist = d; best = A

    # ALEKS breaks ties at random; do the same, then log the draw.
    ties = [A in C where abs(raw_probability(A, state) - target_for(A)) <= best_dist + 0.01]
    return uniform_random_choice(ties)
```

Notes on the selection rules that the pseudocode cannot carry.

Due coverage is the one scoring term because spaced retrieval is the second-ranked mechanic in [01-learning-model.md](01-learning-model.md) and it costs zero extra minutes, being a reordering of work the student was doing anyway [verified, Adesope et al 2017 g = 0.51 against restudy, https://journals.sagepub.com/doi/abs/10.3102/0034654316689306]. Repetition compression is what makes it worth scoring on at all: with 3 to 6 skills per archetype and 1-hop hard ancestors counted, a single well-chosen item can discharge six or more due reviews. The idea is Math Academy's [single-source] with the ALEKS layer-depth retention curves as independent corroboration of the mechanism [verified].

Uniform random within the fringe on a tie, and on the no-due case, is a choice and not a default. With only 31 independently assessable skills, per-skill estimates are identified only through variation in which archetypes are served, and a deterministic tie-break on minimum observation count is a round-robin that produces the least variation available [inferred, track 2]. Randomising also keeps the live policy comparable with the random-fringe control arm in [10-quality-and-evaluation.md](10-quality-and-evaluation.md), because in P1 and P2 the treatment and the control differ in exactly one term.

`TARGET_LEARN` at 0.8 survives as the fading-stage filter in `serve_stage` rather than as a score term (R4). Two sources bracket the value and neither licenses more precision. Math Academy states quizzes are tuned so students score about 80 percent on average [single-source, vendor-published, https://www.mathacademy.com/how-our-ai-works]. Wilson, Shenhav, Straccia and Cohen derive an optimal training error rate of about 15.87 percent, so accuracy about 85 percent, for binary classification learned by stochastic gradient descent under Gaussian decision noise, and state explicitly that the optimum moves to 82 percent for Laplacian and 75 percent for Cauchy noise and that the result "remains to be generalized" to multi-choice tasks and other learning algorithms [verified, https://www.nature.com/articles/s41467-019-12552-4]. Taking 85 percent as an educational constant would be a misreading of a paper that disclaims exactly that. As a stage filter the number has to carry much less weight than it did as half of a score: it decides whether a candidate arrives with a worked example or without one, and being wrong by 0.05 changes support, not what is taught.

Four things stay hard constraints on the assembled set rather than terms in any score, and they are unaffected by the two-term simplification: the interleaving window in `filter_interleaving`, the 20 percent translation floor [inferred share; the requirement itself follows from the exam testing translation between representations and from the CED's Connecting Representations practice at 15 to 30 percent of the multiple-choice section, verified in `research/exam/exam-blueprint.md`], the hypercorrection requeue, and probe injection (R6). A constraint that must hold cannot be a weighted preference, which is the general reason none of the four is expressed as a term.

### Deferred until P7 shows it beats the two-term score

Nothing below is implemented in P1 or P2. It may be turned on only after the simulation in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) shows the five-term score beating the **two-term** score on true mastery per item served, not merely beating random selection within the fringe (R4).

The deferred score, with its constants:

```
W_LEARN   = 0.50   # closeness to TARGET_LEARN on the guessing-corrected scale
W_DUE     = 0.25   # due reviews the item would cover
W_COV     = 0.10   # coverage of under-observed skills
W_WEIGHT  = 0.10   # exam unit weight prior
W_REP     = 0.05   # representation gap
EXPLORE_SHARE = 0.125   # random-within-fringe share, band 0.10 to 0.15

s(A) = W_LEARN  * (1 - abs(p_A_knowledge(A, state) - TARGET_LEARN))
     + W_DUE    * normalise(due_coverage(A, state))
     + W_COV    * (1 / (1 + min_observations(A, state)))
     + W_WEIGHT * exam_weight(A.primary_unit)
     + W_REP    * representation_gap(A, session_history)

# Coverage tie-break: among archetypes within 0.02 of the best score,
# take the one whose least-observed skill has the lowest count.
```

`exam_weight` is the midpoint of the published BC multiple-choice band from `research/exam/exam-blueprint.md`, renormalised over the 10 units: BC-UNIT-06 and BC-UNIT-10 at 15 to 20 percent, BC-UNIT-05 and BC-UNIT-09 at 10 to 15 percent, the remaining six units at 5 to 10 percent [verified, `research/exam/exam-blueprint.md`, BC-SRC-ced p.199]. It is deliberately small, because the bands are ranges, no unit weighting is published for the free-response section at all, and a prior that overwhelms the mastery signal would have the engine teaching series to a student who cannot differentiate. `representation_gap` scores the share of BC-REP ids on an archetype that the student has seen least often.

`EXPLORE_SHARE` belongs to this subsection too, because an exploration arm exists to correct a bias that score-based selection introduces. Adaptive selection breaks naive difficulty estimation, which Pelanek demonstrates by simulation and Gervet et al flag as a general hazard of learning from self-selected data [verified, https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf and https://files.eric.ed.gov/fulltext/EJ1273917.pdf]. Under the two-term score with random tie-breaking, selection is already substantially random within the fringe, so the exploration arm is held at 0 until the five-term score is turned on, and it returns with it. The feedback-loop bias check in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) compares against the simulated random-fringe arm in the meantime.

## Session assembly

Four documents cite "D3, session shape" as a specified rule and none contained it. It is an engine rule and it belongs here (R5).

A session is four blocks, assembled in order. Nothing in it is a schedule, a plan or a target for the student; it is the order in which the selection functions above are called, and the minute figures are a forecast used to decide how many items to assemble, never shown as a goal.

**Block 1, due reviews.** `next_item_review` until either 5 items have been served or 5 minutes of forecast have been assembled, whichever comes first. Hypercorrection requeues are served here and override the FSRS order.

**Block 2, fringe learning.** `next_item_learning` until 25 minutes of forecast have been assembled or the fringe is exhausted. A pending discriminating probe is served first in this block, ahead of any fringe candidate (R6). The productive-failure opener, when one is due, is the first ordinary item of the block.

**Block 3, interleaved mixed review.** Drawn from skills observed at least once and eligible under `RETRIEVAL_ENTRY` (R8), 10 to 15 minutes of forecast. This is the block the interleaving window in `filter_interleaving` matters most in, because it is the only block whose pool spans units.

**Block 4, calibration and error notes.** The confidence-calibration prompts and the one-line student-authored error note for each item corrected in this session. No items are served, so no mastery state is written.

**Minute forecast.** The forecast for an archetype is its running median attempt time, and 3 minutes per item until at least 5 attempts on that archetype exist [inferred]. The forecast is an assembly input only. It is never a countdown, never a quota and never displayed as a target, per the presentation rule in [08-design-brief.md](08-design-brief.md).

**Stop condition.** The session ends when all four blocks are empty. There is no timer and no item count. A student who finishes the due queue early finishes early; block sizes are caps on assembly, not floors on work.

**Productive-failure opener.** `concept_opener_done` is an integer flag stored in `skills_state` on the first skill of each BC-CON. The first time any skill of a flagged concept enters the fringe, block 2 opens with the generation attempt for that concept, then sets the flag. The attempt writes no mastery credit, which is what makes it a productive failure rather than a graded item, and the flag guarantees it happens at most once per concept. This closes the traceability break where [01-learning-model.md](01-learning-model.md) named a flag that existed in no schema.

## Cold-start diagnostic design

The diagnostic runs at first login and after any gap exceeding 21 days. It suspends prerequisite gating, which is the only place in the engine that does.

**The 30-item cap.** ALEKS caps its initial assessment at 30 questions, of which 29 are adaptive and 1 is a randomly chosen extra problem whose answer is excluded from inference and used only for evaluation. Their justification is combinatorial: a 314-item College Placement course has about 10^23 feasible states against 2^314 subsets, and even halving the state space per question would need 77 questions in the worst case, so the assessment accepts an underestimate of the state [verified, https://jmatayoshi.github.io/publications/JMP2021_KST_ALEKS_preprint.pdf]. The empirical justification is stronger: across 2,688,472 full-length College Placement assessments, AUROC, point biserial and accuracy converge early, "with the changes being minimal after question 10" [verified, same source]. Assessment quality at full length reached AUROC 0.875 on Sixth-Grade Math (N = 162,900), 0.863 on College Algebra (N = 174,073) and 0.889 on College Placement (N = 2,775,432) [verified, same source].

This engine copies the cap and the extra-problem device. 30 items maximum, of which 1 is drawn at random from the whole active archetype set, excluded from inference, and logged as the held-out evaluation item. 541 skills will not be resolved by 30 items and the design does not pretend otherwise.

**Unit-level pooling.** Because the item budget cannot resolve skills, the diagnostic's posterior is over unit-level states, not skill-level ones. Each of the 10 units carries a coarse state in `not_started`, `partial`, `fluent`, and the selection targets the item that most reduces entropy over that 10-dimensional posterior. Skill-level state is then seeded from the unit posterior plus whatever skill-level evidence the 29 scored items produced through the normal credit and propagation rules. Pooling at most 4 items per unit before every unit has been probed guarantees coverage of all 10 units within the first 30 items [inferred].

**Informative targets.** ALEKS selects the item whose probability of being known is closest to 0.5 under the current likelihood distribution, with ties broken at random [verified]. That target is correct for their open-response format, where they state lucky guesses are negligible [verified]. For a four-option multiple-choice archetype the equivalent raw target is 0.625 [inferred], derived as `0.5 * 0.75 + 0.25`. Free-response archetypes use 0.5 directly.

**Stopping rule.** Stop at 30 items, or earlier when at least 10 items have been asked and the entropy of the unit-level posterior has not fallen by more than 0.02 bits over the last 3 items [inferred; the "stop when entropy is low and nothing informative remains" shape is ALEKS's, verified, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf]. The 10-item floor is the ALEKS convergence result read as a minimum rather than as a target.

**What is left `not_attempted`.** Every skill the diagnostic does not resolve keeps `mastered` false, `c_k` and `f_k` at 0, and `observation_count` at 0. ALEKS classifies items in-state above about 80 percent likelihood and out-of-state below about 20 percent, and items left uncertain are excluded from the state and fast-tracked in learning [verified, https://jmatayoshi.github.io/publications/JMP2021_KST_ALEKS_preprint.pdf]. This engine does the same: an unresolved skill is treated as unmastered for gating, so it sits in the outer fringe as soon as its hard prerequisites are mastered and is as likely to be drawn as any other fringe candidate. Under the two-term score fast-tracking is a consequence of fringe membership plus uniform random choice rather than a separate mechanism; under the deferred five-term score the `W_COV` term would additionally bias toward it through `1 / (1 + observation_count)`, which at count 0 is its maximum.

A caution that must be carried into the interface: ALEKS is explicit that its own in-state and out-of-state classifications "are not well-calibrated" [verified, same source]. A binary mastered label from a 30-item diagnostic must never be presented as a probability, which is the design constraint behind showing a fading map rather than a percentage in [08-design-brief.md](08-design-brief.md).

**How BC-PRQ non-calculus prerequisites are probed.** They are not probed directly. All 77 begin mastered, and the diagnostic spends none of its 30 items on algebra, trigonometry or function notation in isolation. The probe is indirect and comes for free: diagnostic items are ordinary archetypes, archetypes carry a `prerequisites` list of BC-PRQ ids (BC-QA-06001 carries BC-PRQ-06005, BC-PRQ-06008 and BC-PRQ-06012), and the diagnostician traces a `prerequisite_gap` hypothesis through `prereq_edges` using the `adaptive.prerequisite_gap_if` text on the loaded skills. A diagnosed BC-PRQ gap flips that prerequisite to unmastered, which removes its dependants from the fringe and puts the prerequisite itself at the head of the learning queue.

The cost of this choice is that a broad, quiet weakness in algebraic manipulation will surface slowly, over several diagnosed gaps rather than in one probe. The alternative rejected is a separate pre-diagnostic over the 77 BC-PRQ skills. It was rejected on learning impact first: it spends the student's scarcest resource, minutes, measuring things a BC student very probably has, and the 30-item ALEKS evidence says measurement returns flatten fast. It was rejected on cost second: 77 extra items is more than twice the entire diagnostic budget. If the diagnosed-gap rate on BC-PRQ skills exceeds a threshold in the first month, the decision is revisited in [12-open-questions.md](12-open-questions.md).

## Calibration plan for item difficulty

`beta_k` is declared, not learned. The floor is explicit in the literature: "the system needs at least 100 students to get good estimates of item difficulty" [verified, Pelanek, https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf]. Pelanek, citing Wauters et al 2012, reports that with 200 students the data-driven methods (proportion correct, IRT, Elo, human judgment) give reliable and highly correlated estimates, and that even plain proportion-correct does well [verified, same source]. With one learner none of that is reachable, and worse, Pelanek's simulation shows proportion-correct is a good difficulty estimator only under random item selection and fails under adaptive selection [verified], so the one estimator cheap enough to run is also the one this engine's own policy would corrupt.

**The declared prior.** For a skill `k`, take the archetypes that list `k` in their `skills` array (R25), count the BC-DF difficulty factors on each, average the counts, and set

```
beta_k = -0.35 * (mean_BC_DF_count(archetypes that list k in their skills array) - 2)
```

The earlier phrase "primary archetypes of `k`" and the restriction to "primary loaded skills" are withdrawn: they were never defined, and the pre-computation recorded below was run over every archetype that lists `k` (R25).

[inferred; the 0.35 coefficient stays tunable]. The subtraction of 2 is the correction made in R1 and it is the whole of the difference from the earlier uncentred form. 2 is the median BC-DF count across the 139 active archetypes, whose distribution is 1 on 32 archetypes, 2 on 40, 3 on 34, 4 on 23, 5 on 6, 6 on 3 and 7 on 1, computed from `data/archetypes.json` on 2026-09-19. Centring on the median means a median-difficulty unobserved skill starts at `beta_k = 0`, hence `m_k = 0` and `p = 0.5`, and the prior expresses relative difficulty rather than uniform pessimism.

The uncentred form was not merely pessimistic, it was structurally broken under the conjunctive rule. BC-QA-06001 carries 7 BC-DF factors (BC-DF-01, 03, 05, 10, 14, 15, 16), which under the old formula gave `beta = -2.45` and a base success probability near 0.08 for a skill whose only primary archetype is that one. A conjunctive product over four such skills predicts on the order of 1e-4, at which point every candidate's predicted success probability is indistinguishable from every other's and any score term built on that probability carries no information. Centred, the same archetype gives `beta = -1.75` and the spread across archetypes lands on both sides of 0.5, which is the condition a difficulty target needs in order to discriminate at all.

**The P1 cold-start gate (R1, fix 1).** Before P1 merges, `p_A_knowledge` is computed for all 139 archetypes at the cold-start state under the centred prior and the conjunctive product, and the distribution is published. If the 90th percentile of that distribution is below 0.3, the 0.35 coefficient and `TARGET_LEARN` are recalibrated together before any student sees an item. The gate is carried in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) and in [11-phased-delivery.md](11-phased-delivery.md). It costs an afternoon and it is the only check that catches the failure before the student pays for it.

**Pre-computation of the gate (2026-09-19, from `data/`, before any code exists) [verified, computed; the reading of the rule is inferred].** With `beta_k = -0.35 * (mean BC-DF count - 2)` over each skill's archetypes and `m_k = beta_k` for every unobserved skill, three prediction rules were evaluated over all 139 active archetypes. Conjunctive over hard-linked skills and compensatory (mean logit) over the rest, where hard-linked means a loaded skill that is a `hard_prerequisite` of the archetype's first-listed skill: p10 0.250, p50 0.456, p90 0.587, min 0.071. Pure compensatory: p10 0.332, p50 0.471, p90 0.587. Pure conjunctive over every loaded skill: p10 0.002, p50 0.031, p90 0.207. Only 15 of 139 archetypes load a hard prerequisite of their own primary skill, so the split rule rarely bites and the gate passes (p90 0.587 is above 0.3). A pure conjunctive product over all loaded skills would fail the gate, which is why the split, not the product, is the rule. Per-skill `beta_k` ranges from -1.75 to 0.35 with median 0.00. The gate still runs against the implemented engine before P1 merges; this pre-computation only shows the prior is not degenerate on paper. These recorded percentiles reproduce only under the reading where the primary skill sits in the compensatory mean, not in the conjunctive product; with the primary skill in the product the 90th percentile is 0.344 [verified, computed 2026-09-19].

The 17 BC-DF factors carry no numeric weights in `data/taxonomies.json`, so every factor counts 1. That is a known library gap, recorded as gap (i) in the decisions memo and carried to [12-open-questions.md](12-open-questions.md). Weighting BC-DF-06 (algebraic burden) equal to BC-DF-16 (units and labelling demand) is certainly wrong; nothing in the library says by how much.

36 active archetypes have no `official_examples`, so their difficulty priors rest on BC-DF counts alone with no anchor to observed exam behaviour. Those archetypes are flagged in the content snapshot and their `beta` estimates carry a wider uncertainty band in the metrics dashboard.

**Variant adjustment.** The 395 BC-QV variants carry `difficulty_effect` in `harder`, `easier`, `neutral`. A variant shifts the effective item difficulty by a fixed 0.4 logits in the named direction [inferred, tunable]. This is the only difficulty lever the selection algorithm can pull within an archetype and it is how `pick_variant` moves `p_A` toward the target.

**Within-archetype variance, decided 2026-09-20 [inferred].** Instantiations of one item template do not share a difficulty: the sources in `13-ai-engineering.md` under Radicals and incidentals report a facility spread above 0.15 across variants on 20 of 50 item models, and that ignoring the within-family variance biases ability estimates toward the centre. The prior above does not gain a variance term. It accepts that centre-ward bias on generated items, because a term set with no per-instantiation data would be a second guessed parameter, and the template gate instead checks that a parameter declared incidental leaves the solution path's structure fixed. The measurement that adds the term: first-attempt accuracy per template segmented by instantiation, once a template has 30 or more attempts over at least 5 instantiations; a spread above 0.15 adds the term for that template with the measured spread as its first value.

**Why not learned, restated as a decision.** Learning `beta` from one learner's responses would, by Pelanek's own simulation, produce estimates that are artifacts of the selection policy rather than properties of the items, and the engine would then select on its own artifacts. The learning-impact argument comes first: a corrupted difficulty estimate moves the difficulty target away from the band where learning happens, which directly wastes minutes. The cost argument is secondary and points the same way, since an online Elo update is cheap to build. The convenience argument does not enter. The alternative rejected is item-side Elo with an uncertainty function `U(n) = a / (1 + b n)`, `a = 1`, `b = 0.05`, which is Pelanek's own recommended starting point [verified, same source]. It is rejected only for the item side; the learner side of Elo is effectively what PFA's counts already do here.

**Revisiting once 100+ learners exist.** The multi-user path in [11-phased-delivery.md](11-phased-delivery.md) phase P8 is the trigger. At 100 distinct learners with responses, run item-side Elo with the item K set free and the declared `beta` as the initial rating, which is exactly the "add a new item by setting its difficulty and letting the data find it" property Pelanek describes [verified]. Compare the learned difficulties against the declared ones by rank correlation, and publish the residual against BC-DF count, which is the first empirical evidence the library could ever get about BC-DF weights. Until then, item ratings stay frozen: this is Elo with the item K set to 0.

**Drift monitoring.** Generated items are not the archetype; they are draws from a parameter family, and a generator prompt revision can shift the family's real difficulty without any registry change. Three monitors run continuously:

1. Per-archetype first-attempt accuracy against the model's own `p_A_raw`, reported as a calibration residual. A persistent residual above 0.15 on an archetype with at least 10 observations flags it for review. Both numbers are [inferred] (N14): no source gives a residual threshold for a declared-difficulty prior, and 10 observations is a floor chosen so the residual is not dominated by a single item. What would settle them is the observed residual distribution across archetypes once a few hundred first attempts exist; until then the threshold is a trigger for a look, not a gate.
2. Per-archetype accuracy segmented by generator prompt version, which is logged per item under the provenance rules in [04-item-generation.md](04-item-generation.md). A step change at a prompt-version boundary is drift, not learning.
3. The held-out diagnostic extra problem, one per diagnostic run, whose predicted-versus-observed agreement is the only genuinely unbiased calibration point the system produces, because it alone is selected outside the adaptive policy. ALEKS uses the same device and reports predicted-versus-observed answer correlation in Beginning Algebra "hovers between .7 and .8" [verified, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf], which is the target to beat, not to expect.

## Unit-testable invariants

Each invariant names the exact property and a one-line test. The property-based test harness is specified in [10-quality-and-evaluation.md](10-quality-and-evaluation.md).

The list is renumbered as of this revision: invariant 6 is new (R2) and every invariant from the old 6 onward has moved up by one. The phase gates in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) cite the new numbers.

1. **The prerequisite graph is acyclic.** Loading `data/prereq_edges.csv` produces a DAG over the union of BC-SKL, BC-PRQ and BC-TOP ids, the last of which are loaded and held inert per R13. Test: topological sort the loaded graph on the real `data/` directory and assert it succeeds and consumes all 1226 edges, including the 48 that touch a BC-TOP id.
2. **No dangling references.** Every `from` and `to` in `prereq_edges.csv`, every id in `archetypes.skills`, and every BC-SIG `skill` and `archetype` resolves to a loaded record. Test: loader raises on a fixture with one mutated id, and raises nothing on the real directory.
3. **Gating holds outside diagnostic mode.** For any served archetype in learning, review or rehearsal mode, every `hard_prerequisite` parent of its primary skill is mastered. Test: run 10,000 simulated selections against a random mastery state and assert the property on every served item.
4. **Correct answers never lower strength.** For any state and any observation whose `mastery_state` is `mastered`, `m_k` after the update is greater than or equal to `m_k` before, holding the clock fixed. Test: property test over random `(c_k, f_k, S_k, D_k)` draws, asserting monotonicity. This is the direct analogue of the BKT degeneracy condition `P(G) + P(S) < 1`, where violating it inverts the update so that correct answers reduce estimated mastery [verified, https://files.eric.ed.gov/fulltext/EJ1115329.pdf].
5. **Failures never raise strength.** Symmetric to 4 for `not_mastered`. Test: same property harness, opposite direction.
6. **Partial observations never raise strength (R2).** For any state and any observation whose `mastery_state` is `partial_procedural`, `partial_conceptual` or `partial_unspecified`, `m_k` after the update is less than or equal to `m_k` before, holding the clock fixed. Test: property test over random `(c_k, f_k)` draws for all three partial states, asserting the inequality holds for every `(gamma, rho)` pair the tunables table permits, so that a future weight change cannot silently reopen the ratchet.
7. **Mastery requires every D2 condition.** `mastered` is true only when all six conditions hold simultaneously. Test: six tests, each constructing a state that satisfies five conditions and violates one, asserting `mastered` is false.
8. **Propagated credit cannot cause mastery.** A sequence of observations in which a skill receives only propagated credit never sets `mastered` true for that skill. Test: simulate 500 successes on every descendant of a target skill and assert the target is not mastered.
9. **Retrievability is monotone decreasing between observations.** For fixed `S_k` and `D_k`, `R_k(t2) <= R_k(t1)` for `t2 > t1`, and `R_k = 1` for a skill with null `S_k` (R1). Test: property test over random stabilities and increasing time grids, plus the null case.
10. **Stability never decreases on a success and never increases on a lapse.** Test: property test over the FSRS-7 default parameter vector with random `(S, D, R)` draws in range.
11. **Multiple-choice credit is capped.** No single observation on a four-option multiple-choice item credits more than 0.75 to any `c_k`. Test: assert on the credit function across every `mastery_state` value.
12. **Interleaving constraints hold on every non-diagnostic set.** In any window of 10 consecutive served items: no more than 2 consecutive share a primary skill; at least 4 distinct primary skills appear; at least 2 distinct units appear once 2 units are open; no archetype family supplies more than 3. Test: generate 200 simulated sessions and assert all four on every sliding window.
13. **The translation floor holds.** At least 20 percent of items in any completed session of 10 or more items are BC-REP translation variants. Test: assert over the same 200 simulated sessions.
14. **Exploration share matches the selection regime.** While the two-term score is in force, `EXPLORE_SHARE` is 0 and no selection is drawn outside the two-term rule, because that rule is already random within the tied set (R4). If the five-term score is turned on, the random-within-fringe share over 1,000 selections lies in [0.08, 0.17]. Test: seeded run with a fixed RNG under each regime, asserting the corresponding property.
15. **The diagnostic respects its cap and floor.** No diagnostic run exceeds 30 items, none stops before 10 unless the candidate pool is exhausted, and exactly one item per run is the held-out extra problem excluded from inference. Test: 1,000 simulated diagnostics against random hidden states.
16. **The diagnostic covers all 10 units.** Every completed 30-item diagnostic asks at least one item from each of the 10 units. Test: same simulation, assert unit coverage.
17. **Rehearsal mode does not write mastery state.** After any rehearsal session, `c_k`, `f_k`, `S_k`, `D_k`, `mastered` and `fading_stage` are unchanged for every skill. Test: snapshot the full `skills_state` table before and after a simulated timed part drill and assert equality.
18. **Un-mastery is reachable, lossless and does not move the stage (R7).** When `sigmoid(m_k)` crosses below 0.75, `mastered` flips false, `mastered_at` clears, `fading_stage` is unchanged by the un-mastery itself, and `c_k`, `f_k`, `distinct_archetypes_succeeded` and `success_days` are preserved. Test: drive a mastered skill forward in time until the threshold is crossed and assert all five, including that the stage moved only if the consecutive-failure counter moved it.
19. **BC-PRQ defaults and flips.** All 77 BC-PRQ skills start mastered; a single diagnosed `prerequisite_gap` naming one flips it and removes every dependant from the fringe within one recomputation. Test: assert on the loaded graph for each of the 77.
20. **`BC-SKL-02001` is never selected.** The skill with no archetype never appears as a selection target in any mode. Test: 10,000 simulated selections across all modes, assert absence.
21. **`co_requisite` and BC-TOP edges are inert (R13).** Removing the 2 `co_requisite` edges and the 48 BC-TOP edges from the loaded graph changes no fringe, no propagation result and no selection. Test: run the same seeded 1,000-selection trace with and without those edges and assert identical output, and assert no BC-TOP id ever appears in a fringe or as a propagation target.
22. **Item prediction is bounded and ordered.** `p_A_raw` lies in [0, 1] for every archetype and every state, and lies in [0.25, 1.0] for every four-option multiple-choice archetype. Test: property test over random states across all 139 archetypes.
23. **The conjunctive counterfactual is always logged.** Every observation record carries both the split-model prediction and the pure compensatory prediction. Test: assert both fields are non-null on every row written by a simulated 200-session run.

## Comparison table of the alternatives

Columns are track 2's. Every cell is sourced in `track2-adaptive-engines.md` and the key numbers are repeated here with their tags.

| Model | Cold-start fitness | Multi-skill item handling | Forgetting and decay | Interpretability | Data needs | Implementation cost | Evidence strength |
|---|---|---|---|---|---|---|---|
| BKT (classic) | Fair; runtime is parameter-driven, but 541 x 4 = 2164 parameters must be hand-set [inferred] | None natively; the conjunctive product is a patch that Pavlik et al note was explored but not used for domain-model search [verified] | None; the knowledge bit cannot go 1 back to 0 [verified] | High; four psychologically named parameters | Low at runtime, high to fit | Low | Long-standing but last in every head-to-head fetched: AUC 0.621 on algebra05 [verified] |
| BKT + forgetting + ability | Fair | Still single-skill | Yes, and forgetting is the single most valuable extension on Assistments, recovering 50.6 percent of the reported DKT gap [verified] | High | Moderate | Moderate | Strong: BKT+FSA reaches 0.90 on Assistments, 0.75 on Statics against DKT 0.76 [verified] |
| PFA / AFM | Good; at `s = f = 0` the prediction reduces to declared difficulty [verified, the construction] | Native, compensatory sum over knowledge components [verified] | None [verified from the equation] | High; per-skill easiness, success weight, failure weight | Moderate | Low | Good; AUC 0.769 on algebra05, beaten by Best-LR [verified] |
| Best-LR (PFA + IRT + log counts) | Good, same reason | Native, compensatory | Only via time-window features, which "add no predictive power to logistic regression models" [verified] | High | Moderate | Low to moderate | Strongest classical result fetched: AUC 0.831 on algebra05, best on the small datasets [verified] |
| DKT / SAKT / AKT | Unusable; output before training is noise | Implicit and uninterpretable | Implicit | Very low | Very high; "severely overfit" on the three smallest datasets, the smallest of which had 574 learners and 607,025 interactions [verified] | High | Contested; 31.6 percent of the reported BKT gap was a biased AUC computation [verified] |
| IRT 1PL / 2PL / 3PL | Good on the learner side if item difficulty is declared | None natively | None; assumes constant skill [verified] | High | High for calibrated item parameters | Low to moderate | Very strong psychometrically; AUC 0.768 alone on algebra05 [verified]; matched or beat DKT across Wilson et al's datasets [verified] |
| Elo / Glicko | Good on the learner side, unusable on the item side with one learner | None natively | Only via ad hoc decay variants | High | At least 100 students for item difficulty [verified] | Very low | Good, but Pelanek scopes it away from prerequisite domains explicitly [verified] |
| FSRS alone | Very good; defaults cost about 0.02 log loss against per-user optimization [verified] | None; the unit is a card | Native and best in class | Moderate; D, S and R are named but 34 parameters are not | Low with defaults | Moderate | Very strong on 349,923,850 reviews, unvalidated for mathematical problem solving [inferred from absence] |
| Knowledge space theory | Excellent; the structure is authored, not learned | Native via state membership | None natively | Very high; fringes are directly explainable | None for the structure, a great deal to validate it | High if full, low if reduced to fringe rules | Strong at scale: AUROC 0.863 to 0.889 over millions of assessments [verified] |

### Rationale for the chosen combination

The chosen model is a prerequisite-propagating PFA with an FSRS-7 decay term, selected at the fringe. It takes one property from each of three families and rejects each family's ontology.

From PFA it takes the likelihood shape, because 510 of 541 skills are never isolated by an archetype and PFA is the only classical model in the set designed for the multi-skill case [verified that multi-skill handling is PFA's stated advantage over knowledge tracing]. A model that assumes one skill per opportunity cannot represent 94 percent of this library's observations.

From knowledge space theory it takes the fringe rule and the informative-target rule, and nothing else. The full Bayesian filter over feasible states is not buildable here: ALEKS's own courses run to about 10^23 states and their inference runs over a compact structural representation [verified]. The two rules are free because the 1226-edge graph is already authored and acyclic. This is the largest single asset the project has, because a hard_prerequisite edge makes every observation evidence about more than one skill and so multiplies the effective sample size of a single learner's answers [inferred].

From FSRS it takes the decay term, and only the decay term. This is the one place where the tempting shortcut had to be refused explicitly. Treating each of the 541 skills as an Anki card would be cheap, it has the best cold-start story in the survey, and its evidence base is the largest by orders of magnitude. It is rejected on learning impact: FSRS models the decay of an already-formed memory and has no representation of a skill not yet acquired, of a prerequisite, or of partial credit across the 3 to 6 skills an archetype loads [verified, the unit, inferred for the consequence]. Its entire validated domain is declarative recall. And the benchmark supplies its own sobering context: MOVING-AVG, a zero-parameter recency baseline, beats FSRS-7 on log loss, 0.3369 against 0.3401 [verified, https://github.com/open-spaced-repetition/srs-benchmark], so decay-model sophistication is not where the leverage is. The leverage is in the graph, which FSRS cannot see.

The families rejected outright. Deep knowledge tracing is rejected because the smallest dataset on which it was competitive had 574 learners and 607,025 interactions and even there it lost to logistic regression [verified], and because it produces no interpretable per-skill number, which breaks prerequisite gating, the student-facing explanation, and the mapping to 711 BC-SIG records [inferred]. Classic BKT is rejected for the 2164 hand-set parameters, for the degeneracy constraints `P(G) + P(S) < 1` and `P(T) < 1 - P(S)/(1 - P(G))` that must hold for every one of them [verified], for a binary latent state that cannot express eight mastery_state values, and for AUC 0.621 against 0.831 in the one head-to-head [verified]. Item-side Elo and calibrated IRT are rejected only on the item side, for the 100-student floor [verified]. Best-LR is not rejected in spirit at all; the chosen model is Best-LR minus the unidentifiable `alpha_s`, plus decay, plus the graph.

The honest summary of the evidence, in Gervet et al's own words, is that "the weakest links today are often the adaptive instructional policy and the KC model, not the performance prediction model" [verified, https://files.eric.ed.gov/fulltext/EJ1273917.pdf]. This project has an unusually good knowledge-component model, authored by hand over 541 skills and 1226 edges, and no data. Spending effort on the prediction model rather than on the policy and the graph would be spending it where the literature says the returns are smallest.

## Traceability table

Each mechanic named in [01-learning-model.md](01-learning-model.md), using the D1 names, mapped to the engine rule that implements it.

| Mechanic (01) | Engine rule (this document) | Where |
|---|---|---|
| Interleaving | `filter_interleaving`: max 2 consecutive same primary skill, 4+ distinct skills and 2+ units per 10, no family above 3 per 10 | Item selection algorithm |
| Spaced retrieval scheduled to the exam date | Review mode due test on `R_k` against the desired-retention schedule, 0.90 to 2027-03-15 then 0.95 | Decay; Item selection algorithm |
| Practice testing over restudy | `fading_stage` leaves `example` after 2 consecutive successes and never returns unprompted; stage `unsupported` is the only stage that credits `success_days` | Mastery state schema; Update rules |
| Mastery gating | Outer fringe restriction plus the six-condition mastery declaration | Prerequisite gating; Update rules |
| Adaptive fading | `fading_stage` ladder, advance on 2, drop on 2, with the prerequisite-driven `example` skip | Update rules |
| Elaborated feedback withheld until submission on full items | Engine-side: the observation is not written until the full point vector exists, so no partial credit reaches the model before submission. Feedback content is in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md) | Evidence model |
| Confidence ratings with hypercorrection routing | `hypercorrection_due` set to tomorrow on a high-confidence credited failure; review mode serves it before the FSRS queue | Update rules; Item selection algorithm |
| Structured self-explanation on examples and errors only | Engine-side: prompts attach at `fading_stage` in `example` and `completion`, and on any observation with a diagnosed BC-ERR. Never at `unsupported` with no error | Mastery state schema |
| Split-attention-free figures | Engine-side: `representation_gap` and the 20 percent translation floor select for BC-REP coverage; figure construction is in [04-item-generation.md](04-item-generation.md) and [08-design-brief.md](08-design-brief.md) | Item selection algorithm |
| Implementation intention plus queue-bound streak | Engine-side: the streak unit is a completed due queue, so `next_item_review` returning null is the event that closes a streak day. No engine state rewards volume | Item selection algorithm |
| Mastery-gated practice at the outer fringe (priority 1) | `outer_fringe` plus `candidates` | Prerequisite gating |
| Interleaved and spaced retrieval of everything learned (priority 2) | Review mode with repetition compression | Item selection algorithm |
| Worked examples faded adaptively (priority 3) | `fading_stage` ladder | Update rules |
| Criterion-shaped rehearsal at a low fixed cadence (priority 4) | Rehearsal mode, pacing metrics only, no mastery write | Evidence model; invariant 17 |
| Productive-failure openers for conceptual targets only | `concept_opener_done`, an integer flag in `skills_state` on the first skill of each BC-CON, consumed by block 2 the first time any skill of that concept enters the fringe; no mastery credit is written for the generation attempt | Mastery state schema; Session assembly |
| Representation translation drills | The 20 percent translation floor, enforced in `filter_interleaving` and `pick_variant` as a hard constraint on the assembled set, not as a score term; `representation_gap` returns only under the deferred five-term score | Item selection algorithm |
| FRQ justification writing as criterion practice | None in this document. The rule is the grader contract and the justification-point handling in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md); the engine's only part is crediting the resulting point vector | Evidence model (pointer only) |
| Session shape and daily target | The four-block assembly, the minute forecast and the all-blocks-empty stop condition | Session assembly |
| Metacognitive judgments of learning | None. No engine rule reads or writes a judgment of learning, by design: it is a measurement, not a selection input. Storage lives in the attempts schema in [06-architecture.md](06-architecture.md) and the display in [08-design-brief.md](08-design-brief.md) | Pointer only |

## Tunables to hand to 12-open-questions.md

Every parameter below is [inferred]. None has a source that fixes it. Each is listed with its current value, the quantity that would settle it, and the metric in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) that watches it.

| Tunable | Current | What would settle it | Watched by |
|---|---|---|---|
| `gamma` success weight | 1.0 (corrected 2026-09-19 from 0.4, see Parameters) | per-skill fit once 20+ observations exist on a skill | calibration residual on `p_A_raw` |
| `rho` failure weight | -0.5 (corrected 2026-09-19 from -0.2, see Parameters) | same | same |
| `lambda` decay weight | 0 (R3) | arm 6 of the offline simulation, the ablation that compares `lambda = 0` against `lambda = 2.0` on true mastery per item and on retention; that arm is now the gate that would turn it back on | retention at 7 and 30 days |
| `beta_k` coefficient on BC-DF count | -0.35 per factor, centred on a median count of 2 (R1) | first-attempt accuracy regressed on BC-DF count over 100+ items; before that, the P1 cold-start distribution gate | per-archetype calibration residual; P1 cold-start `p_A` distribution |
| `beta_k` centring constant | median BC-DF count 2, computed from `data/archetypes.json` 2026-09-19 | recomputation on any content snapshot that changes the archetype set | content snapshot diff |
| BC-DF per-factor weights | all 1.0 | library gap (i); residual of first-attempt accuracy against individual factors | drift monitor 1 |
| Variant `difficulty_effect` shift | 0.4 logits | accuracy difference between `harder` and `easier` variants of the same archetype | per-archetype calibration residual |
| Credit weights per `mastery_state` | 1.0 mastered, 0.0 to `c_k` and 0.5 to `f_k` on the three partials (R2), 0.25 notation_only, 0.0 not_attempted | sensitivity sweep in the offline simulation, constrained by invariant 6 | policy comparison on mastery per item |
| MCQ success discount | 0.75 | observed accuracy gap between MCQ and free-response items on matched skills | MCQ versus FRQ calibration split |
| Propagation weights and hops | 0.3 at 1 hop, 0.09 at 2, 0.1 supporting | ablation in the offline simulation against the hidden true state | mastery growth per study hour |
| `prerequisite_gap` forward failure | 0.3 at 1 hop | same | error-type recurrence |
| FSRS grade mapping | 4 / 3 / 2 / 1 as tabulated | calibration of `R_k` against observed first-attempt accuracy on due reviews | retention at 7 and 30 days |
| Propagated stability interpolation | linear in the credit weight | offline simulation ablation | retention at 7 and 30 days |
| Mastery threshold | `sigmoid(m_k) >= 0.9` | rate of un-mastery events after declaration | un-mastery rate per declared skill |
| Un-mastery threshold | 0.75 | same | same |
| `RETRIEVAL_ENTRY`, unsupported successes before a skill joins the block 3 mixed-review pool | 1 (R8) | within-student A/B on `RETRIEVAL_ENTRY` 1 versus 3 in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) | delayed-checkpoint accuracy |
| Mastery corroboration rule, a separate quantity from `RETRIEVAL_ENTRY` (fix 12) | 3 successes, 2 archetypes, 3 days, 7-day span, `R_k >= desired retention` | rate of un-mastery after declaration, and delayed-checkpoint accuracy on declared skills | un-mastery rate per declared skill |
| Fading advance and drop | 2 consecutive | accuracy with and without support on the same skill | expertise reversal check |
| Desired retention schedule | 0.90 then 0.95 from 2027-03-15 | review volume against retention trade-off measured on this student | review queue length, retention at 30 days |
| Long-gap diagnostic trigger | 21 days | calibration error as a function of gap length | calibration error |
| Decayed-skill support cap | `R_k < 0.5` caps stage at `completion` | accuracy on first item after a long gap | mock-exam trajectory |
| `TARGET_LEARN`, now a fading-stage filter (R4) | 0.80 knowledge scale, with stage bands at 0.50 and 0.90 | first-attempt accuracy against delayed-checkpoint accuracy at several targets; recalibrated together with the `beta_k` coefficient if the P1 cold-start gate fails | mastery growth per study hour |
| Selection weights `W_*`, deferred | all off; 0.50 / 0.25 / 0.10 / 0.10 / 0.05 if turned on | the P7 simulation showing the five-term score beating the two-term score on mastery per item, not merely beating random | policy comparison |
| Coverage tie-break band, deferred with the five-term score | 0.02 score | distribution of `observation_count` across 541 skills | coverage histogram |
| `EXPLORE_SHARE`, deferred with the five-term score | 0, would be 0.125 | bias of the calibration residual against the random control arm | feedback-loop bias check |
| Minute forecast default per item (R5) | 3 minutes until 5 attempts exist on the archetype | the archetype's own running median attempt time | items per session against assembled forecast |
| Block forecast caps (R5) | 5 items or 5 minutes, 25 minutes, 10 to 15 minutes | session completion rate and the adherence-versus-effort metric | adherence versus effort |
| `pending_probes` depth and expiry (R6) | 3 entries, 7 days | rate at which probes expire unserved | error-type recurrence |
| Interleaving constants | 2 consecutive, 4 skills, 2 units, 3 per family per 10 | method-selection accuracy on unseen mixed sets | method-selection versus execution accuracy |
| Translation floor | 0.20 | accuracy by (source representation, target representation) pair | representation matrix |
| Diagnostic entropy stop | 0.02 bits over 3 items, floor 10 | agreement on the held-out extra problem at several stopping points | diagnostic held-out agreement |
| Diagnostic unit pool cap | 4 per unit before full coverage | same | same |
| MCQ informative target | 0.625 raw | held-out agreement split by item format | diagnostic held-out agreement |
| BC-PRQ assumed-mastered default | true for all 77 | diagnosed BC-PRQ gap rate in month 1 | prerequisite gap rate |
| Conjunctive and compensatory split | hard conjunctive, supporting compensatory with `1/|K_soft|` scaling | head-to-head calibration against the logged pure compensatory counterfactual | invariant 23 and the calibration dashboard |

The last row is the one to watch hardest. It is the only structural assumption in this engine that no published model shares, it touches every prediction the engine makes, and the counterfactual that would falsify it is already being logged on every observation.
