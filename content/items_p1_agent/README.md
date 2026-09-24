---
title: Agent-drafted P1 items
research_date: 2026-09-23
status: pending_operator_review
purpose: Says what the 130 item records in this directory are, how they were audited, and why they never count as the operator's hand-authored items.
---

# Agent-drafted P1 items [verified]

This directory holds 130 original item records, 10 for each of the 13 P1 archetypes named in scope item 2 of docs/plan/11-phased-delivery.md. Each record is in the output schema of docs/plan/04-item-generation.md and carries `"authored_by": "claude-opus-5-5 agent draft, pending operator review"`. No record copies an AP question stem, figure or rubric text. Every record carries four options, one key with a null `error_path` and three distractors each tagged with a BC-ERR id held by the archetype's own skills, in a per-item shuffled order.

## Provenance and what they count toward [verified]

The operator ruled on 2026-09-23, under delegated authority, that these drafts may be served by the app so it can teach now. They are not the operator's hand-authored items. `app/items/ingest.py` writes their provenance `model` as the `authored_by` value, never `operator`, and only the operator may change that. Exit criterion 7, gates 17 and 30, and the gate 29 key-audit sample count only items whose provenance model is `operator`, so none of these 130 count toward any of them. `tools/check_items.py` prints them under "items per archetype" and leaves them out of "operator-authored items per archetype".

## How they reach the app [verified]

`app/main.py` reads `GROWTH_ITEMS_DIR`. Unset, it points at this directory, and the item bank (`app/runtime/bank.py`) ingests any record whose id is not already in the items table on its first query. `GROWTH_ITEMS_DIR=none` turns that off.

## Audit [verified]

Each archetype's 10 items were re-solved blind by an independent agent on 2026-09-23. Every key matched, and `tools/check_items.py` exited 0 for each archetype. That audit changed only distractor metadata, and no key.

A second audit on 2026-09-23 re-derived every distractor from the archetype's own named errors: 30 options in each of the 12 archetypes other than BC-QA-02010, whose distractors were re-derived the session before. Of those 360 options, 167 had their value, `violated_step` or tag corrected, 42 were left unchanged because no error the archetype's skills hold produces a third distinct value for that stem, and the rest were already correct. No key changed. `tools/check_items.py content/items_p1_agent` exits 0 with all 130 clean, but that gate checks only that each tag resolves to an active id and that options are distinct, so it does not show that a distractor follows from its error.

A third, independent review on 2026-09-23 judged every item: 65 approve, 57 fix, 8 reject, and 0 wrong keys. The fixes and the redesigns of the rejected items were applied to 65 files, and each archetype was then re-checked blind by a separate agent, which corrected 8 more items (01004-06, 01008-08, 02010-05, 02011-01, 02011-09, 03005-00, 03005-06, 03005-09). After that pass `tools/check_items.py content/items_p1_agent` exits 0 with 130 clean.

## Open for the operator [inferred]

Operator sign-off is still pending for all 130, including the reviewed and re-checked items. What the re-check left open is in BUILD-LEDGER.md, Known defects, twenty-sixth session. In 01004 every one of the ten items carries 0 (always `BC-ERR-01008`) and 1 as options. The scratchpad generators and the option shuffle are not in the repository.

A fourth check on 2026-09-23 re-solved every stem in SymPy from the stem text alone and compared the result with the stored key and every option: 130 of 130 keys match and no distractor equals its key (`docs/operator/p1-agent-item-key-check.md`). The same pass reworded 27 stems from "Which of the following is ..." to "Find ...", because R29 serves most attempts as short answers with no options shown. No key changed.
