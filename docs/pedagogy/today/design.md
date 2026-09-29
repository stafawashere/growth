---
title: Today redesign, what is built
research_date: 2026-09-29
status: draft
purpose: The decisions the redesign builds from the gap analysis, each tied to a measured flaw (T1 to T25), the evidence behind it and the rule that bounds it, and what lands in production against what lands behind a switch.
---

# Today redesign, what is built

Every decision names the flaw it answers in `growth-gap-analysis.md`, the evidence in `synthesis.md` or `science.md`, and where it lands. The ground rules bound all of it: no schedule, quota, timer or target shown; the set ends when the blocks are empty; only deterministic grading feeds mastery; no praise, advice or prediction talk; gates strengthened, never loosened; an algorithm change ships only on the simulator bar, otherwise behind a switch, default off.

## The selection policy [inferred]

D1. Retrievability priority (T1, T2; synthesis rank 1; science.md 1). A shared engine function orders candidates by the sum of `1 - R_k` over the skills an archetype reaches (its loaded skills and their 1-hop gating parents) that carry a memory state, highest first, then due coverage, then the seeded uniform draw. It is the engine-side form of the forgetting oracle and reads state that already exists. It is built into `app/engine` so the simulator and the app run one implementation, and it is applied to block 2 and block 3 through the ordering hooks the simulator already uses.

D2. Where it lands is decided by `simulation-record.md`: it replaces two-term in production only if its paired mean difference against two-term on delayed mastery per item and on retention at day 30 has a 95 percent interval wholly above 0 under both forgetting curves on the fixed world at 60 and 226 days, with skills learned not lower on the same reading. Otherwise it ships behind the switch `selection_priority` in `app/experiments/switches.py` (control `two_term`, treatment `retrievability_priority`, unit the session, default off), so the within-student A/B of plan 10 can decide on delayed checkpoint accuracy.

D3. The other candidates (`elo_target`, `spread`, `review_first`) stay in `app/sim` as arms and are not ported unless one clears the bar.

D4. No FSRS parameter, mastery threshold, block cap or retrieval floor moves. The block 1 cap and the review floor are rulings C1 and C2; the redesign instruments them instead: every due skill left unserved is written to the coverage-gap audit with its reason (no published item, below the retrieval floor, refused by the window, past the block cap), so the operator's ruling rests on counts (T3, T17).

## Session assembly and feedback [inferred]

D5. The wrong-answer feedback shows what the correct response would have been (T16; plan 03 Content part 3; synthesis rank 5). The feedback payload gains the item's correct answer (the key's MathJSON, or the keyed option's label for a choice) and the client shows it after the violated step as the step's correct result. Nothing is shown before submission, so the timing rule holds, and nothing credits anything.

D6. The math field commits before the check (T18). The client reads the field's current value at submit time and refuses to check an empty short answer, so an attempt is never written with a null answer by a fast click. A server-side refusal of a null short answer is not added, because tests that post ungraded attempts rely on the current route; it is listed in the rulings file.

D7. The opener and the reinforcement sentence degrade in words when the tutor is off (T23): the opener's feedback states that the comparison needs the tutor and shows the canonical worked solution's first step instead of an empty panel. No model call is added.

D8. The requeue lane, the hypercorrection lane, the self-explanation prompt and the error note keep their plan 03 behaviour; they were found working on the walk.

## The day screen [inferred]

D9. Today states the whole due queue when block 1 cannot hold it (T17; synthesis rank 6): a line under the counts reads "N more skills are due today, about M minutes, beyond this set" from `due_today_skills` and `due_today_minutes`, which the payload already carries. It is a count, not a target, and it disappears at 0.

D10. The mixed-practice card names units and a count, not skills (T20; rulings R10). The review and new-ground cards keep their skill lists.

D11. The pace verdict stays until the operator rules (T21; C5). The end screen keeps its two sentences; the ungraded-attempt case of T22 disappears with D6.

D12. Typography and spacing come from `app/design/growth-tokens.json`, the column stays full width, and no footer is added.

## Question standards [inferred]

D13. The nine lints in `app/items/standards.py` stand: five run by default (calculator decimals, choice-worded short answer, command verb, stem length, no all-or-none) because the operator's fixture passes them, and four run under `--standards` (option count, distinct error paths, value option type, distractor provenance) because the fixture would fail them and a fixture is never edited to pass. The default set is a strengthening of `tools/check_items.py`; moving the other four into the default is ruling C8.

D14. The fix order, each item through the pipeline (check, blind re-solve on a stems-only file, distractor-path check, duplicate gate), committed per unit: the 22 sample items with a verdict (T8 to T11), then the 98 records that fail a default lint, then `distinct_error_paths` unit by unit for as long as the run allows, with the remainder counted in the handoff. No item is relabelled; drafts stay drafts.

D15. New items are drafted only for a measured gap (T12, T13): calculator items on archetypes with none, and tabular or graphical variants where an archetype has no representation but symbolic, under the draft provenance and the plan 04 contract, through the same pipeline. Drafting is last in order and is counted in the handoff if not reached.

## What is not built and why [inferred]

The wider block 1 cap and the lower retrieval floor (C1, C2), the uncredited retry (C3), the sibling requeue (C4), the pace verdict's removal (C5) and the choice of block (C6) each change a plan rule or a threshold and wait for the operator. The fringe breadth on a fresh student (T24) and the placement's unit order (T25) belong to the diagnostic and gating, outside this brief; both are recorded for the operator.
