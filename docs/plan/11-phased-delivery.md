---
title: Phased delivery plan, P1 to P8
research_date: 2026-09-19
status: draft
purpose: The build order. Eight phases, one pull request each, exactly as decisions memo D12. Each phase states what a user can do at the end, what must already exist, the numbered deliverables naming modules, tables, endpoints, prompt templates and library IDs, what is explicitly out of scope, the tests that gate it, measurable exit criteria, and the rollback. P1 is specified so that an implementation agent can build it without asking a question.
---

# Phased delivery

Eight phases, one pull request each, in the order fixed by decision D12 of the decisions memo. Every phase must teach something or measure something by the time it merges. Nothing merges with a failing gate.

Numbers carry their source and an evidence tag: [verified], [single-source], [inferred]. Library counts come from the registries under `data/` as computed on 2026-09-19 and recorded in the repo-facts ledger. Exam counts and timings come only from `research/exam/exam-structure.md`. Unit weights come only from `research/exam/exam-blueprint.md`. Where a value is not known this document writes unknown.

Justification order throughout: learning impact first, then cost, then convenience, with the rejected alternative named.

Cross-references: 01-learning-model.md, 02-adaptive-engine.md, 03-diagnosis-and-feedback.md, 04-item-generation.md, 05-assessment-modes.md, 06-architecture.md, 07-ai-provider-layer.md, 08-design-brief.md, 09-security-and-privacy.md, 10-quality-and-evaluation.md, 12-open-questions.md.

## P1 Teaches from day one

Every rule in this phase that the post-review decisions memo settled is cited as R-n. Where this phase and an earlier document disagree, R-n wins.

### Goal

At the end of P1 a student registers with a passkey, opens the app, and is handed a finite queue of calculus work drawn from a fixed subset of Units 1, 2 and 3. They work through items that arrive at one of three support stages, a fully worked example with a self-explanation prompt, a completion problem with the last step blanked, or an unsupported problem. They type their answer into a MathLive field or pick a multiple-choice option, rate their confidence on a three-point scale before seeing anything, and then get feedback: step-level verification while support is present, and withheld elaborated feedback naming the rule violated and its scoring consequence on unsupported items. Every corrected item is requeued at a 1 to 2 day gap and the student writes one line saying what went wrong before that happens. The requeued items are read by block 1 of session assembly, which exists in P1 as a minimal review mode; FSRS scheduling arrives in P2 [R23]. Across sessions, per-skill mastery state changes visibly and correctly under the D2 model as amended by R1 to R8, the support stage rises and falls with performance, and the app refuses to serve a skill whose hard prerequisites are unmastered. It is a working mastery tutor over 54 skills, built on 130 hand-authored items [R9], with no diagnostic, no generator, no free response, and no second provider.

### Entry criteria

