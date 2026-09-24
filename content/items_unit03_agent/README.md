---
title: Unit 3 item bank, stage 1
research_date: 2026-09-24
status: signed_off
purpose: Says what the 20 item records in this directory are, how they were checked, and where their scope rule lives.
---

# Unit 3 item bank, stage 1 [verified]

20 agent-drafted items, by archetype: BC-QA-03009 20. Each record is in the output schema of docs/plan/04-item-generation.md with four options, one key and three distractors, each distractor tagged with a BC-ERR id held by its own archetype's skills. No record copies an AP question stem, figure or rubric text.

The scope rule that chose these archetypes, the authoring and verification workflow, and what stays open are in docs/operator/items-units-4-to-10.md.

## Checks [verified]

`key_formulations.py` computes each stem's answer in SymPy. A separate agent wrote it from the stems alone and never saw the keys. `.venv/bin/python tools/key_recheck.py content/items_unit03_agent content/items_unit03_agent/key_formulations.py` matched every key with its control holding, and `tests/items/test_key_recheck.py` reruns it on every suite run. `tools/check_items.py content/items_unit03_agent` reports 0 violations. Every record was signed off on 2026-09-24 with `tools/sign_off_items.py --by` on the operator's delegation, so `drafted_by` names the drafting run and `signed_off_by` names the review. The gate 29 audit over these banks is docs/operator/key-audit-p2/.
