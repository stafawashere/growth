---
title: P4 item generation at full coverage
research_date: 2026-09-24
status: complete
purpose: The canonical record of stage 5 (docs/plan/11 P4): how every active archetype got a structured parameter spec and a gated template, how the generated items were verified and published, and the measurements the exit criteria ask for.
---

# P4 item generation at full coverage

## Result [verified]

Every one of the 139 active archetypes has at least 20 published, verified items: the smallest
archetype holds 20, the bank serves 3,125 items, and 2,339 of them are generated items in
`content/items_gen_unit01` to `content/items_gen_unit10`. Each generated item passed the record
checks ingest runs, the template's own SymPy answer rebuilt from its seed, a blind formulation
written from the stem alone, the calculator boundary and both stages of the duplicate gate, and was
signed off with `tools/sign_off_items.py --by "claude-opus-5-5 on the operator's delegation of
2026-09-24, docs/operator/p4-generation.md"`. The P4 key audit is 0/100 (Wilson 95 percent upper
bound 0.037), not above the P1 baseline ([key-audit-p4/](key-audit-p4/)). The duplicate gate was
measured on four labelled samples ([duplicate-gate/](duplicate-gate/)).

## How an item is made [verified]

1. **Parameter spec.** Every archetype carries `parameter_spec` in `data/archetypes.json`, validated
   by `schemas/archetypes.schema.json` `$defs/parameter_spec` and by `app/generation/spec.py`
   against its own archetype (typed parameters with a `safe` or `difficulty` role and an explicit
   domain, evaluable constraints and invariants, dial bindings to the archetype's BC-DF dials, a
   calculator guard, representation bindings). The spec is proposed by the template module and
   reaches the registry only through `data/staging/parameter-spec-p4.json`, a `"merge": "fields"`
   staging file `tools/merge_staging.py` applies without touching any other field.
   `tests/generation/test_parameter_specs.py` holds all 139 to the schema and to their templates.
2. **Template.** `app/generation/templates/qa_<digits>.py` builds one item from one draw: stem, key
   (exact, three-decimal on calculator items, or a labelled statement), worked steps, three
   distractors each derived by making a named BC-ERR error, and a declarative figure where the
   representation needs one. Eight Claude Code sessions authored the 139 templates offline from
   `prompts/generator/template_v1.md`, `figure_spec_v1.md` and `calculator_v1.md`.
3. **Template gate and Monte Carlo pass.** `tools/template_gate.py` (`app/generation/template.py`)
   draws 300 parameter tuples per template and fails the family on a single bad draw: invariants,
   pairwise distinct options (exact, and at three decimals), error paths held by the archetype's
   skills, the last valued step equal to the key, no vacuous step, exact keys and no numeric method
   on no-calculator templates, the setup asked for on calculator items, figure and label rules,
   parallel statement labels, at least 2,000 constraint-satisfying tuples, at least 100 distinct
   problems, and safe parameters that never change the solution path. `test_monte_carlo_invariants`
   reruns all 139.
4. **Instantiation.** `tools/generate_bank.py plan` draws seeds, aims each draw at a requested
   success probability spread over what the family can realise, and writes candidates with their
   provenance (template, seed, draw, spec version, author, prompt version, content snapshot). It runs
   offline, outside any student session.
5. **Blind re-solve.** Fourteen separate Claude Code sessions, following
   `prompts/verifier/independent_resolve_v1.md`, received stems, figure data and statement choices
   only and wrote `formulations_<batch>.py`; `tools/key_recheck.py --template-answers` compares their
   answers and the template's own answers with every key, with its planted-error control.
   `app/generation/batch_api.py` builds and prices the same re-solve as a Message Batches job, the
   paid fallback, which was never sent.
6. **Publication.** `tools/generate_bank.py publish` runs `app/generation/verify.py`: unanimity
   publishes; anything else goes to `content/generation_review/` with the rule that stopped it.
   `tools/item_review.py` shows a held item as 04 describes and records each decision in
   `content/generation_review/decisions.json`; rejected items are kept with their provenance.

## Numbers [verified]

- 2,437 candidates: 2,339 published and 98 rejected. 187 review decisions: 71 approvals (66
  duplicate sets settled with the first copy kept, and 5 keys the blind solver got wrong by
  dropping absolute values, verified by differentiation on every side of the roots) and 116
  rejections (72 duplicates of a kept or served item, and 44 items of two templates retired when
  their families were widened).
- Defects the blind solvers found in templates before publication, each fixed in the template and
  the affected items regenerated: a false premise in BC-QA-99001 (the stated point was not on the
  curve), second defensible choices in 02004, 05003, 05005 and seven group A templates, the
  "must there be" wording of 05001 (by Darboux a c exists, so the key had to be about what the Mean
  Value Theorem guarantees), a same-function "forgot C" distractor in 06008, and an absolute value
  the recheck could not see in 06010.
- 47 BC-ERR records gained skills through `data/staging/error-links-p4.json` (an `"append"` staging
  file), each link proposed by a template author with its reason and read before merging.

## Cost [verified]

API spend for the whole stage: $0.00. Templates were authored and items re-solved in Claude Code
sessions on the operator's subscription (docs/operator/offline-authoring.md), and no paid call was
made. Bought on the API at `tools/cost_model.py`'s per-call figures for the Claude-only routing
(claude-opus-5-5 authoring at 2.5 attempts per template, claude-haiku-4-5 re-solving each
candidate), `tools/p4_cost.py` prices the same work at $51.27 at list price and $25.64 with the
Batch API's 50 percent discount: $0.0219 per published item at list, $0.0110 with the batch
discount. The subscription sessions reported at least 2.8 million tokens for template authoring (one of
eight authoring sessions was cut off by a usage limit before it reported) and about 2.4 million for
the blind re-solves; those are subscription usage, not API spend.

## Open [inferred]

- Heavy paraphrase of official text is caught on 40 to 55 percent of the labelled pairs; the
  residual rests on construction (no official text given to any author or solver) and on the
  25-word span check.
- The keys were checked by the same model family three ways; the operator has not read them.
- Predicted success probabilities come from the BC-DF dial arithmetic of 04, whose 0.35-logit
  step is unmeasured (D13 item i).