1. The registries under `data/` load and validate against `schemas/`: `curriculum.json`, `skills.json`, `prereq_edges.csv`, `archetypes.json`, `errors.json`, `misconceptions.json`, `diagnostic_signals.json`, `taxonomies.json`, `scoring_points.json`, `frq_records.json`, `mcq_records.json` and `sources.json`. The last three were missing from this list and are added (R30): 06-architecture.md's loader reads and schema-validates all twelve registries, and the integration test in 10-quality-and-evaluation.md asserts 249 FRQ parts and 91 MCQ records on every run, so a P1 that loaded only nine would fail its own loader test.
2. `qa/12_report.py` exits 0 on the library as it stands, and `qa/04_tags.py` produces the ok-status source list.
3. `prereq_edges.csv` contains 0 cycles over the 1226 edges [verified, repo-facts ledger].
4. An Anthropic API key exists with at least Start-tier limits, which are 1,000 RPM, 2,000,000 ITPM and 400,000 OTPM for the Opus 5, Sonnet 5, Opus 4.x, Sonnet 4.x and Haiku 4.5 bucket, with a $500 monthly spend cap [verified, https://platform.claude.com/docs/en/api/rate-limits].
5. The design tokens exist as a file. **Q18.** 08-design-brief.md fixes token names and roles and deliberately fixes no hex values, so the implementer produces the values in P1 from those roles: the nine-step neutral ramp, the accent ramp, the two semantic ramps, both themes, the nine type-scale steps and the nine-value spacing scale. Every value is checked against a contrast checker that is named by tool and version in the pull request, with the measured ratio for each text token recorded beside it, before `test_contrast_floors` is allowed to count as evidence.

### Scope

1. **Content loader** (`app/content/loader.py`). Reads `data/*.json` and `data/prereq_edges.csv` by ID at startup into an immutable in-memory graph plus a versioned snapshot row in `content_snapshots`. Validates against `schemas/`. Refuses to start on a cycle or a dangling ID. This is the D7 rule and it is not negotiable in P1, because every later phase's correctness rests on the graph being what the registries say it is. **Q3.** The 48 edges carrying a BC-TOP id on either side (31 with a BC-TOP source, 17 with a BC-TOP target, 4 of them reaching the P1 subgraph) are loaded and validated against `curriculum.json`, and are then inert: they do not gate, they neither receive nor send propagated credit, and `outer_fringe` does not iterate over them [R13]. They are carried to 12-open-questions.md as a library gap, because the edges should be remapped to BC-SKL ids.

2. **The P1 archetype subset**: 13 archetypes, every one of them `calculator_status: no_calculator`, primary unit in BC-UNIT-01, BC-UNIT-02 or BC-UNIT-03, and with an `expected_solution_path` that terminates in a closed-form expression SymPy can compare. The list is exact and is read off `data/archetypes.json`:

   - BC-QA-01004 Indeterminate limit resolved by algebraic rewriting
   - BC-QA-01008 Parameter solved so that a piecewise function is continuous
   - BC-QA-01015 Intervals of continuity determined from the domain of an expression
   - BC-QA-02002 Derivative computed from the limit definition
   - BC-QA-02006 Derivative of a polynomial or power expression by rule
   - BC-QA-02007 Derivative of an expression built from the basic transcendental functions
   - BC-QA-02008 Derivative of a product or a quotient by rule
   - BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression
   - BC-QA-02011 Tangent line written at a point on a curve
   - BC-QA-03001 Chain rule derivative of a composite given symbolically
   - BC-QA-03004 Implicit differentiation producing or verifying dy/dx
   - BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve
   - BC-QA-03008 Higher-order derivative of a function or of a derivative expression

   Excluded from P1 although they are also `no_calculator` in Units 1 to 3: BC-QA-01001, BC-QA-01005, BC-QA-01006, BC-QA-01007, BC-QA-01009, BC-QA-01011, BC-QA-01013, BC-QA-02004, BC-QA-02005, BC-QA-02012 and BC-QA-03003, because each of them can only be posed through a figure, a graph read or a verbal justification, so no symbolic form of the question exists; and BC-QA-01003, BC-QA-01014, BC-QA-02003, BC-QA-02009 and BC-QA-03009, because the answer is a selection, a table read or a named procedure rather than a closed-form expression, so SymPy cannot decide it. The rule is about the only form the question can take, not about the representations the archetype record lists [C13]: BC-QA-02011 and BC-QA-03005 carry BC-REP-02 graphical and BC-QA-03008 carries BC-REP-06, and all three are included because P1 serves them at BC-REP-01 symbolic only, which is a form each of them supports.

   **Q19.** All 13 P1 archetypes carry declared variants, 43 BC-QV in total: BC-QV-01004-01 to -04, 01008-01 to -03, 01015-01 to -03, 02002-01 to -04, 02006-01 to -03, 02007-01 to -03, 02008-01 to -04, 02010-01 to -03, 02011-01 to -03, 03001-01 to -03, 03004-01 to -04, 03005-01 to -03 and 03008-01 to -03 [computed from `data/` on 2026-09-19]. `pick_variant` is disabled in P1 and returns the parent archetype; variants are future difficulty settings [R23].

   **Q17.** Every P1 archetype is served in both formats, and the alternation is scoped by stage (R29, the rule is stated once in 02-adaptive-engine.md under Fading ladder). Stages `example` and `completion` are always short answer, because neither a worked example with a self-explanation prompt nor a completion problem with a blanked step has a four-option form. Four-option MCQ and MathLive short answer alternate per attempt only at stage `unsupported`, per user per archetype, and the first `unsupported` attempt on an archetype is short answer. Attempts at the other two stages neither consume nor advance the alternation. The format is stored on the attempt in `attempts.format` and the 0.75 discount is applied per item rather than per archetype [R16]. All 13 carry `common_distractors` [verified from `data/` on 2026-09-19], so the MCQ form is authorable for every one of them, and R26 below says where each option's BC-ERR id is stored.

3. **The P1 skill set**: 54 BC-SKL records, the union of the `skills` arrays of those 13 archetypes, listed individually here and in the fixture, because range shorthand misstates the set. **Q20.** These are the 54 that go into `tests/fixtures/graph_p1.json` [R23, fix 37]: BC-SKL-01024, 01025, 01026, 01027, 01028, 01046, 01047, 01048, 01049, 01050, 01051, 01052, 01053, 02006, 02007, 02008, 02009, 02012, 02013, 02025, 02026, 02027, 02028, 02029, 02030, 02031, 02032, 02033, 02034, 02036, 02038, 02039, 02040, 02042, 02043, 02044, 02045, 02046, 03002, 03003, 03006, 03007, 03008, 03009, 03010, 03011, 03012, 03013, 03014, 03030, 03031, 03032, 03033, 03034. BC-SKL-02037 and BC-SKL-02041 are not in the set. Those 54 skills carry 74 BC-SIG diagnostic signals, 40 BC-ERR error records and 20 BC-MIS misconception records, and 101 prerequisite edges point into them, 50 hard_prerequisite, 50 supporting and 1 co_requisite, from 19 BC-PRQ non-calculus prerequisites and 6 BC-SKL parents outside the set [computed from `data/` on 2026-09-19].

   **"Active" has no backing field (C12).** No BC-SKL record in `data/skills.json` carries a `status` field [verified, `data/` on 2026-09-19], so "active BC-SKL" means the whole registry, all 541 records, and the loader filters nothing. The word is kept only because the library counts are published that way. Where this document or 10-quality-and-evaluation.md writes "541 active BC-SKL" or "54 active BC-SKL", read it as 541 and 54 records, with no filter to implement. BC-ERR, BC-MIS and BC-QA do carry `status`, and there "active" is a real filter.

   **`skills_state` is seeded in full, not at 54 rows (R27).** At account creation the table gets one row per BC-SKL, 541 rows, and one row per BC-PRQ, 77 rows, so 618 rows, exactly as 06-architecture.md states. The 54-skill subgraph is a selection scope and a test fixture, never a row count: `tests/fixtures/graph_p1.json` is what the engine unit tests, including `test_fringe_membership`, range over, while the live table holds all 618 rows from the first login. The 25 seeded assumed-mastered parents in Q8 below are 25 of those 618 rows, not extra ones. BC-TOP ids get no row at all [R13].

   **Q21.** The co_requisite edge is included in `tests/fixtures/graph_p1.json`, and invariant 21, not invariant 20, which asserts that removing every co_requisite edge changes nothing, runs in P1 [R23, R30]. In 02-adaptive-engine.md invariant 20 is "BC-SKL-02001 is never selected" and invariant 21 is "co_requisite and BC-TOP edges are inert"; 02's numbering is the one this document and 10-quality-and-evaluation.md use, and the earlier "invariant 20" here and at test 14 was a citation error.

   **Q8.** The seeded assumed-mastered parents are the 19 BC-PRQ records and the 6 external BC-SKL parents, which are BC-SKL-01018, BC-SKL-01039, BC-SKL-01044, BC-SKL-02001, BC-SKL-02002 and BC-SKL-03001. Every one of those 25 rows starts with `beta_k = 0.0`, `c_k = f_k = 0`, `S_k` and `D_k` null, `fading_stage` unsupported, `mastered` true and `mastered_at` set to account creation, and is flipped to unmastered only by a diagnosed gap or a credited failure [R15]. The 4 BC-TOP parents are inert and hold no state [R13]. BC-SKL-02001 has no archetype of its own, so it is seeded and never served.

4. **Engine core** (`app/engine/state.py`, `app/engine/update.py`, `app/engine/fringe.py`). Implements the D2 per-skill state: `beta_k`, `c_k`, `f_k`, `S_k`, `D_k`, `last_practised_at`, `fading_stage`, `observation_count`, `distinct_archetypes_succeeded`, `success_days`, `mastered`, `mastered_at`, plus the columns named in Q12 below. Implements `m_k = beta_k + gamma * log(1 + c_k) + rho * log(1 + f_k)` with gamma = 1.0 and rho = -0.5 (corrected 2026-09-19 from 0.4 and -0.2, see 02), and with `lambda = 0` until the arm 6 ablation in 10-quality-and-evaluation.md reports, so the FSRS retrievability `R_k` is used only to schedule due reviews and to test the mastery condition `R_k >= desired retention` at declaration time [R3]. The lambda row stays in the tunables table at current value 0.

   **Q2.** For a skill with no credited observation, `R_k = 1` and `c_k = f_k = 0`, so `m_k = beta_k`, which is defined and finite for every skill from startup [R1]. `beta_k` is centred: `beta_k = -0.35 * (mean BC-DF count over the archetypes that list k in their skills array - 2)` (R25), where 2 is the median BC-DF count across the 139 active archetypes, whose distribution is 1:32, 2:40, 3:34, 4:23, 5:6, 6:3, 7:1 [computed from `data/archetypes.json` on 2026-09-19; the 0.35 coefficient is inferred and stays tunable]. A median-difficulty unobserved skill therefore starts at p = 0.5 rather than near 0.08. `beta_k` is never learned, because data-driven item difficulty needs at least 100 students [verified, Pelanek, via track 2]. The set averaged over is every archetype whose `skills` array contains `k`, with no restriction to a "primary" subset (R25); the phrases "primary archetypes of `k`" and "primary loaded skills" are withdrawn from 02-adaptive-engine.md because they were never defined, and the set named here is the one the recorded pre-computation in 02's Calibration plan was run over. Separately, `primary_skill(A)` is defined in 02 as the first entry of `archetypes.skills`, which is what the fringe, candidate selection, interleaving and tests 2, 20 and 21 read.

5. **Engine rules P1 implements**: the item-level conjunctive-over-hard-prerequisite and compensatory-over-the-rest split from D2; credit assignment from a mastery_state, which is mastered 1.0 to `c_k`, `partial_procedural`, `partial_conceptual` and `partial_unspecified` 0 to `c_k` and 0.5 to `f_k`, `notation_only` 0.25 to `c_k` because the mathematics was demonstrated, `prerequisite_gap` 0 to the target and 1.0 failure to the named prerequisite, `not_mastered` 1.0 to `f_k`, and `not_attempted` nothing [R2, inferred], together with the invariant that no `partial_*` observation may increase `m_k`; the MCQ 0.75 success discount against a 3PL guessing floor of 0.25 for four options [R19]; prerequisite propagation at 0.3 of a success to hard_prerequisite ancestors at 1 hop, 0.09 at 2 hops, 0.1 to supporting parents at 1 hop only, and 1.0 failure to a diagnosed prerequisite plus 0.3 failure to its hard dependants at 1 hop [inferred]; the FSRS-7 decay term with the 34 default parameters taken verbatim from `src/inference_v7.rs` of https://github.com/open-spaced-repetition/fsrs-rs [verified at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae on 2026-09-19 that the vector has 34 entries; the srs-benchmark README block of 35 values is a superseded draft; its suitability for skills rather than cards is unsourced], with the `S0`, `D0`, `S'`, `D'` and `R` forms read off `model_v7.rs` in that repository, because the awesome-fsrs wiki page documents only v0 to v6, and the D2 grade mapping; and the outer-fringe restriction, so no archetype is served whose primary skill's hard prerequisites are unmastered.

   **Q6a. The unwritten FSRS entries (R28).** No entry of the vector is written in any plan document and none is invented here. The implementer copies the full 34-entry vector out of `src/inference_v7.rs` into a versioned constants file at implementation time, commits that source file as a test fixture, and records the commit hash and digest beside it. `test_retrievability_monotone` then asserts that the constants file matches the fixture, which is what makes the test checkable without the numbers living in prose.

   **Q6.** Mastery has six conditions, not five [R19, C7]: `sigma(m_k) >= 0.9`, at least 3 credited unaided successes at stage unsupported, on at least 2 distinct archetypes or on every archetype listing the skill when fewer than 2 do (02, corrected 2026-09-19), on at least 3 distinct calendar days, spanning at least 7 days, and `R_k >= desired retention` at declaration time, with no same-day repeat counting.

   **Q7.** MCQ credit is 0.75 against a four-option guessing floor of 0.25. The five-option, 0.8 reading in 01-learning-model.md is stale [R19, C1].

   Retrieval eligibility is a separate quantity from mastery. A skill enters the interleaved review pool, which is block 3, after its first credited success at stage unsupported, so `RETRIEVAL_ENTRY = 1` in P1 [R8]. The A/B in 10-quality-and-evaluation.md tests `RETRIEVAL_ENTRY` 1 against 3 and does not test the mastery rule.

   **Fading stage precedence.** One counter pair decides stage changes: 2 consecutive credited successes at a stage advance it, 2 consecutive credited failures drop it. Un-mastery, which is a credited failure at stage unsupported or `sigma(m_k)` falling below 0.75, flips `mastered` to false and does not itself move the stage [R7]. That counter pair is the only writer of `fading_stage`, and `serve_stage` is not a second writer (R32): it chooses the initial stage for a skill with no observation, from the `p_A_knowledge` bands, and returns the stored stage unchanged once any observation exists. The `example` skip condition is stated once, in 02-adaptive-engine.md under Fading ladder, and reads "every hard prerequisite of the skill is mastered and the student's first attempt succeeds with confidence not rated `guess`". This document points there and does not restate it; the earlier phrase "confidence-corrected first attempt" was not a defined term and is withdrawn (R32).

   **Q1 and Q5. The no-diagnostician mastery_state rule.** P1 wires no diagnostician, so the mastery_state per loaded skill is produced by a rule, and that rule is what P1 implements and what `test_credit_assignment_table` tests [R12, inferred]: a correct answer at the served stage yields `mastered` for every skill the archetype loads, with MCQ credit discounted to 0.75; an incorrect MCQ answer whose chosen distractor carries a BC-ERR path, meaning the selected entry of `items.options` has a non-null `error_path` (R26), yields `not_mastered` for the skills listed on that BC-ERR and `not_attempted` for the rest; an incorrect answer with no error path yields `not_mastered` for the archetype's first listed skill, which is `primary_skill(A)` (R25), and `not_attempted` for the rest; and a MathLive answer that SymPy judges equivalent but mis-notated yields `notation_only` for every loaded skill. `prerequisite_gap` and the two conceptual partial states are unreachable in P1 because nothing produces them, and the test reaches the three unreachable states by calling the credit function directly with a synthetic observation, which for `prerequisite_gap` names a prerequisite skill explicitly, so the row has a defined arithmetic to assert even though no P1 answer shape produces it. The test asserts the table's arithmetic for all eight states over the fixture rather than over the 74 BC-SIG records, which cover only a subset of the enum; the expected value for a state with no P1 signal is the table value, and the signal set is not the test's domain.

   **Q4 and Q16. Archetypes with no point types.** Eight of the thirteen carry `point_types: []`: BC-QA-01004, 01008, 01015, 02002, 02006, 02010, 03004 and 03005. For those eight the completion-stage blank falls on a step of `expected_solution_path` rather than on a BC-PT step, and elaborated feedback names the violated step and the BC-ERR path and names a BC-PT only when the archetype lists one [R14]. Rejection rule 9 in 04-item-generation.md applies only when `point_types` is non-empty. Such archetypes are served only as MCQ or short answer until the library fills `point_types`, which every P1 archetype already is. A completion blank requires an `expected_solution_path` of at least 2 steps, so that one step can be given and one blanked; an archetype with fewer is served at stages example and unsupported only, and the fixture records which of the 13 that applies to. It applies to none of them: every one of the 13 carries an `expected_solution_path` of 4 steps or more [verified, computed from `data/archetypes.json` on 2026-09-19], so the 2-step minimum never binds in P1 and the fixture field records an empty set.

6. **Engine rules P1 explicitly stubs or holds**: diagnostic mode, where the cold-start entry point returns the fixed fringe of the P1 subset instead of running an information-targeted search; review mode, which in P1 is limited to block 1 due reviews and gains FSRS scheduling in P2 [R23]; and the interleaving constraints beyond the max-2-consecutive-same-primary-skill rule, since the P1 subset spans only 3 units and the renderer has one representation.

   **Selection is two-term in P1 and stays two-term in P2** [R4]. Candidates are fringe archetypes with at least one published item. The score is due coverage, meaning the count of due skills including 1-hop hard ancestors that the archetype covers. Ties and the no-due case are resolved by uniform random choice within the fringe. Interleaving, the representation-translation floor, hypercorrection and probe injection remain hard constraints on the assembled set rather than score terms. `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE` are deferred to a P7 gate and may be turned on only after the simulation shows the five-term score beating the two-term score on mastery per item, not merely beating random. `TARGET_LEARN` 0.8 survives as a fading-stage filter on the initial stage only (R32, C9): for a skill with no credited observation, `p_A_knowledge` below 0.5 starts it at stage example, between 0.5 and 0.9 at completion, above 0.9 at unsupported. After the first observation the R7 counter pair owns the stage and the bands are not consulted again. The earlier `min(stage_of(A, state), "completion")` form in 02-adaptive-engine.md could never return example and overrode the counters, and it is withdrawn there.

   **Q15.** The random-within-fringe control arm in `eval_simulation_mastery_growth` is a separate simulation run over the same fixtures, not the live exploration arm. The live exploration share is 0 in P1, and under R4 it is moot, because uniform random choice inside the fringe is already how ties and the no-due case resolve.

   **Q24.** The 1-day due date set by a high-confidence error, and the 1 to 2 day requeue of every corrected item, are read by block 1 of session assembly, which exists in P1 [R23]. Nothing in P1 is written to a due date that nothing reads.

   **Probe injection.** `pending_probes` exists from P3, when the diagnostician that writes to it arrives. In P1 the table is created and no P1 component writes to it, so in ordinary operation the queue is empty. Every selection function drains it before its own scoring regardless, so the drain path is wired from day one [R6]. Because an always-empty queue makes the drain unobservable, `test_pending_probes_drained` injects a probe row directly into `pending_probes` and asserts it is served first in block 2, ahead of any fringe candidate (R34). That is the only thing in P1 that ever puts a row in the table, and it is a test, not a feature.

7. **Hand-authored items and the verification tools** (`app/items/verify.py`). The generator, the independent re-solve and the item review queue move to P4 [R9]. P1 ships the SymPy equivalence checker, the numeric check at several points, the distractor checks and the provenance record, and the operator authors 130 items, 10 per P1 archetype, using the archetype record as the mould: `invariant_structure`, `safe_variables`, `difficulty_variables`, `calculator_status`, the target representation, which is always BC-REP-01 symbolic in P1, and `expected_solution_path`. Every item carries a MathJSON key checked by SymPy, and its provenance record sets `model = "operator"` with `prompt_template_version` and `generation_job_id` null, plus the authoring date and the archetype and variant ids (R30). There is no separate `provenance` string key; the earlier `model = null` reading here contradicted 06-architecture.md and is withdrawn. No official item's text is ever read into an item.

   **MCQ option error paths (R26).** Each entry of `items.options` carries `error_path`, a BC-ERR id or null. The key's is null and each of the three distractors carries a BC-ERR id drawn from the 40 error records the P1 skills hold. The operator records it by hand while authoring the 130 items, and from P4 the generator emits it as `generating_error_path`. `archetypes.common_distractors` is prose and is the operator's authoring guide, never machine input: nothing parses it, in P1 or later. This is the field the P1 mastery_state rule reads and the field `eval_p1_distractor_paths` ranges over.

   **Q14.** There is no generation-to-publication yield to assume, because the items are hand-authored and each is verified before it is committed. The fail-closed rule still stands: an archetype with no published item is excluded from selection and logged as a coverage gap [R18]. **Published means `items.status = 'verified'`**, which is the vocabulary 06-architecture.md defines; "published" is a description of what that status permits, not a fifth status value, and `has_published_item(A)` in 02-adaptive-engine.md tests for at least one item on `A` at status `verified`. P1 cannot hit the empty case with its own 130 items, so test 18 reaches it by loading a fixture archetype whose only item is at status `draft`, and the test asserts exclusion and the logged coverage gap.

8. **Fading ladder rendering** (`app/web/session/Item.tsx`). Three item states, `example`, `completion`, `unsupported`, rendering the session wireframes in 08-design-brief.md. Backward fading: the last solution step is the blank first and earlier steps are removed later [single-source, Renkl and Atkinson, https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6]. The completion stage requires the 2-step minimum in Q16 above.

9. **Session assembly** (`app/session/build.py`), implementing the rule of the same name in 02-adaptive-engine.md [R5]. **Q9.** Block 1 is due reviews, at most 5 items or 5 minutes of forecast. Block 2 is fringe learning until 25 minutes of forecast are assembled or the fringe is exhausted, and it serves a pending discriminating probe first when one exists, which in ordinary P1 operation it never does because no P1 component writes to `pending_probes`, and which test 15 makes happen by injecting one (R34). Block 3 is interleaved mixed review drawn from skills observed at least once **and eligible under `RETRIEVAL_ENTRY`**, which in P1 is a first credited success at stage unsupported, `RETRIEVAL_ENTRY = 1` (R33). That is the rule in 02-adaptive-engine.md and the one `test_retrieval_entry` asserts; the observed-at-least-once reading written here earlier was looser and is withdrawn. Block 3 runs at 10 to 15 minutes of forecast. Block 4 is the calibration prompts and the one-line error notes for corrected items. The minute forecast is the sum of the per-archetype median attempt time, defaulting to 3 minutes per item until 5 attempts exist for that archetype [inferred]. A session ends when all four blocks are empty; there is no timer, and the forecast is a presentation of the assembled queue and never an input to selection. **The productive-failure opener is out of P1 scope (R35).** The `concept_opener_done` column exists in `skills_state` from P1 so that no migration is needed later, and in P1 it is never set and never read: block 2 opens with an ordinary fringe item. The opener needs a conceptual generation prompt that P1 has no component to produce, since P1 has no generator and its one tutor role is restricted to feedback wording. The mechanic is specified in 02-adaptive-engine.md under Session assembly and is wired when a generator exists.

   **Q10.** The repeat rule: no item is served twice in one session, and no item is served twice within 7 days unless it is a corrected item returning through block 1, which is scheduled deliberately at a 1 to 2 day gap. The max-2-consecutive-same-primary-skill constraint applies across the whole assembled set, not per block.

10. **Feedback and confidence** (`app/feedback/render.py`). Step-level immediate verification at stages `example` and `completion`; nothing until submission at stage `unsupported`, then elaborated feedback naming the violated rule and the scoring consequence [verified, Shute 2008, https://journals.sagepub.com/doi/10.3102/0034654307313795]. A 3-point confidence rating (guess, unsure, confident) is collected before feedback on every item. A high-confidence error sets `hypercorrection_due` to tomorrow. Exactly one structured self-explanation prompt, in the form "which rule justifies step k, and why does it apply here", attached to worked examples and corrected errors only [verified, Bisra et al 2018 g = 0.55, https://link.springer.com/article/10.1007/s10648-018-9434-x]. One student-authored error note per corrected item, collected before the retry is scheduled [single-source, the position, Nielsen, https://cognitivemedium.com/srs-mathematics, which is an essay with no study, no n and no effect size].

11. **Input** (`app/web/input/`). MathLive field with MathJSON export, keyboard-first, plus a four-option MCQ control (option count stored per item). The verifier consumes MathJSON, not a LaTeX string, because MathJSON is a structured semantic form that maps cleanly onto a symbolic check [verified that MathLive exports MathJSON, https://www.npmjs.com/package/mathlive]. No animation on any keystroke-driven action [verified, https://emilkowal.ski/ui/great-animations].

12. **Provider layer, Anthropic only** (`app/providers/anthropic.py`). **Q13.** P1 wires exactly one role: tutor on claude-sonnet-5, guardrailed, streaming, no tools, never giving the final answer during practice, used for feedback wording only. There is no classifier in P1; the "cheap classifier on claude-haiku-4-5" is removed, because D8 defines six roles and none of them is a classifier [R17]. Generator, verifier, grader, diagnostician and transcriber are not wired in P1; the transcriber and its quality gate arrive in P3. Structured outputs everywhere a schema exists, using `output_config.format` with `{"type": "json_schema", "schema": {...}}` and `strict: true` on tool definitions [verified, https://platform.claude.com/docs/en/build-with-claude/structured-outputs]. Prompt caching on the static prefix with a 1 hour TTL via `cache_control: {type: "ephemeral", ttl: "1h"}`; the minimum cacheable prefix is per model, 1,024 tokens for claude-sonnet-5 and 512 for Opus 5, and below the minimum the prompt is silently processed uncached with no error, so the prefix length is asserted in a test [verified, track 4, https://platform.claude.com/docs/en/build-with-claude/prompt-caching]. P1's one role is the tutor and it is routed to claude-sonnet-5, so the number that binds in P1 is 1,024 (R30); the earlier "512 for Sonnet 5 and Opus 5" reading here and at test 22 was wrong, and a test passing at 512 would have asserted nothing about a prefix that was in fact being processed uncached. Extended thinking uses `thinking: {type: "adaptive"}` with `output_config: {effort: ...}`, because manual `thinking.type: "enabled"` returns 400 on Claude 4.7 and later, which includes Opus 5 and Sonnet 5 [verified, https://platform.claude.com/docs/en/build-with-claude/extended-thinking].

13. **Prompt templates**, versioned in the repo with golden tests. P1 has two, `prompts/tutor/guardrailed_practice_v1.md` and `prompts/feedback/elaborated_v1.md`, both run by the one wired role. **Who composes the elaborated feedback (R35):** the content is selected deterministically and the sentence is written by the tutor. The application picks the violated `expected_solution_path` step, the `observed_behavior` and `scoring_consequence` fields of the chosen option's BC-ERR record, and the item's stored worked solution, and passes exactly those into `prompts/feedback/elaborated_v1.md`, which the tutor role renders. The tutor receives nothing else, and it never receives the final answer before the student has submitted. The earlier pair of sentences here, that the text is assembled deterministically and that the template is not a provider template, could not both be true of one string, and this is the reading that keeps the "feedback wording only" restriction intact. The generator and verifier templates move to P4 with the pipeline [R9].

14. **Data tables** from the D7 model, subset: `users`, `provider_configs`, `content_snapshots`, `skills_state` (one row per user per BC-SKL), `items`, `item_verifications`, `sessions`, `attempts`, `pending_probes`, `judgments`, `review_queue`, `jobs`, `budgets`, `audit_log`. `pending_probes` and `judgments` were missing from this list and are added (R27): the probe queue is drained by every selection function and is injected into by test 15, and block 4 collects judgments of learning, so both are needed in P1. Not created in P1: `gradings`, `diagnoses`.

    **Q12a. `attempts` columns P1 adds (R27).** Beyond the shape in 06-architecture.md, `attempts` carries `served_stage` TEXT holding example, completion or unsupported, `format` TEXT holding mcq or short_answer, and `per_skill_states` JSON holding the `mastery_state` assigned to each skill the item loaded. Without the first, exit criterion 5's requirement that all six D2 conditions be individually satisfiable from `attempts` cannot be met, because three of them count successes at stage unsupported. Without the second, `test_format_alternates` has nothing to read. Without the third, a credit assignment cannot be replayed from the event log.

    **Q11 and Q12.** `users.exam_date` defaults to 2027-05-10, which is the date `research/exam/exam-structure.md` gives [single-source], and `purge_after` derives from it. `skills_state` carries `hypercorrection_due` as TEXT holding an ISO date, not an integer flag, plus `consecutive_successes`, `consecutive_failures` and `concept_opener_done` as INTEGER [R19].

    **Q22.** In P1 `review_queue` holds only `item_audit` entries, which are the operator's hand-audit verdicts on published items [R23]. `item_audit` is added to the `kind` vocabulary in 06-architecture.md, where it was missing (R27). The four other kinds in 06-architecture.md's list need `gradings` and `diagnoses`, which P1 does not create, and they arrive with those tables.

15. **Auth and storage**: passkeys (WebAuthn) as the only authentication path, SQLite through SQLAlchemy, provider keys encrypted at rest with a passphrase-derived key using libsodium secretbox and never logged [decisions memo D10]. **Q23.** The passkey re-authentication flow is in P1 scope, because P1 ships purge and purge requires a typed confirmation and re-authentication [R23].

16. **Fixtures**, committed under `tests/fixtures/`: (a) `graph_p1.json`, the 54-skill subgraph with its 101 inbound edges including the one co_requisite edge, frozen; (b) `items_p1/`, the 130 hand-authored items, 10 per archetype, each with its MathJSON key, its parameter draw, its served format assignment and its `provenance = "operator"` record; (c) `student_trajectories/`, 6 synthetic students with a hidden true state over `graph_p1.json`, one at floor, one at ceiling, one with a seeded prerequisite gap at BC-SKL-02025, one slipping at 0.1, one guessing at 0.2, one with a 30 day absence to exercise the decay term [the count of 6 is a choice, not a sourced number]; (d) `answers_equiv/`, 53 answer pairs in total, 40 that are mathematically equivalent but textually different and 13 that are not equivalent, each pair carrying an `equivalent` boolean, to pin the SymPy equivalence check in both directions and to measure the settle rate (R34). The non-equivalent pairs were missing and are added, because `test_sympy_equivalence`'s second clause, that no non-equivalent pair compares equal, had no domain without them; three of the thirteen are numeric near misses added on 2026-09-19 to pin the numeric tolerance within an order of magnitude. The settle rate in eval 28 and exit criterion 3 is still reported over the 40 equivalent pairs, so that number is unchanged by the addition [the counts of 40 and 13 are choices, not sourced numbers]; (e) `provider_cassettes/`, recorded Anthropic responses for the tutor template so the test suite runs with no network.

17. **Screens from 08-design-brief.md** built in P1: home (queue ready, queue empty, session in progress), session (all four blocks, all item states and both feedback states, and no photo capture anywhere on the screen, per R10), and settings (providers, budgets, queue settings, data export and purge only). Not built in P1: onboarding diagnostic, review, progress, mock.

### Out of scope

Cold-start diagnostic design and whole-graph selection. FSRS-scheduled review beyond block 1 due reviews. Item generation, the independent re-solve and the item review queue, all of which are P4 [R9]. FRQ capture in any form, paper or typed beyond short answers. Per-point grading. The diagnostician. Calculator-bearing or figure-bearing archetypes. Monte Carlo family checks and the duplicate gate. Any provider other than Anthropic, and any role other than tutor. Timed modes and Bluebook tools. The mastery map and the calibration curve as screens. Multi-user. Postgres.

### Tests that gate the phase

Named as in 10-quality-and-evaluation.md.

Unit:
1. `test_graph_acyclic` over the real `prereq_edges.csv`, property: a topological sort of the whole loaded typed edge set, over the union of BC-SKL, BC-PRQ and BC-TOP ids, succeeds and consumes all 1226 edges, so 0 cycles of any edge type. This is 02-adaptive-engine.md invariant 1's reading, and 06-architecture.md's loader step 3 is corrected to match it (C11); a hard_prerequisite-only cycle check is a weaker assertion and is not what this test makes.
2. `test_fringe_membership`, property: over `tests/fixtures/graph_p1.json`, a skill is on the outer fringe if and only if it is unmastered and every hard_prerequisite parent is mastered or is a seeded assumed-mastered parent, and BC-TOP nodes are never iterated [R13]. The test ranges over the 54-skill fixture and its 25 seeded parents, not over the live 618-row table, per the fixture-discipline rule in 10-quality-and-evaluation.md that engine unit tests run against hand-built graphs (R27).
3. `test_credit_assignment_table`, property: each of the eight mastery_state values moves `c_k` and `f_k` by exactly the R2 weights, and the no-diagnostician rule in R12 maps every P1 answer shape, which is correct, incorrect with a distractor error path, incorrect with no error path and equivalent-but-mis-notated, onto the states it names.
4. `test_correct_never_lowers_m`, property: no credited success on any path, including propagated fractional credit, decreases `m_k` for any skill.
5. `test_partial_never_raises_m`, property: no `partial_procedural`, `partial_conceptual` or `partial_unspecified` observation increases `m_k` [R2].
6. `test_retrievability_monotone`, property: `R_k` is monotone decreasing between reviews under the 34-entry FSRS-7 default vector as held in the versioned constants file, and `R_k = 1` for a skill with no credited observation [R1]. The same test asserts that the constants file matches the committed `inference_v7.rs` fixture at the commit hash and digest recorded beside it, which is what makes the 34 entries checkable without any of them being written into a plan document (R28).
7. `test_mastery_conditions`, property: `mastered` flips true only when all six D2 conditions hold simultaneously, and same-day repeats never count [R19].
8. `test_retrieval_entry`, property: a skill enters block 3 after its first credited success at stage unsupported, with `RETRIEVAL_ENTRY = 1` [R8].
9. `test_fading_ladder`, property: stage advances on exactly 2 consecutive credited successes and drops on exactly 2 consecutive credited failures, never skips two levels, and un-mastery alone never moves the stage [R7].
10. `test_propagation_weights`, property: 1-hop hard credit is 0.3, 2-hop is 0.09, supporting is 0.1 at 1 hop, and propagation terminates at 2 hops.
11. `test_mcq_guess_discount`, property: a correct 4-option MCQ credits 0.75, not 1.0.
12. `test_format_alternates`, property: consecutive stage-`unsupported` attempts by one user on one archetype alternate MCQ and MathLive short answer, the first such attempt is short answer, attempts at stages example and completion are short answer and neither consume nor advance the alternation, and `attempts.format` records the format on every row [R16, R29, R27].
13. `test_sympy_equivalence` over the 53-pair `answers_equiv/` fixture, property: all 40 pairs marked equivalent compare equal and none of the 13 pairs marked non-equivalent does (R34).
14. `test_co_requisite_inert`, property: invariant 21 holds on the P1 fixture (R30), so a seeded 1,000-selection trace run with and without the subgraph's one co_requisite edge produces identical output and identical state. The test drives a real selection trace rather than inspecting the loader, so it can fail: an implementation that let a co_requisite parent gate the fringe would diverge between the two runs.
15. `test_pending_probes_drained`, property: with a probe row injected directly into `pending_probes`, block 2 serves that probe first, ahead of any fringe candidate, and the selection function's own scoring runs only after the queue is drained; with the queue empty, block 2 serves the ordinary fringe candidate [R6, R34]. No P1 component writes to the table, so the injection is the test's own setup.

Integration:
16. `test_loader_against_real_data`, property: the loader reads the actual `data/` directory, validates against `schemas/`, refuses to start on an injected cycle and on an injected dangling ID, and loads the 48 BC-TOP edges as inert.
17. `test_item_verification_tools`, property: for each of the 13 archetypes, a hand-authored item's MathJSON key passes SymPy equivalence, the numeric check and the distractor checks before it reaches `items`, and a seeded bad key is refused [R9].
18. `test_fail_closed_no_item`, property: an archetype whose only item is at `status = 'draft'`, so it has no item at `status = 'verified'` and therefore no published item, is excluded from selection and logged as a coverage gap [R18]. The fixture supplies that archetype, since P1's own 130 items never reach the state.
19. `test_session_assembly_blocks`, property: an assembled session presents blocks 1 to 4 in order, block 1 is capped at 5 items or 5 minutes of forecast, block 2 stops at 25 minutes of forecast or an empty fringe, and the session ends when all four blocks are empty [R5].
20. `test_interleave_max_two`, property: no served set contains 3 consecutive items sharing a primary skill, where the primary skill of an archetype is the first entry of its `skills` array (R25).
21. `test_never_serve_unmastered_prereq`, property: over 1,000 simulated selections against random mastery states drawn over the full 618-row `skills_state` (R25, R27), no archetype is served whose primary skill, the first entry of its `skills` array, has an unmastered hard prerequisite. The random state generator draws `mastered` independently per row and is part of the test, not of the application.
22. `test_prompt_cache_prefix_length`, property: the tutor template's static prefix exceeds 1,024 tokens, which is claude-sonnet-5's minimum cacheable prefix and therefore the one that binds on P1's only routed model, so the prefix is not silently processed uncached (R30) [verified minimum, track 4, https://platform.claude.com/docs/en/build-with-claude/prompt-caching].

End to end:
23. `test_session_login_to_feedback`, property: a passkey login, a full session over the P1 subset, a confidence rating, an elaborated feedback screen, a written error note, and a persisted `skills_state` change, with no network calls outside the recorded cassettes.
24. `test_purge_requires_reauth`, property: purge refuses without a typed confirmation and a passkey re-authentication [R23].
25. `test_reduced_motion_replaces`, property: under `prefers-reduced-motion: reduce` every transform or scale transition is replaced by an opacity cross-fade, and each of the five P1 feedback affordances is still present and still reaches the student: the step-level verification mark at stages example and completion, the elaborated feedback panel at stage unsupported, the confidence prompt, the self-explanation prompt, and the error-note field. That list is the test's domain, and an affordance added later is added to it [verified, https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion].
26. `test_contrast_floors`, property: every text token holds 4.5:1, and `type-title` and `type-display` hold 3:1, in both themes [verified, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html]. The test reads the hex values out of the token file the implementer produces under entry criterion 5 and computes the ratios itself, so it is authorable as soon as that file exists and does not depend on any value being written into a plan document. The pull-request record of the named checker tool and version stands alongside it as the manual cross-check, not in place of it.

Eval:
27. `eval_cold_start_pA_distribution`, property: `p_A_knowledge` is computed for all 139 archetypes at the cold-start state, with `beta_k` averaged over the archetypes that list each skill (R25) and the conjunctive-over-hard-linked rule applied, and the 10th, 50th and 90th percentiles are published. This is a measurement that produces a number, and the 0.3 floor on the 90th percentile is a merge gate on that number rather than an assertion inside the test: the test asserts only that the distribution computes over all 139 archetypes and is finite everywhere. If the published 90th percentile is below 0.3, the 0.35 coefficient and `TARGET_LEARN` are recalibrated together and the distribution is recomputed before merge [R1].
28. `eval_sympy_settle_rate`, property: the share of the 40 `answers_equiv/` pairs that SymPy settles either way, without timing out or returning an undecided comparison, is measured and published. P4's unanimity publication rule is conditional on that rate [R9].
29. `eval_p1_key_error_rate`, a measurement rather than a pass or fail gate, and the only entry in this list that is. On a 100-item sample drawn at random from published P1 items and audited by hand by the operator against the archetype's `expected_solution_path`, the key error rate is measured and reported, where a key error is any item whose stated key is mathematically wrong or whose stem the operator judges ambiguous enough to admit a second correct answer. Ambiguity is an operator judgement and is recorded per item with the second answer the operator found, so the verdict is auditable even though it is not mechanical. What CI checks is that all 100 verdicts exist and that the rate is published; no threshold is set in P1, per exit criterion 4.
30. `eval_p1_distractor_paths`, property: every MCQ distractor carries a non-null `error_path` on its `items.options` entry, resolving to one of the 40 BC-ERR records the P1 skills hold (R26), is not equal to the key symbolically or numerically, and is pairwise distinct from the other distractors. The eval reads `items.options`, never `archetypes.common_distractors`, which is prose and holds no ids.
31. `eval_simulation_mastery_growth`, property: over the 6 synthetic trajectories, mastery per item served exceeds a random-within-fringe control arm run as a separate simulation over the same fixtures. The prerequisite-attribution clause is not asserted in P1: the rule-based assignment can never emit `prerequisite_gap`, so nothing in P1 charges a failure to a prerequisite, and the clause moves to P3 with the diagnostician. What the seeded gap at BC-SKL-02025 does exercise in P1 is gating, since a student who fails its dependants repeatedly should stall rather than progress, and that is what the trajectory is read for here.

### Exit criteria

1. All 31 gates above pass in CI, with output quoted in the pull request.
2. The cold-start `p_A_knowledge` distribution over all 139 archetypes is published in the pull request, with its 90th percentile stated. If that percentile is below 0.3, the coefficient and `TARGET_LEARN` are recalibrated and the distribution is recomputed before merge [R1].
3. The SymPy settle rate on the 40-pair `answers_equiv/` fixture is measured and published in the pull request, as the precondition P4's unanimity rule depends on [R9].
4. The 100-item audited key error sample is complete, with every item's verdict recorded, and the measured key error rate is published in the pull request. No pass threshold is set here because no source gives one; the requirement is that the number exists, is measured rather than estimated, and is carried to 12-open-questions.md as the baseline against which P4 must not regress.
5. A student completes a session over Unit 2 skills and at least one of the P1 BC-SKL records in Unit 2 changes mastery state, with the transition visible in `skills_state` and its six D2 conditions individually satisfiable from `attempts`, which is what `attempts.served_stage` and `attempts.per_skill_states` are there to make possible (R27).
6. At least one skill demonstrates the full mastery path across 3 distinct calendar days spanning at least 7 days, and at least one skill demonstrates un-mastery, dropping below sigma 0.75 or failing at stage unsupported, with the fading stage moving only on the counter [R7].
7. Every one of the 13 archetypes has 10 hand-authored items that passed the SymPy, numeric and distractor checks, each carrying a provenance record with `model = "operator"` (R30), and every MCQ option on those items carries an `error_path` that is a BC-ERR id on each distractor and null on the key (R26).
8. Median cost per served item is recorded, along with the cache read share, over the one wired role. No budget threshold is set in P1; the requirement is the measurement.
9. `qa/12_report.py` still exits 0 on the library, since P1 reads the registries and must not have needed to change them.

### Remaining implementer decisions, fixed here [inferred]

Six small choices that the completion re-check found unstated. None has evidence behind it; each is a convention so that no question remains.

1. Column names drop the `_k` suffix: `beta_k` in 02-adaptive-engine.md is the column `beta` in `skills_state`, and likewise `c`, `f`, `S`, `D`. The formulas keep the subscript.
2. `attempts` carries `snapshot_id`, the content snapshot the item was served under, so an attempt can be reinterpreted after a library update.
3. The confidence rating is collected after the student commits an answer and before feedback at stages `completion` and `unsupported`; at stage `example` no rating is collected, because there is no answer to be confident about.
4. In P1 `desired_retention(today)` returns the constant 0.90; the dated switch to 0.95 arrives with FSRS scheduling in P2 and the function signature does not change.
5. Fixture formats: `student_trajectories/` holds one JSON file per synthetic student with `true_state`, `slip`, `guess`, and `absence_days`; `answers_equiv/` is one JSON array of objects with `left`, `right` (MathJSON) and `equivalent` (boolean); `items_p1/` is one JSON file per item in the 04-item-generation.md output schema with provenance `model = "operator"`.
6. The design tokens file is authored by the implementer in this pull request from the roles in 08-design-brief.md, with every text and background pair checked against a named WCAG 2.2 contrast checker and the checker's output pasted into the pull request; 08 fixes no hex values.

### Risks and rollback

The main modelling risk is the conjunctive-over-hard-prerequisite and compensatory-over-the-rest split, which is the one place the model departs from every published approach and which the ledger flags as [inferred] (track 2 says the compensatory sum is the published default and that the conjunctive product has been explored but not for domain-model search). R1's centred `beta_k` keeps the cold-start prediction off the floor, and gate 27 is what proves it did. If the published distribution or the simulation shows mastery states that do not move, the fallback is a pure compensatory sum behind a configuration flag, which requires no schema change.

The second risk is that 54 skills across 13 archetypes with 1 to 6 skills per archetype leaves per-skill estimates weakly identified, since only 31 of the 541 skills in the library are marked `independently_assessable` and the P1 subset contains few of them. The mitigation is the deliberate variation of archetype skill sets and the uniform random choice inside the fringe, which spreads observations rather than concentrating them; the residual is accepted and instrumented rather than solved.

The third risk is key error in hand-authored items. It is bounded by the 100-item audit and by the rule that an item whose key fails any of the three checks is never published. Hand authoring trades a pipeline risk for an operator-throughput risk, and 130 items is the size of that bet.

Rollback is a revert of the single pull request. The library is untouched by P1, so a revert costs only the application. SQLite data is a single file and is exported before the revert.

## P2 Cold start and scheduling

### Goal

At the end of P2 a new student runs a capped adaptive diagnostic at first login, gets placed across the whole 541-skill graph rather than the 54-skill P1 subset, and from the next day forward receives a genuinely finite due-today queue scheduled against the exam date. Sessions are interleaved to the full D3 constraints, exam weight biases which fringe skill comes next, and the confidence ratings collected since P1 start producing a calibration record.

### Entry criteria

P1 merged with all gates green. The engine's `R_k` term is computed and stored for every observed skill, so the scheduler has something to read.

### Scope

1. **Diagnostic mode** (`app/engine/diagnostic.py`): pick the archetype with `p_A` nearest 0.5 for free response and 0.625 raw for a 4-option MCQ, over the whole graph with unit-level pooling, capped at 30 items, stopping early when entropy over unit-level states stops falling. Skills not resolved are left `not_attempted` and fast-tracked in learning mode.
2. **Whole-graph selection**: the two-term score from P1 extended to the whole 541-skill graph, which is due coverage with uniform random choice inside the fringe for ties and for the no-due case [R4]. The five-term score stays off. `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE` are deferred to a P7 gate and may be turned on only once the P7 simulation shows the five-term score beating the two-term score on mastery per item, not merely beating random. `TARGET_LEARN` 0.8 remains a fading-stage filter rather than a score term. Exam weight and representation coverage still act, as hard constraints on the assembled set rather than as weights.
3. **Review mode and FSRS scheduling**: any mastered skill with `R_k` below desired retention is due; desired retention 0.9 until 15 March 2027 and 0.95 from then to exam day [verified, the trade-off direction, inferred for the schedule]. Repetition compression prefers the archetype covering the most due skills including propagated ancestors.
4. **Full interleaving constraints**: max 2 consecutive same-primary-skill, each block of 10 drawing from at least 4 skills spanning at least 2 units once 2 units are open, and at least 20 percent representation-translation variants over BC-REP pairs [inferred].
5. **Exam-weight priors** from `research/exam/exam-blueprint.md`: BC bands are 5 to 10 percent for Units 1, 2, 3, 4, 7 and 8, 10 to 15 percent for Units 5 and 9, and 15 to 20 percent for Units 6 and 10, on the multiple-choice section only, with no unit weighting published for free response [verified]. Because every band is a range, the prior uses the band midpoint and records that the CED constrains rather than fixes the composition of any one form.
6. **Calibration capture** and the progress screen's calibration curve from 08-design-brief.md.
7. **Onboarding diagnostic screen** and the **long gap** home state (a gap over 21 days routes to a re-diagnostic).
8. **Archetype expansion** to every `no_calculator` archetype whose answer is closed-form across all ten units, so the diagnostic has something to serve outside Units 1 to 3. Those items are hand-authored on the P1 pattern and verified by the same SymPy, numeric and distractor checks, because the generator does not exist until P4 [R9]. The fail-closed rule decides the rest: an archetype with no published item is excluded from selection and logged as a coverage gap, so the diagnostic's reach is whatever the bank covers and is reported as such [R18].
9. New tables in use: `diagnoses`.
10. Prompt templates: none new. P2 adds no provider role, and its items are hand-authored [R9, R17].

### Out of scope

Calculator archetypes, figures, FRQ, grading, the diagnostician, the mastery map as a screen, the review screen.

### Tests that gate the phase

Unit: `test_diagnostic_target_probability` (the selected archetype's `p_A` is the nearest to 0.5, or 0.625 raw for MCQ); `test_entropy_stopping` (the diagnostic stops when unit-level entropy stops falling and never exceeds 30 items); `test_desired_retention_switch` (retention target changes at 15 March 2027 and not before). `test_two_term_selection_whole_graph` (the selected archetype maximises due coverage over the whole graph, and ties resolve uniformly at random inside the fringe, with no five-term weight read) [R4]. Integration: `test_interleave_full_constraints` (every block of 10 draws from at least 4 skills spanning at least 2 units, and at least 20 percent are representation translations); `test_due_queue_finite` (the due queue for any day is finite and its minute estimate is stated); `test_repetition_compression` (among similarly scored candidates the chosen archetype covers the most due skills including 1-hop ancestors). End to end: `test_cold_start_to_first_session` (a new user runs the diagnostic and lands on a populated queue). Eval: `eval_diagnostic_information` (over synthetic students, measures after item 10 move less than before item 10, which is the ALEKS-observed shape [verified, https://www.aleks.com/about_aleks/Science_Behind_ALEKS.pdf]); `eval_selection_bias_control` (a random-within-fringe control arm, run as a separate simulation, is compared against the policy arm on mastery per item and on measurement bias, which is the feedback-loop check 10-quality-and-evaluation.md requires); `eval_two_term_against_five_term` (both scores are simulated side by side and the comparison is recorded as the evidence the P7 gate will rule on, with no change to the live policy in P2) [R4].

### Exit criteria

The diagnostic completes in at most 30 items and stops early on at least half of the synthetic students. A new user reaches a populated, finite, minute-stated due queue on day 2 without operator intervention. Every session produced by the scheduler satisfies the four interleaving constraints, verified over 1,000 simulated sessions with zero violations. The five-term score is still off, and the two-term against five-term comparison is recorded for the P7 gate [R4]. A calibration curve renders from at least 30 real confidence-rated attempts. The random-control arm exists and its comparison is recorded.

### Risks and rollback

The diagnostic's unit-level pooling may place a student wrongly in a unit whose archetypes are heterogeneous; the mitigation is that unresolved skills are left `not_attempted` and fast-tracked rather than assumed mastered, so the error direction is conservative. The desired-retention schedule is [inferred] and is a single configuration value. Rollback is a revert of the phase's pull request; P1 behaviour returns intact, because P1 stubs remain in the codebase behind flags rather than being deleted.

## P3 Free response, grading and diagnosis

### Goal

At the end of P3 a student answers a free-response item the way the exam demands it, inside a unit check, a part drill, a mock or the six-week checkpoint, which are the only four places per-point grading runs [R10, fix 4, fix 5]. The daily micro-session does not capture paper and is not point-graded: it serves MCQ and MathLive short answers, graded deterministically, plus one-sentence justification prompts that the tutor role answers as feedback only and that carry no credit. Inside those four modes the student prints or displays a booklet-shaped page, writes on paper by hand, photographs it, confirms or corrects a rendered read-back of what the app read, and then receives a per-point grading with deterministic checks deciding the mechanical points and a model deciding only justification, interpretation and notation. A diagnostician turns the graded point vector plus the observed work into observed errors with probability-weighted candidate misconceptions, and a review queue holds everything provisional.

### Entry criteria

P2 merged. The transcriber role is wired in the provider layer. `data/scoring_points.json` loads its 76 BC-PT records, and `data/frq_records.json` loads its 249 parts, 227 with points [verified, repo-facts ledger].

### Scope

1. **Booklet-shaped capture**: a printable page that is boxed, unlined, question-addressed and part-addressed, matching the documented booklet, which instructs students to write in pencil or pen with black or dark blue ink, to write answers in the booklet, and that erased or crossed-out work will not be scored [verified, https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf].
2. **Image quality gate** before any grading call: blur, crop, contrast and page-marker detection, because poor image quality is a named failure mode in the applied literature [single-source, https://arxiv.org/abs/2605.19043].
3. **Transcription as an inspectable stage**: the read-back is rendered as math and confirmed or corrected before any point is committed, because roughly 87 percent of the best model's residual errors in the 2026 AIED study were transcription failures rather than rubric misapplication [single-source, same URL].
4. **Per-point grader** (`app/grading/point.py`): one structured call per BC-PT, with deterministic pre-checks deciding the mechanical points, namely SymPy equivalence, numeric to three decimals, bounds match and units present. Two separate rules from the exam's own scoring note govern this, and they are stated separately rather than as one continuous restatement [R21]. The first is that answers need not be simplified and that decimal approximations should be accurate to three places after the decimal point. The grader applies that to the answer value alone. The second is a cap: at most one rounding point is lost per free-response question, so the cap is enforced per question and never per part [verified, https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf].
5. **Disagreement escalation**: each judged point is sampled 2 times at temperature 0 and once at a strictness-varied prompt; any disagreement escalates to `review_queue` and is shown as provisional. Samples are never averaged. This is the ceiling the evidence supports: best reported kappa 0.56 on one grading study and question-level exact agreement at most 0.22 on another [single-source, https://arxiv.org/pdf/2603.00451 and https://arxiv.org/html/2607.01247].
6. **Show the setup** as a first-class rubric field on every calculator-part item, since the 2025 Question 1 stem ends with that instruction and the rubric splits the two points into a formula point and an answer point [verified, https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf].
7. **Diagnostician** (`app/diagnosis/diagnose.py`): input is the graded point vector plus the observed work plus the item's archetype and skills; output is a list of BC-ERR ids or new candidates, each with a probability-weighted list of BC-MIS candidates via `possible_misconceptions` (388 of 390 errors carry that field) and `non_conceptual_causes` (all 390 carry it), never a single cause at probability 1.0. A prerequisite_gap hypothesis is traced through `prereq_edges.csv` from the item's skills using `adaptive.prerequisite_gap_if`. When the top two hypotheses are within 0.2, the leading misconception's `discriminating_probe` is scheduled as the next item; 213 of the 213 active misconceptions carry a probe and 210 carry rivals, out of 236 records in the registry including the 23 retired ones [verified, computed from `data/misconceptions.json` on 2026-09-19]. The earlier "236 of 236 and 233" counted retired records alongside active ones, which is the same registry the 213 active BC-MIS figure in 02-adaptive-engine.md, 06-architecture.md and 10-quality-and-evaluation.md comes from (C13). Output names a mastery_state per loaded skill from the enum, matched where possible to one of the 711 BC-SIG records.
8. **Review screen** from 08-design-brief.md, with the hypercorrection lane, the error notes and the grading disputes.
9. Typed MathLive entry promoted to the secondary FRQ mode and the mode for short answers.
10. New tables in use: `gradings` (one row per point).
11. Prompt templates: `prompts/grader/point_strict_v1.md`, `prompts/grader/point_liberal_v1.md`, `prompts/transcriber/readback_v1.md`, `prompts/diagnostician/error_hypotheses_v1.md`.

### Out of scope

Timed modes, the Bluebook tool set, the full mock, the score band, calculator archetypes, generation beyond the closed-form set.

### Tests that gate the phase

Unit: `test_three_decimal_cap` (at most one rounding point lost per question, never per part); `test_deterministic_precheck_priority` (a mechanical point is never decided by the model when a deterministic check can decide it); `test_diagnosis_never_certain` (no misconception is ever returned at probability 1.0). Integration: `test_readback_gate` (no grading call fires before the student confirms the read-back); `test_image_quality_gate` (a blurred fixture is rejected before any provider call); `test_disagreement_escalates` (a seeded disagreement lands in `review_queue` and is shown provisional, and is never averaged). End to end: `test_paper_to_grade` (print, photograph a fixture page, correct one transcription error, receive per-point grading with one provisional point). Eval: `eval_grader_against_operator_goldens` (operator-authored FRQ-style responses graded by hand against BC-PT definitions, no official responses redistributed, reporting exact agreement and mean absolute error per point); `eval_leniency_calibration` (strict against liberal prompt, reporting the MAE difference, because a liberal policy improved MAE for every model tested in the one study that isolated it [single-source, https://arxiv.org/html/2607.01247]); `eval_transcription_error_share` (of residual grading errors, the share attributable to transcription, to be compared against the 87 percent figure).

### Exit criteria

No point is committed without a confirmed read-back, verified by test and by 20 manual runs. The per-point grader's exact agreement against the operator golden set is measured and published, together with its mean absolute error per point. No threshold is imposed because no published figure exists for LLM agreement with AP Readers on the nine-point scale; the requirement is the measurement and its comparison against the operator set. Every provisional point is reachable from the review screen with a one-click re-read path. The diagnostician returns at least two ranked hypotheses on at least 80 percent of diagnosed errors [untagged target, carried to 12-open-questions.md] and schedules a discriminating probe whenever the top two are within 0.2. Metric 9 is measured and published: free-response items attempted per week during the P3 trial, which must hold a non-zero floor in every trial week, and the read-back abandonment rate, meaning captures started where confirm was never pressed, which is measured and published with no threshold imposed because no source gives one [R11, fix 6].

### Risks and rollback

Grading agreement may prove poor enough that a score is not worth showing. The mitigation is already in the design: every point is provisional until it agrees with itself across samples, and the copy says so. No published source reports how LLM graders handle eligibility-after-error rules, where a wrong earlier step still permits later points, which is a defining feature of AP rubrics and a plausible new failure mode; P3 must instrument it explicitly and carry the result to 12-open-questions.md. Rollback returns the app to typed-answer-only, which P2 already supports.

## P4 Generation at full coverage

### Goal

At the end of P4 the app generates verified items for every active archetype in the library, not only the closed-form no-calculator subset, including calculator-status items and items that carry a figure. Generation runs as a background batch rather than in the student's session, and every published item has passed a Monte Carlo family check and a two-stage duplicate gate.

### Entry criteria

P3 merged. The parameter-spec gap named in D13 item (c) is closed for the archetypes P4 targets, since `safe_variables` and `difficulty_variables` are prose today and generation needs a structured parameter spec per archetype.

### Scope

1. Generation for all 139 active BC-QA archetypes in 77 families, including the 37 `either` and 27 `calculator` archetypes [verified, repo-facts ledger].
2. Figure generation as declarative specs rather than free-form images, with labels and the relevant algebraic step inside the figure, never in a caption, because integrated presentation beat split presentation at g = 0.63 [verified, https://link.springer.com/article/10.1007/s10648-018-9435-9].
3. Monte Carlo family checks over the parameter family, a few hundred draws per archetype, asserting the archetype's declared invariants.
4. Distractor checks: each distractor not equal to the key symbolically and numerically, distractors pairwise distinct, each distractor produced by a named BC-ERR path from the 390 active error records.
5. Calculator-boundary check: every `no_calculator` item must be closed-form solvable.
6. Duplicate gate, two stages: MinHash over 5-grams at Jaccard 0.8 against the official corpus text cache and the generated bank, then embedding cosine at 0.85 [verified, the MinHash configuration, https://arxiv.org/pdf/2107.06499; single-source for the cosine operating point, https://futureagi.com/glossary/cosine-similarity/]. Both thresholds must be validated on a labelled sample rather than adopted as given.
7. Item generation, the independent re-solve and the item review queue, all three moved here from P1 [R9]: `app/generation/generate.py`, `app/generation/verify.py`, the `prompts/generator/*` and `prompts/verifier/*` templates, and human adjudication of every split decision. Publication on unanimous agreement is conditional on the SymPy settle rate P1 measured and published; if that rate leaves too many items undecided, the rule is revised with the measurement recorded rather than kept on faith.
8. Batch API for generation and verification, at 50 percent off input and output, 100,000 requests or 256 MB per batch, most batches finishing under an hour and all expiring at 24 hours, results retained 29 days, with `max_tokens: 0` rejected inside a batch [verified, https://platform.claude.com/docs/en/build-with-claude/batch-processing].
9. Provenance logged per item: archetype, variant, parameter draw, model, prompt version.
10. Copyright rule enforced in code: no official stem, figure or rubric text is ever served, because College Board defines commercial use to include test-prep settings [verified, https://privacy.collegeboard.org/copyright-trademark/request-instructions].
11. Prompt templates: `prompts/generator/symbolic_v1.md` and `prompts/verifier/independent_resolve_v1.md`, both authored here rather than in P1 [R9], plus `prompts/generator/figure_spec_v1.md`, `prompts/generator/calculator_v1.md` and `prompts/verifier/monte_carlo_v1.md`.

### Out of scope

Timed modes, the score band, provider routing beyond Anthropic, the evaluation harness.

### Tests that gate the phase

Unit: `test_no_calculator_closed_form` (every `no_calculator` item is closed-form solvable); `test_distractor_distinct` (no distractor equals the key or another distractor, symbolically or numerically); `test_minhash_threshold` (5-grams, Jaccard 0.8, 256 hashes, on a labelled sample). Integration: `test_monte_carlo_invariants` (a few hundred draws per archetype preserve the declared `invariant_structure`); `test_duplicate_gate_blocks` (an item lightly edited from a cached official stem is blocked at stage one, and a paraphrase is blocked at stage two); `test_no_official_text_served` (no served item's text matches any cached corpus page above the anchor-quote cap). End to end: `test_batch_generation_run` (a batch of generation jobs completes, publishes on unanimous agreement, and queues every split decision). Eval: `eval_p4_key_error_rate`, the same 100-item audited protocol as P1, property: the key error rate does not exceed the P1 baseline; `eval_duplicate_gate_labelled` (precision and recall of both stages on a hand-labelled sample of near-duplicates and true negatives).

### Exit criteria

Every one of the 139 active archetypes has at least 20 published, verified items. The P4 key error rate on the 100-item audit is measured and does not exceed the P1 baseline. The duplicate gate's precision and recall are measured on a labelled sample and the thresholds are either confirmed or adjusted with the evidence recorded. Cost per published item is recorded, with the batch discount visible in the figure. No served item contains official stem, figure or rubric text.

### Risks and rollback

The duplicate thresholds are the main exposure: 0.8 Jaccard is grounded in published deduplication practice, while 0.85 cosine is a practitioner rule of thumb rather than a validated standard, so a bad operating point either blocks good items or leaks near-copies. The mitigation is the labelled sample. The 56 archetypes with no `point_types` and the 36 with no `official_examples` mean difficulty priors for those rest on BC-DF alone, and BC-DF factors carry no numeric weights, so those priors are weaker; P4 must serve those archetypes with a wider exploration share and flag them in provenance. Rollback disables the newly covered archetypes by configuration and returns the served set to the P3 bank.

## P5 Assessment modes

### Goal

At the end of P5 a student can sit a full 2027-shaped mock exam with the documented tool set and hard part boundaries, run a timed part drill at exactly the exam's shape, and take an untimed unit check. They receive pacing metrics and a score band with its assumptions stated, and none of the timed work contaminates their mastery estimates.

### Entry criteria

P4 merged, so the bank can fill a full form. P3's FRQ capture works end to end.

### Scope

1. **Unit check**: untimed, 8 to 12 items spanning every fringe-adjacent skill of the unit, updating the model [inferred].
2. **Timed part drills** at exactly the four part shapes: 29 questions in 62 minutes with no calculator, 13 in 38 minutes with a calculator, 2 in 30 minutes with a calculator, 4 in 60 minutes with no calculator [verified, research/exam/exam-structure.md].
3. **Bluebook tool set**: a hideable timer with a five-minute alert, highlight and notes, mark for review, option eliminator, a question menu showing skipped and flagged questions, and zoom, with a Desmos-equivalent graphing panel present only on calculator parts [verified, https://bluebook.collegeboard.org/students/tools].
4. **Hard part boundaries**: the calculator control is removed rather than disabled on no-calculator parts, and a closed part cannot be reopened, because every documented fidelity cue attaches to a part boundary [verified, https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf].
5. **Full mock** on the 2027 form shape, 42 multiple choice and 6 free response, 9 points per free-response question, Section I and Section II at 50 percent each, 3 hours 10 minutes of testing time, cadence every 4 to 6 weeks and more often in the final 8 weeks [verified, the structure, research/exam/exam-structure.md; inferred for the cadence].
6. **Pacing metrics only**: timed sessions update pacing, never mastery state, because speededness contaminates ability estimates [single-source]. Their graded errors still feed the diagnostician for feedback.
7. **Score band**: never a single number. Per-question FRQ means against published 2023 to 2025 means, plus a band with stated assumptions, because section weights are published at 50/50 while cut points are unpublished, the uncertainty is at least one full score point, and the 2027 form is new.
8. **Radian-mode note** carried on calculator items, since the 2025 Question 1 stem carries that parenthetical and an app that never shows a mode setting silently drops it [single-source, https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf].
9. **Reference sheet treated as absent** until confirmed, which is the conservative direction: if a sheet does exist the student is over-prepared rather than under-prepared [verified that the Bluebook tools page mentions a reference sheet generically and does not name AP Calculus, https://bluebook.collegeboard.org/students/tools; the question is uncertain].
10. Mock screens and the mock history section of progress, from 08-design-brief.md.

### Out of scope

Provider routing and fallbacks, the evaluation harness, the design-system completion pass.

### Tests that gate the phase

Unit: `test_part_shapes` (each of the four drills has exactly the documented count and duration); `test_timed_does_not_update_mastery` (no `skills_state` row changes during a timed session); `test_score_band_never_single_number` (the result payload always carries a band and an assumptions list). Integration: `test_calculator_lockout` (the calculator control is absent, not disabled, on Section I Part A and Section II Part B); `test_part_boundary_closed` (a closed part cannot be reopened); `test_tool_set_present` (the six tools 05-assessment-modes.md selects are present, and the graphing panel only on calculator parts; Bluebook documents eight and the six are the product's deliberate subset) [R22, fix 40]. End to end: `test_full_mock_run` (a complete 42 plus 6 run including booklet capture, read-back and grading, with pacing metrics recorded and mastery untouched). Eval: `eval_mock_against_published_means` (per-question means compared against published 2023, 2024 and 2025 means); `eval_pacing_metrics` (time per question by part, against the documented per-part budgets).

### Exit criteria

A full mock runs end to end at the exact documented shape, including the paper capture path, in a single sitting. No `skills_state` row changes during any timed session, verified over 20 runs. The score result carries a band and its assumptions and never a single predicted score. Pacing metrics render per part. The reference-sheet question and the Desmos-variant question are both still open and are restated in 12-open-questions.md with what would settle them.

### Risks and rollback

The 2027 booklet layout under the revised 42-question Section I is an assumption: the booklet overview is effective January 2026 and describes the 2026 administration, and full-length 2027 sample booklets were promised for early 2027 and are not yet available. The mock must therefore be built so that the booklet template is data, not code. Rollback disables the mock and the timed drills by configuration and leaves unit checks, which do not depend on the booklet shape.

## P6 Provider layer completion

### Goal

At the end of P6 every role routes through a configured provider with a fallback chain, a per-role daily budget, and a cooldown, and the operator can switch providers from settings without touching code. Offline sessions keep running on pre-generated items.

### Entry criteria

P5 merged. Every prompt template in the repo has a golden test.

### Scope

1. Role routing for tutor, generator, verifier, grader, diagnostician and transcriber, with the D8 default: Anthropic first, claude-opus-5 for generator, verifier and diagnostician, claude-sonnet-5 for tutor and per-point grader, claude-haiku-4-5 for transcription quality gate.
2. Gemini 3.8 Flash as second tier for bulk grading and batch verification, priced at $0.75 in and $3.75 out per 1M through 31 December 2026 and $1.50 / $7.50 after, with implicit caching requiring a 4,096-token minimum on the 3.x Flash line and cache reads at $0.075 per 1M through the same date [verified, https://ai.google.dev/gemini-api/docs/pricing and https://ai.google.dev/gemini-api/docs/caching].
3. Ollama with DeepSeek-R1-Distill-Qwen-14B as the offline fallback, keeping sessions running on pre-generated items and never acting as a grading peer. That model is the smallest officially documented option above 93 on MATH-500, at 93.9 with AIME 2024 at 69.7 [verified, https://huggingface.co/deepseek-ai/DeepSeek-R1]. VRAM per quantisation is not published in any official Ollama page and must be measured rather than assumed.
4. OpenAI adapter supported but off by default; OpenRouter adapter supported but not in the hot path. OpenRouter's SSE stream emits keepalive comment lines that must be skipped before JSON parsing, and mid-stream errors arrive as an event with `finish_reason: "error"` under a 200 OK, which is a real trap for a naive client [verified, https://openrouter.ai/docs/api-reference/streaming].
5. Fallback chain per role with cooldowns and pre-call context checks, shaped like a LiteLLM router, with the provider interface shaped like the AI SDK language-model specification.
6. Per-role daily budget caps enforced before the call, with the running total shown in settings.
7. claudebox adapter behind the D8 guard: disabled by default, enabling requires `CLAUDEBOX_SINGLE_OPERATOR=1` plus a typed acknowledgement, binds only to localhost, refuses to start if the app has more than one user record, and is not routable for the tutor role because it has no streaming path. Its warning copy is the text in 08-design-brief.md and states the consumer-terms constraints: account credentials may not be shared and the account may not be made available to anyone else, and the Services may not be accessed by automated or non-human means except via an API key [verified, https://www.anthropic.com/legal/consumer-terms]. Note also that claudebox's inbound authentication is bypassed entirely when `CLAUDEBOX_API_KEY` is unset, so anyone reaching the port can spend the operator's subscription [verified, its `server.js`], and that its licence is contested, with the GitHub API returning no license object while the README text says MIT [verified, https://api.github.com/repos/ArmanJR/claudebox].
8. Prompt template golden tests for every template in the repo.

### Out of scope

The evaluation harness, multi-user, the accessibility pass.

### Tests that gate the phase

Unit: `test_budget_blocks_before_call` (a role over its daily cap never issues the request); `test_claudebox_guard` (the adapter refuses to start without the environment variable, without the typed acknowledgement, on a non-localhost bind, or with more than one user row, and is never selectable for the tutor role); `test_openrouter_stream_parser` (keepalive comment lines are skipped and a mid-stream `finish_reason: "error"` under a 200 is surfaced as a failure). Integration: `test_fallback_chain` (a seeded 429 on the primary moves the role to the next provider and applies the cooldown); `test_offline_session` (with the network down, a session runs to completion on pre-generated items and no grading peer is Ollama). End to end: `test_provider_switch_from_settings` (changing a role's provider in settings takes effect on the next call with no restart). Eval: `eval_prompt_goldens` (every template produces schema-valid output against its recorded golden); `eval_cross_provider_grading_agreement` (Anthropic against Gemini on the same operator golden set, reporting agreement per point).

### Exit criteria

Every role has at least one configured fallback and a cooldown, exercised by test. Budgets block before the call, not after, verified per role. claudebox fails closed on all four guard conditions. An offline session completes with the network disabled. Cross-provider grading agreement is measured and recorded; no threshold is imposed, since no published figure exists.

### Risks and rollback

Provider drift is the standing risk: model IDs, prices and caching minimums in the ledgers are as of September 2026 and every one of them can change. The mitigation is that prices and limits live in configuration with their source URL beside them, never in code. The claudebox path carries a terms-of-service exposure the tool's own README does not warn about, which is why it fails closed on four independent conditions. Rollback pins every role back to Anthropic.

## P7 Evaluation harness

### Goal

At the end of P7 the operator can answer, with evidence, whether the system is teaching anything. Golden sets, offline simulation against synthetic students, a metrics view, A/B switches, and a 6-week released-material checkpoint flow all exist and run.

### Entry criteria

P6 merged. At least 8 weeks of real attempt data exists for one student, so the metrics have something to compute over.

### Scope

1. Golden sets: generated items hand-verified by the operator, and FRQ-style responses authored by the operator and graded by hand against BC-PT definitions. No official responses are redistributed.
2. Offline simulation: synthetic students with a hidden true state over the real 541-skill graph, with forgetting, slip and guess rates, comparing policies on mastery per item and on measurement bias, with a random-selection control arm as the feedback-loop check.
3. Learning metrics: mastery growth per study hour, retention at 7 and 30 days measured as first-attempt accuracy on due reviews, mock trajectory against published distributions, calibration as Brier and confidence minus accuracy, method-selection accuracy tracked separately from execution accuracy, and error-type recurrence rate after diagnosis.
4. A/B switches, per-item randomisation within one student: elaborated against verification-only feedback, and retrieval entry after 1 against 3 unaided successes. Both are within-student designs a single student can power over a few months.
5. The 6-week released-material checkpoint flow, which is the direct answer to local-test inflation, since intelligent tutoring systems raised scores by a median 0.66 standard deviations but the effect was much larger on locally developed tests than on standardized tests [verified, Kulik and Fletcher 2016, https://journals.sagepub.com/doi/abs/10.3102/0034654315581420].
6. A stable internal concept probe, a fixed item set never used for practice, administered every 8 weeks, reported separately from practice accuracy.
7. Progress screen completion: the representation matrix and the checkpoint history.
8. **The five-term selection gate** [R4]: the two-term score that P1 and P2 run is simulated against the five-term score on mastery per item over the synthetic trajectories. `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE` may be turned on in the live policy only if the five-term score wins that comparison. Beating random selection is not sufficient and is not the bar.

### Out of scope

The design-system completion pass, multi-user, data export and purge beyond what P1 shipped.

### Tests that gate the phase

Unit: `test_brier_and_calibration` (the calibration metrics compute correctly on fixtures with known answers); `test_ab_assignment_balanced` (per-item randomisation is balanced within skill). Integration: `test_simulation_reproducible` (a fixed seed reproduces the trajectory exactly); `test_checkpoint_isolated` (checkpoint items never enter the practice pool and never update mastery). End to end: `test_metrics_view_renders` (every metric renders from real data with its denominator stated). Eval: `eval_policy_against_random_control` (the policy arm beats random-within-fringe on mastery per item, and the measurement bias of both is reported); `eval_five_term_against_two_term` (the five-term score is compared against the live two-term score on mastery per item, and the result is what decides whether the five terms are enabled) [R4]; `eval_retention_7_30` (first-attempt accuracy on due reviews at 7 and 30 days).

### Exit criteria

Every learning metric renders with its denominator stated, because a count without a denominator is not a claim. The simulation reproduces exactly from a seed. At least one A/B has accumulated enough within-student items for its comparison to be stated with an interval. The first 6-week checkpoint against released material has run and its result is recorded alongside the internal numbers for the same period. The expectation recorded against that checkpoint is d = 0.4 to 0.7 against a standardized criterion, not two sigma [single-source, the Kulik, Kulik and Bangert-Drowns 1990 half of the range; verified for Kulik and Fletcher 2016, https://journals.sagepub.com/doi/abs/10.3102/0034654315581420] [R20, T2].

### Risks and rollback

A single student cannot power most comparisons, which is why the designs here are within-student and per-item. The honest risk is that the checkpoint shows the internal numbers moving and the criterion not moving, which is exactly the finding the harness exists to detect and is not a reason to weaken the checkpoint. Rollback removes the metrics view and leaves the raw tables, which are the actual evidence.

## P8 Design system, accessibility and multi-user readiness

### Goal

At the end of P8 every screen is built from the token set rather than from ad hoc values, the accessibility floor is verified rather than asserted, the app can run on Postgres with more than one user and per-user budgets, and a student can export everything and purge everything.

### Entry criteria

P7 merged. Every screen in 08-design-brief.md exists in some form.

### Scope

1. Token audit: every colour, size, spacing and duration in the codebase resolves to a token from 08-design-brief.md, with zero literal values outside the token file.
2. Both themes completed as independent HSL shade sets with reduced saturation at low lightness, not as inversions.
3. Accessibility pass: keyboard operability of every primary action, focus order following reading order, no focus trap outside dismissible modals, math exposed to screen readers via MathLive's math-to-speech and ARIA labels and via MathML output from the renderer, colour independence verified by greyscale render on every screen, and reduced motion replacing rather than removing.
4. Contrast verification at 4.5:1 for body and below and 3:1 for the two large steps, in both themes [verified, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html]. The WCAG 1.4.11 non-text ratio must be fetched in this phase and applied to the mastery map's node borders and the calibration curve's axes; it is unknown today.
5. Multi-user readiness: Postgres migration path exercised, per-user budgets, and the claudebox guard's single-user refusal verified against a multi-row `users` table.
6. Data export and purge: full JSON export, FRQ image deletion, and a purge path, with a default retention of until 30 days after the exam date [decisions memo D10]. The exam date is Monday 10 May 2027 [single-source, research/exam/exam-structure.md].
7. Model output treated as untrusted data throughout: rendered as text or KaTeX, never executed, never used as instructions to tools, with generated items sanitised before rendering and the tutor holding no tools [decisions memo D10].

### Out of scope

Nothing is deferred past P8. Anything not done here is a defect, not a phase.

### Tests that gate the phase

Unit: `test_no_literal_values` (a lint rule failing on any colour, size, spacing or duration literal outside the token file); `test_retention_default` (the purge date computes to 30 days after 10 May 2027). Integration: `test_postgres_parity` (the full test suite passes against Postgres as well as SQLite); `test_per_user_budget_isolation` (one user's spend never draws on another's cap); `test_claudebox_refuses_multi_user` (the adapter refuses to start with two rows in `users`). End to end: `test_keyboard_only_session` (a complete session with no pointer events); `test_export_then_purge` (export produces a complete JSON, purge removes everything, and the export still opens). Eval: `eval_contrast_all_screens` (every screen in both themes against the 4.5:1 and 3:1 floors); `eval_screen_reader_math` (every math region exposes structure, not glyph soup); `eval_greyscale_states` (no state is lost when colour is removed).

### Exit criteria

Zero literal design values outside the token file. Every screen passes the contrast floors in both themes. A full session completes with no pointer events. Every math region reads as structure under a screen reader. Every screen survives a greyscale render with no state lost. The suite passes against Postgres. Export produces a complete archive and purge removes everything, verified by re-reading the database after purge.

### Risks and rollback

MathLive's licence is unconfirmed in the ledgers and must be read out of the installed package before P8 merges; if it is incompatible, the typed-input path needs a replacement and MathQuill is not it, since its public repository is now published as an archive [single-source, https://github.com/desmosinc/mathquill-archive]. The WCAG 1.4.11 ratio is unknown today and P8 cannot exit without it. Rollback here is partial by nature: the token audit and the accessibility fixes are safe to keep even if the Postgres work is reverted.

## Dependency order

```
                        library registries under data/
                                     |
                                     v
  P1  loader, engine core, fading ladder, session assembly,
      130 hand-authored items plus SymPy, numeric and
      distractor checks, Anthropic tutor only, SQLite, passkeys
                    |                          |
                    v                          v
  P2  diagnostic, whole-graph        P4  generator, re-solve and
      two-term selection, FSRS           item review queue, all 139
      review, interleaving,              archetypes, figures, Monte
      calibration capture                Carlo, duplicate gate, batch
                    |                          |
                    v                          |
  P3  FRQ capture, read-back,                  |
      per-point grading, SymPy                 |
      pre-checks, diagnostician,               |
      review queue                             |
                    |                          |
                    +-------------+------------+
                                  v
  P5  unit checks, timed part drills, Bluebook tools,
      full 2027 mock, pacing metrics, score band
                                  |
                                  v
  P6  role routing, fallbacks, budgets, Gemini, Ollama,
      OpenAI, OpenRouter, claudebox guard, prompt goldens
                                  |
                                  v
  P7  golden sets, offline simulation, metrics,
      A/B switches, 6-week checkpoint flow
                                  |
                                  v
  P8  token audit, accessibility pass, Postgres,
      per-user budgets, export and purge
```

Two edges are worth naming because they are the only places the order could be argued. P4 builds the generator and the independent re-solve itself [R9], depends on P1 only for the SymPy, numeric and distractor checks and for the measured settle rate, and depends on nothing in P2 or P3, so it can be built in parallel with P3 by a second worker; it is placed after P3 in the sequence only because P5 needs both and one pull request at a time is the working rule. P3 depends on P2 rather than on P1 alone, because the diagnostician traces prerequisite gaps through the whole graph and that tracing is only meaningful once the student has a whole-graph state.

## What each phase is not allowed to defer

P1 may not defer: the acyclicity check and the refusal to start on a dangling ID; the fringe restriction, so an archetype whose hard prerequisites are unmastered is never served outside diagnostic mode; the confidence rating before feedback, because retrofitting it later loses the entire calibration history; withholding feedback until submission on unsupported items; the student-authored error note before the retry is scheduled; passkey-only authentication with re-authentication on purge, and encrypted provider keys; the cold-start `p_A_knowledge` distribution over all 139 archetypes, because a policy calibrated wrong at cold start is wrong for the whole phase [R1]; the SymPy settle rate on the 40-pair fixture, because P4's publication rule depends on it [R9]; and the 100-item audited key error sample, which is the baseline every later phase is measured against.

P2 may not defer: the diagnostic cap at 30 items; uniform random choice inside the fringe, which under the two-term score is how ties and the no-due case resolve and is what keeps the feedback-loop bias the adaptive-engine literature warns about from forming [R4]; the separate random-selection control arm, since a control added later cannot reconstruct the history; and the finite due queue, since an infinite queue is the streak mechanic in disguise.

P3 may not defer: the restriction of per-point grading to unit checks, part drills, mocks and the six-week checkpoint [R10]; metric 9's weekly free-response attempt floor and its published abandonment rate [R11]; the confirmed read-back before any point is committed; the deterministic pre-checks taking priority over the model on mechanical points; the multi-sample disagreement escalation with no averaging; and the rule that a diagnosis never returns a single cause at probability 1.0.

P4 may not defer: the duplicate gate on both stages; the rule that no official stem, figure or rubric text is ever served; and per-item provenance, because provenance cannot be reconstructed after the fact and is the defensible answer if a copyright question is raised.

P5 may not defer: the hard part boundaries with the calculator control absent rather than disabled; the rule that timed sessions update pacing and never mastery; and the score band with stated assumptions instead of a single predicted score.

P6 may not defer: budgets blocking before the call; the claudebox guard's four failure-closed conditions; and treating model output as untrusted data.

P7 may not defer: the denominator on every reported count; the random-selection control arm; and the released-material checkpoint, which is the only thing standing between this project and local-test inflation.

P8 may not defer: anything. It is the last phase and its scope is the remainder.

## Library work that must land before each phase

From decision D13. The library is a separate workstream and the application cannot invent these records.

Before P1: nothing blocking. The 13 archetypes, their 54 skills, their 74 signals, 40 errors and 20 misconceptions are all present and complete enough to build against. One caution: BC-DF factors carry no numeric weights, so the `beta_k` prior is [inferred] and must be registered as a tunable in 12-open-questions.md rather than presented as calibrated. A second caution: gap (d), BC-SKL-02001 has no archetype, so it is simply not servable and must be excluded from any fringe computation rather than silently failing.

Before P2: exam-blueprint unit weights are already verified and are enough for the `w_weight` term, but every band is a range and the plan must use midpoints and say so. Gap (e), 10 block-99 misconceptions link to no skill or archetype, must be resolved or explicitly excluded, since the whole-graph diagnostic will otherwise reach records it cannot attach to anything.

Before P3: gap (a) is blocking for FRQ grading, because 56 active archetypes have no `point_types` and their free-response variants therefore cannot be point-graded; those 56 are listed in the repo-facts ledger and P3 must either land their point types or restrict FRQ mode to the 83 archetypes that have them. Gap (f), the 2018 FRQ records carry no points, must be filled or those records excluded from the means comparison. Gap (g), the sg-24 derived records are OCR single-source, must be re-verified before they anchor any grading calibration.

Before P4: gap (c) is blocking, since `safe_variables` and `difficulty_variables` are prose today and generation at full coverage needs a machine-readable parameter spec per archetype. Gap (b), 36 archetypes have no official examples, is not blocking but must be flagged in provenance so those items carry a wider exploration share. Gap (i), BC-DF factors carry no numeric weights, is the same caution as P1 and now affects 139 archetypes rather than 13.

Before P5: gap (k) is the sharp one. `research/exam/exam-structure.md` is silent on the Bluebook tool set and on whether a reference sheet is shown for AP Calculus, and track 3 records this as an open conflict: the Bluebook tools page states generically that a reference sheet with commonly used formulas appears on all tests with math questions, it is written for the SAT suite as well as AP, it does not name AP Calculus, and the Calculus scoring guidelines and CED do not mention one. P5 builds on the assumption that no sheet is supplied, which is the conservative direction, and the conflict stays open. Gap (l), whether the Bluebook Desmos meets all four CED calculator capabilities, is also unresolved and must be restated in 12-open-questions.md rather than assumed. Gap (h), the 2026 samples, statistics, distributions and Chief Reader report are not yet published, bounds what the score band can be compared against.

Before P6: nothing from the library. The blocking work is provider documentation, which changes underneath the plan and must be re-fetched at the start of the phase rather than trusted from the September 2026 ledgers.

Before P7: gap (h) again, since the 6-week checkpoint flow needs released material and the most recent statistics and distributions. Gap (j), misconception literature citations are single-source, bounds how strongly any diagnosis-driven metric can be stated.

Before P8: nothing from the library.

## Decisions the decisions memo did not settle

Three, carried to 12-open-questions.md rather than invented here. R1 to R24 settled everything else this plan previously left open, including the 24 completion questions the adversarial review raised against P1; these three are what the R decisions deliberately did not close.

First, no pass threshold for the P1 key error rate. D12 requires that the rate be measured on a 100-item audited sample and does not name an acceptable value, and no source in any ledger gives one, so this plan requires the measurement and makes P4 unable to regress against it. R9 moved the generator to P4 and left the audit where it was, so the open question is unchanged: the items are now hand-authored and the operator still solves 100 of them without the key.

Second, no agreement threshold for the per-point grader. D4 fixes the sampling and escalation design and cites kappa at best 0.56 and exact agreement at most 0.22, but it does not say at what agreement the app should stop showing scores at all. The plan keeps every point provisional and measures agreement; the stopping rule is open.

Third, whether P4 may proceed in parallel with P3. D12 lists the phases as one pull request each in a linear order but does not say whether two may be open at once, and the dependency graph shows P4 needs nothing from P2 or P3. This plan keeps them serial and records that the constraint is the working rule, not a technical one.
